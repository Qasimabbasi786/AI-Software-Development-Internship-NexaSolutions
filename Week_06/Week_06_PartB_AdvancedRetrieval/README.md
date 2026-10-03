# Week 6 — Part B: Smarter Splitting & Advanced Retrieval

## 🌟 Overview
In production RAG systems, fixed-size chunking and single-query semantic searches frequently miss relevant passages due to vocabulary mismatch, boundary truncation, and phrasing variations. This module implements:
1. **`RecursiveCharacterTextSplitter`**: Bounding chunks hierarchically along semantic paragraph (`\n\n`), sentence (`. `), and word (` `) boundaries.
2. **Local Vector Store**: ChromaDB backed by **Google Gemini embeddings** (`models/gemini-embedding-001`).
3. **`MultiQueryRetriever`**: Autonomous LLM-driven query expansion generating multiple perspectives of the user's intent to maximize recall.

---

## 🏗️ Architecture: Advanced Retrieval Flow

```
                      ┌──────────────────────────────────────┐
                      │          Raw Book Documents          │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    RecursiveCharacterTextSplitter    │
                      │  (chunk_size=500, chunk_overlap=50)  │
                      │  Separators: ["\n\n", "\n", ". ", " "]│
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │        Chroma Vector Store           │
                      │     (models/gemini-embedding-001)    │
                      └──────────────────┬───────────────────┘
                                         │
             ┌───────────────────────────┴───────────────────────────┐
             │                                                       │
             ▼                                                       ▼
  [Standard Single Retriever]                              [MultiQueryRetriever]
  - 1 vector search for raw query                          - LLM generates 3 query variants
  - May miss chunks if query uses                          - Executes 3 parallel searches
    different vocabulary                                   - Merges & deduplicates results
             │                                                       │
             ▼                                                       ▼
      Top-k Chunks (k=3)                                    Comprehensive Context Set
```

---

## 📊 Comparative Evaluation: Single Query vs. MultiQueryRetriever

Benchmarking across the 5 canonical test questions from Week 5:

| # | Test Question | Plain Retriever (k=3) | MultiQueryRetriever | Reformulation & Recall Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Q1** | *What storage engines and streaming technologies are discussed in Designing Data-Intensive Applications?* | DDIA (book_2), Microservices (book_4), Clean Code (book_1) | DDIA (book_2), Microservices (book_4), Clean Code (book_1) | **Equal**: Both prioritize DDIA as top result. |
| **Q2** | *Who wrote Clean Code and what does it teach about functions?* | Clean Code (book_1), Microservices (book_4), DDIA (book_2) | Clean Code (book_1), Microservices (book_4), DDIA (book_2) | **Equal**: Exact author and keyword match cleanly indexed. |
| **Q3** | *What is the spice melange in the novel Dune?* | Dune (book_3), DDIA (book_2), Microservices (book_4) | Dune (book_3), Clean Code (book_1), Microservices (book_4), DDIA (book_2) | **Higher Recall**: MultiQuery rephrased for "sci-fi concepts" and captured 4 deduplicated chunks. |
| **Q4** | *What deployment strategies are recommended for microservices?* | Microservices (book_4), DDIA (book_2), Clean Code (book_1) | Microservices (book_4), DDIA (book_2), Clean Code (book_1) | **Equal**: Both isolate Sam Newman's microservices text. |
| **Q5** | *How do you calculate eigenvalues in linear algebra using NumPy?* | Out-of-catalog chunks (DDIA, Clean Code, Dune) | Deduplicated all 4 catalog chunks | **Dilution Risk**: MultiQuery attempted broader math/programming phrasings, pulling extra irrelevant context. |

---

## ⚖️ Trade-Off Analysis: When MultiQuery Helps vs. When It Hurts

### 1. When MultiQuery Helps (High-Recall Scenarios):
- **Vocabulary Gap:** When users ask questions using colloquialisms, acronyms, or non-technical synonyms (e.g., *"How do I keep my server from dying when traffic spikes?"* vs. text containing *"load balancing and horizontal scaling"*).
- **Multi-Faceted Queries:** Questions that touch on overlapping architectural concepts where one query vector cannot span all latent dimensions.

### 2. When MultiQuery Hurts (Precision Dilution & Latency Scenarios):
- **Specific Unanswerable Queries:** For narrow queries where the answer does *not* exist in the corpus (e.g., *"What exact year was the first single-leader replication paper written?"*), single-query retrieval returns low-similarity chunks that can be filtered out by threshold. In contrast, `MultiQueryRetriever` generates broad exploratory queries (e.g., *"History of distributed algorithms"* or *"Academic research in computer science"*), retrieving unrelated software engineering documents and injecting noise into the LLM context window.
- **Cost & Latency Overhead:** MultiQuery introduces 1 extra synchronous LLM call per query. In high-throughput APIs, this doubles prompt latency and increases API costs.

---

## 🚀 Execution

Run the Part B demonstration using the configured Python environment:

```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" advanced_retrieval_demo.py
```
