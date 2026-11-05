"""RecallAI — Page 2: Upload Notes (PDF, pasted text, or sample notes)."""

import io
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.warnings_init  # noqa: F401 — suppress HF/transformers noise first

import streamlit as st

try:
    st.set_page_config(page_title="Upload Notes — RecallAI", page_icon="📤", layout="wide")
except Exception:
    pass

from src.ui_components import inject_custom_css, init_session_state, render_sidebar, render_header
from src.pdf_processor import extract_text_from_pdf, validate_text_input
from src.text_cleaner import extract_key_terms

inject_custom_css()
init_session_state()
render_sidebar()

render_header(
    "📤 Upload Study Notes",
    "Upload a PDF, paste study text, or load a sample note to run the deep learning pipeline"
)

# ── Ensure persistent staged note state ──────────────────────────────────────
if "staged_raw_text" not in st.session_state:
    st.session_state["staged_raw_text"] = ""
if "staged_title" not in st.session_state:
    st.session_state["staged_title"] = "Study Notes"
if "staged_meta" not in st.session_state:
    st.session_state["staged_meta"] = {}
if "staged_pages" not in st.session_state:
    st.session_state["staged_pages"] = []
if "staged_source_label" not in st.session_state:
    st.session_state["staged_source_label"] = ""

# ── Input method selection ──────────────────────────────────────────────────
tab_pdf, tab_text, tab_sample = st.tabs(["📄 Upload PDF", "✍️ Paste Text", "📁 Try Sample Notes"])

with tab_pdf:
    st.markdown(
        '<div class="study-box"><div class="study-box-title">📄 Drag & Drop or Browse PDF</div>',
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        "Select your PDF study notes",
        type=["pdf"],
        help="Accepts standard digital PDFs. Scanned image PDFs are not supported.",
        key="pdf_uploader_widget"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded is not None:
        file_key = f"pdf_{uploaded.name}_{uploaded.size}"
        if st.session_state.get("last_uploaded_pdf_key") != file_key:
            with st.spinner("📖 Extracting and validating text from PDF via PyMuPDF…"):
                pdf_bytes = uploaded.read()
                result = extract_text_from_pdf(pdf_bytes)

            if not result["success"]:
                st.error(f"⚠️ {result['error']}")
            else:
                st.session_state["staged_raw_text"] = result["text"]
                st.session_state["staged_title"] = uploaded.name.replace(".pdf", "").replace("_", " ").title()
                st.session_state["staged_meta"] = result["metadata"]
                st.session_state["staged_pages"] = result["pages"]
                st.session_state["staged_source_label"] = f"PDF: {uploaded.name}"
                st.session_state["last_uploaded_pdf_key"] = file_key
                st.rerun()

    if st.session_state.get("staged_source_label", "").startswith("PDF:") and st.session_state.get("staged_pages"):
        meta = st.session_state.get("staged_meta", {})
        pages = st.session_state.get("staged_pages", [])
        st.success(
            f"✅ Extracted **{meta.get('total_words', len(st.session_state['staged_raw_text'].split()))} words** "
            f"from **{len(pages)} page(s)**"
        )
        with st.expander("📋 View page-by-page breakdown"):
            for p in pages:
                st.markdown(
                    f"**Page {p['page_number']}** — "
                    f"{p['word_count']} words, {p['image_count']} image(s)"
                )

with tab_text:
    st.markdown(
        '<div class="study-box"><div class="study-box-title">✍️ Paste Study Notes</div>',
        unsafe_allow_html=True,
    )
    pasted = st.text_area(
        "Paste your notes here",
        height=240,
        placeholder="e.g. 'Photosynthesis is the biochemical process by which green plants convert light energy into glucose…'",
        key="pasted_text_widget"
    )
    doc_title_input = st.text_input("Document title (optional)", placeholder="e.g. Biology Lecture 3", key="pasted_title_widget")
    
    col_paste_btn, _ = st.columns([1, 2])
    with col_paste_btn:
        if st.button("📥 Load Pasted Notes", use_container_width=True, key="btn_load_pasted"):
            if pasted.strip():
                val = validate_text_input(pasted)
                if not val["valid"]:
                    st.error(f"⚠️ {val['error']}")
                else:
                    title = doc_title_input.strip() if doc_title_input.strip() else "Pasted Study Notes"
                    st.session_state["staged_raw_text"] = val["text"]
                    st.session_state["staged_title"] = title
                    st.session_state["staged_meta"] = {"total_words": val["word_count"], "total_characters": len(pasted)}
                    st.session_state["staged_pages"] = []
                    st.session_state["staged_source_label"] = f"Pasted Text: {title}"
                    st.success(f"✅ Loaded {val['word_count']} words into staging!")
                    st.rerun()
            else:
                st.warning("⚠️ Please paste some text into the box above before loading.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_sample:
    st.markdown(
        '<div class="study-box"><div class="study-box-title">📁 Quick-Load Pre-Built Academic Notes</div>'
        '<p style="color:#94a3b8;font-size:0.9rem;margin-bottom:1rem;">Click any academic subject below to load verified course material and test RecallAI immediately:</p>',
        unsafe_allow_html=True,
    )

    sample_col1, sample_col2, sample_col3 = st.columns(3)

    with sample_col1:
        if st.button("💻 Computer Systems & OS", use_container_width=True, key="btn_sample_cs"):
            sample_path = os.path.join("data", "sample_notes", "computer_systems.txt")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.session_state["staged_raw_text"] = content
                st.session_state["staged_title"] = "Operating Systems & Virtual Memory"
                st.session_state["staged_meta"] = {"total_words": len(content.split()), "total_characters": len(content)}
                st.session_state["staged_pages"] = []
                st.session_state["staged_source_label"] = "Sample: Operating Systems & Virtual Memory"
                st.rerun()

    with sample_col2:
        if st.button("🌿 Cellular Biology", use_container_width=True, key="btn_sample_bio"):
            sample_path = os.path.join("data", "sample_notes", "cellular_biology.txt")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.session_state["staged_raw_text"] = content
                st.session_state["staged_title"] = "Cellular Biology & Photosynthesis"
                st.session_state["staged_meta"] = {"total_words": len(content.split()), "total_characters": len(content)}
                st.session_state["staged_pages"] = []
                st.session_state["staged_source_label"] = "Sample: Cellular Biology & Photosynthesis"
                st.rerun()

    with sample_col3:
        if st.button("🤖 Machine Learning", use_container_width=True, key="btn_sample_ml"):
            sample_path = os.path.join("data", "sample_notes", "machine_learning.txt")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.session_state["staged_raw_text"] = content
                st.session_state["staged_title"] = "Machine Learning & Neural Networks"
                st.session_state["staged_meta"] = {"total_words": len(content.split()), "total_characters": len(content)}
                st.session_state["staged_pages"] = []
                st.session_state["staged_source_label"] = "Sample: Machine Learning & Neural Networks"
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ── Preview & Process ────────────────────────────────────────────────────────
raw_text = st.session_state.get("staged_raw_text", "").strip()
source_title = st.session_state.get("staged_title", "Study Notes")
source_meta = st.session_state.get("staged_meta", {})
source_pages = st.session_state.get("staged_pages", [])
source_label = st.session_state.get("staged_source_label", "Loaded Material")

if raw_text:
    st.markdown("---")

    col_info, col_clear = st.columns([4, 1])
    with col_info:
        word_count = len(raw_text.split())
        st.markdown(
            f"""
            <div style="background:#151823;border:1.5px solid #232838;border-left:4px solid #6366f1;border-radius:10px;padding:0.85rem 1.15rem;margin-bottom:0.75rem;">
                <div style="font-size:0.75rem;color:#818cf8;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">Staged Material Ready For Processing</div>
                <div style="font-size:1.15rem;font-weight:700;color:#ffffff;margin-top:2px;">{source_title}</div>
                <div style="font-size:0.82rem;color:#94a3b8;margin-top:3px;">Source: <strong>{source_label}</strong> · Total: <strong>{word_count} words</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_clear:
        if st.button("🗑️ Clear Note", use_container_width=True, key="btn_clear_staged"):
            st.session_state["staged_raw_text"] = ""
            st.session_state["staged_title"] = ""
            st.session_state["staged_meta"] = {}
            st.session_state["staged_pages"] = []
            st.session_state["staged_source_label"] = ""
            st.session_state["last_uploaded_pdf_key"] = None
            st.rerun()

    st.markdown("### 👁️ Extracted Text Preview")
    preview_text = raw_text[:2500]
    with st.expander(f"Review Extracted Text ({len(raw_text.split())} words)", expanded=False):
        st.markdown(
            f'<div style="background:#151823;border:1px solid #282f44;border-radius:12px;'
            f'padding:1.25rem;font-size:0.92rem;line-height:1.7;max-height:320px;overflow-y:auto;color:#e2e8f0;">'
            f'{preview_text.replace(chr(10), "<br>")}{"…" if len(raw_text) > 2500 else ""}</div>',
            unsafe_allow_html=True,
        )

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.metric("Total Extracted Words", source_meta.get("total_words", len(raw_text.split())))
    with col_right:
        prefer_abs = st.checkbox("Enable abstractive summarizer (slower)", value=False, key="chk_abs_sum")

    if st.button("🚀 Process Notes with Deep Learning", type="primary", use_container_width=True, key="btn_process_dl"):
        progress = st.progress(0, text="Initialising deep learning engine…")

        # 1. Embeddings & Classification
        progress.progress(20, text="Classifying topic with DistilBERT zero-shot…")
        from src.topic_classifier import classify_study_notes
        topic_result = classify_study_notes(raw_text)

        # 2. Summarisation
        progress.progress(45, text="Generating semantic centroid summary (MMR)…")
        from src.summarizer import generate_summary
        summary_result = generate_summary(raw_text, prefer_abstractive=prefer_abs)

        # 3. Key terms
        progress.progress(65, text="Extracting key concept definitions…")
        key_terms = extract_key_terms(raw_text, max_terms=15)

        # 4. Flashcards
        progress.progress(80, text="Generating interactive flashcards…")
        from src.flashcards import generate_flashcards
        cards = generate_flashcards(raw_text, max_cards=8)

        # 5. Quiz questions
        progress.progress(92, text="Generating questions with semantic distractors…")
        from src.question_generator import generate_quiz_questions
        questions = generate_quiz_questions(raw_text, max_questions=6)

        progress.progress(100, text="✅ Processing complete!")

        doc_record = {
            "title":     source_title,
            "text":      raw_text,
            "metadata":  source_meta,
            "pages":     source_pages,
            "topic":     topic_result,
            "summary":   summary_result,
            "key_terms": key_terms,
            "flashcards": cards,
            "questions": questions,
        }

        st.session_state["active_document"] = doc_record
        st.session_state["documents_history"].append(doc_record)
        st.session_state["total_documents"] = len(st.session_state["documents_history"])

        # Create active quiz immediately so Quiz page has questions ready to start
        from src.quiz_engine import create_quiz_session
        st.session_state["active_quiz"] = create_quiz_session(questions, title=f"{source_title} Quiz")
        st.session_state["quiz_current_idx"] = 0

        st.success("🎉 Notes successfully processed! Your study material is ready.")
        st.balloons()
        st.rerun()

# ── If an active document exists, show status banner and direct navigation ───
active_doc = st.session_state.get("active_document")
if active_doc:
    topic_res = active_doc.get("topic", {})
    summary_res = active_doc.get("summary", {})
    cards_list = active_doc.get("flashcards", [])
    qs_list = active_doc.get("questions", [])

    st.markdown("---")
    st.markdown(
        f"""
        <div style="background-color: #171b2d; border: 2px solid #4338ca; border-radius: 14px; padding: 1.35rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div style="font-size: 0.76rem; color: #818cf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Active Processed Document</div>
            <div style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin: 0.25rem 0;">
                {active_doc.get('title', 'Study Notes')} — {topic_res.get('primary_topic', 'General')}
            </div>
            <div style="display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.65rem;">
                <span class="topic-pill">Confidence: {topic_res.get('confidence_percent', '—')}</span>
                <span class="model-badge">Model: {topic_res.get('model_used', 'DistilBERT')}</span>
                <span class="model-badge">Summary Compression: {summary_res.get('compression_ratio', '—')}</span>
                <span class="model-badge">{len(cards_list)} Flashcards</span>
                <span class="model-badge">{len(qs_list)} Practice Questions</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.button("📚 Open Study Workspace →", type="primary", use_container_width=True, key="nav_ws_btn"):
            st.switch_page("pages/3_Study_Workspace.py")
    with nav_col2:
        if st.button("✏️ Take Practice Quiz →", use_container_width=True, key="nav_quiz_btn"):
            st.switch_page("pages/4_Quiz.py")
