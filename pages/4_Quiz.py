"""RecallAI — Page 4: Quiz (one-question-at-a-time with submit + nav)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.warnings_init  # noqa: F401

import streamlit as st

try:
    st.set_page_config(page_title="Quiz — RecallAI", page_icon="✏️", layout="wide")
except Exception:
    pass

from src.ui_components import inject_custom_css, init_session_state, render_sidebar, render_header
from src.quiz_engine import create_quiz_session, record_answer, evaluate_quiz

inject_custom_css()
init_session_state()
render_sidebar()

render_header("✏️ Quiz Mode", "Test your knowledge — one question at a time")

doc = st.session_state.get("active_document")

# ── If no quiz session yet, offer to start one ──────────────────────────────
if not st.session_state.get("active_quiz"):
    if not doc:
        st.warning("⚠️ No study notes loaded. Visit **Upload Notes** first.")
        st.stop()

    questions = doc.get("questions", [])
    if not questions:
        st.warning("⚠️ No questions available. Process notes in **Upload Notes** first.")
        st.stop()

    st.info(f"📋 **{len(questions)} questions** ready from: *{doc['title']}*")
    if st.button("▶️ Start Quiz", type="primary", use_container_width=True):
        session = create_quiz_session(questions, title=f"{doc['title']} Quiz")
        st.session_state["active_quiz"] = session
        st.rerun()
    st.stop()

# ── Active quiz session ──────────────────────────────────────────────────────
session = st.session_state["active_quiz"]

# If already submitted → redirect to results
if session.get("is_submitted"):
    st.success("✅ Quiz already submitted! View your results on the **Results** page.")
    if st.button("📊 Go to Results"):
        st.switch_page("pages/5_Results.py")
    st.stop()

questions  = session["questions"]
total_q    = session["total_questions"]
answered   = session["user_answers"]
current_idx = st.session_state.get("quiz_current_idx", 0)

# Guard bounds
if current_idx >= total_q:
    current_idx = total_q - 1
    st.session_state["quiz_current_idx"] = current_idx

q = questions[current_idx]
q_id = q["id"]

# ── Progress bar ─────────────────────────────────────────────────────────────
answered_count = len(answered)
st.progress(answered_count / total_q, text=f"{answered_count}/{total_q} answered")

# ── Question card ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="quiz-card">
        <div class="quiz-question-number">Question {current_idx + 1} of {total_q}</div>
        <div class="quiz-question-text">{q['question']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Radio options ─────────────────────────────────────────────────────────────
options_labels = [f"{chr(65+i)}. {opt}" for i, opt in enumerate(q["options"])]
prev_answer = answered.get(q_id)

selected_label = st.radio(
    "Select your answer:",
    options_labels,
    index=prev_answer if prev_answer is not None else None,
    key=f"q_radio_{q_id}",
)
if selected_label is not None:
    selected_idx = options_labels.index(selected_label)
    record_answer(session, q_id, selected_idx)
    st.session_state["active_quiz"] = session

# ── Navigation row ────────────────────────────────────────────────────────────
col_back, col_status, col_next = st.columns([1, 3, 1])

with col_back:
    if current_idx > 0:
        if st.button("← Previous"):
            st.session_state["quiz_current_idx"] = current_idx - 1
            st.rerun()

with col_next:
    if current_idx < total_q - 1:
        if st.button("Next →"):
            st.session_state["quiz_current_idx"] = current_idx + 1
            st.rerun()

with col_status:
    # Mini dot indicator
    dots = []
    for i in range(total_q):
        qi_id = questions[i]["id"]
        if i == current_idx:
            dots.append("🔵")
        elif qi_id in answered:
            dots.append("✅")
        else:
            dots.append("⚪")
    st.markdown(" ".join(dots))

# ── Submit ────────────────────────────────────────────────────────────────────
st.markdown("---")
unanswered = total_q - len(answered)
if unanswered > 0:
    st.info(f"ℹ️ {unanswered} question(s) not yet answered.")

if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
    results = evaluate_quiz(session)
    st.session_state["active_quiz"] = session
    st.session_state["quiz_history"].append(results)
    st.session_state["total_quizzes"] += 1
    # Reset nav index
    st.session_state["quiz_current_idx"] = 0
    st.success("✅ Quiz submitted! Redirecting to Results…")
    st.switch_page("pages/5_Results.py")

# ── Retake / Abandon ──────────────────────────────────────────────────────────
col_r, col_a = st.columns(2)
with col_r:
    if st.button("🔄 Restart Quiz"):
        fresh = create_quiz_session(questions, title=session.get("title", "Quiz"))
        st.session_state["active_quiz"] = fresh
        st.session_state["quiz_current_idx"] = 0
        st.rerun()
with col_a:
    if st.button("🗑️ Abandon Quiz"):
        st.session_state["active_quiz"] = None
        st.session_state["quiz_current_idx"] = 0
        st.rerun()
