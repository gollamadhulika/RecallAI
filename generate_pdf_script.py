"""Generate a clean, high-contrast, professional PDF for the RecallAI presentation script."""

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
            self.drawString(54, letter[1] - 36, "RecallAI — DS306 Deep Learning Project | Presentation Guide & Script")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)
        
        footer_text = "Presenters: Golla Madhulika (23STUCHH010826) & Reethu Reddy (23STUCHH011082) · Instructor: Dr. Kongara Srinivasa Rao"
        self.drawString(54, 32, footer_text)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf():
    pdf_filename = r"d:\mare\RecallAI_Presentation_Script.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom palette
    C_PRIMARY = colors.HexColor("#312e81")   # Deep Indigo
    C_ACCENT  = colors.HexColor("#0d9488")   # Teal
    C_AMBER   = colors.HexColor("#b45309")   # Warm Amber
    C_DARK    = colors.HexColor("#0f172a")   # Slate 900
    C_BODY    = colors.HexColor("#1e293b")   # Slate 800
    C_MUTED   = colors.HexColor("#64748b")   # Slate 500
    C_BG_BOX  = colors.HexColor("#f8fafc")   # Card background
    C_LINE    = colors.HexColor("#e2e8f0")   # Border

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=C_PRIMARY,
        spaceAfter=4,
    )

    sub_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=C_ACCENT,
        textTransform="uppercase",
        spaceAfter=6,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=C_PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SlideH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=C_DARK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    speaker_m = ParagraphStyle(
        "SpeakerM",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#4338ca"),
    )

    speaker_r = ParagraphStyle(
        "SpeakerR",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0f766e"),
    )

    speech_body = ParagraphStyle(
        "SpeechBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=C_BODY,
        leftIndent=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "StandardBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=C_BODY,
        spaceAfter=4,
    )

    bold_body = ParagraphStyle(
        "BoldBody",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=C_DARK,
    )

    card_text = ParagraphStyle(
        "CardText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=C_BODY,
    )

    story = []

    # ── HEADER BANNER ──────────────────────────────────────────────────────────
    story.append(Paragraph("DEEP LEARNING COURSE PROJECT (DS306)", sub_style))
    story.append(Paragraph("RecallAI: 2-Person Presentation Script & Viva Guide", title_style))
    story.append(Paragraph("<b>Course Instructor:</b> Dr. Kongara Srinivasa Rao &nbsp;|&nbsp; <b>Deck:</b> RecallAI_DS306_Presentation.pptx (8 Slides)", body_style))
    story.append(Spacer(1, 6))

    # Meta Info Table
    meta_data = [
        [
            Paragraph("<b>Presenter 1:</b> Golla Madhulika (23STUCHH010826)", card_text),
            Paragraph("<b>Presenter 2:</b> Reethu Reddy (23STUCHH011082)", card_text)
        ],
        [
            Paragraph("<b>Assigned Slides:</b> 1, 2, 3, 6, 8 (shared)", card_text),
            Paragraph("<b>Assigned Slides:</b> 1, 4, 5, 7, 8 (shared)", card_text)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_BOX),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ── PART 1: QUICK CHEAT SHEET ──────────────────────────────────────────────
    story.append(Paragraph("Part 1: Quick Project Understanding (Cheat Sheet)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    p_what = (
        "<b>What is RecallAI?</b> An autonomous deep learning study assistant that ingests lecture notes/PDFs "
        "and transforms them into 100% hallucination-free extractive summaries, zero-shot academic domain classifications, "
        "interactive flashcards, and semantic distractor quizzes."
    )
    story.append(Paragraph(p_what, body_style))
    story.append(Spacer(1, 4))

    # Models comparison table
    tech_data = [
        [
            Paragraph("<b>Component</b>", bold_body),
            Paragraph("<b>Model / Architecture</b>", bold_body),
            Paragraph("<b>Why Selected & Role</b>", bold_body)
        ],
        [
            Paragraph("<b>Dense Embeddings</b>", card_text),
            Paragraph("<code>all-MiniLM-L6-v2</code><br/>(22.7M params, 384-d)", card_text),
            Paragraph("Generates contextual vector embeddings of sentences. Runs in under 50ms on CPU; captures deep semantic relations without needing exact keywords.", card_text)
        ],
        [
            Paragraph("<b>Topic Classifier</b>", card_text),
            Paragraph("<code>distilbert-base-uncased-mnli</code><br/>(66M params)", card_text),
            Paragraph("Zero-shot Natural Language Inference. Evaluates whether notes entail <i>'This text is about {topic}'</i> without requiring subject-specific fine-tuning.", card_text)
        ],
        [
            Paragraph("<b>Summarizer</b>", card_text),
            Paragraph("<b>Centroid + MMR Ranking</b><br/>(Maximal Marginal Relevance)", card_text),
            Paragraph("Computes document centroid vector C. Selects verbatim central sentences with lambda=0.7 to maximize relevance while eliminating redundancy and hallucinations.", card_text)
        ],
        [
            Paragraph("<b>Quiz Engine</b>", card_text),
            Paragraph("<b>Vector Distractor Clustering</b>", card_text),
            Paragraph("Extracts key terms and selects distractors from nearby semantic vector clusters, producing plausible, rigorous test options.", card_text)
        ]
    ]
    tech_table = Table(tech_data, colWidths=[90, 150, 260])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ede9fe")),
        ('BOX', (0,0), (-1,-1), 1, C_LINE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # ── PART 2: SLIDE SCRIPT ───────────────────────────────────────────────────
    story.append(Paragraph("Part 2: Complete Slide-by-Slide 2-Person Script", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    slides = [
        {
            "num": "Slide 1",
            "title": "Title Slide & Welcome",
            "visual": "Title, Course DS306, Dr. Kongara Srinivasa Rao, Presenter names & IDs.",
            "dialogue": [
                (
                    "speaker_m",
                    "MADHULIKA",
                    "\"Respected Sir and good morning/afternoon everyone. Welcome to our Deep Learning course project presentation for DS306. "
                    "I am Golla Madhulika (ID: 23STUCHH010826), and joining me is my project partner, Reethu Reddy (ID: 23STUCHH011082). "
                    "Under the guidance of Dr. Kongara Srinivasa Rao sir, we have built RecallAI — A Deep Learning-Based Personalized Study Assistant.\""
                ),
                (
                    "speaker_r",
                    "REETHU",
                    "\"Our objective is to tackle information overload by transforming complex, unstructured lecture materials into active, memorable study tools "
                    "using deep learning transformers — with 100% factual accuracy and zero hallucination.\""
                )
            ]
        },
        {
            "num": "Slide 2",
            "title": "Problem Statement: The Study & Retention Dilemma",
            "visual": "Cards: Cognitive Overload, LLM Hallucination Risk, Proposed Solution.",
            "dialogue": [
                (
                    "speaker_m",
                    "MADHULIKA",
                    "\"To understand the motivation behind RecallAI, let us look at the core challenges students face: "
                    "First, Cognitive Overload: Before semester exams, engineering students are overwhelmed by dense textbooks and lengthy slide decks. Cognitive research confirms that passive re-reading yields less than 20% retention after 48 hours. "
                    "Second, The Hallucination Risk of LLMs: While students attempt to use generic LLMs like ChatGPT, these models frequently hallucinate facts, invent fake citations, or rewrite formulas incorrectly. In technical STEM subjects, verbatim accuracy is critical. "
                    "This created the need for an autonomous study platform that operates directly on verified course notes, guarantees zero hallucination, and encourages active recall through testing.\""
                )
            ]
        },
        {
            "num": "Slide 3",
            "title": "Introduction & Core Objectives",
            "visual": "4 Feature Cards: Ingestion, Zero-Shot Classification, Hallucination-Free Summary, Active Recall.",
            "dialogue": [
                (
                    "speaker_m",
                    "MADHULIKA",
                    "\"RecallAI delivers a comprehensive 4-stage active learning pipeline: "
                    "1. Smart Document Ingestion: Extracts clean text from multi-page PDFs using PyMuPDF, filtering out noise, corrupt pages, and non-text artifacts. "
                    "2. Zero-Shot Domain Classification: Automatically identifies the academic domain of the material without needing any subject-specific retraining. "
                    "3. Hallucination-Free Summarization: Uses dense semantic centroid selection to produce concise summaries with over 70% compression while preserving verbatim original sentences. "
                    "4. Active Recall & Testing: Automatically generates interactive flashcards and multiple-choice questions with intelligent vector-matched distractors. "
                    "Now, Reethu will walk you through the deep learning technologies and architecture powering this system.\""
                )
            ]
        },
        {
            "num": "Slide 4",
            "title": "Deep Learning Technologies & Framework Stack",
            "visual": "Cards: Sentence-Transformers all-MiniLM-L6-v2, DistilBERT Zero-Shot NLI, Supporting Stack.",
            "dialogue": [
                (
                    "speaker_r",
                    "REETHU",
                    "\"Thank you, Madhulika. For our deep learning backbone, we intentionally selected architectures optimized for high semantic fidelity and fast CPU execution: "
                    "1. Sentence-Transformers (all-MiniLM-L6-v2): A 6-layer Transformer with 22.7 million parameters. It projects every sentence into a 384-dimensional dense semantic vector space. Unlike classical keyword search, it understands contextual relationships — for example, recognizing that 'gradient descent' and 'optimization algorithm' are semantically proximate even if they share no words in common. "
                    "2. DistilBERT Zero-Shot NLI (typeform/distilbert-base-uncased-mnli): DistilBERT has 66 million parameters and is 40% smaller and 60% faster than BERT-base. We leverage its Natural Language Inference capabilities by posing candidate hypotheses like 'This text is about Computer Science'. By computing the softmax over entailment logits, the model classifies topics with high confidence out-of-the-box. "
                    "The system is powered by PyTorch and Hugging Face Transformers, served through a modern reactive Streamlit web interface.\""
                )
            ]
        },
        {
            "num": "Slide 5",
            "title": "Deep Learning Architecture: How It Works",
            "visual": "Step 1: Embeddings -> Step 2: Centroid & MMR -> Step 3: Zero-Shot -> Step 4: Distractors.",
            "dialogue": [
                (
                    "speaker_r",
                    "REETHU",
                    "\"Here is how the deep learning pipeline functions end-to-end: "
                    "Step 1 (Dense Embedding Projection): Incoming notes are split into clean sentences. Each sentence is passed through all-MiniLM-L6-v2 to extract 384-dimensional embeddings via token self-attention and mean pooling. "
                    "Step 2 (Centroid & MMR Summarizer): We compute the document's global semantic centroid vector C. Using Maximal Marginal Relevance (MMR) with lambda = 0.7, we iteratively pick sentences that maximize cosine similarity to C while penalizing similarity to already selected sentences. Because each sentence is selected verbatim from the source, hallucination is mathematically impossible. "
                    "Step 3 (Zero-Shot Classification): The document representation is evaluated across 10 academic domains to assign domain labels and confidence percentages. "
                    "Step 4 (Semantic Distractor Synthesis): For quiz questions, key terms are extracted, and distractor options are sampled from semantically close embedding neighbors. This ensures distractors are challenging and plausible rather than trivially obvious. "
                    "Now, Madhulika will present the working system demonstration using live project screenshots.\""
                )
            ]
        },
        {
            "num": "Slide 6",
            "title": "Working Demonstration: Note Ingestion & Study Workspace",
            "visual": "Screenshots: Upload Notes staging panel (Left) & Study Workspace summary/tabs (Right).",
            "dialogue": [
                (
                    "speaker_m",
                    "MADHULIKA",
                    "\"As you can see on Slide 6, this is our actual deployed application running on localhost:8501: "
                    "On the left screenshot, we have the Upload Notes interface. Students can upload a PDF, paste text, or click pre-built academic sample notes. Here, we loaded notes on Machine Learning & Neural Networks (235 words). The system validates the content, previews the text, and triggers the 5-step deep learning pipeline. "
                    "On the right screenshot, we have the Study Workspace. In under 2 seconds on standard CPU, our model generated an AI extractive summary with a 71.5% compression ratio, condensing 235 words into 67 high-impact words. "
                    "Below the summary, it lists the MMR-ranked core concept takeaways, and provides tabs for interactive flashcards, key concept definitions, and vector semantic search where students can ask questions in natural language.\""
                )
            ]
        },
        {
            "num": "Slide 7",
            "title": "Working Demonstration: Student Dashboard & Quiz Analytics",
            "visual": "Screenshots: USER01 Dashboard with metrics (Left) & Diagnostic Quiz Results (Right).",
            "dialogue": [
                (
                    "speaker_r",
                    "REETHU",
                    "\"Moving to Slide 7, we see the student assessment and tracking experience: "
                    "On the left panel, the Student Dashboard (USER01) displays 100% authentic session data. It immediately updates our counters: 8 Flash Cards generated, 1 Test taken, 1 Study Guide active, and our current mastery score. It also maintains a recent activity feed so students can switch between lecture notes with a single click. "
                    "On the right panel, we have the Diagnostic Results Page. After the student completes the 6-question quiz generated by our distractor model, it calculates the mastery percentage — in this test run, 50.0% (3 out of 6 correct). "
                    "Most importantly, the deep learning engine doesn't just give a score; it diagnoses 'Concepts to Review' — specifically highlighting Backpropagation and Supervised Learning so the student knows exactly where to focus revision.\""
                )
            ]
        },
        {
            "num": "Slide 8",
            "title": "Conclusion & Future Research Directions",
            "visual": "Cards: Key Achievements & Future Scope.",
            "dialogue": [
                (
                    "speaker_m",
                    "MADHULIKA",
                    "\"To conclude our presentation: RecallAI demonstrates that targeted, lightweight deep learning transformers can outperform massive generative LLMs for focused academic tasks. By combining Sentence-Transformers with Extractive Centroid Summarization, we provide 100% hallucination-free study aids with sub-second CPU inference and zero cloud API dependency.\""
                ),
                (
                    "speaker_r",
                    "REETHU",
                    "\"For future work, we plan to extend RecallAI in three key areas: "
                    "1. Incorporating Vision-Language Models like CLIP or ViT to interpret formulas, diagrams, and textbook charts. "
                    "2. Adding the SuperMemo SM-2 algorithm for automated spaced-repetition scheduling. "
                    "3. Integrating Whisper for speech-to-text to transcribe recorded lectures directly into study notes. "
                    "We would like to express our sincere gratitude to our instructor, Dr. Kongara Srinivasa Rao sir, for his guidance throughout this Deep Learning course. We are now ready for your questions and feedback. Thank you!\""
                )
            ]
        }
    ]

    for s in slides:
        slide_flow = []
        slide_flow.append(Paragraph(f"<b>{s['num']}: {s['title']}</b>", h2_style))
        slide_flow.append(Paragraph(f"<i>Visual on screen:</i> {s['visual']}", ParagraphStyle('Vis', parent=card_text, textColor=C_MUTED, spaceAfter=4)))
        for sp_style_key, sp_name, text in s['dialogue']:
            st_style = speaker_m if sp_style_key == "speaker_m" else speaker_r
            slide_flow.append(Paragraph(f"<b>[{sp_name}]:</b>", st_style))
            slide_flow.append(Paragraph(text, speech_body))
        slide_flow.append(Spacer(1, 4))
        story.append(KeepTogether(slide_flow))

    story.append(Spacer(1, 10))

    # ── PART 3: VIVA QUESTIONS ─────────────────────────────────────────────────
    story.append(Paragraph("Part 3: Anticipated Viva / Examiner Q&A", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_PRIMARY, spaceAfter=8))

    qa_list = [
        (
            "Q1: Why did you use Extractive Summarization instead of Abstractive models like BART or T5?",
            "Abstractive models decode new tokens from vocabulary and can hallucinate inaccurate facts, misquote scientific laws, or garble formulas. Extractive summarization using semantic centroid MMR mathematically selects verbatim sentences from the instructor's verified notes, guaranteeing 0% hallucination."
        ),
        (
            "Q2: What is the mathematical definition and role of Cosine Similarity?",
            "Sentence vectors are normalized to unit Euclidean length (||v|| = 1). The cosine similarity is the dot product u · v. We use it in three places: (1) calculating sentence relevance to document centroid C, (2) semantic vector search query ranking, and (3) selecting proximate distractors for MCQ options."
        ),
        (
            "Q3: What is the difference between Zero-Shot Classification and Supervised Fine-Tuning?",
            "Supervised fine-tuning requires thousands of domain-labeled training pairs and updates model weights via backpropagation. In contrast, Zero-Shot Classification with DistilBERT-MNLI uses pre-trained premise-hypothesis entailment. We formulate topic prediction as an inference problem without updating weights, allowing RecallAI to generalize across any academic subject instantly."
        ),
        (
            "Q4: How does the quiz engine generate distractors?",
            "Instead of generating random options, the system extracts key terms and projects them into embedding space. For any target term T, distractors are chosen from neighboring semantic clusters that have moderate-to-high cosine similarity to T but are distinct concepts. This creates realistic, high-quality test questions that test true conceptual mastery."
        )
    ]

    for q, a in qa_list:
        qa_flow = []
        qa_flow.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=C_DARK)))
        qa_flow.append(Paragraph(f"<b>Answer:</b> {a}", ParagraphStyle('AStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=C_BODY, leftIndent=8, spaceAfter=6)))
        story.append(KeepTogether(qa_flow))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
