"""Generate a professional widescreen PPTX presentation for RecallAI DS306 submission."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color palette
    COLOR_BG = RGBColor(15, 23, 42)          # #0f172a Slate dark
    COLOR_CARD = RGBColor(30, 41, 59)        # #1e293b
    COLOR_CARD_BORDER = RGBColor(51, 65, 85) # #334155
    COLOR_PRIMARY = RGBColor(99, 102, 241)   # #6366f1 Indigo
    COLOR_ACCENT = RGBColor(45, 212, 191)    # #2dd4bf Teal/Emerald
    COLOR_AMBER = RGBColor(251, 191, 36)     # #fbbf24 Amber
    COLOR_WHITE = RGBColor(248, 250, 252)    # #f8fafc
    COLOR_SILVER = RGBColor(148, 163, 184)   # #94a3b8
    COLOR_MUTED = RGBColor(100, 116, 139)    # #64748b

    img_dir = r"C:/Users/acer/.gemini/antigravity/brain/c1187c71-0140-46c7-bc0b-71e82d76f710/.user_uploaded"
    img_results = os.path.join(img_dir, "media_1793521364318_9d073517.png")
    img_dashboard = os.path.join(img_dir, "media_1793521364335_a6ba596e.png")
    img_upload = os.path.join(img_dir, "media_1793521364345_399101c8.png")
    img_workspace = os.path.join(img_dir, "media_1793521364377_86f5bc2f.png")

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="DS306 · DEEP LEARNING PROJECT"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_PRIMARY
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE

    def add_card(slide, left, top, width, height, title, body_lines, accent_color=COLOR_PRIMARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.25), width - Inches(0.6), height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.space_after = Pt(10)

        for line in body_lines:
            p = tf.add_paragraph()
            p.text = ("• " if not line.startswith("  ") else "   ") + line.strip()
            p.font.size = Pt(13)
            p.font.color.rgb = COLOR_WHITE if not line.startswith("  ") else COLOR_SILVER
            p.space_after = Pt(6)

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 1: Title Slide
    # ══════════════════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative gradient accent bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(11.733), Inches(0.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_PRIMARY
    top_bar.line.fill.background()

    # Main Title box
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True

    p_sub = tf_title.paragraphs[0]
    p_sub.text = "DEEP LEARNING COURSE PROJECT · DS306"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_ACCENT
    p_sub.space_after = Pt(8)

    p_main = tf_title.add_paragraph()
    p_main.text = "RecallAI — A Deep Learning-Based\nPersonalized Study Assistant"
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_WHITE
    p_main.space_after = Pt(12)

    p_desc = tf_title.add_paragraph()
    p_desc.text = "Transforming complex study notes into structured summaries, zero-shot academic domain classifications, interactive flashcards, and vector-distractor quizzes."
    p_desc.font.size = Pt(14)
    p_desc.font.color.rgb = COLOR_SILVER

    # 2 Info Cards: Instructor & Submissions
    # Instructor Card
    c_inst = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.4))
    c_inst.fill.solid()
    c_inst.fill.fore_color.rgb = COLOR_CARD
    c_inst.line.color.rgb = COLOR_CARD_BORDER
    c_inst.line.width = Pt(1.5)

    tf_inst = c_inst.text_frame
    tf_inst.word_wrap = True
    p_in_lbl = tf_inst.paragraphs[0]
    p_in_lbl.text = "COURSE INSTRUCTOR"
    p_in_lbl.font.size = Pt(11)
    p_in_lbl.font.bold = True
    p_in_lbl.font.color.rgb = COLOR_PRIMARY
    p_in_lbl.space_after = Pt(8)

    p_in_name = tf_inst.add_paragraph()
    p_in_name.text = "Dr. Kongara Srinivasa Rao"
    p_in_name.font.size = Pt(20)
    p_in_name.font.bold = True
    p_in_name.font.color.rgb = COLOR_WHITE
    p_in_name.space_after = Pt(4)

    p_in_sub = tf_inst.add_paragraph()
    p_in_sub.text = "Subject: Deep Learning (DS306)"
    p_in_sub.font.size = Pt(13)
    p_in_sub.font.color.rgb = COLOR_SILVER

    # Submissions Card
    c_sub = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.3), Inches(5.6), Inches(2.4))
    c_sub.fill.solid()
    c_sub.fill.fore_color.rgb = COLOR_CARD
    c_sub.line.color.rgb = COLOR_CARD_BORDER
    c_sub.line.width = Pt(1.5)

    tf_sub = c_sub.text_frame
    tf_sub.word_wrap = True
    p_su_lbl = tf_sub.paragraphs[0]
    p_su_lbl.text = "SUBMITTED BY"
    p_su_lbl.font.size = Pt(11)
    p_su_lbl.font.bold = True
    p_su_lbl.font.color.rgb = COLOR_ACCENT
    p_su_lbl.space_after = Pt(8)

    p_s1 = tf_sub.add_paragraph()
    p_s1.text = "1. Golla Madhulika"
    p_s1.font.size = Pt(16)
    p_s1.font.bold = True
    p_s1.font.color.rgb = COLOR_WHITE

    p_s1_id = tf_sub.add_paragraph()
    p_s1_id.text = "    ID: 23STUCHH010826"
    p_s1_id.font.size = Pt(13)
    p_s1_id.font.color.rgb = COLOR_SILVER
    p_s1_id.space_after = Pt(6)

    p_s2 = tf_sub.add_paragraph()
    p_s2.text = "2. Reethu Reddy"
    p_s2.font.size = Pt(16)
    p_s2.font.bold = True
    p_s2.font.color.rgb = COLOR_WHITE

    p_s2_id = tf_sub.add_paragraph()
    p_s2_id.text = "    ID: 23STUCHH011082"
    p_s2_id.font.size = Pt(13)
    p_s2_id.font.color.rgb = COLOR_SILVER

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 2: Problem Statement
    # ══════════════════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement: The Study & Retention Dilemma")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "1. Cognitive Overload",
             [
                 "Students encounter dense, unstructured academic textbooks and slide decks.",
                 "Passive reading yields low retention (<20% recall after 48 hours).",
                 "Manual summarization and card creation is tedious and time-consuming."
             ], COLOR_AMBER)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "2. The LLM Hallucination Risk",
             [
                 "Generative LLMs frequently hallucinate facts or invent incorrect definitions.",
                 "In STEM subjects, factual precision is non-negotiable for exam preparation.",
                 "Generative text cannot guarantee verbatim fidelity to lecture syllabus."
             ], RGBColor(251, 113, 133))

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "3. The Proposed Solution",
             [
                 "RecallAI: A grounded deep learning study assistant.",
                 "Extractive Centroid Summarization with 0% hallucination risk.",
                 "Dense vector embeddings for active recall and semantic self-assessment."
             ], COLOR_ACCENT)

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 3: Introduction & Core Objectives
    # ══════════════════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Introduction: What is RecallAI?")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "Document Ingestion & Parsing",
             [
                 "PyMuPDF engine parses digital course lecture PDFs and raw notes.",
                 "Robust validation removes non-text artifacts, noise, and scanned scans.",
                 "Outputs clean sentence-level representations ready for vectorization."
             ], COLOR_PRIMARY)

    add_card(s3, Inches(6.9), Inches(1.8), Inches(5.6), Inches(2.4),
             "Zero-Shot Academic Classification",
             [
                 "Categorizes incoming text across 10 academic domains automatically.",
                 "No domain-specific fine-tuning required; generalizes across subjects.",
                 "Provides confidence scores and secondary topic distributions."
             ], COLOR_ACCENT)

    add_card(s3, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "Hallucination-Free Summarization",
             [
                 "Semantic Centroid MMR (Maximal Marginal Relevance) ranking.",
                 "Selects verbatim central sentences that capture 70%+ information.",
                 "100% faithful to instructor notes — zero false statements."
             ], COLOR_AMBER)

    add_card(s3, Inches(6.9), Inches(4.5), Inches(5.6), Inches(2.4),
             "Active Recall & Quiz Engine",
             [
                 "Generates MCQs using semantic distractor embeddings.",
                 "Creates interactive concept flashcards with flip-to-reveal mastery.",
                 "Tracks progress dynamically with personalized diagnostic scoring."
             ], RGBColor(244, 114, 182))

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 4: Deep Learning Technologies Used
    # ══════════════════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Deep Learning Technologies & Framework Stack")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Sentence-Transformers",
             [
                 "Model: all-MiniLM-L6-v2",
                 "Parameters: 22.7 Million",
                 "Dimension: 384-d dense vectors",
                 "Purpose: Dense semantic embeddings for sentences, cosine similarity search, and distractor ranking.",
                 "Advantage: Blazing-fast inference on standard CPU environments."
             ], COLOR_PRIMARY)

    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "DistilBERT Zero-Shot NLI",
             [
                 "Model: distilbert-base-uncased-mnli",
                 "Parameters: 66 Million",
                 "Architecture: 6-layer Transformer",
                 "Purpose: Natural Language Inference hypothesis testing ('This text is about {topic}').",
                 "Advantage: 40% smaller and 60% faster than BERT-base while retaining 97% accuracy."
             ], COLOR_ACCENT)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "Supporting Stack",
             [
                 "PyTorch (v2.6+): Tensor operations and neural inference runtime.",
                 "Hugging Face Transformers: Model hub and tokenizer pipeline.",
                 "PyMuPDF (fitz): High-speed PDF text stream extraction.",
                 "Streamlit: Modern reactive dark-mode web application interface."
             ], COLOR_AMBER)

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 5: How the Deep Learning Model Works & Architecture
    # ══════════════════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Deep Learning Architecture: End-to-End Pipeline")

    steps = [
        ("Step 1: Embedding Projection", "Sentences are passed into all-MiniLM-L6-v2 to obtain 384-dimensional dense semantic vectors using Mean Pooling over contextual token states.", COLOR_PRIMARY),
        ("Step 2: Centroid & MMR Summarizer", "Document centroid vector C is calculated. Maximal Marginal Relevance iteratively selects sentences with high cosine similarity to C while penalizing redundancy.", COLOR_ACCENT),
        ("Step 3: Zero-Shot Classification", "DistilBERT compares note embeddings against candidate academic hypotheses using softmax probability distribution over entailment logits.", COLOR_AMBER),
        ("Step 4: Vector Distractor Generation", "Key terms are extracted; distractor options are sampled from semantically proximate yet incorrect embedding clusters to form challenging test questions.", RGBColor(244, 114, 182)),
    ]

    for idx, (title, desc, col) in enumerate(steps):
        top_y = Inches(1.8 + idx * 1.3)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y, Inches(11.733), Inches(1.15))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_CARD
        c.line.color.rgb = COLOR_CARD_BORDER
        c.line.width = Pt(1.5)

        tf = c.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(12)
        p1.font.color.rgb = COLOR_WHITE

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 6: Working Demonstration — Ingestion & Study Workspace (Images)
    # ══════════════════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Working System: Note Ingestion & Study Workspace")

    # Left: Upload Screenshot
    if os.path.exists(img_upload):
        s6.shapes.add_picture(img_upload, Inches(0.8), Inches(1.8), width=Inches(5.6))
    caption1 = s6.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(5.6), Inches(1.4))
    tf_c1 = caption1.text_frame
    tf_c1.word_wrap = True
    p_c1 = tf_c1.paragraphs[0]
    p_c1.text = "1. Notes Ingestion & Processing"
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_PRIMARY
    p_c1_sub = tf_c1.add_paragraph()
    p_c1_sub.text = "Supports PDF drag-and-drop, raw text pasting, or 1-click sample notes. Displays word count, token length, and processing status."
    p_c1_sub.font.size = Pt(11)
    p_c1_sub.font.color.rgb = COLOR_SILVER

    # Right: Workspace Screenshot
    if os.path.exists(img_workspace):
        s6.shapes.add_picture(img_workspace, Inches(6.9), Inches(1.8), width=Inches(5.6))
    caption2 = s6.shapes.add_textbox(Inches(6.9), Inches(5.5), Inches(5.6), Inches(1.4))
    tf_c2 = caption2.text_frame
    tf_c2.word_wrap = True
    p_c2 = tf_c2.paragraphs[0]
    p_c2.text = "2. AI Study Workspace"
    p_c2.font.size = Pt(14)
    p_c2.font.bold = True
    p_c2.font.color.rgb = COLOR_ACCENT
    p_c2_sub = tf_c2.add_paragraph()
    p_c2_sub.text = "Renders MMR-ranked summary (71.5% compression), core concept takeaways, interactive flashcards, and dense vector semantic search."
    p_c2_sub.font.size = Pt(11)
    p_c2_sub.font.color.rgb = COLOR_SILVER

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7: Working Demonstration — Dashboard & Quiz Analytics (Images)
    # ══════════════════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Working System: Student Dashboard & Quiz Results")

    # Left: Dashboard Screenshot
    if os.path.exists(img_dashboard):
        s7.shapes.add_picture(img_dashboard, Inches(0.8), Inches(1.8), width=Inches(5.6))
    caption3 = s7.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(5.6), Inches(1.4))
    tf_c3 = caption3.text_frame
    tf_c3.word_wrap = True
    p_c3 = tf_c3.paragraphs[0]
    p_c3.text = "3. Authentic Student Dashboard (USER01)"
    p_c3.font.size = Pt(14)
    p_c3.font.bold = True
    p_c3.font.color.rgb = COLOR_PRIMARY
    p_c3_sub = tf_c3.add_paragraph()
    p_c3_sub.text = "Real-time session statistics: Flash Cards (8), Tests (1), Study Guides (1), and active mastery (50%). Seamless 1-click workspace switching."
    p_c3_sub.font.size = Pt(11)
    p_c3_sub.font.color.rgb = COLOR_SILVER

    # Right: Results Screenshot
    if os.path.exists(img_results):
        s7.shapes.add_picture(img_results, Inches(6.9), Inches(1.8), width=Inches(5.6))
    caption4 = s7.shapes.add_textbox(Inches(6.9), Inches(5.5), Inches(5.6), Inches(1.4))
    tf_c4 = caption4.text_frame
    tf_c4.word_wrap = True
    p_c4 = tf_c4.paragraphs[0]
    p_c4.text = "4. Diagnostic Quiz & Mastery Analytics"
    p_c4.font.size = Pt(14)
    p_c4.font.bold = True
    p_c4.font.color.rgb = COLOR_AMBER
    p_c4_sub = tf_c4.add_paragraph()
    p_c4_sub.text = "Detailed score breakdown (3/6 correct) with automated concept weakness diagnosis (Backpropagation, Supervised Learning) for targeted revision."
    p_c4_sub.font.size = Pt(11)
    p_c4_sub.font.color.rgb = COLOR_SILVER

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 8: Conclusion & Future Scope
    # ══════════════════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Conclusion & Future Research Directions")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9),
             "Key Achievements",
             [
                 "100% Hallucination-Free: Verbatim extractive centroid summarization preserves academic accuracy.",
                 "High Efficiency: Zero-shot DistilBERT and MiniLM achieve sub-second inference on standard CPU.",
                 "Active Learning Impact: Converts passive reading into active testing through vector-matched distractors.",
                 "User-Centric Architecture: Elegant dark academic desktop interface with real-time state tracking."
             ], COLOR_ACCENT)

    add_card(s8, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.9),
             "Future Scope",
             [
                 "Multimodal Learning: Vision-Language Models (e.g. CLIP / ViT) to summarize textbook diagrams and graphs.",
                 "Adaptive Spaced Repetition: SuperMemo SM-2 algorithm to schedule flashcards based on forgetting curves.",
                 "Cross-Document Synthesis: Semantic graph clustering across semester-long lecture series.",
                 "Audio Lecture Transcription: Whisper integration to process recorded classroom audio directly into notes."
             ], COLOR_AMBER)

    output_path = r"d:\mare\RecallAI_DS306_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
