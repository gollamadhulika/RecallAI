"""RecallAI Deep Learning Engine: Topic Classification using Pretrained DistilBERT and Embeddings."""

import os
import warnings
import logging

# ── Suppress Transformers 5.x image-processor registry __path__ spam ────────
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
warnings.filterwarnings("ignore", message="Accessing `__path__`")
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=FutureWarning, module="sentence_transformers")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
# ────────────────────────────────────────────────────────────────────────────

from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Standard academic study domain labels
ACADEMIC_TOPICS = [
    "Computer Science & Information Technology",
    "Biology & Life Sciences",
    "Physics & Astronomy",
    "Chemistry & Materials Science",
    "Mathematics & Statistics",
    "History & Humanities",
    "Economics & Business",
    "Psychology & Cognitive Science",
    "Medicine & Healthcare",
    "Environmental & Earth Sciences"
]

# Rich semantic anchor descriptions for zero-shot embedding projection
TOPIC_DESCRIPTIONS = {
    "Computer Science & Information Technology": "algorithms, data structures, programming, operating systems, networks, software, machine learning, databases, computing",
    "Biology & Life Sciences": "cells, genetics, DNA, RNA, photosynthesis, evolution, organisms, ecology, anatomy, cellular respiration, proteins, molecular biology",
    "Physics & Astronomy": "mechanics, thermodynamics, quantum physics, electromagnetism, optics, relativity, forces, gravity, energy, astrophysics",
    "Chemistry & Materials Science": "chemical reactions, atomic structure, periodic table, molecules, organic chemistry, bonds, compounds, thermodynamics, solutions",
    "Mathematics & Statistics": "calculus, linear algebra, probability, differential equations, geometry, statistics, theorems, proofs, matrices, discrete math",
    "History & Humanities": "historical events, civilizations, revolutions, ancient history, modern history, philosophy, literature, culture, treaties",
    "Economics & Business": "microeconomics, macroeconomics, finance, market supply and demand, inflation, management, marketing, investment, monetary policy",
    "Psychology & Cognitive Science": "human behavior, cognition, memory, neuroscience, perception, mental health, developmental psychology, cognitive theories",
    "Medicine & Healthcare": "pathology, pharmacology, clinical diagnosis, immunology, physiology, diseases, therapeutics, anatomy, health systems",
    "Environmental & Earth Sciences": "climate change, geology, ecosystems, plate tectonics, renewable energy, meteorology, biosphere, oceanography, minerals"
}

_CLASSIFIER_PIPELINE = None


def get_classifier_pipeline(model_name: str = "typeform/distilbert-base-uncased-mnli"):
    """
    Lazily loads the pretrained DistilBERT zero-shot classification pipeline.
    """
    global _CLASSIFIER_PIPELINE
    if _CLASSIFIER_PIPELINE is not None:
        return _CLASSIFIER_PIPELINE

    try:
        from transformers import pipeline
        logger.info(f"Loading pretrained DistilBERT zero-shot pipeline: {model_name}...")
        _CLASSIFIER_PIPELINE = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=-1  # Force CPU execution for universal compatibility
        )
        return _CLASSIFIER_PIPELINE
    except Exception as exc:
        logger.warning(f"Could not load DistilBERT pipeline '{model_name}': {exc}. Using embedding-similarity classifier.")
        return None


def classify_topic_distilbert(text: str, candidate_topics: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """
    Classifies academic text using the pretrained DistilBERT MNLI zero-shot model.
    """
    topics = candidate_topics or ACADEMIC_TOPICS
    classifier = get_classifier_pipeline()
    if classifier is None:
        return None

    # Take representative sample (first 1200 characters / ~200 words) for efficient inference
    sample_text = text[:1500].strip()
    if not sample_text:
        return None

    try:
        result = classifier(
            sample_text,
            candidate_labels=topics,
            hypothesis_template="This educational text is about {}."
        )

        labels = result["labels"]
        scores = result["scores"]

        scored_topics = [
            {
                "topic": label,
                "score": round(float(score), 4),
                "percentage": f"{score * 100:.1f}%"
            }
            for label, score in zip(labels, scores)
        ]

        top_label = scored_topics[0]["topic"]
        top_score = scored_topics[0]["score"]

        return {
            "primary_topic": top_label,
            "confidence_score": top_score,
            "confidence_percent": scored_topics[0]["percentage"],
            "all_scores": scored_topics,
            "model_used": "Pretrained DistilBERT (typeform/distilbert-base-uncased-mnli)",
            "training_distinction": "Pretrained Zero-Shot NLI (Inference Only; no task-specific weights fine-tuned)",
            "method": "Transformer Cross-Encoder Zero-Shot NLI",
            "sample_analyzed_length": len(sample_text)
        }
    except Exception as exc:
        logger.error(f"Error in DistilBERT classification: {exc}")
        return None


def classify_topic_embeddings(text: str, candidate_topics: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Semantic Topic Classifier using Sentence-Transformers (all-MiniLM-L6-v2).
    Computes cosine similarity between document embedding and topic anchor embeddings.
    Applies temperature-scaled Softmax to produce well-calibrated topic probabilities.
    """
    from src.text_embeddings import generate_embeddings, compute_cosine_similarity

    topics = candidate_topics or ACADEMIC_TOPICS
    sample_text = text[:2000].strip()
    if not sample_text:
        sample_text = "General Academic Study Material"

    # 1. Document embedding
    doc_emb = generate_embeddings([sample_text])

    # 2. Topic anchor descriptions
    anchor_texts = [f"{topic}: {TOPIC_DESCRIPTIONS.get(topic, topic)}" for topic in topics]
    topic_embs = generate_embeddings(anchor_texts)

    # 3. Pairwise cosine similarity
    similarities = compute_cosine_similarity(doc_emb, topic_embs)[0]

    # 4. Softmax with temperature scaling for normalized probability distribution
    temperature = 0.15
    exp_sims = np.exp((similarities - np.max(similarities)) / temperature)
    probabilities = exp_sims / np.sum(exp_sims)

    scored_topics = []
    for topic, score, prob in zip(topics, similarities, probabilities):
        scored_topics.append({
            "topic": topic,
            "score": round(float(prob), 4),
            "raw_similarity": round(float(score), 4),
            "percentage": f"{prob * 100:.1f}%"
        })

    # Sort descending by probability
    scored_topics.sort(key=lambda x: x["score"], reverse=True)

    top_topic = scored_topics[0]["topic"]
    top_score = scored_topics[0]["score"]

    return {
        "primary_topic": top_topic,
        "confidence_score": top_score,
        "confidence_percent": scored_topics[0]["percentage"],
        "all_scores": scored_topics,
        "model_used": "Pretrained Sentence-Transformers (all-MiniLM-L6-v2)",
        "training_distinction": "Pretrained Dense Embedding Cosine Similarity (Inference Only)",
        "method": "Semantic Vector Similarity with Temperature-Scaled Softmax",
        "sample_analyzed_length": len(sample_text)
    }


def classify_study_notes(text: str, prefer_distilbert: bool = True) -> Dict[str, Any]:
    """
    High-level entry point for classifying study notes.
    Tries DistilBERT if preferred and available, with instant fallback to Sentence-Transformers.
    """
    if prefer_distilbert:
        distil_res = classify_topic_distilbert(text)
        if distil_res is not None:
            return distil_res

    # Use embedding classifier
    return classify_topic_embeddings(text)
