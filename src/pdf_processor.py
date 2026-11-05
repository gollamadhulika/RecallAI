"""RecallAI Document Processor: PDF Text Extraction & Validation using PyMuPDF."""

import io
from typing import Dict, Any, Union
import pymupdf  # PyMuPDF
from src.text_cleaner import clean_text


def extract_text_from_pdf(file_input: Union[bytes, io.BytesIO, str]) -> Dict[str, Any]:
    """
    Extracts text and structural metadata from a PDF file.

    Parameters:
        file_input: File path (str), raw bytes (bytes), or BytesIO stream.

    Returns:
        Dict containing success flag, extracted text, page breakdown,
        document metadata, and diagnostic error information.
    """
    result: Dict[str, Any] = {
        "success": False,
        "text": "",
        "raw_text": "",
        "page_count": 0,
        "pages": [],
        "metadata": {
            "title": "Untitled",
            "author": "Unknown",
            "total_characters": 0,
            "total_words": 0,
            "is_likely_scanned": False,
        },
        "error": None,
    }

    try:
        # 1. Open document
        if isinstance(file_input, bytes):
            if len(file_input) == 0:
                result["error"] = "The uploaded file is empty (0 bytes). Please upload a valid PDF."
                return result
            doc = pymupdf.open(stream=file_input, filetype="pdf")
        elif isinstance(file_input, io.BytesIO):
            stream_data = file_input.getvalue()
            if len(stream_data) == 0:
                result["error"] = "The uploaded file stream is empty. Please upload a valid PDF."
                return result
            doc = pymupdf.open(stream=stream_data, filetype="pdf")
        elif isinstance(file_input, str):
            doc = pymupdf.open(file_input)
        else:
            result["error"] = f"Unsupported input type: {type(file_input).__name__}."
            return result

        # 2. Check encryption / password
        if doc.is_encrypted:
            result["error"] = "This PDF file is password protected or encrypted. Please unlock it before uploading."
            doc.close()
            return result

        page_count = len(doc)
        result["page_count"] = page_count

        if page_count == 0:
            result["error"] = "The PDF contains 0 pages."
            doc.close()
            return result

        # 3. Read metadata
        meta = doc.metadata or {}
        result["metadata"]["title"] = meta.get("title") or "Study Notes Document"
        result["metadata"]["author"] = meta.get("author") or "Student / Unknown"

        # 4. Extract page-by-page text
        raw_text_parts = []
        total_chars = 0
        total_images = 0

        for page_idx in range(page_count):
            page = doc[page_idx]
            page_raw = page.get_text("text") or ""
            images = page.get_images()
            total_images += len(images)

            cleaned_page = clean_text(page_raw)
            raw_text_parts.append(page_raw)

            word_count = len(cleaned_page.split()) if cleaned_page else 0
            char_count = len(cleaned_page)
            total_chars += char_count

            result["pages"].append({
                "page_number": page_idx + 1,
                "text": cleaned_page,
                "character_count": char_count,
                "word_count": word_count,
                "image_count": len(images)
            })

        doc.close()

        combined_raw = "\n\n".join(raw_text_parts)
        combined_cleaned = clean_text(combined_raw)
        total_words = len(combined_cleaned.split()) if combined_cleaned else 0

        result["raw_text"] = combined_raw
        result["text"] = combined_cleaned
        result["metadata"]["total_characters"] = total_chars
        result["metadata"]["total_words"] = total_words

        # 5. Validation: Detect scanned or empty documents
        if total_chars < 50:
            if total_images > 0:
                result["metadata"]["is_likely_scanned"] = True
                result["error"] = (
                    "Scanned or Image-only PDF detected: This document contains images but almost no selectable text "
                    f"({total_chars} characters extracted across {page_count} pages). "
                    "RecallAI deep learning models require digital text. Please paste the notes directly or use an OCR-processed PDF."
                )
            else:
                result["error"] = (
                    f"Unreadable or empty document: Only {total_chars} characters found. "
                    "Please ensure the file has readable study notes."
                )
            return result

        result["success"] = True
        return result

    except Exception as exc:
        result["error"] = f"Failed to parse PDF document: {str(exc)}"
        return result


def validate_text_input(text: str, min_words: int = 15) -> Dict[str, Any]:
    """
    Validates user-pasted or raw study notes text.
    """
    cleaned = clean_text(text)
    words = cleaned.split()
    word_count = len(words)

    if not cleaned or word_count == 0:
        return {
            "valid": False,
            "word_count": 0,
            "text": "",
            "error": "The pasted text is empty. Please enter study notes."
        }

    if word_count < min_words:
        return {
            "valid": False,
            "word_count": word_count,
            "text": cleaned,
            "error": f"The text is too short ({word_count} words). Please provide at least {min_words} words for meaningful analysis."
        }

    return {
        "valid": True,
        "word_count": word_count,
        "text": cleaned,
        "error": None
    }
