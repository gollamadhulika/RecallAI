"""RecallAI Study Content Engine: Practice Question Generation with Semantic Distractors."""

import re
import random
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from src.text_cleaner import clean_text, split_into_sentences, extract_key_terms
from src.text_embeddings import generate_embeddings, compute_cosine_similarity

logger = logging.getLogger(__name__)

# Common academic fallback distractors categorized by academic field
DOMAIN_DISTRACTOR_BANK = {
    "Computer Science": [
        "Memory Buffer", "Binary Search Tree", "Garbage Collection", "Deadlock",
        "Context Switch", "Cache Hit", "Hash Table", "Paging", "Thread Pool", "Recursion"
    ],
    "Biology": [
        "Mitochondria", "Cell Membrane", "Endoplasmic Reticulum", "Active Transport",
        "Ribosome", "Osmosis", "Golgi Apparatus", "ATP Synthase", "Enzyme Catalysis"
    ],
    "Physics": [
        "Kinetic Energy", "Magnetic Flux", "Angular Momentum", "Centripetal Force",
        "Thermodynamic Equilibrium", "Refraction Index", "Wave Interference", "Potential Energy"
    ],
    "General": [
        "Static Variable", "Dynamic Equilibrium", "Controlled Variable", "Iterative Refinement",
        "Inductive Reasoning", "Empirical Observation", "Statistical Variance", "Null Hypothesis"
    ]
}


def _find_candidate_distractors(target_term: str, all_terms: List[str], num_needed: int = 3) -> List[str]:
    """
    Selects semantically plausible distractors using Sentence-Transformers cosine similarity.
    Distractors should be semantically related (high similarity) but distinct strings.
    """
    candidates = [t for t in all_terms if t.lower() != target_term.lower() and len(t) > 2]

    # If we don't have enough candidate terms from the text itself, supplement with domain bank
    if len(candidates) < num_needed:
        for bank_terms in DOMAIN_DISTRACTOR_BANK.values():
            for bt in bank_terms:
                if bt.lower() != target_term.lower() and bt not in candidates:
                    candidates.append(bt)
                if len(candidates) >= 12:
                    break

    try:
        # Compute embeddings for target and candidate distractors
        target_emb = generate_embeddings([target_term])
        cand_embs = generate_embeddings(candidates)

        sims = compute_cosine_similarity(target_emb, cand_embs)[0]

        # Filter out near-identical terms (sim > 0.96) to avoid duplicate answers
        valid_pairs = []
        for term, score in zip(candidates, sims):
            if 0.15 <= score <= 0.94 and term.lower() not in target_term.lower() and target_term.lower() not in term.lower():
                valid_pairs.append((term, score))

        # Sort by similarity descending (most plausible distractors first)
        valid_pairs.sort(key=lambda x: x[1], reverse=True)

        chosen = [term for term, _ in valid_pairs[:num_needed]]

        # Fallback if filtered list is too small
        if len(chosen) < num_needed:
            remaining = [c for c in candidates if c not in chosen and c.lower() != target_term.lower()]
            random.shuffle(remaining)
            chosen.extend(remaining[:(num_needed - len(chosen))])

        return chosen[:num_needed]

    except Exception as exc:
        logger.warning(f"Error computing semantic distractors: {exc}")
        safe_candidates = [c for c in candidates if c.lower() != target_term.lower()]
        random.shuffle(safe_candidates)
        return safe_candidates[:num_needed]


def generate_quiz_questions(text: str, max_questions: int = 5) -> List[Dict[str, Any]]:
    """
    Generates multiple-choice quiz questions from study notes.

    Methodology:
    - Sentences containing definitions, mechanisms, or relationships are parsed.
    - Key concepts are identified and blanked or queried.
    - Plausible distractors are calculated using Sentence-Transformers vector similarity.
    - Accurate explanations are generated directly from the notes.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    key_terms_data = extract_key_terms(text, max_terms=20)
    all_term_names = [k["term"] for k in key_terms_data]

    # Informative sentence patterns: e.g. "X is defined as...", "X is a...", "X enables..."
    definition_regex = re.compile(
        r"^(?P<subject>[A-Z][A-Za-z0-9_\s]{2,28})\s+(is|are|refers to|is defined as|represents|functions as|describes|is known as)\s+(?P<predicate>.+)$",
        re.IGNORECASE
    )

    questions: List[Dict[str, Any]] = []
    used_sentences = set()
    used_answers = set()

    # Pass 1: Extract direct definitions and properties
    for sent in sentences:
        if len(questions) >= max_questions:
            break

        if sent in used_sentences:
            continue

        match = definition_regex.match(sent)
        if match:
            subject = match.group("subject").strip()
            predicate = match.group("predicate").strip().rstrip(".")

            # Ensure subject is plausible and not a generic pronoun
            if (
                len(subject.split()) <= 4
                and subject.lower() not in {"this", "that", "these", "it", "they", "there", "what", "which"}
                and len(predicate) > 15
                and subject.lower() not in used_answers
            ):
                distractors = _find_candidate_distractors(subject, all_term_names, num_needed=3)
                if len(distractors) == 3:
                    options = [subject] + distractors
                    random.shuffle(options)
                    correct_idx = options.index(subject)

                    q_type = random.choice(["definition", "fill_blank"])
                    if q_type == "definition":
                        q_text = f"According to the notes, which concept or component is described as:\n\"{predicate}\"?"
                    else:
                        q_text = f"Fill in the blank: \"__________ {match.group(2)} {predicate}.\""

                    questions.append({
                        "id": len(questions) + 1,
                        "question": q_text,
                        "options": options,
                        "correct_index": correct_idx,
                        "correct_answer": subject,
                        "explanation": f"Source reference from notes: \"{sent}\"",
                        "source_sentence": sent,
                        "concept": subject,
                        "difficulty": "Medium",
                        "generation_method": "Semantic Distractor Matching (Sentence-Transformers + Dependency Extraction)"
                    })

                    used_sentences.add(sent)
                    used_answers.add(subject.lower())

    # Pass 2: Key term cloze / statement validation for remaining questions
    for term_info in key_terms_data:
        if len(questions) >= max_questions:
            break

        term = term_info["term"]
        if term.lower() in used_answers:
            continue

        # Find a sentence containing this term
        matching_sentences = [
            s for s in sentences
            if re.search(r"\b" + re.escape(term) + r"\b", s, re.IGNORECASE)
            and s not in used_sentences
            and len(s) > 30
        ]

        if not matching_sentences:
            continue

        chosen_sent = matching_sentences[0]
        distractors = _find_candidate_distractors(term, all_term_names, num_needed=3)

        if len(distractors) == 3:
            # Mask the term
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            masked_sentence = pattern.sub("__________", chosen_sent, count=1)

            options = [term] + distractors
            random.shuffle(options)
            correct_idx = options.index(term)

            questions.append({
                "id": len(questions) + 1,
                "question": f"Based on your study notes, complete the following statement:\n\"{masked_sentence}\"",
                "options": options,
                "correct_index": correct_idx,
                "correct_answer": term,
                "explanation": f"Source reference: \"{chosen_sent}\"",
                "source_sentence": chosen_sent,
                "concept": term,
                "difficulty": "Medium",
                "generation_method": "Semantic Concept Cloze with Dense Vector Distractors"
            })

            used_sentences.add(chosen_sent)
            used_answers.add(term.lower())

    return questions
