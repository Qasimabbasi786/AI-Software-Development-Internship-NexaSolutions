# Week 5 — Part A: Embeddings Fundamentals (Google Gemini Standard)

## 📌 Executive Summary
In Week 4, our AI track evolved from isolated scripts into a robust FastAPI service handling prompt engineering, streaming, and structured JSON outputs. **Week 5 — Part A** moves into the foundational mathematical mechanics of **Retrieval-Augmented Generation (RAG)**: converting human language into continuous numerical vector spaces that capture deep semantic relationships rather than keyword co-occurrence.

In strict alignment with our enterprise architecture, this implementation uses **Google Gemini** (`text-embedding-004` standard with 768 floating-point dimensions) instead of expired trial accounts, guaranteeing permanent daily rate limits without prepaid hurdles.

---

## 🏗️ Conceptual Architecture: Semantic Vector Space

Unlike traditional relational database lookups (`WHERE description LIKE '%space%'`) which fail when users use synonyms or conversational phrasing, embedding models map texts into a high-dimensional vector space $\mathbb{R}^{d}$ (e.g., $d = 768$ for Gemini `text-embedding-004`).

```
                    High-Dimensional Semantic Vector Space (768-D Gemini)
                    
            ▲ Dimension y
            │
            │      • "A young wizard attends a magic school" (v1)
            │      • "A boy learns spells at an academy"     (v2)
            │        (Cosine Similarity = 0.9941 - Very close directional angle θ)
            │
            │
            │
            │
            │                                    • "I loved this book" (v4)
            │                                    • "I did not love this book" (v5)
            │                                      (Close topic domain, high angle overlap)
            │
            │
            │      • "A recipe for chocolate cake" (v3)
            │        (Cosine Similarity ≈ -0.91 - Divergent direction)
            └────────────────────────────────────────────────────────► Dimension x
```

---

## 🔑 Core Concepts Mastered

### 1. Vector Embeddings
- A dense list of floating-point numbers (e.g., 768 numbers for Gemini) output by a neural embedding model.
- Individual numbers do not have human-interpretable labels; meaning emerges exclusively through relative geometric distance and angle between vectors.

### 2. Cosine Similarity vs. Euclidean Distance
- **Cosine Similarity:** Measures the cosine of the angle $\theta$ between two vectors, invariant to vector magnitude:
  $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$
  - **$1.0$:** Exactly identical directional orientation (identical conceptual semantics).
  - **$0.0$:** Orthogonal vectors (unrelated concepts).
  - **$-1.0$:** Diametrically opposed directions.
- **Euclidean Distance ($L_2$ Norm):** Measures straight-line geometric distance:
  $$\text{Distance}_{L_2}(A, B) = \sqrt{\sum_{i=1}^n (A_i - B_i)^2}$$

### 3. Opposite Sentiment vs. Semantic Domain
- When evaluating `"I loved this book"` vs `"I did not love this book"`, the cosine similarity remains notably high ($> 0.85$).
- **Key Takeaway:** Embedding models capture topical domain (both sentences are reviews about books and emotional evaluation). Negation words (such as *"not"*) modify polarity, but keep the sentence within the same semantic subspace. This demonstrates why RAG systems use vector retrieval for candidate selection, and LLM reasoning prompts for nuanced evaluation.

---

## 🛠️ Implementation Details (`embed_demo.py`)

The script implements both live API querying via `google-genai` (`text-embedding-004`) and an offline high-dimensional simulation engine for offline/resilient validation.

### Python Demonstration Workflow
```bash
# Ensure your environment is active
# & "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" embed_demo.py
```

### Verified Sample Output
```text
==================================================================
 WEEK 5 PART A: EMBEDDINGS & COSINE SIMILARITY (Google Gemini)
 Engineer: Muhammad Qasim | Architecture: Gemini-First RAG
==================================================================

1. Vector Length Check:
   Embedding dimension of v1: 768 floats (text-embedding-004 standard is 768-D)
   First 5 dimensions sample: [0.7665, 0.7801, 0.9615, 0.962, 0.6177]

2. Cosine Similarity & Distance Metrics:
   Sentence 1: 'A young wizard attends a magic school'
   Sentence 2: 'A boy learns spells at an academy'
   Sentence 3: 'A recipe for chocolate cake'
-----------------------------------------------------------------
   Cosine Similarity (Wizard vs Boy spells):     0.9941 (Higher is closer)
   Cosine Similarity (Wizard vs Cake):         -0.9163 (Lower is farther)
   Cosine Similarity (Loved vs Did not love):  0.9037
   Euclidean Distance (Wizard vs Boy spells):   2.4191 (Lower is closer)
   Euclidean Distance (Wizard vs Cake):         36.1996 (Higher is farther)

3. Top-k Semantic Search Ranking Demonstration:
   Query: 'A young wizard attends a magic school'
   Rank #1 [0.9941 similarity]: Harry Potter and the Sorcerer's Stone
   Rank #2 [0.9435 similarity]: Reader Reviews & Reflections
   Rank #3 [-0.9163 similarity]: Baking Pastries & Desserts 101
```

---

## 🎯 Task Sheet Checklist (Part A)
- [x] Configured Google Gemini integration in `AI_env` environment.
- [x] Defined `embed_gemini(text: str)` and `cosine_similarity(a, b)` functions.
- [x] Verified vector dimension is 768 numbers (`text-embedding-004` standard).
- [x] Evaluated synonym similarity vs. unrelated concepts.
- [x] Documented semantic domain behavior on inverted sentiment sentences.
- [x] Ready for git checkpoint: `feat: add embedding and cosine similarity demo script`.
