# 🔍 Retrieval-Augmented Generation (RAG) & Vector Database Architecture

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 5 — Manual RAG Pipeline, Vector Embeddings & FastAPI Integration  

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6F00?logo=chroma&logoColor=white)](https://www.trychroma.com/)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Architecture: 8--Stage RAG](https://img.shields.io/badge/Architecture-8--Stage_RAG-blueviolet)](https://github.com/)

---

## 🌟 Overview

This repository contains the complete implementation for **Week 5: Retrieval-Augmented Generation (RAG)** built strictly on the **Google Gemini Standard** (`text-embedding-004` and `gemini-2.5-flash`). It completely replaces temporary trial-based providers (like OpenAI) with Google Gemini's daily-refreshing free tier for sustainable, cost-effective enterprise AI engineering.

```
       ┌────────────────┐      ┌─────────────────┐      ┌────────────────┐
       │ Ingest / Chunks│ ───> │ Vector Database │ <─── │ User Question  │
       │ (Fixed+Overlap)│      │  (ChromaDB HNSW)│      │   Embedding    │
       └────────────────┘      └─────────────────┘      └────────────────┘
                                        │
                                        ▼ Top-K Chunks
                               ┌─────────────────┐
                               │ Prompt Template │
                               │ Strict Grounding│
                               └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ LLM Generation  │ ───> Grounded Answer +
                               │ (Google Gemini) │      Source Citations
                               └─────────────────┘
```

---

## 📂 Repository Structure

| Directory / File | Description |
| :--- | :--- |
| **`Week_05_PartA_Embeddings/`** | Google Gemini `text-embedding-004` vector representations, Cosine Similarity, and top-$k$ semantic search rankings. |
| **`Week_05_PartB_VectorDatabases/`** | ChromaDB collection indexing, L2 distance queries, and compound `$and` metadata filtering. |
| **`Week_05_PartC_RAGPipeline/`** | Manual 8-stage RAG pipeline with chunking, retrieval, prompt assembly, and hallucination guardrails. |
| **`Week_05_PartD_Evaluation/`** | Quantitative RAG evaluation framework measuring chunk size trade-offs and hit rate @ $k$. |
| **`Week_05_PartE_FastAPIAsk/`** | FastAPI microservice exposing `/ask` with Pydantic validation, CORS, error handling, and citations. |
| **`Week_05_PartF_GitRevert/`** | Git revert documentation and safe commit rollback walkthroughs. |
| **`Week_05_Final_Project/`** | End-to-end Library Assistant CLI & grounding test suite over persistent catalog vectors. |
| **`Week_05_CheckStage_Answers.md`** | Comprehensive architectural and theoretical answers to all Week 5 assessment questions. |

---

## 🚀 Quickstart & Execution

### 1. Configure Local Environment (`.env`)
Each subfolder includes its own isolated `.env` template:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 2. Run Module Demos

#### Part A: Vector Embeddings & Similarity (Google Gemini)
```bash
python Week_05_PartA_Embeddings/embed_demo.py
```

#### Part B: ChromaDB Vector Storage & Metadata Filtering
```bash
python Week_05_PartB_VectorDatabases/chroma_demo.py
```

#### Part C: Manual 8-Stage RAG Pipeline
```bash
python Week_05_PartC_RAGPipeline/rag_pipeline.py
```

#### Part D: RAG Quality & Evaluation Suite
```bash
python Week_05_PartD_Evaluation/rag_evaluation.py
```

#### Part E: FastAPI /ask Microservice
```bash
uvicorn Week_05_PartE_FastAPIAsk.app:app --reload --port 8000
# Interactive Swagger Documentation: http://127.0.0.1:8000/docs
```

#### Project: Grounding & Verification Test Suite
```bash
python Week_05_Final_Project/test_grounding.py
```

---

## 🛡️ Grounding & Hallucination Guardrails

The RAG pipeline enforces strict negative constraint prompting:
- **Strict Grounding:** The LLM is explicitly commanded to rely solely on the retrieved context chunks.
- **Zero-Shot Refusal:** If the answer is not present in the retrieved documents, the system returns `"I don't have that information."` rather than hallucinating external facts.
- **Source Attribution:** Every response includes the list of source document names referenced during generation.

---

## 👤 Author

- **Name:** Muhammad Qasim  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)
