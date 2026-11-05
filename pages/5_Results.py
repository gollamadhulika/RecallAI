"""RecallAI — Page 5: Results & Progress (score, breakdown, session stats)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.warnings_init  # noqa: F401

import streamlit as st

try:
    st.set_page_config(page_title="Results — RecallAI", page_icon="📊", layout="wide")
except Exception:
    pass

from src.ui_components import inject_custom_css, init_session_state, render_sidebar, render_header
from src.quiz_engine import create_quiz_session

inject_custom_css()
init_session_state()
render_sidebar()

render_header("📊 Results & Progress", "Your quiz scores, concept mastery, and session analytics")

quiz_session = st.session_state.get("active_quiz")
quiz_history = st.session_state.get("quiz_history", [])
doc = st.session_state.get("active_document")

# ── Determine which results to show ─────────────────────────────────────────
results = None
if quiz_session and quiz_session.get("is_submitted"):
    results = quiz_session.get("results")
elif quiz_history:
    results = quiz_history[-1]   # Show most recent completed quiz

if not results:
    st.info("ℹ️ No quiz results yet. Complete a quiz on the **Quiz** page first.")
    if doc:
        st.markdown(
            f'**Ready to test yourself on:** *{doc["title"]}* — '
            f'{len(doc.get("questions",[]))} questions available.'
        )
        if st.button("▶️ Start Quiz", type="primary"):
            questions = doc.get("questions", [])
            session   = create_quiz_session(questions, title=f'{doc["title"]} Quiz')
            st.session_state["active_quiz"] = session
            st.session_state["quiz_current_idx"] = 0
            st.switch_page("pages/4_Quiz.py")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# SCORE BANNER
# ─────────────────────────────────────────────────────────────────────────────
pct   = results["percentage"]
score = results["correct_count"]
total = results["total"]
color = results.get("badge_color", "#2563eb")

st.markdown(
    f"""
    <div style="background:linear-gradient(135deg, {color}22 0%, {color}11 100%);
         border:2px solid {color}55; border-radius:18px; padding:2rem; text-align:center;
         margin-bottom:1.5rem; box-shadow:0 6px 24px rgba(0,0,0,0.3);">
        <div style="font-size:3.75rem; font-weight:900; color:{color}; line-height:1;">{pct}%</div>
        <div style="font-size:1.25rem; font-weight:700; color:#ffffff; margin:0.35rem 0;">
            {results['mastery_level']}
        </div>
        <div style="color:#cbd5e1; font-size:0.95rem;">{score} / {total} correct answers</div>
        <div style="color:#94a3b8; font-size:0.85rem; margin-top:0.4rem; font-style:italic;">
            {results.get('feedback','')}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Summary stats row ────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("✅ Correct",   results["correct_count"])
with c2:
    st.metric("❌ Incorrect", results["incorrect_count"])
with c3:
    st.metric("⬜ Unanswered", results["unanswered_count"])

# ── Concepts to review ────────────────────────────────────────────────────────
concepts_to_review = results.get("concepts_to_review", [])
if concepts_to_review:
    st.markdown("---")
    st.markdown("### 🔁 Concepts to Review")
    pills = " ".join(
        f'<span class="topic-pill" style="margin:.2rem;">{c}</span>'
        for c in concepts_to_review
    )
    st.markdown(pills, unsafe_allow_html=True)

# ── Detailed breakdown ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📋 Question-by-Question Breakdown")

for item in results.get("breakdown", []):
    is_correct  = item["is_correct"]
    is_answered = item["is_answered"]
    box_class   = "result-card-correct" if is_correct else "result-card-incorrect"
    icon        = "✅" if is_correct else ("❌" if is_answered else "⬜")
    badge_color = "#10b981" if is_correct else "#ef4444"

    with st.expander(f"{icon} Q{item['id']}: {item['question'][:75]}…"):
        st.markdown(f"**{item['question']}**")

        for i, opt in enumerate(item["options"]):
            if i == item["correct_index"] and i == item.get("selected_index"):
                marker = "✅ **Your answer (Correct)**"
            elif i == item["correct_index"]:
                marker = "✅ Correct answer"
            elif i == item.get("selected_index"):
                marker = "❌ Your answer"
            else:
                marker = ""
            st.markdown(f"**{chr(65+i)}.** {opt}  {f'— *{marker}*' if marker else ''}")

        if item.get("explanation"):
            st.markdown(
                f'<div style="background:#1e1b4b;border:1px solid #3730a3;border-radius:8px;'
                f'padding:0.75rem 1rem;font-size:0.88rem;margin-top:0.6rem;color:#c7d2fe;">'
                f'📌 <strong>Explanation:</strong> {item["explanation"]}</div>',
                unsafe_allow_html=True,
            )

# ── Session history ────────────────────────────────────────────────────────────
if len(quiz_history) > 0:
    st.markdown("---")
    st.markdown("### 🕐 Session Quiz History")
    for i, past in enumerate(reversed(quiz_history), 1):
        pct_p = past.get("percentage", 0)
        color_p = "#10b981" if pct_p >= 80 else ("#f59e0b" if pct_p >= 60 else "#ef4444")
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:0.65rem 1rem;background:#151823;border:1px solid #282f44;border-radius:10px;margin:0.4rem 0;">'
            f'<span style="color:#ffffff;font-weight:600;">Quiz #{len(quiz_history)+1-i}</span>'
            f'<span style="color:{color_p};font-weight:800;font-size:1.15rem;">{pct_p}%</span>'
            f'<span style="color:#94a3b8;font-size:0.85rem;">{past["correct_count"]}/{past["total"]} correct</span>'
            f'<span style="color:#64748b;font-size:0.8rem;">{past.get("evaluated_at","")}</span></div>',
            unsafe_allow_html=True,
        )

# ── Actions ───────────────────────────────────────────────────────────────────
st.markdown("---")
col_retake, col_workspace = st.columns(2)
with col_retake:
    if st.button("🔄 Retake Quiz", type="primary", use_container_width=True):
        if doc:
            qs = doc.get("questions", [])
            session = create_quiz_session(qs, title=f'{doc["title"]} Quiz')
            st.session_state["active_quiz"] = session
            st.session_state["quiz_current_idx"] = 0
            st.switch_page("pages/4_Quiz.py")
        else:
            st.warning("No document active.")
with col_workspace:
    if st.button("📚 Back to Workspace", use_container_width=True):
        st.switch_page("pages/3_Study_Workspace.py")
