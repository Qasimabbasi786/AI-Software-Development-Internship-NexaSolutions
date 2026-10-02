# Week 5 — Part C: RAG Fundamentals (Manual 8-Stage Pipeline)

## 📌 Executive Summary
**Retrieval-Augmented Generation (RAG)** is the industry-standard architecture for grounding Large Language Models in verifiable source documentation. Before querying the model, relevant text chunks are dynamically retrieved from a vector database and injected into the prompt as bounded context. **Week 5 — Part C** constructs the complete 8-stage RAG pipeline from scratch by hand without frameworks like LangChain, ensuring complete mechanical transparency.

---

## 🏗️ The 8 Stages of the Complete RAG Architecture

```
 1. Document Loading        2. Chunking / Text Splitting      3. Embedding
┌─────────────────────┐    ┌─────────────────────────────┐   ┌──────────────────────┐
│ Raw Books & Texts   ├───►│ Fixed Size (300 chars)       ├──►│ Vector Embeddings    │
│ (Plaintext/Catalog) │    │ Overlap (40 chars)          │   │ (Dense Representation)│
└─────────────────────┘    └─────────────────────────────┘   └──────────┬───────────┘
                                                                        │
                                                                        ▼ 4. Vector Storage
 8. Source Attribution     7. Answer Generation              ┌──────────────────────┐
┌─────────────────────┐    ┌─────────────────────────────┐   │ ChromaDB Collection  │
│ Return Document     │◄───┤ Google Gemini / Local Engine│   │ library_rag          │
│ Sources to Client   │    │ Grounded Zero Hallucination │   └──────────┬───────────┘
└─────────────────────┘    └──────────────▲──────────────┘              │
                                          │                             ▼ 5. Retrieval
                           6. Context Construction           ┌──────────────────────┐
                           ┌─────────────────────────────┐   │ Query Vector &       │
                           │ Grounding Prompt Template   │◄──┤ Top-k Chunks (k=3)   │
                           │ Negative Refusal Constraint │   └──────────────────────┘
                           └─────────────────────────────┘
```

---

## 🔑 Deep-Dive into the 8 Stages

1. **Document Loading:** Ingesting raw corpus data from text files, APIs, or database rows.
2. **Chunking / Text Splitting:** Breaking long documents into smaller segments. Fixed-size chunking with sliding overlap (e.g., 300–500 characters with 40–50 character overlap) prevents sentence fragmentation at boundaries.
3. **Embedding:** Passing each chunk through the embedding model to produce normalized dense vectors.
4. **Vector Storage:** Inserting chunk embeddings, raw text, and metadata (`{"source": "Clean_Code.txt", "chunk": 0}`) into ChromaDB.
5. **Retrieval:** Embedding the user query and retrieving the top-$k$ nearest chunks.
6. **Context Construction:** Assembling the retrieved chunks into a prompt with strict negative constraints.
7. **Answer Generation:** Sending the prompt to Google Gemini with instructions to answer *only* from the context.
8. **Source Attribution:** Returning verifiable document citations (`sources: ['DDIA.txt', ...]`) alongside the generated answer.

---

## 🛡️ Grounding Prompt Architecture
```python
def build_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(chunks)
    return f"""Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have that information."
Do not use outside knowledge.

Context:
{context}

Question: {question}"""
```

---

## 🛠️ Implementation Details (`rag_pipeline.py`)

### Execution Command
```bash
# & "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" rag_pipeline.py
```

### Verified Pipeline Execution Output
```text
=== Week 5 Part C: Full Manual RAG Pipeline ===
[INGEST] Added 'Clean_Code.txt' (1 chunks).
[INGEST] Added 'DDIA.txt' (1 chunks).
[INGEST] Added 'Dune.txt' (1 chunks).

--- Testing Query 1: 'What topics does Designing Data-Intensive Applications cover?' ---
Retrieved Chunks: 3
Sources: ['Clean_Code.txt', 'DDIA.txt', 'Dune.txt']
Answer:
 Designing Data-Intensive Applications covers data systems, storage engines (LSM-trees and B-trees), replication, transactions (ACID), and Apache Kafka stream processing.

--- Testing Query 2 (Out of Catalog): 'Who is the Prime Minister of Australia and what is their economic policy?' ---
Sources: ['Clean_Code.txt', 'DDIA.txt', 'Dune.txt']
Answer:
 I don't have that information.
```

---

## 🎯 Task Sheet Checklist (Part C)
- [x] Implemented `chunk_text(text, chunk_size=500, overlap=50)`.
- [x] Initialized ChromaDB with native vector embeddings.
- [x] Ingested 3-4 multi-paragraph documents into the collection.
- [x] Verified retrieval of top-$k$ relevant chunks for in-domain questions.
- [x] Verified zero-shot refusal on out-of-domain questions.
- [x] Returned and logged source attribution metadata for every query.
- [x] Ready for git checkpoint: `feat: build manual RAG pipeline: chunk, embed, store, retrieve, generate`.
