# Week 6 Project — Library AI Assistant (Fully Wired)

## 🌟 Overview & System Architecture
This project connects the entire full-stack system into a production-grade, resilient, multi-turn AI assistant with live token streaming and dynamic database tool calling across:
1. **Angular Client (:4200):** Modern conversational chat drawer with token-by-token live rendering.
2. **ASP.NET Core Web API Gateway (:5000):** Resilient Polly proxy enforcing security and unbuffered streaming.
3. **FastAPI AI Microservice (:8000):** LangChain LCEL RAG pipeline powered by Google Gemini, ChromaDB vector search, session memory, and tool calling.

---

## 🌊 Complete Tri-Layer Data Flow

```
[ Angular Chat UI (:4200) ]
       │  1. Native fetch() -> POST /api/assistant/ask/stream (Bearer JWT)
       ▼
[ .NET 8 Web API Gateway (:5000) ]
       │  2. Resilient Polly Proxy -> POST /ask/stream (Unbuffered)
       ▼
[ FastAPI AI Microservice (:8000) ]
       │  3. LangChain LCEL Pipeline:
       │     • RunnableLambda (Input Guard >= 3 chars)
       │     • Session Memory (InMemoryChatMessageHistory)
       │     • @tool check_book_availability (Dynamic PostgreSQL lookup)
       │     • RecursiveCharacterTextSplitter & MultiQueryRetriever
       ▼
[ Google Gemini LLM Token Generator ]
       │  4. Server-Sent Events (SSE): data: <chunk>\n\n
       ▼
[ .NET Response.Body.FlushAsync() ]
       │  5. Immediate TCP Socket Flush Forwarding
       ▼
[ Angular Chat UI ] ──> Token-by-token real-time live render!
```

---

## 🛠️ Key Architectural Components

### 1. Angular Chat UI (`frontend/`)
- **Native `fetch` with `ReadableStream`:** Standard `HttpClient` buffers whole HTTP payloads; native `fetch()` combined with `response.body.getReader()` progressively decodes SSE text chunks as they arrive.
- **Dynamic Floating Drawer:** Responsive chat window with typing indicator, message history, session reset, and stream cancellation via `AbortController`.

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

- **In-Memory Session Persistence:** Conversation history is stored in-process via `InMemoryChatMessageHistory` (`session_store: Dict[str, BaseChatMessageHistory]`). If the FastAPI service restarts or scales across multiple load-balanced instances, active conversation context will not persist across nodes. In production (Week 7+), this should be backed by Redis or PostgreSQL session stores.

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
