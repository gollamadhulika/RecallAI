"""Generate a comprehensive, beautifully formatted PDF code explanation guide for RecallAI."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "RecallAI — Deep Learning Code Walkthrough & Architecture Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        
        footer_text = "DS306 Deep Learning · Golla Madhulika (23STUCHH010826) & Reethu Reddy (23STUCHH011082) · Instructor: Dr. Kongara Srinivasa Rao"
        self.drawString(54, 32, footer_text)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_filename = r"d:\mare\RecallAI_Code_Explanation_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Palette
    C_PRIMARY = colors.HexColor("#1e1b4b")   # Dark Indigo
    C_INDIGO  = colors.HexColor("#4338ca")   # Mid Indigo
    C_ACCENT  = colors.HexColor("#0f766e")   # Deep Teal
    C_AMBER   = colors.HexColor("#b45309")   # Amber
    C_DARK    = colors.HexColor("#0f172a")   # Slate 900
    C_BODY    = colors.HexColor("#1e293b")   # Slate 800
    C_MUTED   = colors.HexColor("#475569")   # Slate 600
    C_BG_BOX  = colors.HexColor("#f8fafc")   # Card background
    C_LINE    = colors.HexColor("#cbd5e1")   # Border
    C_CODE_BG = colors.HexColor("#f1f5f9")   # Code block background

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=C_PRIMARY,
        spaceAfter=4,
    )

    sub_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=C_ACCENT,
        textTransform="uppercase",
        spaceAfter=4,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=C_PRIMARY,
        spaceBefore=14,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "ModuleH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=C_INDIGO,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "StandardBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=C_BODY,
        spaceAfter=4,
    )

    say_style = ParagraphStyle(
        "WhatToSay",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0f172a"),
        leftIndent=10,
        spaceAfter=4,
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    )

    bold_label = ParagraphStyle(
        "BoldLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=C_DARK,
    )

    card_text = ParagraphStyle(
        "CardText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=C_BODY,
    )

    story = []

    # ── HEADER BANNER ──────────────────────────────────────────────────────────
    story.append(Paragraph("DEEP LEARNING (DS306) · CODE ARCHITECTURE & TECHNICAL VIVA GUIDE", sub_style))
    story.append(Paragraph("RecallAI: End-to-End Source Code & Deep Learning Walkthrough", title_style))
    story.append(Paragraph("<b>Course Instructor:</b> Dr. Kongara Srinivasa Rao &nbsp;|&nbsp; <b>Framework:</b> PyTorch · Transformers · Streamlit", body_style))
    story.append(Spacer(1, 4))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Student 1:</b> Golla Madhulika (23STUCHH010826)", body_style),
            Paragraph("<b>Student 2:</b> Reethu Reddy (23STUCHH011082)", body_style)
        ],
        [
            Paragraph("<b>Focus:</b> Deep Learning Models, Math & Pipelines", body_style),
            Paragraph("<b>Files Covered:</b> 10 Modular Components (18 Tests Passing)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_BOX),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # PART 1: PRIMARILY THE DEEP LEARNING MODELS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 1: The Deep Learning Architecture (Show These First)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=8))

    # Module 1: text_embeddings.py
    story.append(Paragraph("1. <code>src/text_embeddings.py</code> — Dense Semantic Embeddings Engine", h2_style))
    p_emb_say = (
        "<b>What to tell Sir:</b> <i>\"Sir, this is our mathematical foundation. Instead of using classical Bag-of-Words "
        "or TF-IDF which fail when synonyms are used, we utilize the Sentence-Transformers model <code>all-MiniLM-L6-v2</code>. "
        "It maps sentences into a continuous 384-dimensional dense semantic vector space where contextual similarity equals geometric proximity.\"</i>"
    )
    story.append(Paragraph(p_emb_say, say_style))

    emb_code = (
        "def generate_embeddings(texts, model_name='all-MiniLM-L6-v2'):\n"
        "    model = get_embedding_model(model_name)  # Cached SentenceTransformer instance\n"
        "    embeddings = model.encode(texts, show_progress_bar=False,\n"
        "                              convert_to_numpy=True, normalize_embeddings=True)\n"
        "    return embeddings  # Shape: (N, 384) with unit L2 norm\n\n"
        "def compute_cosine_similarity(vec_a, vec_b):\n"
        "    # Cosine Similarity = (A . B) / (||A|| * ||B||)\n"
        "    return np.dot(vec_a_norm, vec_b_norm.T)  # Pairwise matrix dot product"
    )
    t_c1 = Table([[Paragraph(emb_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[500])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c1)

    story.append(Paragraph(
        "<b>Key Technical Details to Highlight:</b><br/>"
        "• <b>Transformer Architecture:</b> 6-layer Transformer, 12 attention heads, 22.7M parameters.<br/>"
        "• <b>Mean Pooling:</b> Token embeddings produced by self-attention are averaged with attention masking.<br/>"
        "• <b>Unit Normalization (L2):</b> Vectors are scaled so ||v|| = 1.0, meaning Cosine Similarity is simply the Dot Product.<br/>"
        "• <b>Execution Time:</b> Runs entirely on CPU with PyTorch runtime, encoding a full page of notes in under 50ms.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Module 2: topic_classifier.py
    story.append(Paragraph("2. <code>src/topic_classifier.py</code> — Zero-Shot NLI Classification", h2_style))
    p_cls_say = (
        "<b>What to tell Sir:</b> <i>\"Sir, instead of training a custom supervised classifier which requires thousands of labeled examples "
        "and cannot generalize across college subjects, we formulate topic identification as Natural Language Inference (NLI) using "
        "<code>typeform/distilbert-base-uncased-mnli</code> (66M parameters). It evaluates entailment against 10 academic domains zero-shot.\"</i>"
    )
    story.append(Paragraph(p_cls_say, say_style))

    cls_code = (
        "# Zero-Shot NLI Formulation\n"
        "result = classifier(\n"
        "    sample_text,\n"
        "    candidate_labels=['Computer Science', 'Biology', 'Physics', 'Mathematics', ...],\n"
        "    hypothesis_template='This educational text is about {}.'\n"
        ")\n"
        "# Model computes Softmax probability over Entailment vs Contradiction logits"
    )
    t_c2 = Table([[Paragraph(cls_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[500])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c2)

    story.append(Paragraph(
        "<b>Key Technical Details to Highlight:</b><br/>"
        "• <b>NLI Mechanism:</b> Text is the <i>Premise</i>; candidate topics become the <i>Hypothesis</i>. The model calculates entailment logits.<br/>"
        "• <b>DistilBERT Efficiency:</b> 40% smaller and 60% faster than BERT-base while retaining 97% of language understanding.<br/>"
        "• <b>Secondary Centroid Fallback:</b> If NLI pipeline fails, line 148 calculates Temperature-Scaled Softmax (tau=0.15) over topic anchor embeddings.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Module 3: summarizer.py
    story.append(Paragraph("3. <code>src/summarizer.py</code> — Centroid & Maximal Marginal Relevance (MMR)", h2_style))
    p_sum_say = (
        "<b>What to tell Sir:</b> <i>\"Sir, generative models like ChatGPT hallucinate non-existent formulas or reword definitions inaccurately. "
        "In our summarizer, we guarantee 0% hallucination by selecting verbatim sentences mathematically using Document Centroid Vector "
        "and Maximal Marginal Relevance (MMR) with lambda = 0.75.\"</i>"
    )
    story.append(Paragraph(p_sum_say, say_style))

    sum_code = (
        "# 1. Calculate Document Global Centroid Vector C (Mean of sentence embeddings)\n"
        "doc_centroid = np.mean(sent_embs, axis=0, keepdims=True)\n"
        "sims = compute_cosine_similarity(sent_embs, doc_centroid).flatten()\n\n"
        "# 2. Maximal Marginal Relevance (MMR) Selection Loop\n"
        "for _ in range(target_sentences):\n"
        "    # Centrality = CosineSim(sentence, Centroid)\n"
        "    # Redundancy = Max CosineSim(sentence, already_selected_sentences)\n"
        "    mmr_score = lambda_param * centrality - (1 - lambda_param) * redundancy\n"
        "    selected_indices.append(best_candidate_index)"
    )
    t_c3 = Table([[Paragraph(sum_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[500])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c3)

    story.append(Paragraph(
        "<b>Mathematical Formula:</b><br/>"
        "MMR = argmax_{D_i in R \\ S} [ lambda * CosineSim(D_i, Centroid) - (1 - lambda) * max_{D_j in S} CosineSim(D_i, D_j) ]<br/>"
        "• <b>lambda = 0.75:</b> Balances high topic coverage (centrality) with strict non-redundancy (diversity).<br/>"
        "• <b>Academic Integrity:</b> Every sentence is extracted verbatim, guaranteeing zero hallucinated facts.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Module 4: question_generator.py
    story.append(Paragraph("4. <code>src/question_generator.py</code> — Vector-Space Distractor Synthesis", h2_style))
    p_q_say = (
        "<b>What to tell Sir:</b> <i>\"Sir, typical multiple choice question generators use random distractors that are trivially easy to eliminate. "
        "We use dense embedding cosine similarity to pick distractors from semantically proximate clusters (similarity between 0.15 and 0.94). "
        "This creates realistic, high-quality test questions that evaluate genuine conceptual understanding.\"</i>"
    )
    story.append(Paragraph(p_q_say, say_style))

    q_code = (
        "# Vector Distractor Proximity Filter\n"
        "target_emb = generate_embeddings([target_term])\n"
        "cand_embs = generate_embeddings(candidate_terms)\n"
        "sims = compute_cosine_similarity(target_emb, cand_embs)[0]\n\n"
        "# Filter sweet spot: related enough to be plausible, distinct enough to not be duplicate\n"
        "if 0.15 <= score <= 0.94 and term.lower() not in target_term.lower():\n"
        "    valid_distractors.append((term, score))"
    )
    t_c4 = Table([[Paragraph(q_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[500])
    t_c4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_c4)
    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # PART 2: ALL SUPPORTING MODULES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 2: Walkthrough of All Other Supporting Modules", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=8))

    mod_data = [
        [
            Paragraph("<b>Module & File Path</b>", bold_label),
            Paragraph("<b>Core Function & Code Highlights</b>", bold_label),
            Paragraph("<b>What to Tell Sir</b>", bold_label)
        ],
        [
            Paragraph("<b>5. PDF Processor</b><br/><code>src/pdf_processor.py</code>", card_text),
            Paragraph("<code>extract_text_from_pdf()</code><br/>Uses PyMuPDF (<code>pymupdf</code>) to parse PDF byte streams, inspect encryption flags, detect scanned image PDFs, and extract page-by-page word counts.", card_text),
            Paragraph("<i>\"Sir, PyMuPDF parses digital lecture PDFs directly in memory without saving temporary files, extracting raw text and page counts at C-speed.\"</i>", card_text)
        ],
        [
            Paragraph("<b>6. Text Cleaner</b><br/><code>src/text_cleaner.py</code>", card_text),
            Paragraph("<code>clean_text()</code>, <code>split_into_sentences()</code><br/>Strips page stamps (e.g. 'Page 1 of 5'), rejoins hyphenated breaks (trans-\\nformer -> transformer), and protects abbreviations (Dr., e.g., vs., 3.14) during sentence splitting.", card_text),
            Paragraph("<i>\"Sir, regex masks abbreviations so sentences aren't split prematurely, ensuring high embedding quality for the transformer.\"</i>", card_text)
        ],
        [
            Paragraph("<b>7. Flashcard Engine</b><br/><code>src/flashcards.py</code>", card_text),
            Paragraph("<code>generate_flashcards()</code><br/>Applies linguistic definition pattern heuristics (<code>r'^(?P<term>\\w+)\\s+is\\s+(?P<def>.+)'</code>) to pair academic concepts with their exact explanations.", card_text),
            Paragraph("<i>\"Sir, this extracts term-definition pairs from lecture notes and creates flip-to-reveal study cards with mastery state tracking.\"</i>", card_text)
        ],
        [
            Paragraph("<b>8. Quiz Engine</b><br/><code>src/quiz_engine.py</code>", card_text),
            Paragraph("<code>create_quiz_session()</code>, <code>evaluate_quiz()</code><br/>Maintains active quiz state, calculates scores, and generates diagnostic feedback (e.g. tagging 'Backpropagation' for review if missed).", card_text),
            Paragraph("<i>\"Sir, this module tracks quiz sessions and diagnoses weak concepts so the student gets targeted revision recommendations.\"</i>", card_text)
        ],
        [
            Paragraph("<b>9. UI Components</b><br/><code>src/ui_components.py</code>", card_text),
            Paragraph("<code>init_session_state()</code>, <code>inject_custom_css()</code><br/>Injects dark-mode academic CSS styling, renders the persistent sidebar with live session counters, and maintains multi-page session state.", card_text),
            Paragraph("<i>\"Sir, this defines our modern matte charcoal academic UI inspired by modern Figma study apps, maintaining state across page reloads.\"</i>", card_text)
        ],
        [
            Paragraph("<b>10. Multi-Page Controller</b><br/><code>app.py</code> & <code>pages/</code>", card_text),
            Paragraph("<code>st.navigation([st.Page(...)])</code><br/>Directs routing across 5 pages: (1) Dashboard, (2) Upload Notes, (3) Study Workspace, (4) Quiz, (5) Results & Progress.", card_text),
            Paragraph("<i>\"Sir, <code>app.py</code> controls multi-page navigation using Streamlit's official navigation API, ensuring zero page-state desynchronization.\"</i>", card_text)
        ]
    ]
    mod_table = Table(mod_data, colWidths=[110, 190, 200])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ede9fe")),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # PART 3: VIVA CHEATSHEET
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 3: 5 Critical Viva Questions Sir Might Ask", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=8))

    viva_qa = [
        (
            "Q1: Where exactly is the Deep Learning happening in your project?",
            "Sir, primarily in 3 files: (1) <code>src/text_embeddings.py</code> where <code>all-MiniLM-L6-v2</code> maps sentences into 384-dimensional dense vectors via self-attention and mean pooling; (2) <code>src/topic_classifier.py</code> where <code>distilbert-base-uncased-mnli</code> performs zero-shot cross-encoder inference; and (3) <code>src/summarizer.py</code> where MMR optimizes sentence cosine similarities against the document centroid."
        ),
        (
            "Q2: Why did you choose Pretrained Zero-Shot models rather than training your own network?",
            "Sir, university students study hundreds of diverse subjects (from Operating Systems to Organic Chemistry). Training a custom network would require millions of domain-labeled pairs and expensive GPU infrastructure. Pretrained transformers already possess generalized contextual semantic representations, allowing RecallAI to execute zero-shot inference across any syllabus instantly on standard CPU."
        ),
        (
            "Q3: Why is your summarizer Extractive instead of Abstractive (like BART or T5)?",
            "Sir, abstractive models generate new words and frequently hallucinate inaccurate formulas, false historical dates, or altered definitions. In technical subjects, student exam answers must match textbook rigor. Our MMR extractive summarizer mathematically selects verified verbatim sentences from the source notes, guaranteeing 0% hallucination."
        ),
        (
            "Q4: What is the significance of the lambda parameter in your MMR summarizer?",
            "Sir, lambda balances relevance versus redundancy. In our implementation (lambda = 0.75), 75% of the weight is given to choosing sentences closest to the document centroid C (high centrality), while 25% penalizes similarity to sentences already chosen (diversity). This prevents the summary from repeating the same concept in different words."
        ),
        (
            "Q5: How do you handle speed and latency on a student's personal laptop?",
            "Sir, both models are distilled: MiniLM has only 22.7M parameters and DistilBERT has 66M parameters (40% smaller and 60% faster than BERT-base). By running PyTorch inference on CPU with vector batching, the entire 5-step pipeline executes in under 2 seconds for a standard lecture note."
        )
    ]

    for q, a in viva_qa:
        q_flow = []
        q_flow.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('VQ', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12.5, textColor=C_DARK)))
        q_flow.append(Paragraph(f"<b>Answer:</b> {a}", ParagraphStyle('VA', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=C_BODY, leftIndent=8, spaceAfter=5)))
        story.append(KeepTogether(q_flow))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Code Explanation PDF successfully built: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
