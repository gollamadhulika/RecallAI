"""RecallAI Study Content Engine: Interactive Flashcard Generation."""

import re
from typing import List, Dict, Any
from src.text_cleaner import split_into_sentences, extract_key_terms
from src.text_embeddings import generate_embeddings, compute_cosine_similarity


def generate_flashcards(text: str, max_cards: int = 8) -> List[Dict[str, Any]]:
    """
    Generates concept flashcards (Front: Term/Concept, Back: Definition/Explanation)
    by pairing extracted key terminology with their most semantically relevant
    explanatory sentences from the source material.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    terms_data = extract_key_terms(text, max_terms=max_cards * 2)
    if not terms_data:
        return []

    flashcards: List[Dict[str, Any]] = []
    used_sentences = set()

    # Pre-encode sentences for semantic matching
    sent_embs = generate_embeddings(sentences)

    for item in terms_data:
        if len(flashcards) >= max_cards:
            break

        term = item["term"]

        # 1. First look for direct sentence mentions
        exact_matches = [
            (idx, s) for idx, s in enumerate(sentences)
            if re.search(r"\b" + re.escape(term) + r"\b", s, re.IGNORECASE)
            and s not in used_sentences
        ]

        if exact_matches:
            # Pick the most informative sentence (length between 40 and 200 chars)
            best_idx, best_sent = min(
                exact_matches,
                key=lambda x: abs(len(x[1]) - 110)
            )
            definition = best_sent
            used_sentences.add(best_sent)
        else:
            # 2. Semantic fallback: find sentence with highest cosine similarity to the term
            term_emb = generate_embeddings([f"What is {term} and its function?"])
            sims = compute_cosine_similarity(term_emb, sent_embs)[0]
            ranked_idx = int(sims.argmax())
            best_sent = sentences[ranked_idx]
            if best_sent not in used_sentences:
                definition = best_sent
                used_sentences.add(best_sent)
            else:
                continue

        # Format clean card
        flashcards.append({
            "id": len(flashcards) + 1,
            "term": term,
            "definition": definition,
            "category": item.get("type", "Key Concept"),
            "status": "unreviewed"  # "unreviewed" | "mastered" | "needs_review"
        })

    return flashcards
