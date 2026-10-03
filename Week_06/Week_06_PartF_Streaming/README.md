# Week 6 — Part F: End-to-End Streaming (FastAPI $\rightarrow$ .NET Proxy $\rightarrow$ Angular Client)

## 🌟 Executive Architectural Blueprint
In production AI applications, waiting 5 to 12 seconds for an entire response to generate before rendering anything creates an unresponsive, sluggish user experience. **End-to-End Streaming** delivers tokens live to the UI as they are synthesized by the model, slashing **Time-to-First-Token (TTFT)** down to $< 500\text{ms}$.

This document details the complete tri-layer streaming blueprint implemented across:
1. **Python FastAPI**: Exposing Server-Sent Events (SSE) via `StreamingResponse` backed by LangChain / Google Gemini asynchronous generator streams (`astream`).
2. **ASP.NET Core Web API**: Acting as a secure gateway proxy that validates JWTs, opens an unbuffered upstream channel via `HttpCompletionOption.ResponseHeadersRead`, and flushes byte chunks immediately with `FlushAsync()`.
3. **Angular Frontend**: Consuming continuous byte streams via native `fetch()` and `ReadableStream` (`response.body!.getReader()`), updating the chat UI token by token.

---

## 🌊 Tri-Layer Architecture & Hop-by-Hop Data Flow

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

## 💻 Layer-by-Layer Technical Blueprint

### Layer 1: FastAPI SSE Streaming (`main.py`)
FastAPI implements an asynchronous generator yielding standard Server-Sent Event formatted chunks (`data: <content>\n\n`):

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

@app.post("/ask/stream")
async def ask_stream(req: AskRequest):
    # 1. Retrieve catalog context docs from vector store
    context_text = retrieve_context(req.question)

    # 2. Async event generator yielding SSE tokens
    async def event_generator():
        # Async stream tokens directly from LangChain / Google Gemini
        async for chunk in rag_chain.astream({"context": context_text, "question": req.question}):
            token_text = chunk if isinstance(chunk, str) else getattr(chunk, "content", "")
            if token_text:
                yield f"data: {token_text}\n\n"
        
        # End-of-Stream Sentinel Marker
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no" # Prevents NGINX reverse-proxy buffering
        }
    )
```

---

### Layer 2: ASP.NET Core Secure Proxy (`AssistantController.cs`)
The .NET API must act as a streaming proxy rather than a direct passthrough URL because the browser must never directly access the AI microservice (the AI service has no authentication and is kept inside the private internal network).

```csharp
[HttpPost("ask/stream")]
[Authorize] // Enforce JWT Bearer Authentication at the perimeter
public async Task AskStream([FromBody] AskDto dto, CancellationToken clientDisconnectToken)
{
    Response.ContentType = "text/event-stream";
    Response.Headers["Cache-Control"] = "no-cache";
    Response.Headers["X-Accel-Buffering"] = "no";

    var upstreamRequest = new HttpRequestMessage(HttpMethod.Post, "/ask/stream")
    {
        Content = JsonContent.Create(new { question = dto.Question, sessionId = dto.SessionId })
    };

    // CRITICAL 1: ResponseHeadersRead prevents buffering the entire body before returning
    using var upstreamResponse = await _httpClient.SendAsync(
        upstreamRequest, 
        HttpCompletionOption.ResponseHeadersRead, 
        clientDisconnectToken
    );

    upstreamResponse.EnsureSuccessStatusCode();

    await using var upstreamStream = await upstreamResponse.Content.ReadAsStreamAsync(clientDisconnectToken);
    using var reader = new StreamReader(upstreamStream);

    while (!reader.EndOfStream && !clientDisconnectToken.IsCancellationRequested)
    {
        var line = await reader.ReadLineAsync(clientDisconnectToken);
        if (string.IsNullOrEmpty(line)) continue;

        // Forward SSE chunk onward to client
        await Response.WriteAsync(line + "\n\n", clientDisconnectToken);

        // CRITICAL 2: Body.FlushAsync() forces the socket buffer to transmit immediately
        await Response.Body.FlushAsync(clientDisconnectToken);
    }
}
```

---

### Layer 3: Angular Streaming Client (`chat.service.ts`)
Angular's standard `HttpClient` expects discrete, monolithic responses and cannot process progressive chunk emissions. Instead, the browser's native `fetch` and `ReadableStream` APIs are used:

```typescript
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { AuthService } from '../auth.service';

@Injectable({ providedIn: 'root' })
export class ChatService {
  constructor(private auth: AuthService) {}

  async askStream(
    question: string,
    onChunk: (token: string) => void,
    abortSignal?: AbortSignal
  ): Promise<void> {
    const response = await fetch(`${environment.apiUrl}/api/assistant/ask/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.auth.getToken()}`
      },
      body: JSON.stringify({ question }),
      signal: abortSignal
    });

    if (!response.ok || !response.body) {
      throw new Error(`Streaming failed with status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunkText = decoder.decode(value, { stream: true });
      const lines = chunkText.split('\n\n');

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6);
        if (data === '[DONE]') return;
        onChunk(data); // Append incremental token to the UI
      }
    }
  }
}
```

---

## 🔬 Critical Challenge Questions & Deep-Dive Analysis

### 1. What happens if `await Response.Body.FlushAsync()` is removed in the .NET proxy?
- **The Failure Mode:** Web servers (Kestrel and IIS) and TCP sockets buffer outbound writes into default packet frames (typically 4KB to 16KB) to maximize network throughput and minimize syscall overhead.
- **The Consequence:** If `FlushAsync()` is omitted, the .NET proxy buffers each small token internally until the entire AI response is finished or the buffer fills up. The browser client receives *nothing* for 8 seconds, and then the entire response dumps onto the screen in one single frame, completely destroying live streaming. Calling `FlushAsync()` explicitly commands the operating system to flush the socket buffer immediately over the TCP wire.

### 2. Why must .NET proxy the stream instead of Angular calling FastAPI directly?
1. **Security & Perimeter Defense:** The AI service resides on an internal virtual network (`localhost:8000` / private subnet) and has no public ingress. Angular already authenticates via JWT Bearer tokens against the .NET API.
2. **Audit Logging & Rate Limiting:** The .NET gateway logs caller identity, tracks user quotas, prevents denial-of-service abuse, and enforces user authorization.
3. **CORS & Domain Protection:** Passing through .NET prevents multi-domain CORS complications and keeps internal microservice topologies concealed from browser inspectors.

### 3. Handling User Navigation Cancellation Mid-Stream
- If a user navigates away or closes the browser tab while the model is halfway through a 1,000-token response, the connection is abandoned.
- By binding `CancellationToken clientDisconnectToken` from `HttpContext.RequestAborted` into `_httpClient.SendAsync` and `ReadLineAsync`, .NET detects the client socket severance immediately, cancels the upstream HTTP connection to FastAPI, and halts the Gemini API call, preventing wasted billing credits and leaked socket handles.

---

## 🎯 Summary
This tri-layer streaming blueprint establishes the technical foundation for the **Week 6 Final Project**, ensuring resilient, high-speed, and secure token delivery across FastAPI, ASP.NET Core, and Angular.
