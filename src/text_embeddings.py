"""RecallAI Deep Learning Engine: Text Embeddings via Sentence-Transformers."""

import os
import warnings
import logging

os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
warnings.filterwarnings("ignore", message="Accessing `__path__`")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=FutureWarning, module="sentence_transformers")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
# Suppress the BertModel LOAD REPORT table printed to stdout by transformers 5.x
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

from typing import List, Dict, Any, Union, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Global cache for the embedding model instance
_EMBEDDING_MODEL = None
_FALLBACK_VECTORIZER = None


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Lazily loads and caches the SentenceTransformer model on CPU.
    """
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is not None:
        return _EMBEDDING_MODEL

    try:
        from sentence_transformers import SentenceTransformer
        # device="cpu" ensures lightweight execution across all machines
        logger.info(f"Loading SentenceTransformer model: {model_name}...")
        _EMBEDDING_MODEL = SentenceTransformer(model_name, device="cpu")
        return _EMBEDDING_MODEL
    except Exception as exc:
        logger.warning(f"Could not load SentenceTransformer '{model_name}': {exc}. Using TF-IDF fallback.")
        return None


def generate_embeddings(texts: Union[str, List[str]], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """
    Generates 384-dimensional dense vectors for the given texts using Sentence-Transformers.
    Falls back gracefully to TF-IDF normalized vectors if model cannot be loaded.
    """
    if isinstance(texts, str):
        texts = [texts]

    if not texts or all(not t.strip() for t in texts):
        return np.zeros((len(texts), 384), dtype=np.float32)

    model = get_embedding_model(model_name)
    if model is not None:
        try:
            embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
            return embeddings
        except Exception as exc:
            logger.error(f"Error encoding with SentenceTransformer: {exc}")

    # Fallback: Scikit-learn TF-IDF with L2 normalization
    return _generate_tfidf_fallback(texts)


def _generate_tfidf_fallback(texts: List[str]) -> np.ndarray:
    """
    Fallback vector representation when neural model weights cannot be accessed.
    """
    global _FALLBACK_VECTORIZER
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    if _FALLBACK_VECTORIZER is None or len(texts) > 2:
        _FALLBACK_VECTORIZER = TfidfVectorizer(max_features=384, stop_words="english")
        try:
            tfidf = _FALLBACK_VECTORIZER.fit_transform(texts).toarray()
        except ValueError:
            # If vocab is empty
            return np.zeros((len(texts), 384), dtype=np.float32)
    else:
        try:
            tfidf = _FALLBACK_VECTORIZER.transform(texts).toarray()
        except Exception:
            return np.zeros((len(texts), 384), dtype=np.float32)

    # Pad to 384 dimensions if fewer features
    if tfidf.shape[1] < 384:
        padding = np.zeros((tfidf.shape[0], 384 - tfidf.shape[1]), dtype=np.float32)
        tfidf = np.hstack([tfidf, padding])
    elif tfidf.shape[1] > 384:
        tfidf = tfidf[:, :384]

    return normalize(tfidf, norm="l2")


def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> np.ndarray:
    """
    Computes pairwise cosine similarities between two sets of embeddings.
    Both inputs can be 1D or 2D arrays.
    """
    a = np.atleast_2d(vec_a)
    b = np.atleast_2d(vec_b)

    # Normalize vectors if not already unit length
    norm_a = np.linalg.norm(a, axis=1, keepdims=True)
    norm_b = np.linalg.norm(b, axis=1, keepdims=True)
    norm_a[norm_a == 0] = 1e-10
    norm_b[norm_b == 0] = 1e-10

    a_norm = a / norm_a
    b_norm = b / norm_b

    similarity_matrix = np.dot(a_norm, b_norm.T)
    return similarity_matrix


def semantic_search(query: str, corpus: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Performs dense semantic vector search of a query across a list of text passages.
    Returns ranked matches with similarity score (0.0 to 1.0).
    """
    if not corpus or not query.strip():
        return []

    query_emb = generate_embeddings([query])
    corpus_embs = generate_embeddings(corpus)

    sims = compute_cosine_similarity(query_emb, corpus_embs)[0]
    ranked_indices = np.argsort(sims)[::-1][:min(top_k, len(corpus))]

    results = []
    for rank, idx in enumerate(ranked_indices):
        results.append({
            "rank": rank + 1,
            "index": int(idx),
            "text": corpus[idx],
            "similarity_score": round(float(sims[idx]), 4)
        })

    return results
