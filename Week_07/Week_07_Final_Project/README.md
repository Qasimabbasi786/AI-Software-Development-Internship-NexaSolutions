# 🏛️ Library AI Assistant (LangChain LCEL, Resilient .NET Proxy & Angular Streaming)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 6 Final Project — Production Multi-Tier Streaming Architecture  

[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![.NET: 8.0](https://img.shields.io/badge/.NET-8.0_Web_API-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![Angular: 18](https://img.shields.io/badge/Angular-18_Standalone-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-FF6F00?logo=chroma&logoColor=white)](https://www.trychroma.com/)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 📌 Executive Summary
The **Week 6 Final Project** connects the entire internship full-stack architecture into a unified, production-grade **Library AI Assistant**. Building upon the RAG foundation of Week 5, this capstone delivers real-time token-by-token streaming from Google Gemini, routed through a secured ASP.NET Core gateway proxy with Polly resilience, and rendered into a modern Angular chat drawer.

---

## 🏗️ Complete Multi-Tier Data Flow Architecture

```
┌────────────────────────────────────────────────────────────────┐
│               Layer 3: Angular Frontend Client (:4200)         │
│  - chat-assistant.component: Floating reactive drawer          │
│  - chat.service.ts: Native fetch() with ReadableStream reader  │
│  - Decodes SSE stream chunks ("data: ...\n\n")                 │
│  - Live progressive token UI rendering with typing cursor      │
└───────────────────────────────┬────────────────────────────────┘
                                │ HTTP POST /api/assistant/ask/stream (JWT Bearer)
                                ▼
┌────────────────────────────────────────────────────────────────┐
│             Layer 2: ASP.NET Core 8 Web API Gateway (:5000)    │
│  - AssistantController.cs: Validates JWT perimeter claims      │
│  - Sets Response.ContentType = "text/event-stream"             │
│  - SendAsync(..., HttpCompletionOption.ResponseHeadersRead)    │
│  - CRITICAL: await Response.Body.FlushAsync() avoids buffering │
│  - Polly Policies: 3x Exponential Retry & Circuit Breaker (503)│
└───────────────────────────────┬────────────────────────────────┘
                                │ HTTP POST /ask/stream (Internal Network)
                                ▼
┌────────────────────────────────────────────────────────────────┐
│            Layer 1: FastAPI AI Microservice (:8000)            │
│  - main.py: LangChain LCEL Declarative Pipeline (|)            │
│  - RunnableLambda: Input guard (< 3 chars -> HTTP 400)         │
│  - MultiQueryRetriever: Generates query variations on ChromaDB │
│  - Session-Scoped Memory: RunnableWithMessageHistory           │
│  - @tool check_book_availability: Dynamic availability lookup  │
│  - StreamingResponse: Emits data: {chunk}\n\n + data: [DONE]   │
└───────────────────────────────┬────────────────────────────────┘
                                │ Asynchronous Generator (astream)
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                   Google Gemini AI Model Engine                │
│  - Models: gemini-3.5-flash-lite / models/gemini-embedding-001 │
│  - Temperature: 0.0 for deterministic factual grounding        │
└────────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Subdirectories

| Directory | Role | Technologies |
| :--- | :--- | :--- |
| **`ai-services/`** | Production AI microservice with LCEL RAG, memory, and SSE streaming. | FastAPI, LangChain, Google Gemini, ChromaDB |
| **`backend/`** | Core library API, JWT authentication, and resilient streaming proxy. | ASP.NET Core 8, EF Core, Polly, Npgsql |
| **`frontend/`** | Client web application with real-time streaming chat drawer. | Angular 18, TypeScript, Native Fetch / SSE |

---

## 🛠️ Key Architectural Components

### 1. Angular Chat UI (`frontend/`)
- **Native `fetch` with `ReadableStream`:** Angular's standard `HttpClient` buffers whole HTTP payloads; native `fetch()` combined with `response.body.getReader()` progressively decodes SSE text chunks as they arrive.
- **Dynamic Floating Drawer:** Responsive chat window with animated cursor, message history, session reset, and stream cancellation via `AbortController`.

### 2. ASP.NET Core Streaming Proxy (`backend/`)
- **`HttpCompletionOption.ResponseHeadersRead`:** Unblocks .NET from waiting for the downstream stream to complete before writing headers to the browser.
- **`await Response.Body.FlushAsync()`:** Essential to defeat internal Kestrel and TCP socket buffering, ensuring tokens are pushed over the wire immediately.
- **Polly Resilience Policies:**
  - **Retry Policy:** 3 retries with exponential backoff (`2^attempt` seconds).
  - **Timeout Policy:** 10-second per-request ceiling.
  - **Circuit Breaker:** Opens after 3 consecutive failures for 30 seconds, returning a clean `503 Service Unavailable` JSON response.

### 3. FastAPI & LangChain AI Engine (`ai-services/`)
- **LCEL Composition:** Composed using `RunnableSequence` and `|` pipe syntax.
- **Boundary Splitting:** `RecursiveCharacterTextSplitter` chunking library knowledge on semantic boundaries.
- **Multi-Query Retrieval:** Reformulates user questions to overcome vocabulary mismatch against ChromaDB embeddings.
- **Dynamic Tool Calling:** Bound `@tool check_book_availability` querying `GET /api/books/{id}/availability`.
- **Session-Scoped Memory:** `RunnableWithMessageHistory` maintaining conversation context per `session_id`.

---

## ⚠️ Known Architectural Limitations

- **In-Memory Session Persistence:** Conversation history is stored in-process via `InMemoryChatMessageHistory` (`session_store: Dict[str, BaseChatMessageHistory]`). If the FastAPI service restarts or scales across multiple load-balanced instances, active conversation context will not persist across nodes. In production (Week 7+), this will be backed by Redis or PostgreSQL persistence stores.

---

## 🧪 Verification & Execution

### 1. Run Comprehensive Automated Test Suite
```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" test_week6_suite.py
```
**Tests Verified:**
- Input Guard (< 3 characters rejected with HTTP 400).
- Multi-turn session memory & pronoun resolution (*"Tell me about Dune"* $\rightarrow$ *"What genre is it?"*).
- Dynamic tool calling (`check_book_availability`).
- Out-of-catalog refusal grounding (*"What is the recipe for chocolate lava cake?"*).
- End-to-end SSE live chunk streaming.

### 2. Interactive Terminal Streaming Chat
```powershell
& "D:\Software\PythonEnvironments\AI_env\Scripts\python.exe" interactive_client.py
```
