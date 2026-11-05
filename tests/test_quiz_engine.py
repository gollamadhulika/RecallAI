"""Unit tests for question generation and quiz scoring engine."""

import pytest
from src.question_generator import generate_quiz_questions
from src.flashcards import generate_flashcards
from src.quiz_engine import create_quiz_session, record_answer, evaluate_quiz


SAMPLE_STUDY_TEXT = (
    "Virtual Memory is a storage allocation scheme in which secondary memory can be addressed as though it were part of main memory. "
    "Paging is a memory management scheme by which a computer stores and retrieves data from secondary storage. "
    "A Page Fault occurs when a program attempts to access a block of memory that is not stored in the physical RAM. "
    "The Translation Lookaside Buffer (TLB) is a specialized hardware cache used to improve virtual address translation speed. "
    "CPU Scheduling is the process by which the operating system decides which process in the ready queue is allocated the processor. "
    "A Deadlock is a state in which two or more competing processes are unable to proceed because each is waiting for the other."
)


def test_question_generation():
    questions = generate_quiz_questions(SAMPLE_STUDY_TEXT, max_questions=4)
    assert len(questions) > 0

    for q in questions:
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert 0 <= q["correct_index"] < 4
        assert q["correct_answer"] == q["options"][q["correct_index"]]
        assert "explanation" in q
        assert "generation_method" in q


def test_flashcard_generation():
    cards = generate_flashcards(SAMPLE_STUDY_TEXT, max_cards=4)
    assert len(cards) > 0
    for c in cards:
        assert "term" in c
        assert "definition" in c
        assert len(c["definition"]) > 10


def test_quiz_session_lifecycle():
    questions = generate_quiz_questions(SAMPLE_STUDY_TEXT, max_questions=3)
    assert len(questions) >= 2

    # 1. Create session
    session = create_quiz_session(questions, title="OS Quiz")
    assert session["total_questions"] == len(questions)
    assert session["is_submitted"] is False

    # 2. Answer question 1 correctly, question 2 incorrectly
    q1 = questions[0]
    q2 = questions[1]
    record_answer(session, q1["id"], q1["correct_index"])
    wrong_idx = (q2["correct_index"] + 1) % 4
    record_answer(session, q2["id"], wrong_idx)

    # 3. Evaluate quiz
    results = evaluate_quiz(session)
    assert session["is_submitted"] is True
    assert results["total"] == len(questions)
    assert results["correct_count"] >= 1
    assert "percentage" in results
    assert "mastery_level" in results
    assert len(results["breakdown"]) == len(questions)
