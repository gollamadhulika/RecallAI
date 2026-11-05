"""Unit tests for deep learning topic classification."""

import pytest
from src.topic_classifier import (
    classify_topic_embeddings,
    classify_study_notes,
    ACADEMIC_TOPICS
)


def test_classify_computer_science_text():
    cs_text = (
        "Operating systems use virtual memory, paging, and CPU scheduling to allocate hardware. "
        "Deadlocks occur when processes enter circular wait conditions on mutex locks."
    )
    result = classify_topic_embeddings(cs_text)

    assert result["primary_topic"] == "Computer Science & Information Technology"
    assert result["confidence_score"] > 0.0
    assert len(result["all_scores"]) == len(ACADEMIC_TOPICS)
    assert "Pretrained" in result["model_used"]


def test_classify_biology_text():
    bio_text = (
        "Photosynthesis takes place in chloroplasts where chlorophyll pigments absorb solar photons. "
        "The Calvin cycle utilizes ATP and NADPH to fix carbon dioxide into glucose molecules."
    )
    result = classify_topic_embeddings(bio_text)

    assert result["primary_topic"] == "Biology & Life Sciences"
    assert result["confidence_score"] > 0.0


def test_classification_metadata_distinction():
    sample = "Calculus is the study of continuous change, derivatives, and integral equations."
    res = classify_study_notes(sample, prefer_distilbert=False)

    assert "training_distinction" in res
    assert "Inference Only" in res["training_distinction"]
    assert "all_scores" in res
