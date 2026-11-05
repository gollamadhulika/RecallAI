# RecallAI — Deep Learning-Based Personalized Study Assistant

> A working academic web application that transforms study notes into **summaries, topic classifications, practice questions, flashcards, and adaptive quizzes** powered by pretrained Transformer models.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Deep Learning Components](#deep-learning-components)
5. [Project Structure](#project-structure)
6. [Setup & Installation](#setup--installation)
7. [Running the Application](#running-the-application)
8. [Running Tests](#running-tests)
9. [Pages & Features](#pages--features)
10. [Sample Notes](#sample-notes)
11. [Limitations & Honest Disclaimers](#limitations--honest-disclaimers)
12. [Instructor Explanation Guide](#instructor-explanation-guide)

---

## Project Overview

RecallAI is built as an end-to-end student project demonstrating applied deep learning. It processes PDF or pasted study notes through a pipeline of:

1. **Document extraction** — PyMuPDF
2. **Text embedding** — Sentence-Transformers (`all-MiniLM-L6-v2`, 384-dim dense vectors)
3. **Topic classification** — DistilBERT zero-shot NLI (`typeform/distilbert-base-uncased-mnli`)
4. **Semantic extractive summarisation** — Centroid + Maximal Marginal Relevance (MMR)
5. **Question generation** — Dependency-pattern extraction + dense semantic distractor selection
6. **Flashcard generation** — Semantic nearest-sentence matching
7. **Quiz scoring & analytics** — session-state evaluation engine

---

## System Architecture

```
Student Input (PDF / Paste)
           │
           ▼
  Document Processing (PyMuPDF, text_cleaner)
           │
           ▼
  Deep Learning Engine
  ┌─────────────────────────────────────┐
  │  Sentence-Transformers              │   ← Text Embeddings (all-MiniLM-L6-v2)
  │  DistilBERT Zero-Shot NLI           │   ← Topic Classification
  │  Semantic Centroid + MMR            │   ← Extractive Summarisation
  │  Dense Distractor Generation        │   ← Quiz Question Creation
  └─────────────────────────────────────┘
           │
           ▼
  RecallAI Streamlit Dashboard
  ┌──────────────────────────────────────┐
  │  Dashboard · Upload · Workspace      │
  │  Quiz · Results & Analytics          │
  └──────────────────────────────────────┘
```

---

## Technology Stack

| Component             | Technology                          |
|-----------------------|-------------------------------------|
| Programming Language  | Python 3.10+                        |
| Web Interface         | Streamlit 1.30+                     |
| PDF Extraction        | PyMuPDF (pymupdf)                   |
| Deep Learning Runtime | PyTorch (CPU mode)                  |
| Text Embeddings       | sentence-transformers               |
| Topic Classification  | Hugging Face Transformers           |
| Data Processing       | pandas, NumPy                       |
| Evaluation Metrics    | scikit-learn                        |
| Testing               | pytest                              |

---

## Deep Learning Components

### 1. Text Embeddings — `src/text_embeddings.py`
- **Model:** `sentence-transformers/all-MiniLM-L6-v2` (22.7M parameters)
- **Output:** 384-dimensional dense semantic vectors
- **Used for:** Document-level understanding, semantic search, distractor selection, MMR summarisation
- **Training status:** Pretrained on MS MARCO + Natural Language Inference corpora. **Inference only — weights are frozen.**

### 2. Topic Classification — `src/topic_classifier.py`
- **Primary model:** `typeform/distilbert-base-uncased-mnli` (DistilBERT Cross-Encoder, 66M parameters)
- **Method:** Zero-Shot Natural Language Inference — classifies text against 10 academic domain labels using the hypothesis: *"This educational text is about {topic}."*
- **Fallback:** Embedding-centroid cosine similarity with temperature-scaled Softmax
- **Training status:** Both models use **pretrained frozen weights** (zero-shot inference, no fine-tuning performed)

### 3. Extractive Summarisation — `src/summarizer.py`
- **Method:** Semantic Centroid Selection + Maximal Marginal Relevance (MMR)
- **Guarantees 0% hallucination** — only selects real sentences from your notes
- **Optional:** Abstractive DistilBART pipeline (loads on demand)

### 4. Quiz Question Generation — `src/question_generator.py`
- **Approach:** Regex-based definition extraction + dense embedding distractor ranking
- **Distractors:** Selected by computing cosine similarity between candidate terms and the correct answer — semantically related but distinct
- **Clearly labelled** as template + semantic similarity method (not a generative LLM)

---

## Project Structure

```
RecallAI/
├── app.py                          ← Main Streamlit entry point
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Upload_Notes.py
│   ├── 3_Study_Workspace.py
│   ├── 4_Quiz.py
│   └── 5_Results.py
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py            ← PyMuPDF extraction & validation
│   ├── text_cleaner.py             ← Cleaning, sentence splitting, chunking, key terms
│   ├── text_embeddings.py          ← Sentence-Transformers dense embeddings
│   ├── topic_classifier.py         ← DistilBERT zero-shot + embedding classifier
│   ├── summarizer.py               ← Semantic MMR extractive + optional DistilBART
│   ├── question_generator.py       ← MCQ generation with semantic distractors
│   ├── flashcards.py               ← Flashcard term-definition pairing
│   ├── quiz_engine.py              ← Session, scoring, mastery analytics
│   └── ui_components.py            ← Shared CSS, layout helpers, session state
├── models/
│   └── README.md                   ← Model registry, architecture details
├── data/
│   └── sample_notes/
│       ├── computer_systems.txt / .pdf
│       ├── cellular_biology.txt / .pdf
│       └── machine_learning.txt / .pdf
└── tests/
    ├── test_pdf_processor.py
    ├── test_classifier.py
    ├── test_quiz_engine.py
    └── test_embeddings_and_summary.py
```

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone or download the project
cd RecallAI

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install all dependencies
pip install -r requirements.txt
```

> **Note:** All Hugging Face models download automatically on first use and are cached locally in `~/.cache/huggingface/hub`. An internet connection is required for first run only.

---

## Running the Application

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

**Recommended first-run flow:**
1. Click **Upload Notes**
2. Upload one of the sample PDFs from `data/sample_notes/` (e.g. `cellular_biology.pdf`)
3. Click **Process Notes with Deep Learning**
4. Navigate to **Study Workspace** → explore Summary, Topic, Flashcards, Questions
5. Click **Go to Quiz** → answer questions → Submit
6. Review detailed results on the **Results** page

---

## Running Tests

```bash
python -m pytest -v
```

**18 tests across 4 test files:**

| File | Tests |
|---|---|
| `test_pdf_processor.py` | PDF extraction, empty file, text cleaning, sentence splitting, chunking, key terms, validation |
| `test_classifier.py` | CS text → CS topic, Biology text → Biology topic, model metadata |
| `test_quiz_engine.py` | Question generation, flashcard generation, full quiz lifecycle |
| `test_embeddings_and_summary.py` | Embedding shape (384-dim), cosine similarity, semantic search, extractive summary |

All 18 tests pass in ~32 seconds on CPU.

---

## Pages & Features

| Page | URL | Key Features |
|---|---|---|
| Dashboard | `/` | Session stats, document history, quick links |
| Upload Notes | `/Upload_Notes` | PDF drag-drop, text paste, extraction preview, deep learning processing |
| Study Workspace | `/Study_Workspace` | Summary, topic distribution chart, key concept grid, flashcards, practice questions |
| Quiz | `/Quiz` | One-question-at-a-time, dot progress indicator, previous/next navigation, submit |
| Results | `/Results` | Score banner, mastery badge, concept-to-review list, question breakdown, session history |

---

## Sample Notes

Three pre-written academic note sets are included for immediate testing:

| File | Subject | Sample Topic Prediction |
|---|---|---|
| `cellular_biology.pdf` | Photosynthesis, chloroplasts, Calvin Cycle | Biology & Life Sciences |
| `computer_systems.pdf` | Virtual Memory, Paging, Deadlocks, CPU Scheduling | Computer Science & IT |
| `machine_learning.pdf` | Gradient Descent, Overfitting, Backpropagation | Computer Science & IT |

---

## Limitations & Honest Disclaimers

| Feature | What Works | Honest Limitation |
|---|---|---|
| Topic Classification | Zero-shot NLI on 10 academic domains | Not fine-tuned on university syllabi; works best for clearly domain-specific text |
| Summarisation | Faithful extractive summary (0% hallucination) | Abstractive DistilBART disabled by default (requires ~1.2 GB RAM) |
| Question Generation | Definition-pattern extraction + semantic distractors | Works best on notes written with clear definitional sentences |
| PDF Support | Digital PDFs, multi-page | Scanned/image-only PDFs are not supported (no OCR) |
| Embeddings | 384-dimensional dense vectors, cosine similarity | Not domain-adapted; general-purpose model |
| Storage | Session-state only | No persistence between app restarts |

---

## Instructor Explanation Guide

> "RecallAI has three main parts. First, the **document processing** component extracts and cleans text from student notes using PyMuPDF. Second, the **deep learning** component uses two pretrained Transformer models — Sentence-Transformers generates 384-dimensional dense vector representations of the text, and DistilBERT predicts the academic topic using Zero-Shot Natural Language Inference across ten subject domains. Third, the **application layer** converts the processed material into summaries using Semantic Centroid and Maximal Marginal Relevance selection, generates flashcards and multiple-choice questions with semantically plausible distractors, and presents everything through a Streamlit dashboard with a full quiz and scoring system. All models use pretrained frozen weights — this is demonstrated inference, not training from scratch."

---

*Built with PyTorch · Hugging Face Transformers · Sentence-Transformers · Streamlit · PyMuPDF*
