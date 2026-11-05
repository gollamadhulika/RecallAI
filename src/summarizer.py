"""RecallAI Deep Learning Engine: Text Summarization (Semantic Extractive & Abstractive)."""

import os
import warnings
import logging

os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
warnings.filterwarnings("ignore", message="Accessing `__path__`")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
logging.getLogger("transformers").setLevel(logging.ERROR)

from typing import List, Dict, Any, Optional
import numpy as np
from src.text_cleaner import clean_text, split_into_sentences
from src.text_embeddings import generate_embeddings, compute_cosine_similarity

logger = logging.getLogger(__name__)

_ABSTRACTIVE_PIPELINE = None


def get_abstractive_pipeline(model_name: str = "sshleifer/distilbart-cnn-12-6"):
    """
    Lazily loads the pretrained transformer abstractive summarization pipeline.
    """
    global _ABSTRACTIVE_PIPELINE
    if _ABSTRACTIVE_PIPELINE is not None:
        return _ABSTRACTIVE_PIPELINE

    try:
        from transformers import pipeline
        logger.info(f"Loading summarization pipeline: {model_name}...")
        _ABSTRACTIVE_PIPELINE = pipeline(
            "summarization",
            model=model_name,
            device=-1  # CPU execution
        )
        return _ABSTRACTIVE_PIPELINE
    except Exception as exc:
        logger.warning(f"Could not load abstractive summarizer '{model_name}': {exc}. Using Semantic Extractive fallback.")
        return None


def summarize_extractive_semantic(text: str, target_sentences: int = 4) -> Dict[str, Any]:
    """
    Semantic Extractive Summarization using Sentence-Transformers (all-MiniLM-L6-v2).
    1. Splits text into sentences.
    2. Encodes each sentence into a 384-dimensional dense semantic vector.
    3. Calculates the centroid (mean vector) representing the entire document theme.
    4. Computes cosine similarity of each sentence to the centroid.
    5. Selects top diverse central sentences (Maximal Marginal Relevance) and preserves chronological flow.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return {
            "summary_text": clean_text(text),
            "bullet_points": [],
            "method": "Direct passthrough (text too short)",
            "model_used": "None",
            "original_words": len(text.split()),
            "summary_words": len(text.split()),
            "compression_ratio": "0%"
        }

    if len(sentences) <= target_sentences:
        summary_text = " ".join(sentences)
        return {
            "summary_text": summary_text,
            "bullet_points": sentences,
            "method": "Direct passthrough (text already concise)",
            "model_used": "Sentence-Transformers (all-MiniLM-L6-v2)",
            "original_words": len(text.split()),
            "summary_words": len(summary_text.split()),
            "compression_ratio": "0%"
        }

    # Generate sentence embeddings
    sent_embs = generate_embeddings(sentences)
    # Global document centroid vector
    doc_centroid = np.mean(sent_embs, axis=0, keepdims=True)

    # Cosine similarities to centroid
    sims = compute_cosine_similarity(sent_embs, doc_centroid).flatten()

    # Maximal Marginal Relevance (MMR) for diversity and coverage
    selected_indices: List[int] = []
    candidates = list(range(len(sentences)))
    lambda_param = 0.75  # Balance between centrality and diversity

    for _ in range(min(target_sentences, len(sentences))):
        best_idx = None
        best_score = -float("inf")

        for c in candidates:
            centrality = sims[c]
            if not selected_indices:
                redundancy = 0.0
            else:
                redundancy = max(
                    compute_cosine_similarity(sent_embs[c:c+1], sent_embs[s:s+1])[0][0]
                    for s in selected_indices
                )
            mmr_score = lambda_param * centrality - (1 - lambda_param) * redundancy
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = c

        if best_idx is not None:
            selected_indices.append(best_idx)
            candidates.remove(best_idx)

    # Reorder chronologically for natural narrative coherence
    selected_indices.sort()
    chosen_sentences = [sentences[i] for i in selected_indices]
    summary_text = " ".join(chosen_sentences)

    orig_words = sum(len(s.split()) for s in sentences)
    sum_words = sum(len(s.split()) for s in chosen_sentences)
    compression = round((1.0 - (sum_words / max(orig_words, 1))) * 100, 1)

    return {
        "summary_text": summary_text,
        "bullet_points": chosen_sentences,
        "method": "Semantic Centroid & MMR Extractive Summarization",
        "model_used": "Sentence-Transformers (all-MiniLM-L6-v2)",
        "training_distinction": "Zero-shot Semantic Centroid Optimization (No generative hallucinations)",
        "original_words": orig_words,
        "summary_words": sum_words,
        "compression_ratio": f"{compression}%"
    }


def summarize_abstractive(text: str, max_length: int = 140, min_length: int = 40) -> Optional[Dict[str, Any]]:
    """
    Abstractive summarization using Hugging Face Transformer pipeline.
    """
    cleaned = clean_text(text)
    words = cleaned.split()
    if len(words) < 50:
        return None

    pipeline_model = get_abstractive_pipeline()
    if pipeline_model is None:
        return None

    try:
        # Take up to first 750 words to avoid exceeding transformer token window
        input_chunk = " ".join(words[:750])
        result = pipeline_model(
            input_chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        summary_text = result[0]["summary_text"].strip()
        bullets = split_into_sentences(summary_text)

        orig_words = len(words)
        sum_words = len(summary_text.split())
        compression = round((1.0 - (sum_words / max(orig_words, 1))) * 100, 1)

        return {
            "summary_text": summary_text,
            "bullet_points": bullets,
            "method": "Transformer Abstractive Summarization",
            "model_used": "Pretrained DistilBART (sshleifer/distilbart-cnn-12-6)",
            "training_distinction": "Pretrained CNN/DailyMail weights (Inference only)",
            "original_words": orig_words,
            "summary_words": sum_words,
            "compression_ratio": f"{compression}%"
        }
    except Exception as exc:
        logger.error(f"Error during abstractive summarization: {exc}")
        return None


def generate_summary(text: str, prefer_abstractive: bool = False, target_sentences: int = 4) -> Dict[str, Any]:
    """
    Main summarization entry point. Default is Semantic Extractive (fast, 100% faithful to notes).
    Can attempt Abstractive if requested.
    """
    if prefer_abstractive:
        abs_res = summarize_abstractive(text)
        if abs_res is not None:
            return abs_res

    return summarize_extractive_semantic(text, target_sentences=target_sentences)
