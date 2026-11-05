"""RecallAI Core Module: Text Cleaner and Segmenter."""

import re
from typing import List, Dict, Any


def clean_text(raw_text: str) -> str:
    """
    Cleans raw text extracted from documents or user input.
    - Removes excessive whitespace, null bytes, and non-printable artifacts.
    - Strips recurring header/footer artifacts and page number stamps (e.g. 'Page 1 of 12').
    - Fixes hyphenated line breaks (e.g. 'trans- \nformer' -> 'transformer').
    """
    if not raw_text or not isinstance(raw_text, str):
        return ""

    # Replace null characters and control characters except common whitespace
    text = raw_text.replace("\x00", " ")
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)

    # Rejoin words broken across line breaks with hyphens: "inter- \npret" -> "interpret"
    text = re.sub(r"(\b\w+)-\s*\n\s*(\w+\b)", r"\1\2", text)

    # Normalize standalone page number lines: e.g. "Page 1 of 5", "--- 1 ---", "Page 2"
    text = re.sub(r"(?im)^\s*(page\s+\d+(\s+of\s+\d+)?|-+\s*\d+\s*-+|\d+)\s*$", "", text)

    # Replace multiple newline sequences with double newlines (paragraphs)
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Replace multiple horizontal spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Strip leading and trailing whitespace from each line
    lines = [line.strip() for line in text.split("\n")]
    cleaned = "\n".join(lines).strip()

    return cleaned


def split_into_sentences(text: str) -> List[str]:
    """
    Splits text into meaningful sentences while respecting abbreviations,
    numbers, and acronyms (e.g., 'Dr.', 'e.g.', 'i.e.', 'vs.', '3.14').
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    # Common abbreviations to protect
    abbrevs = [
        r"e\.g\.", r"i\.e\.", r"et al\.", r"etc\.", r"vs\.", r"approx\.",
        r"fig\.", r"dr\.", r"prof\.", r"mr\.", r"mrs\.", r"ms\.",
        r"no\.", r"vol\.", r"dept\."
    ]
    protected_text = cleaned
    replacements = {}
    for i, abbr in enumerate(abbrevs):
        placeholder = f"__ABBR_{i}__"
        # Case insensitive substitution
        matches = re.findall(abbr, protected_text, flags=re.IGNORECASE)
        for match in set(matches):
            replacements[placeholder] = match
            protected_text = protected_text.replace(match, placeholder)

    # Protect decimal numbers (e.g., 3.14)
    decimal_matches = re.findall(r"\d+\.\d+", protected_text)
    for i, dec in enumerate(set(decimal_matches)):
        placeholder = f"__DEC_{i}__"
        replacements[placeholder] = dec
        protected_text = protected_text.replace(dec, placeholder)

    # Sentence boundary: punctuation followed by space or newline and uppercase letter
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])|\n\n+", protected_text)

    sentences = []
    for s in raw_sentences:
        s_restored = s
        for placeholder, original in replacements.items():
            s_restored = s_restored.replace(placeholder, original)
        s_clean = s_restored.strip()
        # Keep sentences that have at least 4 words or 20 characters
        if len(s_clean.split()) >= 3 and len(s_clean) >= 15:
            sentences.append(s_clean)

    return sentences


def chunk_text(text: str, max_words: int = 250, overlap_words: int = 50) -> List[Dict[str, Any]]:
    """
    Divides text into overlapping logical sections suitable for transformer model context limits.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current_chunk: List[str] = []
    current_word_count = 0

    for sent in sentences:
        sent_words = len(sent.split())
        if current_word_count + sent_words > max_words and current_chunk:
            chunk_content = " ".join(current_chunk)
            chunks.append({
                "chunk_id": len(chunks) + 1,
                "text": chunk_content,
                "word_count": len(chunk_content.split()),
                "sentence_count": len(current_chunk),
            })
            # Overlap: keep last few sentences that fit within overlap_words
            overlap_sentences = []
            overlap_count = 0
            for prev_sent in reversed(current_chunk):
                p_count = len(prev_sent.split())
                if overlap_count + p_count <= overlap_words:
                    overlap_sentences.insert(0, prev_sent)
                    overlap_count += p_count
                else:
                    break
            current_chunk = overlap_sentences
            current_word_count = sum(len(s.split()) for s in current_chunk)

        current_chunk.append(sent)
        current_word_count += sent_words

    if current_chunk:
        chunk_content = " ".join(current_chunk)
        chunks.append({
            "chunk_id": len(chunks) + 1,
            "text": chunk_content,
            "word_count": len(chunk_content.split()),
            "sentence_count": len(current_chunk),
        })

    return chunks


def extract_key_terms(text: str, max_terms: int = 15) -> List[Dict[str, Any]]:
    """
    Extracts key terminology and candidate concepts from study text.
    Combines capitalised noun phrases, technical acronyms, and high-frequency terms.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []

    # Stopwords list for academic text
    stopwords = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
        "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
        "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
        "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
        "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's",
        "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on",
        "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
        "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some",
        "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
        "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
        "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
        "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
        "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
        "yours", "yourself", "yourselves", "also", "using", "used", "study", "example", "notes",
        "chapter", "page", "section", "figure", "table", "result", "system", "different"
    }

    words = re.findall(r"\b[A-Za-z][A-Za-z0-9_-]{2,}\b", cleaned)
    term_counts: Dict[str, int] = {}
    term_original: Dict[str, str] = {}

    for w in words:
        low = w.lower()
        if low not in stopwords and len(low) > 3:
            term_counts[low] = term_counts.get(low, 0) + 1
            if low not in term_original or w[0].isupper():
                term_original[low] = w

    # Also detect 2-word technical phrases (e.g., "machine learning", "photosystem ii")
    bigrams = re.findall(r"\b([A-Za-z]{3,})\s+([A-Za-z]{3,})\b", cleaned)
    bigram_counts: Dict[str, int] = {}
    for w1, w2 in bigrams:
        l1, l2 = w1.lower(), w2.lower()
        if l1 not in stopwords and l2 not in stopwords:
            phrase = f"{l1} {l2}"
            bigram_counts[phrase] = bigram_counts.get(phrase, 0) + 1

    results = []
    # Add top multi-word phrases that appear at least twice
    for phrase, count in sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 2:
            results.append({
                "term": phrase.title(),
                "frequency": count,
                "type": "Key Phrase"
            })
            if len(results) >= max_terms // 2:
                break

    # Add top single words
    for low, count in sorted(term_counts.items(), key=lambda x: x[1], reverse=True):
        orig = term_original.get(low, low.capitalize())
        # Avoid duplicating parts of phrases already added
        if not any(low in r["term"].lower() for r in results):
            results.append({
                "term": orig,
                "frequency": count,
                "type": "Key Concept"
            })
        if len(results) >= max_terms:
            break

    return results
