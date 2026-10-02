# 🏛️ Library Knowledge Assistant (RAG Pipeline & Vector Search)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 5 Final Project — Capstone Multi-Tier Architecture  

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6F00?logo=chroma&logoColor=white)](https://www.trychroma.com/)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 📌 Executive Summary
The **Week 5 Final Project** integrates the entire week's learnings into an end-to-end, production-style **Library Knowledge Assistant**. It builds a RAG-powered `/ask` microservice that queries our diverse library book catalog (encompassing Tech / Software Engineering, classic Urdu Novels, and Pakistani Literature), performs high-dimensional vector search via **ChromaDB** (`library_rag_final`), and generates grounded, cited responses with zero hallucination using **Google Gemini**.

---

## 🏗️ Complete Multi-Tier Data Flow Architecture

```
 ┌────────────────────────────────────────────────────────┐
 │   PostgreSQL Database (librarydb_week3 @ localhost)    │
 │   Single Source of Truth for Books Catalog             │
 └───────────────────────────┬────────────────────────────┘
                             │ Live Catalog Data
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │   .NET 8 Web API (GET http://localhost:5000/api/books) │
 │   Public Endpoint serving Library Records              │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │   Python Corpus Ingestion (fetch_corpus / ingest)      │
 │   - Fetches live books from .NET API (/api/books)      │
 │   - Fallback to 10 rich books (Tech, Urdu, Pakistani)  │
 │   - chunk_text(chunk_size=350, overlap=40)             │
 │   - Generates Embeddings (Google Gemini / Local)       │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │   ChromaDB Vector Store (vector_store.py)              │
 │   - Persistent Collection: 'library_rag_final'         │
 │   - Stores Vectors + Metadata (title, author, category)│
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │   FastAPI Microservice (main.py)                       │
 │   - POST /ask {"question": "..."}                      │
 │   - Top-k Vector Similarity Search (k=3)               │
 └──────────────┬───────────────────────────▲─────────────┘
                │                           │
                ▼                           │
 ┌────────────────────────────────────────────────────────┐
 │   Grounding & Inference Engine (Google Gemini)         │
 │   - Strictly constrained prompt                        │
 │   - Adheres to: "I don't have that information."       │
 └──────────────┬─────────────────────────────────────────┘
                │
                ▼
 ┌────────────────────────────────────────────────────────┐
 │   AskResponse Schema                                   │
 │   {"answer": "...", "sources": ["Book Title", ...]}    │
 └────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Data Flow Progression:**  
> `PostgreSQL (librarydb_week3) -> .NET API (/api/books) -> Python Corpus Script -> ChromaDB -> /ask Endpoint -> Gemini LLM -> Answer + Sources`

---

## 📁 Project Components & File Structure

| File | Purpose |
| :--- | :--- |
| **[`corpus.json`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/corpus.json)** | 10 rich book records across Tech, Pakistani Literature, and Urdu Novels. |
| **[`fetch_corpus.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/fetch_corpus.py)** | Queries `.NET API` `GET /api/books`, formats structured book records into documents with offline fallback. |
| **[`ingest_corpus.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/ingest_corpus.py)** | Dedicated ingestion pipeline reading `corpus.json`, chunking text, generating embeddings, and storing in `library_rag_final`. |
| **[`vector_store.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/vector_store.py)** | Persistent Chroma collection manager for indexing and querying top-k relevant chunks. |
| **[`rag_pipeline.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/rag_pipeline.py)** | Complete end-to-end RAG pipeline orchestration module (Chunking, Embedding, Chroma `library_rag_final`, Gemini). |
| **[`main.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/main.py)** | FastAPI application providing `POST /ask`, `GET /health`, and `POST /reindex` with Pydantic validation & CORS. |
| **[`test_grounding.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/test_grounding.py)** | Automated verification test suite executing 3 in-catalog queries and 1 out-of-catalog negative check. |
| **[`interactive_ask.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_05/Week_05_Final_Project/interactive_ask.py)** | Interactive CLI allowing developers and mentors to ask arbitrary questions directly to the assistant. |

---

## 🚀 Execution & Verification Guide

### 1. Ingest Corpus & Build Vector Index
```bash
# Ingest 10 books into persistent ChromaDB collection
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" ingest_corpus.py
```

### 2. Launch FastAPI Microservice
```bash
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" -m uvicorn main:app --reload --port 8000
```
- Interactive Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Automated Grounding Tests
```bash
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" test_grounding.py
```

---

## 🛡️ Grounding Test Suite Results

```text
=================================================================
 WEEK 5 PROJECT — GROUNDING & SOURCE ATTRIBUTION TEST SUITE
=================================================================

[TEST 1] In-Catalog / Urdu Novels: Which novel discusses spiritual transformation, Salar Sikandar, and Imama Hashim?
  Answer: Peer-e-Kamil (The Perfect Mentor) by Umera Ahmed chronicles the transformative spiritual journeys of Imama Hashim and Salar Sikandar, depicting personal redemption, faith, and divine guidance.
  Sources: ['Peer-e-Kamil']
  Result: PASSED (Expected source present)

[TEST 2] In-Catalog / Data Engineering: What book should I read to learn about database storage engines, replication, and Kafka?
  Answer: Designing Data-Intensive Applications by Martin Kleppmann covers storage engines, transactions, replication, and Apache Kafka.
  Sources: ['Designing Data-Intensive Applications']
  Result: PASSED (Expected source present)

[TEST 3] In-Catalog / Pakistani Literature: Which satirical novel investigates the plane crash of General Zia-ul-Haq?
  Answer: A Case of Exploding Mangoes by Mohammed Hanif is a political satire investigating the mysterious plane crash of General Zia-ul-Haq.
  Sources: ['A Case of Exploding Mangoes']
  Result: PASSED (Expected source present)

[TEST 4] Out-of-Catalog Grounding Check: What is the capital city of France and what are its top tourist attractions?
  Answer: I don't have that information.
  Sources: []
  Result: PASSED (Zero hallucination refusal triggered)
```

---

## 🎯 Task Sheet Checklist (Final Project)
- [x] Step 1: Expanded custom corpus with 10 diverse books (Tech, Pakistani Lit, Urdu Novels).
- [x] Step 2: Built `ingest_corpus.py` to chunk, embed, and store in collection `library_rag_final`.
- [x] Step 3: Implemented FastAPI `/ask` endpoint with `AskRequest` and `AskResponse` schemas.
- [x] Step 4: Conducted grounding tests (3 in-catalog + 1 out-of-catalog refusal check).
- [x] Step 5: Verified source attribution list for all in-catalog answers.
- [x] Step 6: Documented full end-to-end data flow with architecture diagrams in README.
- [x] Step 7: Completed Git PR merges across all feature branches and tagged milestone `v0.5-week5`.

---

## 👤 Author

- **Name:** Muhammad Qasim  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)

