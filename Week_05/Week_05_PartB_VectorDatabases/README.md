# Week 5 — Part B: Vector Databases (ChromaDB)

## 📌 Executive Summary
Comparing a query embedding against every document in memory via a naive Python `for` loop works for 10 records, but fails to scale when indexing thousands or millions of documents. **Week 5 — Part B** introduces dedicated **Vector Databases**, using **ChromaDB** to store high-dimensional embeddings, execute Approximate Nearest Neighbor (ANN) vector lookups, and filter candidate chunks using metadata.

---

## 🏗️ Architecture: Vector Indexing & Querying

```
      Document Ingestion Flow
      ┌──────────────────────────────────────────────────────────────┐
      │ Document Text + Metadata ("Fantasy", "book_1.txt", year)      │
      └──────────────────────────────┬───────────────────────────────┘
                                     │
                                     ▼
                           ┌───────────────────┐
                           │ Embedding Engine  │
                           └─────────┬─────────┘
                                     │ Dense Vectors
                                     ▼
                       ┌───────────────────────────┐
                       │   ChromaDB Collection     │
                       │   (HNSW Graph Index)      │
                       └─────────────┬─────────────┘
                                     ▲
     Query & Filtering Flow          │ Cosine / L2 Nearest Neighbor
      ┌──────────────────────────────┴───────────────────────────────┐
      │ Query Text + Metadata Filter (where={"category": "Fantasy"}) │
      └──────────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Vector Database vs. Naive Python List
- **Linear Scan ($O(N \cdot d)$):** Comparing each vector sequentially is computationally expensive, memory-bound, and requires $N$ full dot-product computations per query.
- **Hierarchical Navigable Small World (HNSW) Index:** Vector databases build multi-layer geometric graphs to traverse and locate nearest neighbors in $O(\log N)$ sub-linear time, scaling to millions of documents.

### 2. Document & Metadata Storage
Each entry in ChromaDB stores:
- **`id`:** Unique chunk or document identifier (e.g., `book_1`, `book_2`).
- **`embedding`:** High-dimensional floating-point vector.
- **`document`:** The raw text content of the chunk.
- **`metadata`:** Structured key-value properties (e.g., `{"source": "book_1.txt", "category": "Fantasy", "year": 1997}`).

### 3. Metadata Filtering (Hybrid Search)
ChromaDB supports pre-filtering vector search results using structured metadata fields:
```python
# Simple Category Filter
results = collection.query(
    query_texts=["a space journey story"],
    n_results=2,
    where={"category": "Fantasy"}
)

# Compound Filter ($and with category and year)
compound_results = collection.query(
    query_texts=["futuristic artificial intelligence and cyberspace"],
    n_results=2,
    where={"$and": [{"category": {"$eq": "Science Fiction"}}, {"year": {"$gte": 2020}}]}
)
```

### 4. Vector Database Landscape
- **Local / Embedded:** ChromaDB, FAISS (ideal for rapid development, testing, and CI/CD).
- **Enterprise / Distributed:** Qdrant, Pinecone, Weaviate, Milvus, PostgreSQL with `pgvector`.

---

## 🛠️ Implementation Details (`chroma_demo.py`)

### Execution Command
```bash
# & "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" chroma_demo.py
```

### Verified Execution Output
```text
=== Week 5 Part B: Local Vector Database Demo (ChromaDB) ===

Adding 5 documents with metadata to Chroma collection...
Total documents indexed in 'books_demo': 5

--- Query 1: Unfiltered Nearest-Neighbor Search for 'a space journey story' ---
  [1] ID: book_2 | Category: Science Fiction | Text: A crew travels through a wormhole to save humanity from a dying Earth.
  [2] ID: book_5 | Category: Science Fiction | Text: A cyberpunk hacker uncovers an AI conspiracy in Neo-Tokyo in the year 2099.

--- Query 2: Filtered Search (category == 'Fantasy') for 'a story about battles and destiny' ---
  [1] ID: book_1 | Category: Fantasy | Text: A young wizard attends a magic school and fights a dark lord.

--- Query 3: Compound Filter ($and: category == 'Science Fiction', year >= 2020) ---
  [1] ID: book_5 | Year: 2023 | Category: Science Fiction | L2 Distance: 0.8648
       Text: A cyberpunk hacker uncovers an AI conspiracy in Neo-Tokyo in the year 2099.

--- ChromaDB Summary ---
[+] Successfully demonstrated vector indexing, distance querying, and hybrid metadata filtering.
```

---

## 🎯 Task Sheet Checklist (Part B)
- [x] Initialized local Chroma client (`chromadb.Client()`).
- [x] Created collection named `books_demo`.
- [x] Added sample documents with metadata (`source`, `category`, `year`) and unique IDs.
- [x] Verified semantic retrieval returns Science Fiction document first for space query.
- [x] Implemented metadata filtering (`where={"category": "Fantasy"}`).
- [x] Added two custom practice documents (Victorian London Mystery & Neo-Tokyo Cyberpunk).
- [x] Tested compound filtering with `$and` operator on metadata.
- [x] Ready for git checkpoint: `feat: add local Chroma vector database demo`.
