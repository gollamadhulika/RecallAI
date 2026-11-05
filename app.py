"""RecallAI — Main Application Controller & Navigator.

Run with:  python -m streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import src.warnings_init  # noqa: F401 — suppress HF/transformers noise first

import streamlit as st

st.set_page_config(
    page_title="RecallAI — Study Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui_components import inject_custom_css, init_session_state

# Inject unified CSS and session state
inject_custom_css()
init_session_state()

# Clean multi-page navigation (eliminates 'app' entry completely from sidebar)
pages = [
    st.Page("pages/1_Dashboard.py", title="Dashboard", icon="🏠", default=True),
    st.Page("pages/2_Upload_Notes.py", title="Upload Notes", icon="📤"),
    st.Page("pages/3_Study_Workspace.py", title="Study Workspace", icon="📚"),
    st.Page("pages/4_Quiz.py", title="Quiz", icon="✏️"),
    st.Page("pages/5_Results.py", title="Results & Progress", icon="📊"),
]

pg = st.navigation(pages)
pg.run()
