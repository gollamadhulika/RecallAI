"""Unit tests for PDF extraction and text validation."""

import os
import pytest
from src.pdf_processor import extract_text_from_pdf, validate_text_input
from src.text_cleaner import clean_text, split_into_sentences, chunk_text, extract_key_terms

SAMPLE_PDF_PATH = os.path.join("data", "sample_notes", "computer_systems.pdf")


def test_extract_valid_pdf():
    assert os.path.exists(SAMPLE_PDF_PATH), f"Sample file {SAMPLE_PDF_PATH} does not exist"
    result = extract_text_from_pdf(SAMPLE_PDF_PATH)

    assert result["success"] is True
    assert result["page_count"] >= 1
    assert "Virtual Memory" in result["text"]
    assert result["metadata"]["total_words"] > 50
    assert result["error"] is None


def test_extract_bytes_input():
    with open(SAMPLE_PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    result = extract_text_from_pdf(pdf_bytes)
    assert result["success"] is True
    assert "Paging" in result["text"]


def test_empty_input_handling():
    result = extract_text_from_pdf(b"")
    assert result["success"] is False
    assert "empty" in result["error"].lower()


def test_clean_text():
    dirty = "This is a test--   \n\nPage 1 of 5\n\nwith excessive   spaces\x00 and line- \nbreaks."
    cleaned = clean_text(dirty)
    assert "\x00" not in cleaned
    assert "Page 1 of 5" not in cleaned
    assert "linebreaks" in cleaned


def test_split_into_sentences():
    text = "Virtual memory allows large programs. E.g., it uses secondary storage! What is paging? Paging divides memory."
    sentences = split_into_sentences(text)
    assert len(sentences) >= 3
    assert any("E.g." in s for s in sentences)


def test_chunk_text():
    text = (
        "Operating systems coordinate hardware resources. Virtual memory maps physical addresses. "
        "Paging divides memory into equal blocks. A page fault triggers an interrupt. "
        "The kernel services the interrupt by reading from disk. CPU scheduling selects processes."
    )
    chunks = chunk_text(text, max_words=15, overlap_words=5)
    assert len(chunks) >= 2
    for c in chunks:
        assert "text" in c
        assert c["word_count"] > 0


def test_extract_key_terms():
    text = "Machine learning algorithms learn parameters using gradient descent. Machine learning models require regularization."
    terms = extract_key_terms(text, max_terms=5)
    assert len(terms) > 0
    term_names = [t["term"].lower() for t in terms]
    assert any("machine learning" in tn or "gradient" in tn for tn in term_names)


def test_validate_text_input():
    valid = validate_text_input("This is a sufficiently long study note discussing algorithms and data structures in detail.", min_words=5)
    assert valid["valid"] is True
    assert valid["word_count"] >= 10

    too_short = validate_text_input("Too short", min_words=10)
    assert too_short["valid"] is False
    assert "too short" in too_short["error"].lower()
