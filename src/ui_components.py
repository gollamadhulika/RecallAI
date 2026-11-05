"""RecallAI UI Design System — Dribbble-Inspired Modern Dark Study Dashboard.

Sleek matte charcoal background, vibrant metric cards (Periwinkle, Coral, Emerald, Amber),
interactive segmented controls, and crisp contrast optimized for desktop web.
"""

import streamlit as st
from typing import Dict, Any, List, Optional

# RecallAI Palette — Inspired by UX Jungle Study App
COLOR_BG_APP = "#0d0f15"
COLOR_BG_SIDEBAR = "#0d0f15"
COLOR_BG_CARD = "#151823"
COLOR_BG_CARD_HOVER = "#1c2030"
COLOR_BORDER = "#232838"
COLOR_BORDER_FOCUS = "#4f46e5"

COLOR_TEXT_PRIMARY = "#ffffff"
COLOR_TEXT_SECONDARY = "#94a3b8"
COLOR_TEXT_MUTED = "#64748b"

# Metric Card Gradients
GRADIENT_PURPLE = "linear-gradient(135deg, #6366f1 0%, #4338ca 100%)"
GRADIENT_CORAL = "linear-gradient(135deg, #fb7185 0%, #e11d48 100%)"
GRADIENT_EMERALD = "linear-gradient(135deg, #2dd4bf 0%, #0d9488 100%)"
GRADIENT_AMBER = "linear-gradient(135deg, #fbbf24 0%, #d97706 100%)"


def init_session_state() -> None:
    """Initializes global session state variables for RecallAI across all pages."""
    defaults = {
        "active_document": None,       # Current processed document dict
        "documents_history": [],       # List of all processed documents in this session
        "active_quiz": None,           # Current active quiz session dict
        "quiz_history": [],            # List of completed quiz results
        "total_documents": 0,
        "total_quizzes": 0,
        "mastered_flashcards": set(),  # Set of card ids mastered
        "quiz_current_idx": 0,
        "student_name": "USER01",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def inject_custom_css() -> None:
    """
    Injects custom CSS styling for a modern, sleek dark academic web dashboard
    inspired by top Figma/Dribbble study UI designs.
    """
    st.markdown(
        """
        <style>
        /* ── 1. Global Typography & Background ────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
            color: #f8fafc !important;
            background-color: #0d0f15 !important;
        }

        [data-testid="stAppViewContainer"], .main, .block-container {
            background-color: #0d0f15 !important;
            color: #f8fafc !important;
        }

        /* ── 2. Headings & Typography ─────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        p, span, label, li, td, th {
            color: #94a3b8;
        }

        /* ── 3. Sleek Charcoal Sidebar ───────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background-color: #0d0f15 !important;
            border-right: 1.5px solid #1f2433 !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #0d0f15 !important;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] label {
            color: #94a3b8;
        }

        /* ── 4. Sidebar Navigation Links (High Contrast Dark Style) ───────── */
        [data-testid="stSidebarNav"] {
            background-color: #0d0f15 !important;
            padding: 0.5rem 0.25rem 0.75rem 0.25rem !important;
            border-bottom: 1px solid #1f2433 !important;
            margin-bottom: 0.85rem !important;
        }
        [data-testid="stSidebarNav"] ul {
            list-style: none !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.4rem !important;
        }
        [data-testid="stSidebarNav"] li {
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Inactive Navigation Card */
        [data-testid="stSidebarNav"] a {
            background-color: #151823 !important;
            border: 1px solid #232838 !important;
            border-radius: 10px !important;
            padding: 0.55rem 0.9rem !important;
            text-decoration: none !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            transition: all 0.18s ease-in-out !important;
        }
        [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNav"] a div {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
        }
        [data-testid="stSidebarNav"] a svg {
            fill: #818cf8 !important;
            color: #818cf8 !important;
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: #1c2132 !important;
            border-color: #4338ca !important;
            transform: translateX(3px) !important;
        }
        [data-testid="stSidebarNav"] a:hover span {
            color: #ffffff !important;
        }

        /* Active Navigation Card (Glowing Indigo Pill) */
        [data-testid="stSidebarNav"] a[aria-current="page"],
        [data-testid="stSidebarNav"] li:has(a[aria-current="page"]) a {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
            border: 1px solid #6366f1 !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span,
        [data-testid="stSidebarNav"] a[aria-current="page"] div,
        [data-testid="stSidebarNav"] a[aria-current="page"] p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }

        /* ── 5. Student Welcome Header Banner ─────────────────────────────── */
        .student-header-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #151823;
            border: 1px solid #232838;
            border-radius: 16px;
            padding: 1.25rem 1.75rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }
        .student-header-left {
            display: flex;
            flex-direction: column;
        }
        .student-sub {
            color: #94a3b8;
            font-size: 0.88rem;
            font-weight: 500;
        }
        .student-name {
            color: #ffffff;
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-top: 2px;
        }
        .student-header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .avatar-circle {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
            border: 2px solid #ffffff22;
        }
        .bell-icon {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: #1c2030;
            border: 1px solid #2d344d;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            color: #cbd5e1;
            cursor: pointer;
        }

        /* ── 6. Dribbble-Style Vibrant Metric Cards ───────────────────────── */
        .metric-cards-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.75rem;
        }
        @media (max-width: 900px) {
            .metric-cards-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        .vibrant-card {
            border-radius: 16px;
            padding: 1.4rem 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        .vibrant-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
        }
        .card-purple {
            background: linear-gradient(135deg, #5c6bf2 0%, #4338ca 100%);
        }
        .card-coral {
            background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%);
        }
        .card-emerald {
            background: linear-gradient(135deg, #2dd4bf 0%, #0d9488 100%);
        }
        .card-amber {
            background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
        }
        .vibrant-num {
            font-size: 2.35rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1;
            margin-bottom: 0.35rem;
            letter-spacing: -0.02em;
        }
        .vibrant-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #ffffff;
            opacity: 0.95;
            letter-spacing: 0.02em;
        }

        /* ── 7. Segmented Pill Tab Bar ────────────────────────────────────── */
        .pill-tab-bar {
            display: flex;
            background: #151823;
            border: 1px solid #232838;
            border-radius: 12px;
            padding: 0.35rem;
            gap: 0.35rem;
            margin-bottom: 1.5rem;
        }
        .pill-tab-item {
            flex: 1;
            padding: 0.65rem 1rem;
            border-radius: 9px;
            text-align: center;
            text-decoration: none !important;
            font-size: 0.88rem;
            font-weight: 600;
            color: #94a3b8 !important;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.45rem;
        }
        .pill-tab-item:hover {
            background: #1e2334;
            color: #ffffff !important;
        }
        .pill-tab-active {
            background: #ffffff !important;
            color: #0f1117 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            font-weight: 700;
        }
        .pill-tab-active span {
            color: #0f1117 !important;
        }

        /* ── 8. Recent Items Section (Dribbble List Style) ─────────────────── */
        .recents-box {
            background: #151823;
            border: 1px solid #232838;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .recents-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .recent-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            background: #1a1e2b;
            border: 1px solid #282f44;
            border-radius: 12px;
            padding: 0.85rem 1.15rem;
            margin-bottom: 0.6rem;
            transition: all 0.18s ease;
        }
        .recent-row:hover {
            background: #202638;
            border-color: #3b4566;
            transform: translateX(3px);
        }
        .recent-date-badge {
            background: #242a3e;
            border: 1px solid #333c56;
            border-radius: 9px;
            width: 46px;
            height: 46px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            flex-shrink: 0;
        }
        .recent-date-month {
            font-size: 0.65rem;
            font-weight: 700;
            color: #818cf8;
            text-transform: uppercase;
            line-height: 1;
        }
        .recent-date-day {
            font-size: 1rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }
        .recent-info {
            flex: 1;
            overflow: hidden;
        }
        .recent-title {
            color: #ffffff;
            font-weight: 700;
            font-size: 0.95rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .recent-meta {
            color: #94a3b8;
            font-size: 0.78rem;
            margin-top: 2px;
        }

        /* ── 9. Study Boxes, Cards & Containers ───────────────────────────── */
        .study-box {
            background-color: #151823 !important;
            border: 1px solid #232838 !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.25rem !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        }
        .study-box-title {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            border-bottom: 1px solid #232838 !important;
            padding-bottom: 0.65rem !important;
            margin-bottom: 1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }

        /* Topic Pills & Badges */
        .topic-pill {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.4rem !important;
            background-color: #1e1b4b !important;
            color: #a5b4fc !important;
            padding: 0.35rem 0.85rem !important;
            border-radius: 20px !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            border: 1px solid #3730a3 !important;
        }
        .model-badge {
            display: inline-block !important;
            background-color: #1a1e2b !important;
            color: #cbd5e1 !important;
            padding: 0.25rem 0.65rem !important;
            border-radius: 6px !important;
            font-size: 0.78rem !important;
            font-family: monospace !important;
            border: 1px solid #2d344d !important;
            font-weight: 500 !important;
        }

        /* Flashcards & Quiz Cards */
        .flashcard {
            background: #151823 !important;
            border: 1px solid #282f44 !important;
            border-radius: 14px !important;
            padding: 1.35rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
            border-left: 5px solid #6366f1 !important;
        }
        .flashcard-term {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            margin-bottom: 0.5rem !important;
        }
        .flashcard-definition {
            font-size: 0.95rem !important;
            color: #cbd5e1 !important;
            line-height: 1.65 !important;
        }

        .quiz-card {
            background: #151823 !important;
            border: 1px solid #282f44 !important;
            border-radius: 16px !important;
            padding: 1.85rem !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
            margin-bottom: 1.5rem !important;
        }
        .quiz-question-number {
            color: #818cf8 !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 0.5rem !important;
        }
        .quiz-question-text {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            line-height: 1.45 !important;
            margin-bottom: 1.25rem !important;
        }

        /* ── 10. Form Controls, Radios & Primary Buttons ──────────────────── */
        button[data-baseweb="tab"] {
            color: #94a3b8 !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important;
            border-bottom-color: #6366f1 !important;
            font-weight: 700 !important;
        }

        .stRadio label, .stCheckbox label, .stSelectbox label,
        .stTextInput label, .stTextArea label, .stFileUploader label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .stRadio div[data-baseweb="radio"] span {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
        }

        /* Primary Action Buttons */
        button[kind="primary"] {
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.25rem !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.5) !important;
            transform: translateY(-1px) !important;
        }

        /* Expanders in Dark Theme */
        .streamlit-expanderHeader {
            background-color: #1a1e2b !important;
            border: 1px solid #232838 !important;
            border-radius: 10px !important;
        }
        .streamlit-expanderHeader p, .streamlit-expanderHeader span {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_header(title: str = "Welcome Aboard,", subtitle: str = "USER01") -> None:
    """Renders the top welcome student bar with authentic user credentials."""
    init_session_state()
    student_name = subtitle if (subtitle and subtitle != "Aleksander Petrov") else st.session_state.get("student_name", "USER01")

    st.markdown(
        f"""
        <div class="student-header-bar">
            <div class="student-header-left">
                <span class="student-sub">Welcome Aboard,</span>
                <span class="student-name">{student_name}</span>
            </div>
            <div class="student-header-right">
                <div class="bell-icon" title="Notifications">🔔</div>
                <div class="avatar-circle" title="{student_name}">👤</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sidebar() -> None:
    """Renders persistent sidebar information, active document state, and session statistics."""
    init_session_state()
    with st.sidebar:
        st.markdown(
            """
            <div style="padding-bottom: 0.75rem; border-bottom: 1px solid #1f2433; margin-bottom: 0.85rem;">
                <h2 style="color: #ffffff; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em;">
                    🧠 RecallAI
                </h2>
                <div style="color: #818cf8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
                    Personalized Study Assistant
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Active Document Status Card
        active_doc = st.session_state.get("active_document")
        if active_doc:
            topic_name = active_doc.get("topic", {}).get("primary_topic", "Classified")
            word_count = active_doc.get("metadata", {}).get("total_words", 0)
            doc_title = active_doc.get("title", "Study Notes")
            if len(doc_title) > 22:
                doc_title = doc_title[:22] + "…"

            st.markdown(
                f"""
                <div style="background-color: #171b2d; border: 1.5px solid #2d3656; border-radius: 12px; padding: 0.85rem; margin-bottom: 0.85rem;">
                    <div style="font-size: 0.7rem; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Active Notes</div>
                    <div style="font-weight: 700; color: #ffffff; font-size: 0.92rem; word-break: break-word; margin-top: 2px;">
                        📄 {doc_title}
                    </div>
                    <div style="font-size: 0.76rem; color: #94a3b8; font-weight: 500; margin-top: 3px;">
                        {topic_name} · {word_count} words
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background-color: #151823; border: 1px dashed #282f44; border-radius: 10px; padding: 0.75rem; font-size: 0.82rem; color: #94a3b8; margin-bottom: 0.85rem;">
                    ℹ️ No active notes loaded. Visit <strong>Upload Notes</strong> to begin.
                </div>
                """,
                unsafe_allow_html=True
            )

        # Session Metrics
        docs_count = len(st.session_state.get("documents_history", []))
        quizzes_count = len(st.session_state.get("quiz_history", []))

        st.markdown(
            '<div style="font-weight: 700; font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">📊 Session Stats</div>',
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", docs_count)
        with col2:
            st.metric("Quizzes", quizzes_count)

        if quizzes_count > 0:
            avg_score = sum(q.get("percentage", 0) for q in st.session_state["quiz_history"]) / quizzes_count
            st.metric("Avg Score", f"{avg_score:.1f}%")

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 0.73rem; color: #64748b; line-height: 1.5;">
                <strong style="color: #94a3b8;">Deep Learning Engine:</strong><br/>
                • <code>all-MiniLM-L6-v2</code> (Embeddings)<br/>
                • <code>DistilBERT MNLI</code> (Topic Classifier)<br/>
                • Semantic Centroid MMR Summarizer<br/>
                • Vector Distractor Generator
            </div>
            """,
            unsafe_allow_html=True
        )
