# Week 6 — Part B: Smarter Splitting & Advanced Retrieval

## 📌 Executive Summary
In production RAG systems, fixed-size character chunking and single-query semantic searches frequently miss relevant passages due to vocabulary mismatch, boundary truncation, and phrasing variations. 

This module implements:
1. **`RecursiveCharacterTextSplitter`**: Bounding chunks hierarchically along semantic paragraph (`\n\n`), sentence (`. `), and word (` `) boundaries.
2. **Local Vector Store**: ChromaDB backed by **Google Gemini embeddings** (`models/gemini-embedding-001`).
3. **`MultiQueryRetriever`**: Autonomous LLM-driven query expansion generating multiple perspectives of user intent to maximize recall.

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
                      │        ChromaDB Vector Store         │
                      │  (Google Gemini Embedding-001)       │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │   User Query: "How to handle scale?" │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │        MultiQueryRetriever           │
                      │  - Perspective 1: Data replication   │
                      │  - Perspective 2: Distributed storage│
                      │  - Perspective 3: Partitioning rules │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │     Deduplicated Union of Docs       │
                      │   (Maximizes Candidate Recall)       │
                      └──────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Recursive Character Splitting
Unlike naive length-based cuts that split words or sentences in half, `RecursiveCharacterTextSplitter` tries separators in order:
- `\n\n` (paragraphs)
- `\n` (lines)
- `. ` (sentences)
- ` ` (words)
This guarantees semantic chunks remain cohesive, complete thoughts.

### 2. Multi-Query Reformulation
Users rarely phrase questions with the exact keywords stored in vector documents. By prompting the LLM to generate 3 alternative formulations of the user's question, `MultiQueryRetriever` executes parallel vector queries, merges results, and deduplicates retrieved passages.

---

## 🛠️ Implementation Details (`advanced_retrieval_demo.py`)

- **Embeddings:** Google Gemini `models/gemini-embedding-001` via `model_factory.py`.
- **Vector Database:** Local ChromaDB in-memory / persistent collection.
- **Verification Command:**
  ```bash
  python Week_06_PartB_AdvancedRetrieval/advanced_retrieval_demo.py
  ```
