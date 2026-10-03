# Week 6 — Part F: End-to-End Streaming (FastAPI $\rightarrow$ .NET Proxy $\rightarrow$ Angular Client)

## 📌 Executive Summary
In production AI applications, waiting 5 to 12 seconds for an entire response to generate before rendering anything creates an unresponsive, sluggish user experience. **End-to-End Streaming** delivers tokens live to the UI as they are synthesized by the model, slashing **Time-to-First-Token (TTFT)** down to $< 500\text{ms}$.

This document details the complete tri-layer streaming blueprint implemented across:
1. **Python FastAPI**: Exposing Server-Sent Events (SSE) via `StreamingResponse` backed by LangChain / Google Gemini asynchronous generator streams (`astream`).
2. **ASP.NET Core Web API**: Acting as a secure gateway proxy that validates JWTs, opens an unbuffered upstream channel via `HttpCompletionOption.ResponseHeadersRead`, and flushes byte chunks immediately with `FlushAsync()`.
3. **Angular Frontend**: Consuming continuous byte streams via native `fetch()` and `ReadableStream` (`response.body!.getReader()`), updating the chat UI token by token.

---

## 🏗️ Tri-Layer Architecture & Hop-by-Hop Data Flow

```
                      ┌────────────────────────────────────────────────────────┐
                      │             Layer 3: Angular Frontend Client           │
                      │                                                        │
                      │   chat.service.ts:                                     │
                      │   - Initiates POST /api/assistant/ask/stream           │
                      │   - Attaches JWT Authorization header                  │
                      │   - Consumes response.body!.getReader()                │
                      │   - TextDecoder splits "data: {token}\n\n"             │
                      │   - Renders live token increments into Chat UI         │
                      └───────────────────────────┬────────────────────────────┘
                                                  │ HTTP POST (SSE Accept)
                                                  ▼
                      ┌────────────────────────────────────────────────────────┐
                      │              Layer 2: ASP.NET Core Web API             │
                      │                                                        │
                      │   AssistantController.cs:                              │
                      │   - Authenticates user claims                          │
                      │   - Sets Response.ContentType = "text/event-stream"    │
                      │   - SendAsync(..., ResponseHeadersRead)                │
                      │   - StreamReader loop forwards lines to Response.Body  │
                      │   - CRITICAL: await Response.Body.FlushAsync()         │
                      │   - Listens to HttpContext.RequestAborted cancellation │
                      └───────────────────────────┬────────────────────────────┘
                                                  │ HTTP POST (Internal Network)
                                                  ▼
                      ┌────────────────────────────────────────────────────────┐
                      │             Layer 1: FastAPI AI Microservice           │
                      │                                                        │
                      │   main.py:                                             │
                      │   - POST /ask/stream                                   │
                      │   - Retrieves relevant context docs from ChromaDB      │
                      │   - Asynchronously invokes Gemini (chain.astream)      │
                      │   - Yields: "data: {chunk}\n\n"                        │
                      │   - Concludes: "data: [DONE]\n\n"                      │
                      │   - StreamingResponse(media_type="text/event-stream")  │
                      └────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Server-Sent Events (SSE) Protocol
Server keeps the HTTP connection open with `media_type="text/event-stream"` and sends incremental chunks formatted as `data: <content>\n\n`, ending with `data: [DONE]\n\n`.

### 2. .NET Gateway Proxy & Immediate Socket Flush
Standard web servers buffer output. In `AssistantController.cs`:
- `HttpCompletionOption.ResponseHeadersRead` returns control before the whole response is read.
- `await Response.Body.FlushAsync()` forces immediate transmission over the TCP socket without buffering.

### 3. Angular Native Fetch & ReadableStream
Angular's `HttpClient` expects single, completed responses. To consume progressive SSE chunks, `chat.service.ts` uses the browser's native `fetch` API and `response.body!.getReader()`.

---

## 🛠️ Verification & Blueprint Testing
- **FastAPI Endpoint:** `POST /ask/stream`
- **.NET Proxy Endpoint:** `POST /api/assistant/ask/stream`
- **Verification Client:** `python Week_06_Final_Project/interactive_client.py`
