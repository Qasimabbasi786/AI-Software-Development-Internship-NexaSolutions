# 🤖 Enterprise AI Assistant Microservice (LangChain LCEL, Tools & Streaming)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 — LangChain & LCEL • Advanced Retrieval • Tool Calling • Polly Resilience • SSE Streaming  

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL_Pipelines-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Streaming: SSE](https://img.shields.io/badge/Streaming-Server--Sent_Events-FF5722)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
[![Resilience: Polly](https://img.shields.io/badge/Resilience-Polly_C%23_Integration-4CAF50)](https://github.com/App-vNext/Polly)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

---

## 🌟 Overview

This repository represents the production-ready AI assistant service built during **Week 6**. Building upon the manual 8-stage RAG pipeline from Week 5, this milestone transitions our system into an enterprise composable, streaming, and tool-augmented intelligence platform capable of dynamic runtime database inspections, multi-turn conversational context resolution, and high-throughput Server-Sent Events (SSE) token streaming.

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 LangChain LCEL Pipeline                │
                  │                                                        │
   User Query ──> │  Input Guard ──> MultiQuery Retriever ──> Context Doc  │
   + Session ID   │  (Runnable)            (ChromaDB)           Formatting │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │          LLM & Tool Calling Orchestrator               │
                  │                                                        │
                  │  ┌───────────────────────┐   ┌───────────────────────┐ │
                  │  │ Multi-Turn Memory     │   │ @tool Availability    │ │
                  │  │ (Session-keyed Store) │   │ (Dynamic DB Lookup)   │ │
                  │  └───────────────────────┘   └───────────────────────┘ │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │ SSE Streaming Response  │ ──> Live Tokens
                                 │   (/ask/stream endpoint)│
                                 └─────────────────────────┘
```

---

## 📂 Repository Structure

| Directory / File | Description |
| :--- | :--- |
| **`Week_06_PartA_LCEL/`** | Declarative LCEL RAG chain using `|`, `RunnablePassthrough`, and `RunnableLambda` input guards. |
| **`Week_06_PartB_AdvancedRetrieval/`** | Hierarchical document chunking with `RecursiveCharacterTextSplitter` and `MultiQueryRetriever`. |
| **`Week_06_PartC_StructuredMemory/`** | Multi-turn session memory with `RunnableWithMessageHistory` and Pydantic structured output validation. |
| **`Week_06_PartD_ToolCalling/`** | Autonomous tool binding (`@tool check_book_availability`) with schema execution against .NET API. |
| **`Week_06_PartE_ResilientNetAI/`** | .NET 8 C# resilient client featuring Polly exponential backoff, timeouts, and circuit breakers. |
| **`Week_06_PartF_Streaming/`** | Tri-layer Server-Sent Events (SSE) streaming blueprint across FastAPI, .NET proxy, and Angular. |
| **`Week_06_PartG_GitRebase/`** | Interactive git rebase practice, history hygiene, and safe remote synchronization guides. |
| **`Week_06_Final_Project/`** | Full-stack production application connecting Angular UI, .NET proxy, and FastAPI AI service. |

---

## 🚀 Quickstart & Execution

### 1. Configure Local Environment (`.env`)
Each subfolder includes its own isolated `.env` template configured for Google Gemini:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
```

### 2. Run Module Demos

#### Part A: LCEL Declarative Pipeline
```bash
python Week_06_PartA_LCEL/lcel_rag_demo.py
```

#### Part B: Multi-Query Advanced Retrieval
```bash
python Week_06_PartB_AdvancedRetrieval/advanced_retrieval_demo.py
```

#### Part C: Structured Memory & Session Store
```bash
python Week_06_PartC_StructuredMemory/structured_memory_demo.py
```

#### Part D: Dynamic Tool Calling
```bash
python Week_06_PartD_ToolCalling/tool_calling_demo.py
```

#### Project: Automated Verification Test Suite
```bash
python Week_06_Final_Project/test_week6_suite.py
```

#### Project: Interactive Terminal Streaming Chat
```bash
python Week_06_Final_Project/interactive_client.py
```

---

## ⚡ Key Architectural Capabilities

- **LCEL Pipe Composition:** Clean, modular chaining without procedural glue code using `RunnableSequence` (`|`).
- **Dynamic Tool Calling:** The AI autonomously queries the live PostgreSQL database via .NET `GET /api/books/{id}/availability` instead of hallucinating.
- **Stateful Memory Isolation:** Safe multi-turn dialogue with pronoun resolution keyed by unique `session_id`.
- **Live SSE Token Streaming:** Low time-to-first-token (TTFT) via unbuffered Server-Sent Events from FastAPI through .NET to Angular.
- **Enterprise Resilience:** Polly exponential backoff with circuit breaking for 503 fallback when downstream AI services degrade.

---

## 👤 Author

- **Name:** Muhammad Qasim  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)
