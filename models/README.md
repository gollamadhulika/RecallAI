# RecallAI — Deep Learning Model Registry & Architecture

This document describes the deep learning models integrated into **RecallAI**, their specific roles, architectural properties, and the distinction between pretrained inference and fine-tuning.

---

## 1. Integrated Models

| Capability | Model Architecture | Hugging Face Checkpoint | Parameters / Dim | Primary Function |
| :--- | :--- | :--- | :--- | :--- |
| **Dense Text Embeddings** | Sentence-Transformers (BERT-based) | `sentence-transformers/all-MiniLM-L6-v2` | 22.7M params / 384 dimensions | Converts text passages into dense vector representations for semantic search and distractor generation. |
| **Topic Classification (Zero-Shot)** | DistilBERT Cross-Encoder | `typeform/distilbert-base-uncased-mnli` | 66M params | Multi-genre Natural Language Inference (MNLI) model predicting probability across 10 academic domains. |
| **Topic Classification (Centroid)** | Dense Cosine Centroid Classifier | `sentence-transformers/all-MiniLM-L6-v2` | 384 dimensions | Fast vector similarity between notes embedding and academic domain anchors with temperature-scaled Softmax. |
| **Abstractive Summarization** | DistilBART Sequence-to-Sequence | `sshleifer/distilbart-cnn-12-6` | 306M params | Generative abstractive synthesis of long study notes into concise summaries. |
| **Extractive Summarization** | Centroid + Maximal Marginal Relevance (MMR) | `sentence-transformers/all-MiniLM-L6-v2` | 384 dimensions | Graph/vector centrality extractive summarizer that guarantees 100% faithfulness to notes with 0% hallucination. |

---

## 2. Pretrained Inference vs. Fine-Tuning Distinction

An important distinction to explain in academic project assessments:

1. **Pretrained Inference (Current Mode)**:
   - Models are loaded with pretrained weights released on Hugging Face Hub (trained on massive corpora like MNLI, MS MARCO, and CNN/DailyMail).
   - The weights remain frozen during inference.
   - Zero-shot classification operates by formulating the topic prediction as a premise-hypothesis textual entailment task (`"This educational text is about {topic}"`).
   - Embeddings project sentences into a high-dimensional Riemannian latent space where semantic similarity corresponds to cosine distance.

2. **Actual Fine-Tuning (Optional Extension)**:
   - To fine-tune, one would collect a labeled dataset of syllabus notes across specific university departments (e.g., 5,000 course notes labeled across CS, Biology, Physics).
   - A classification head (`nn.Linear(768, num_classes)`) would be added on top of `distilbert-base-uncased` and trained with cross-entropy loss using PyTorch and AdamW.
   - RecallAI clearly distinguishes between zero-shot inference and fine-tuning in all UI badges and analytical metrics.

---

## 3. CPU Compatibility & Memory Footprint

- All models default to `device="cpu"` (or `device=-1`).
- Lazy loading is utilized: weights are only instantiated when the student triggers that specific feature.
- Caching is managed via Streamlit's `@st.cache_resource`, ensuring models load into RAM once and remain responsive for all subsequent queries.
