"""RecallAI Evaluation Engine: Quiz Scoring, State Management, and Analytics."""

import datetime
from typing import List, Dict, Any, Optional


def create_quiz_session(questions: List[Dict[str, Any]], title: str = "Notes Quiz") -> Dict[str, Any]:
    """
    Initializes a new quiz session dictionary.
    """
    return {
        "title": title,
        "questions": questions,
        "total_questions": len(questions),
        "current_index": 0,
        "user_answers": {},  # question_id (int) -> selected_index (int)
        "is_submitted": False,
        "started_at": datetime.datetime.now().isoformat(),
        "completed_at": None,
        "results": None
    }


def record_answer(session: Dict[str, Any], question_id: int, selected_index: int) -> None:
    """
    Records or updates the user's selected answer for a question.
    """
    session["user_answers"][question_id] = selected_index


def evaluate_quiz(session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates submitted answers, calculates score percentages, and builds
    detailed diagnostic breakdown with concept mastery feedback.
    """
    questions = session.get("questions", [])
    user_answers = session.get("user_answers", {})

    total = len(questions)
    if total == 0:
        return {
            "score": 0,
            "total": 0,
            "correct_count": 0,
            "incorrect_count": 0,
            "unanswered_count": 0,
            "percentage": 0.0,
            "breakdown": [],
            "concepts_to_review": [],
            "mastery_level": "No Data"
        }

    correct_count = 0
    breakdown = []
    concepts_to_review = []

    for q in questions:
        q_id = q["id"]
        correct_idx = q["correct_index"]
        selected_idx = user_answers.get(q_id, None)

        is_answered = selected_idx is not None
        is_correct = is_answered and (selected_idx == correct_idx)

        if is_correct:
            correct_count += 1
        else:
            concepts_to_review.append(q.get("concept", "Key Term"))

        selected_text = q["options"][selected_idx] if (is_answered and 0 <= selected_idx < len(q["options"])) else "Unanswered"
        correct_text = q["options"][correct_idx]

        breakdown.append({
            "id": q_id,
            "question": q["question"],
            "options": q["options"],
            "selected_index": selected_idx,
            "selected_text": selected_text,
            "correct_index": correct_idx,
            "correct_text": correct_text,
            "is_correct": is_correct,
            "is_answered": is_answered,
            "explanation": q.get("explanation", ""),
            "concept": q.get("concept", "")
        })

    percentage = round((correct_count / total) * 100, 1)

    if percentage >= 80.0:
        mastery = "Excellent Mastery"
        color = "#10b981"
        feedback = "Outstanding comprehension! You have demonstrated strong recall of the key principles."
    elif percentage >= 60.0:
        mastery = "Proficient / Needs Review"
        color = "#f59e0b"
        feedback = "Good foundation! Review the flagged concepts below to reinforce your understanding."
    else:
        mastery = "Developing Comprehension"
        color = "#ef4444"
        feedback = "Key foundational terms require revision. Re-read the source workspace notes and retry."

    results = {
        "score": correct_count,
        "total": total,
        "correct_count": correct_count,
        "incorrect_count": total - correct_count,
        "unanswered_count": sum(1 for b in breakdown if not b["is_answered"]),
        "percentage": percentage,
        "breakdown": breakdown,
        "concepts_to_review": list(set(concepts_to_review)),
        "mastery_level": mastery,
        "badge_color": color,
        "feedback": feedback,
        "evaluated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    session["is_submitted"] = True
    session["completed_at"] = datetime.datetime.now().isoformat()
    session["results"] = results
    return results
