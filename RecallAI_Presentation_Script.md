# 🎓 RecallAI — Complete Project Guide & 2-Person Presentation Script
**Course:** Deep Learning (DS306)  
**Instructor:** Dr. Kongara Srinivasa Rao  
**Presenters:**
- **Speaker 1:** Golla Madhulika (`23STUCHH010826`)
- **Speaker 2:** Reethu Reddy (`23STUCHH011082`)
**PowerPoint File:** `RecallAI_DS306_Presentation.pptx` (8 Widescreen Slides)

---

# 🧠 Part 1: Quick Project Understanding ("Cheat Sheet")

### 1. What is RecallAI in one sentence?
> **RecallAI** is an autonomous deep learning study assistant that ingests raw lecture notes or PDFs and transforms them into 100% hallucination-free summaries, zero-shot academic domain classifications, interactive flashcards, and semantic distractor quizzes.

---

### 2. Why Deep Learning instead of regular Python text matching?
| Traditional / Rule-Based NLP | RecallAI Deep Learning Stack |
| :--- | :--- |
| Keyword matching (exact string overlap) fails when synonyms are used. | **Dense vector embeddings (`all-MiniLM-L6-v2`)** capture deep semantic meaning in 384 dimensions regardless of phrasing. |
| Hardcoded rules cannot generalize across diverse college subjects. | **DistilBERT MNLI Zero-Shot Classification** understands any academic topic out-of-the-box without rule engineering. |
| Generic generative LLMs (e.g., ChatGPT) hallucinate false facts and formulas. | **Semantic Centroid + MMR Extractive Summarizer** extracts exact verbatim sentences from the student's notes, guaranteeing 0% hallucination. |
| Quiz distractors are either random or hardcoded. | **Vector-Space Distractor Generation** picks options that are semantically close to the correct concept, creating realistic, high-quality test questions. |

---

### 3. The Two Core Deep Learning Models Used
1. **Sentence-Transformers (`sentence-transformers/all-MiniLM-L6-v2`):**
   - **Type:** 6-layer Transformer, 22.7M parameters.
   - **Output:** 384-dimensional dense semantic vector for every sentence.
   - **How it works:** Tokenizes sentences, applies multi-head self-attention, and computes **mean pooling** over output contextual embeddings.
   - **Why this model?** It delivers state-of-the-art semantic search accuracy while executing in under 50 milliseconds on standard CPU without requiring GPUs.
2. **DistilBERT Zero-Shot NLI (`typeform/distilbert-base-uncased-mnli`):**
   - **Type:** 6-layer distilled Transformer, 66M parameters.
   - **Task:** Multi-Genre Natural Language Inference (MNLI).
   - **How it works:** Forms pairs of (Premise: Note text, Hypothesis: *"This text is about {topic}"*). It computes entailment probability via softmax logits over 10 academic domains (Computer Science, Biology, Mathematics, etc.).

---

### 4. Key Mathematical Concept: Maximal Marginal Relevance (MMR)
How does our summarizer pick the best sentences without repeating ideas?
$$\text{MMR} = \arg\max_{D_i \in R \setminus S} \left[ \lambda \cdot \text{Sim}_1(D_i, \vec{C}) - (1 - \lambda) \max_{D_j \in S} \text{Sim}_2(D_i, D_j) \right]$$
- $\vec{C}$ = Document Centroid vector (mean of all sentence vectors).
- $\text{Sim}_1(D_i, \vec{C})$ = Cosine similarity to the whole document's main idea (relevance).
- $\text{Sim}_2(D_i, D_j)$ = Cosine similarity to already selected sentences (redundancy penalty).
- $\lambda = 0.7$ gives high priority to core concepts while avoiding duplicate statements.

---

# 🎤 Part 2: Slide-by-Slide 2-Person Presentation Script

---

### **Slide 1: Title Slide & Introduction**
* **Visual:** Slide 1 showing Title, Course DS306, Dr. Kongara Srinivasa Rao, and both names.
* **Speaker 1 (Madhulika):**
  > *"Respected Sir and good morning/afternoon everyone. Welcome to our Deep Learning course project presentation for DS306.  
  > I am Golla Madhulika (ID: 23STUCHH010826), and joining me is my project partner, Reethu Reddy (ID: 23STUCHH011082).  
  > Under the guidance of Dr. Kongara Srinivasa Rao sir, we have designed and implemented **RecallAI — A Deep Learning-Based Personalized Study Assistant**."*

* **Speaker 2 (Reethu):**
  > *"Our goal with RecallAI is to solve one of the biggest challenges students face today: converting vast, unstructured lecture materials into active, memorable study aids using deep learning transformers — without any hallucination or factual inaccuracies."*

---

### **Slide 2: Problem Statement**
* **Visual:** Slide 2 showing Cognitive Overload, LLM Hallucination Risk, and the Solution.
* **Speaker 1 (Madhulika):**
  > *"To understand why we built RecallAI, let us look at the current study dilemma:  
  > First, **Cognitive Overload**: Before exams, engineering students are overwhelmed with hundreds of pages of slides and PDFs. Studies in cognitive science show that passive re-reading has less than a 20% retention rate after 48 hours.  
  > Second, **The Hallucination Risk of LLMs**: While students try using generative models like ChatGPT, these models frequently invent false facts, mix up formulas, or rewrite definitions in ways that lose academic rigor. In technical subjects like computer systems or machine learning, verbatim accuracy is critical.  
  > This created the need for an autonomous study platform that operates on grounded course notes, guarantees 100% academic integrity, and provides active recall testing."*

---

### **Slide 3: Introduction & Core Objectives**
* **Visual:** Slide 3 with 4 feature cards (Ingestion, Classification, Summarization, Active Recall).
* **Speaker 1 (Madhulika):**
  > *"RecallAI provides a complete 4-stage active learning pipeline:  
  > 1. **Smart Document Ingestion**: We extract clean text from multi-page PDFs using PyMuPDF, filtering out noise, corrupt pages, and non-text artifacts.  
  > 2. **Zero-Shot Domain Classification**: The system automatically identifies the academic domain of the material without needing any subject-specific retraining.  
  > 3. **Hallucination-Free Summarization**: Using dense semantic centroid selection, it produces concise summaries with over 70% compression while preserving verbatim original sentences.  
  > 4. **Active Recall & Testing**: It automatically generates interactive flashcards and multiple-choice questions with intelligent vector-matched distractors.  
  > Now, my partner Reethu will walk you through the deep learning architecture and models powering this system."*

*(Madhulika hands over to Reethu)*

---

### **Slide 4: Deep Learning Technologies & Models Used**
* **Visual:** Slide 4 showing MiniLM-L6-v2, DistilBERT MNLI, and PyTorch Stack.
* **Speaker 2 (Reethu):**
  > *"Thank you, Madhulika. For our deep learning backbone, we intentionally selected architectures optimized for semantic precision and rapid CPU inference:  
  > 
  > 1. **Sentence-Transformers (`all-MiniLM-L6-v2`)**:  
  > This is a 6-layer Transformer with 22.7 million parameters. It projects every sentence into a **384-dimensional dense semantic vector space**. Unlike classical TF-IDF or Bag-of-Words, it understands contextual meaning. For instance, it recognizes that 'gradient descent' and 'optimization algorithm' are semantically related even if they share zero identical words.  
  > 
  > 2. **DistilBERT Zero-Shot NLI (`typeform/distilbert-base-uncased-mnli`)**:  
  > DistilBERT has 66 million parameters and is 40% smaller and 60% faster than BERT-base. We leverage its Natural Language Inference capabilities by posing candidate hypotheses such as: *'This text is about Computer Science'* or *'This text is about Biology'*. By computing the softmax over the entailment logits, the model classifies topics with high confidence without any task fine-tuning.  
  > 
  > The system runs on **PyTorch** and **Hugging Face Transformers**, wrapped in a responsive desktop web interface using **Streamlit**."*

---

### **Slide 5: Deep Learning Architecture: How It Works**
* **Visual:** Slide 5 with the 4-step pipeline cards and the end-to-end flowchart.
* **Speaker 2 (Reethu):**
  > *"Here is how the deep learning pipeline functions end-to-end:  
  > 
  > * **Step 1 (Dense Embedding Projection)**: Incoming text is split into clean sentences. Each sentence is passed through `all-MiniLM-L6-v2` to extract 384-dimensional embeddings via token self-attention and mean pooling.  
  > * **Step 2 (Centroid & MMR Summarizer)**: We compute the document's global semantic centroid vector $\vec{C}$. Using **Maximal Marginal Relevance (MMR)** with $\lambda = 0.7$, we select the sentences that maximize cosine similarity to the core theme while penalizing overlap with previously selected sentences. This completely eliminates hallucinations because every sentence is verbatim from the source.  
  > * **Step 3 (Zero-Shot Classification)**: The document representation is evaluated across candidate academic domains to assign domain labels and confidence distributions.  
  > * **Step 4 (Semantic Distractor Synthesis)**: For quiz questions, key terms are extracted, and incorrect options are sampled from semantically close embedding neighbors. This ensures distractors are challenging and plausible rather than obviously incorrect.  
  > 
  > Now, Madhulika will demonstrate the actual working system with live project screenshots."*

*(Reethu hands over to Madhulika)*

---

### **Slide 6: Working System: Note Ingestion & Study Workspace**
* **Visual:** Slide 6 showing the Upload Notes and Study Workspace screenshots.
* **Speaker 1 (Madhulika):**
  > *"As you can see on Slide 6, this is our actual deployed application running on `localhost:8501`:  
  > 
  > On the **left screenshot**, we have the **Upload Notes** interface. Students can upload a PDF, paste text, or click pre-built academic sample notes. Here, we loaded notes on *Machine Learning & Neural Networks* (235 words). The system validates the content, previews the text, and triggers the 5-step deep learning pipeline.  
  > 
  > On the **right screenshot**, we have the **Study Workspace**. In under 2 seconds, our model generated an **AI-extractive summary** with a **71.5% compression ratio**, reducing 235 words into 67 high-impact words.  
  > Below the summary, it lists the MMR-ranked core concept takeaways, and provides tabs for interactive flashcards, key concept definitions, and vector semantic search where students can ask questions in natural language."*

---

### **Slide 7: Working System: Student Dashboard & Quiz Analytics**
* **Visual:** Slide 7 showing USER01 Dashboard and Diagnostic Quiz Results screenshots.
* **Speaker 2 (Reethu):**
  > *"Moving to Slide 7, we see the student assessment and tracking experience:  
  > 
  > On the **left panel**, the **Student Dashboard (USER01)** reflects 100% authentic, real session data. It immediately updates our counters: **8 Flash Cards generated**, **1 Test taken**, **1 Study Guide active**, and our current mastery score. It also maintains a recent activity feed so students can switch between lecture notes with a single click.  
  > 
  > On the **right panel**, we have the **Diagnostic Results Page**. After the student completes the 6-question quiz generated by our distractor model, it calculates the mastery percentage — in this test run, **50.0% (3 out of 6 correct)**.  
  > Most importantly, the deep learning engine doesn't just give a score; it diagnoses **'Concepts to Review'** — specifically highlighting *Backpropagation* and *Supervised Learning* so the student knows exactly where to focus."*

---

### **Slide 8: Conclusion & Future Scope**
* **Visual:** Slide 8 showing Key Achievements and Future Scope.
* **Speaker 1 (Madhulika):**
  > *"To conclude our presentation:  
  > RecallAI proves that targeted, lightweight deep learning transformers can outperform massive generative LLMs for focused academic tasks.  
  > By combining **Sentence-Transformers** with **Extractive Centroid Summarization**, we provide **100% hallucination-free study aids** with sub-second CPU inference and zero cloud API dependency."*

* **Speaker 2 (Reethu):**
  > *"For future work, we plan to extend RecallAI in three key areas:  
  > 1. Incorporating Vision-Language Models like CLIP or ViT to interpret formulas, diagrams, and textbook charts.  
  > 2. Adding the SuperMemo SM-2 algorithm for automated spaced-repetition scheduling.  
  > 3. Integrating Whisper for speech-to-text to transcribe recorded lectures directly into study notes.  
  > 
  > We would like to express our sincere gratitude to our instructor, **Dr. Kongara Srinivasa Rao sir**, for his guidance throughout this Deep Learning course.  
  > We are now ready for your questions and feedback. Thank you!"*

---

# 🎯 Part 3: Anticipated Viva / Examiner Q&A (Dr. Kongara Srinivasa Rao)

#### Q1: "Why did you use Extractive Summarization instead of Abstractive models like BART or T5?"
* **Answer (Madhulika / Reethu):**
  > *"Sir, abstractive models generate new sentences by decoding text tokens. While they produce fluent English, in technical and STEM exams they run the risk of hallucinating inaccurate formulas, misstating scientific definitions, or altering key numerical values. Extractive summarization using semantic centroid MMR mathematically selects verbatim sentences from the instructor's verified notes, guaranteeing 0% hallucination."*

#### Q2: "What is the role of Cosine Similarity in your architecture?"
* **Answer (Reethu):**
  > *"Sir, our Sentence-Transformer normalizes sentence vectors so their Euclidean norm is 1. The cosine similarity is simply the dot product between two normalized vectors:  
  > $$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$  
  > We use cosine similarity in three key places:  
  > 1. Calculating sentence relevance to the document centroid vector $\vec{C}$.  
  > 2. Natural language semantic vector search in the study workspace.  
  > 3. Measuring distractor proximity to generate plausible multiple-choice options."*

#### Q3: "What is the difference between Zero-Shot Classification and Fine-Tuning?"
* **Answer (Madhulika):**
  > *"Sir, supervised fine-tuning requires thousands of labeled domain-specific training pairs and updates the model's weights via backpropagation.  
  > In contrast, Zero-Shot Classification with DistilBERT-MNLI uses a model already pre-trained on premise-hypothesis entailment. We formulate the domain classification as an NLI problem without updating any weights. This allows RecallAI to generalize across any academic subject immediately without retraining."*

#### Q4: "How does the quiz engine generate distractors?"
* **Answer (Reethu):**
  > *"Sir, instead of generating random distractors, our system extracts key terms from the document and computes their embedding similarities. For any term $T$, distractors are chosen from terms that have moderate-to-high cosine similarity to $T$ in vector space but are not identical. This ensures distractors test real conceptual boundaries rather than being trivially obvious."*
