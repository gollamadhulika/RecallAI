"""RecallAI — Page 3: Study Workspace (summary, topic, search, flashcards, questions)."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.warnings_init  # noqa: F401

import streamlit as st

try:
    st.set_page_config(page_title="Study Workspace — RecallAI", page_icon="📚", layout="wide")
except Exception:
    pass

from src.ui_components import inject_custom_css, init_session_state, render_sidebar, render_header
from src.text_embeddings import semantic_search
from src.text_cleaner import split_into_sentences

inject_custom_css()
init_session_state()
render_sidebar()

render_header(
    "📚 Study Workspace",
    "Your AI-generated summaries, key concepts, flashcards, semantic search, and practice questions"
)

doc = st.session_state.get("active_document")
if not doc:
    st.warning("⚠️ No study notes loaded. Please visit **Upload Notes** first to process your material.")
    if st.button("📤 Go to Upload Notes", type="primary"):
        st.switch_page("pages/2_Upload_Notes.py")
    st.stop()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_summary, tab_topic, tab_search, tab_flash, tab_qs, tab_source = st.tabs(
    ["📝 Summary", "🏷️ Topic & Concepts", "🔍 Semantic Search", "🗂️ Flashcards", "❓ Practice Questions", "📄 Source Text"]
)

# ── 1. SUMMARY ────────────────────────────────
with tab_summary:
    summary = doc.get("summary", {})
    method  = summary.get("method", "Semantic Extractive Centroid Selection")
    model   = summary.get("model_used", "Sentence-Transformers (all-MiniLM-L6-v2)")

    st.markdown(
        f"""
        <div class="study-box">
            <div class="study-box-title">
                📝 AI-Generated Summary
                <span class="model-badge">{model}</span>
            </div>
            <p style="color:#94a3b8;font-size:0.85rem;margin-bottom:0.75rem;">
                Method: <strong>{method}</strong> &nbsp;|&nbsp;
                Compression: <strong>{summary.get('compression_ratio','—')}</strong> &nbsp;|&nbsp;
                {summary.get('original_words','—')} words → {summary.get('summary_words','—')} words
            </p>
            <hr style="border:none;border-top:1px solid #232838;margin-bottom:0.75rem;">
            <p style="font-size:1.02rem;line-height:1.75;color:#f8fafc;">{summary.get('summary_text','No summary generated.')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    bullets = summary.get("bullet_points", [])
    if bullets and len(bullets) > 1:
        st.markdown("#### 📌 Core Concept Takeaways (MMR Ranked)")
        for i, b in enumerate(bullets, 1):
            st.markdown(
                f'<div style="padding:0.75rem 0.95rem;margin:0.4rem 0;background:#1a1e2b;'
                f'border:1px solid #282f44;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;'
                f'font-size:0.94rem;color:#f8fafc;line-height:1.55;">{i}. {b}</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div style="margin-top:1.25rem;background:#064e3b33;border:1px solid #059669;border-radius:10px;padding:0.75rem 0.95rem;font-size:0.82rem;color:#6ee7b7;">
            <strong>🎓 Academic Integrity Note:</strong> Semantic Extractive Summarization selects real, verbatim sentences
            from your notes using vector centroid cosine similarity — guaranteeing 0% hallucination and 100% fidelity to the source.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── 2. TOPIC & CONCEPTS ──────────────────────
with tab_topic:
    topic = doc.get("topic", {})
    key_terms = doc.get("key_terms", [])

    st.markdown(
        f"""
        <div class="study-box">
            <div class="study-box-title">🏷️ Predicted Academic Domain</div>
            <div style="margin-bottom:0.75rem; display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center;">
                <span class="topic-pill">📚 {topic.get('primary_topic','—')}</span>
                <span class="model-badge">Confidence: {topic.get('confidence_percent','—')}</span>
                <span class="model-badge">Algorithm: {topic.get('method','—')}</span>
            </div>
            <p style="color:#94a3b8;font-size:0.84rem;margin-top:0.4rem;line-height:1.5;">
                <strong>Model Checkpoint:</strong> <code>{topic.get('model_used','—')}</code><br/>
                <strong>Training Status:</strong> <em>{topic.get('training_distinction','Pretrained Zero-Shot Inference')}</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Full topic score breakdown
    all_scores = topic.get("all_scores", [])
    if all_scores:
        st.markdown("#### 📊 Domain Probability Distribution")
        for entry in all_scores:
            bar_pct = max(min(int(entry.get("score", 0) * 100), 100), 2)
            pct_str = entry.get("percentage", f"{bar_pct}%")
            is_top = entry["topic"] == topic.get("primary_topic")
            color = "#6366f1" if is_top else "#475569"
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:0.75rem;margin:0.4rem 0;font-size:0.88rem;">
                    <div style="width:230px;color:#ffffff;font-weight:{'700' if is_top else '500'};">
                        {entry['topic']}
                    </div>
                    <div style="flex:1;background:#1f2434;border-radius:20px;height:10px;overflow:hidden;">
                        <div style="background:{color};width:{bar_pct}%;height:100%;border-radius:20px;"></div>
                    </div>
                    <div style="width:55px;text-align:right;color:{'#818cf8' if is_top else '#94a3b8'};font-weight:700;">{pct_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Key Terms Grid
    if key_terms:
        st.markdown("#### 🔑 Extracted Key Concepts")
        cols = st.columns(3)
        for i, term in enumerate(key_terms):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:#1a1e2b;border:1px solid #282f44;border-radius:10px;
                         padding:0.7rem 0.9rem;margin:0.35rem 0;font-size:0.88rem;box-shadow:0 2px 6px rgba(0,0,0,0.15);">
                        <strong style="color:#ffffff;">{term['term']}</strong>
                        <span style="color:#94a3b8;font-size:0.76rem;"> · freq {term['frequency']}</span><br/>
                        <span style="color:#818cf8;font-size:0.76rem;font-weight:500;">{term.get('type','Key Concept')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ── 3. SEMANTIC SEARCH ────────────────────────
with tab_search:
    st.markdown("#### 🔍 Semantic Vector Search (Dense Embeddings)")
    st.markdown(
        '<p style="color:#94a3b8;font-size:0.9rem;">Ask a question or enter keywords to find the most relevant sentences in your notes using Sentence-Transformers cosine similarity:</p>',
        unsafe_allow_html=True
    )
    search_query = st.text_input(
        "Enter query:",
        placeholder="e.g. 'What is the role of ATP Synthase?' or 'What causes deadlocks?'",
        key="sem_search_query"
    )

    if search_query.strip():
        all_sentences = split_into_sentences(doc.get("text", ""))
        matches = semantic_search(search_query, all_sentences, top_k=4)

        if matches:
            st.markdown(f"**Top {len(matches)} Relevant Passages:**")
            for m in matches:
                sim_pct = f"{m['similarity_score'] * 100:.1f}%"
                st.markdown(
                    f"""
                    <div style="background:#1a1e2b; border:1px solid #282f44; border-left:4px solid #6366f1; border-radius:0 10px 10px 0; padding:0.9rem 1.15rem; margin:0.5rem 0;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
                            <span style="font-size:0.75rem; font-weight:700; color:#818cf8; text-transform:uppercase;">Rank #{m['rank']} Match</span>
                            <span class="topic-pill" style="font-size:0.75rem; padding:0.15rem 0.5rem;">Cosine Similarity: {sim_pct}</span>
                        </div>
                        <div style="font-size:0.95rem; color:#f8fafc; line-height:1.55;">{m['text']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No matching passages found.")

# ── 4. FLASHCARDS ─────────────────────────────
with tab_flash:
    cards = doc.get("flashcards", [])
    if not cards:
        st.info("No flashcards generated. Try uploading notes with clear definitions.")
    else:
        st.markdown(f"**{len(cards)} flashcards generated** — click each card to reveal the definition.")
        mastered = st.session_state.get("mastered_flashcards", set())

        for card in cards:
            cid = card["id"]
            is_mastered = cid in mastered
            label = "✅ Mastered" if is_mastered else card["category"]

            with st.expander(f"{'✅ ' if is_mastered else '🔵 '} {card['term']}  ·  {label}"):
                st.markdown(
                    f"""
                    <div class="flashcard">
                        <div class="flashcard-term">📖 {card['term']}</div>
                        <div class="flashcard-definition">{card['definition']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                toggle_label = "Mark as Mastered ✅" if not is_mastered else "Unmark"
                if st.button(toggle_label, key=f"flash_btn_{cid}"):
                    if is_mastered:
                        mastered.discard(cid)
                    else:
                        mastered.add(cid)
                    st.session_state["mastered_flashcards"] = mastered
                    st.rerun()

        total_mastered = len(mastered & {c["id"] for c in cards})
        st.progress(total_mastered / len(cards), text=f"{total_mastered}/{len(cards)} mastered")

# ── 5. PRACTICE QUESTIONS ─────────────────────
with tab_qs:
    questions = doc.get("questions", [])
    if not questions:
        st.info("No questions generated. Ensure your notes contain clear definitions or concepts.")
    else:
        st.markdown(
            f"**{len(questions)} practice questions generated** using semantic distractor matching."
        )
        st.markdown(
            '<div style="background:#78350f26;border:1px solid #d97706;border-radius:8px;padding:0.75rem 1rem;'
            'font-size:0.84rem;color:#fcd34d;margin-bottom:1rem;">⚠️ <strong>Generation Method: </strong>'
            'Questions are framed from factual sentences and options are curated using Sentence-Transformers vector similarity. '
            'All answers are verified directly against your uploaded notes.</div>',
            unsafe_allow_html=True,
        )
        for q in questions:
            with st.expander(f"Q{q['id']}: {q['question'][:80]}…"):
                st.markdown(f"**{q['question']}**")
                for i, opt in enumerate(q["options"]):
                    tick = "✅ " if i == q["correct_index"] else "   "
                    st.markdown(f"{tick}**{chr(65+i)}.** {opt}")
                st.markdown(
                    f'<div style="background:#064e3b33;border:1px solid #059669;border-radius:6px;'
                    f'padding:0.6rem 0.85rem;font-size:0.86rem;margin-top:0.5rem;color:#6ee7b7;">'
                    f'📌 <strong>Explanation:</strong> {q["explanation"]}</div>',
                    unsafe_allow_html=True,
                )
                st.caption(f"Method: {q.get('generation_method','—')}")

        if st.button("✏️ Launch Practice Quiz →", type="primary", use_container_width=True):
            from src.quiz_engine import create_quiz_session
            session = create_quiz_session(questions, title=f"{doc['title']} Quiz")
            st.session_state["active_quiz"] = session
            st.switch_page("pages/4_Quiz.py")

# ── 6. SOURCE TEXT ────────────────────────────
with tab_source:
    st.markdown("#### 📄 Extracted Source Notes")
    st.text_area(
        "Source text from your document:",
        value=doc.get("text", ""),
        height=500,
        disabled=True,
    )
