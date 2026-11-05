"""RecallAI — Page 1: Dashboard (modern dark academic study interface with authentic user data)."""

import sys, os
import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.warnings_init  # noqa: F401 — suppress HF/transformers noise first

import streamlit as st

try:
    st.set_page_config(page_title="Dashboard — RecallAI", page_icon="🏠", layout="wide")
except Exception:
    pass

from src.ui_components import inject_custom_css, init_session_state, render_sidebar, render_header

inject_custom_css()
init_session_state()
render_sidebar()

# ── 1. Top Student Welcome Bar ───────────────────────────────────────────────
render_header("Welcome Aboard,", "USER01")

# ── 2. Real Metric Cards (100% Actual Session Data) ──────────────────────────
docs = st.session_state.get("documents_history", [])
quizzes = st.session_state.get("quiz_history", [])
active = st.session_state.get("active_document")

# Calculate authentic counts directly from session state
flashcards_count = sum(len(d.get("flashcards", [])) for d in docs)
tests_count = len(quizzes)
study_guides_count = len(docs)

if quizzes:
    avg_score = round(sum(q.get("percentage", 0) for q in quizzes) / len(quizzes))
    score_display = f"{avg_score}%"
else:
    score_display = "0%"

st.markdown(
    f"""
    <div class="metric-cards-grid">
        <div class="vibrant-card card-purple">
            <div class="vibrant-num">{flashcards_count}</div>
            <div class="vibrant-label">Flash Cards</div>
        </div>
        <div class="vibrant-card card-coral">
            <div class="vibrant-num">{tests_count}</div>
            <div class="vibrant-label">Tests</div>
        </div>
        <div class="vibrant-card card-emerald">
            <div class="vibrant-num">{study_guides_count}</div>
            <div class="vibrant-label">Study Guides</div>
        </div>
        <div class="vibrant-card card-amber">
            <div class="vibrant-num">{score_display}</div>
            <div class="vibrant-label">Mastery</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── 3. Segmented Pill Tab Bar ────────────────────────────────────────────────
tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)
with tab_col1:
    if st.button("📤 Upload Notes", use_container_width=True, key="dash_tab_upload"):
        st.switch_page("pages/2_Upload_Notes.py")
with tab_col2:
    if st.button("📚 Study Workspace", use_container_width=True, key="dash_tab_ws"):
        st.switch_page("pages/3_Study_Workspace.py")
with tab_col3:
    if st.button("✏️ Tests & Quizzes", use_container_width=True, key="dash_tab_quiz"):
        st.switch_page("pages/4_Quiz.py")
with tab_col4:
    if st.button("📊 Analytics & Scores", use_container_width=True, key="dash_tab_results"):
        st.switch_page("pages/5_Results.py")

# ── 4. Recents Section (100% Real User Data) ─────────────────────────────────
st.markdown(
    """
    <div class="recents-box">
        <div class="recents-header">
            <span>Recents</span>
            <span style="font-size: 0.82rem; color: #818cf8; font-weight: 600;">Actual Session Activity</span>
        </div>
    """,
    unsafe_allow_html=True,
)

now = datetime.datetime.now()
month_str = now.strftime("%b")
day_str = now.strftime("%d")

if docs:
    for idx, doc_item in enumerate(reversed(docs)):
        topic_name = doc_item.get("topic", {}).get("primary_topic", "General Academic")
        word_count = doc_item.get("metadata", {}).get("total_words", 0)
        flash_num = len(doc_item.get("flashcards", []))
        q_num = len(doc_item.get("questions", []))
        is_active = (st.session_state.get("active_document") == doc_item)

        col_row, col_act = st.columns([5, 1])
        with col_row:
            st.markdown(
                f"""
                <div class="recent-row">
                    <div class="recent-date-badge">
                        <span class="recent-date-month">{month_str}</span>
                        <span class="recent-date-day">{day_str}</span>
                    </div>
                    <div class="recent-info">
                        <div class="recent-title">{doc_item.get('title', 'Study Notes')}</div>
                        <div class="recent-meta">{topic_name} · {word_count} words · {flash_num} flashcards · {q_num} questions</div>
                    </div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {'#34d399' if is_active else '#818cf8'}; background: #22273a; padding: 0.35rem 0.75rem; border-radius: 8px; border: 1px solid #323b56;">
                        {'Active ✓' if is_active else 'Saved'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_act:
            if st.button("Study →", key=f"btn_study_{idx}", use_container_width=True):
                st.session_state["active_document"] = doc_item
                st.switch_page("pages/3_Study_Workspace.py")
else:
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 1.5rem; background: #1a1e2b; border: 1px dashed #2d344d; border-radius: 12px; margin: 0.5rem 0;">
            <div style="font-size: 1.8rem; margin-bottom: 0.4rem;">📂</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 1rem; margin-bottom: 0.25rem;">No Study Notes Uploaded Yet</div>
            <div style="color: #94a3b8; font-size: 0.85rem; max-width: 440px; margin: 0 auto 1rem auto; line-height: 1.5;">
                Upload a PDF or paste notes to generate AI summaries, topic classifications, flashcards, and quizzes. Your actual notes will appear here.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ── 5. Quick Actions ─────────────────────────────────────────────────────────
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📤 Upload Study Notes", type="primary", use_container_width=True):
        st.switch_page("pages/2_Upload_Notes.py")
with col_btn2:
    if docs:
        if st.button("📚 Open Active Workspace", use_container_width=True):
            st.switch_page("pages/3_Study_Workspace.py")
    else:
        if st.button("📁 Try a Sample Note", use_container_width=True):
            st.switch_page("pages/2_Upload_Notes.py")

st.markdown(
    """
    <div style="font-size: 0.78rem; color: #64748b; text-align: center; padding-top: 1.5rem;">
        RecallAI · Deep Learning Study Assistant · User: <strong>USER01</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
