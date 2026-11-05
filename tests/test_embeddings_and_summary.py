"""Unit tests for dense embeddings and summarizer."""

import pytest
import numpy as np
from src.text_embeddings import generate_embeddings, compute_cosine_similarity, semantic_search
from src.summarizer import summarize_extractive_semantic, generate_summary


def test_generate_embeddings_shape():
    texts = [
        "Photosynthesis converts light into chemical energy in chloroplasts.",
        "Virtual memory allows larger memory space using secondary storage paging."
    ]
    embs = generate_embeddings(texts)
    assert isinstance(embs, np.ndarray)
    assert embs.shape == (2, 384)


def test_cosine_similarity():
    v1 = np.array([[1.0, 0.0, 0.0]])
    v2 = np.array([[1.0, 0.0, 0.0]])
    v3 = np.array([[0.0, 1.0, 0.0]])

    sim_same = compute_cosine_similarity(v1, v2)[0][0]
    sim_ortho = compute_cosine_similarity(v1, v3)[0][0]

    assert pytest.approx(sim_same, 0.001) == 1.0
    assert pytest.approx(sim_ortho, 0.001) == 0.0


def test_semantic_search():
    corpus = [
        "The mitochondria is the powerhouse of the biological cell producing ATP.",
        "Operating systems use scheduling algorithms like Round Robin.",
        "Chlorophyll in plant leaves captures sunlight for photosynthesis.",
        "CPU caches speed up memory access instructions."
    ]
    results = semantic_search("How do cells generate cellular energy?", corpus, top_k=2)
    assert len(results) == 2
    # The first result should be about mitochondria/ATP
    assert "mitochondria" in results[0]["text"].lower() or "chlorophyll" in results[0]["text"].lower()


def test_extractive_summary():
    text = (
        "Operating systems provide an interface between computer hardware and user applications. "
        "Virtual memory maps virtual addresses onto physical RAM and secondary disk storage. "
        "Paging divides memory into fixed blocks to prevent external fragmentation. "
        "A page fault occurs when an address is not currently in physical RAM. "
        "The kernel handles this interrupt by loading the required block from disk storage. "
        "CPU scheduling selects which ready thread executes next on the processor."
    )
    summary = summarize_extractive_semantic(text, target_sentences=2)
    assert "summary_text" in summary
    assert len(summary["bullet_points"]) == 2
    assert summary["summary_words"] < summary["original_words"]
    assert "compression_ratio" in summary
