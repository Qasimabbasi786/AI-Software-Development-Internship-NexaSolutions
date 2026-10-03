# 🤖 Enterprise AI Assistant Microservice (LangChain LCEL, Tools & Streaming)

**Author:** Fawad  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 — LangChain & LCEL • Advanced Retrieval • Tool Calling • Polly Resilience • SSE Streaming  

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL_Pipelines-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Streaming: SSE](https://img.shields.io/badge/Streaming-Server--Sent_Events-FF5722)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
[![Resilience: Polly](https://img.shields.io/badge/Resilience-Polly_C%23_Integration-4CAF50)](https://github.com/App-vNext/Polly)

---

## 🌟 Overview

This repository represents the production-ready AI assistant service built during **Week 6**. It transitions basic RAG pipelines into a composable, streaming, and tool-augmented intelligence system capable of dynamic runtime database inspections, multi-turn conversational context resolution, and high-throughput token streaming.

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
| **`Week6_PartA_LangChainLCEL/`** | Declarative LCEL RAG chain using `|`, `RunnablePassthrough`, and `RunnableLambda` input guards. |
| **`Week6_PartB_AdvancedRetrieval/`** | Hierarchical document chunking and `MultiQueryRetriever` query reformulation. |
| **`Week6_PartC_StructuredMemory/`** | Multi-tenant session memory management and Pydantic structured output validation. |
| **`Week6_PartD_ToolCalling/`** | Autonomous tool binding (`@tool check_book_availability`) with schema execution. |
| **`Week6_PartE_ResilientNetAI/`** | .NET 8 C# client implementation featuring Polly jittered exponential backoff and circuit breakers. |
| **`Week6_PartF_Streaming/`** | Server-Sent Events (SSE) streaming protocols and token generator specifications. |
| **`Week6_PartG_GitRebase/`** | Git rebase documentation, linear commit history maintenance, and conflict resolution guides. |
| **`Week6_Project_FullAssistant/`** | End-to-end interactive CLI assistant and comprehensive verification test suite. |
| **`ai-service/`** | Production FastAPI backend microservice exposing `/ask`, `/ask/stream`, and `/classify-book`. |
| **`Week6_CheckStage_Answers.md`** | Comprehensive architectural and theoretical answers to all Week 6 assessment questions. |

---

## 🚀 Quickstart & Execution

### 1. Setup Virtual Environment
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the AI Microservice
```bash
cd ai-service
uvicorn main:app --reload --port 8000
```
- **Interactive Swagger Documentation:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

### 3. Run Module Demos

#### Part A: LCEL Declarative Pipeline
```bash
python Week6_PartA_LangChainLCEL/lcel_rag_demo.py
```

#### Part B: Multi-Query Advanced Retrieval
```bash
python Week6_PartB_AdvancedRetrieval/advanced_retrieval_demo.py
```

#### Part C: Structured Memory & Session Store
```bash
python Week6_PartC_StructuredMemory/structured_memory_demo.py
```

#### Part D: Dynamic Tool Calling
```bash
python Week6_PartD_ToolCalling/tool_calling_demo.py
```

#### Full Verification Test Suite
```bash
python Week6_Project_FullAssistant/test_week6_suite.py
```

#### Interactive Terminal Assistant
```bash
python Week6_Project_FullAssistant/interactive_client.py
```

---

## ⚡ Key Capabilities

- **LCEL Pipe Composition:** Clean, modular chaining without procedural glue code.
- **Dynamic Tool Calling:** The AI autonomously decides when to query live databases for book inventory rather than hallucinating.
- **Stateful Memory Isolation:** Safe multi-user multi-turn dialogue keyed by unique `session_id`.
- **Live SSE Token Streaming:** Near-instant time-to-first-token (TTFT) via Server-Sent Events.
- **Enterprise Resilience:** Polly exponential backoff with decorrelated jitter and circuit breaking for mission-critical reliability.

---

## 👤 Author

- **Name:** Fawad  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)
