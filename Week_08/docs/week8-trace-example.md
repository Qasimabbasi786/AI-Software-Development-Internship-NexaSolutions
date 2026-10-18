# 🔍 End-to-End Distributed Trace Example

**Milestone:** Week 8 — Part C Deliverable  
**Author:** Muhammad Qasim (Senior Reliability & Observability Engineer)  
**Date:** 2026-10-18  
**Scope:** Distributed request trace spanning Angular Client → ASP.NET Core 8 Web API → FastAPI + LangGraph AI Service  

---

## 🎯 Trace Overview & Architecture

To achieve unified observability across microservices without guesswork, every transaction carries an edge-generated correlation ID passed via the HTTP header:
```
X-Correlation-Id: cid_w8_capstone_7f9b821a4e0c
```

This trace follows a real user interaction where an authenticated student requests book details and reserves a catalog title:
1. **Hop 1 (Angular SPA):** `auth.interceptor.ts` generates `X-Correlation-Id` and attaches JWT Bearer token.
2. **Hop 2 (.NET Web API):** Correlation middleware captures the header, attaches it to ASP.NET Core `ILogger` scope, inspects rate limits and daily token quotas, and proxies the SSE stream to FastAPI.
3. **Hop 3 (FastAPI AI Engine):** Correlation ID middleware injects the ID into Python `contextvars`, records structured JSON events, executes LangGraph state transitions, checks the safe answer cache, and streams typed SSE chunks back.
4. **Hop 4 (.NET Web API):** Emits structured run summary line with latency, token counts, and completion status.

---

## 📜 End-to-End Correlated Log Stream

```log
========================================================================================================================
HOP 1: ANGULAR 18 SPA (Browser Client Console)
Time: 2026-10-18T20:15:02.104Z
========================================================================================================================
[HttpClient] Outgoing request: POST https://localhost:5000/api/assistant/agent/runs
[HttpClient] Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  X-Correlation-Id: cid_w8_capstone_7f9b821a4e0c
  Content-Type: application/json
[ChatService] Starting SSE stream listener for threadId: thread_9a8f21b4

========================================================================================================================
HOP 2: ASP.NET CORE 8 WEB API (Kestrel Server Logs)
Time: 2026-10-18T20:15:02.115Z
========================================================================================================================
info: Microsoft.AspNetCore.Hosting.Diagnostics[1]
      Request starting HTTP/1.1 POST http://localhost:5000/api/assistant/agent/runs - application/json 78
info: libraryAPI.Program[0]
      [CorrelationScope: cid_w8_capstone_7f9b821a4e0c] Correlation ID attached to request context and response headers.
info: libraryAPI.Controllers.AssistantController[0]
      [CorrelationScope: cid_w8_capstone_7f9b821a4e0c] User student_demo (ID: u_441) verified. Daily tokens used: 1,420 / 25,000. Budget OK.
info: libraryAPI.Controllers.AssistantController[0]
      [CorrelationScope: cid_w8_capstone_7f9b821a4e0c] Active thread thread_9a8f21b4 ownership validated. Forwarding stream to FastAPI http://localhost:8000/agent/run...

========================================================================================================================
HOP 3: FASTAPI + LANGGRAPH AI SERVICE (Python Structured JSON Logs)
Time: 2026-10-18T20:15:02.126Z
========================================================================================================================
{"timestamp": "2026-10-18 20:15:02,128", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "Inbound request: POST /agent/run from host 127.0.0.1"}
{"timestamp": "2026-10-18 20:15:02,135", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "[CACHE_CHECK] Query 'Tell me about Dune' missed answer cache. Executing LangGraph agent turn."}
{"timestamp": "2026-10-18 20:15:02,142", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "[ROUTER_NODE] Model 'gemini-1.5-flash' classified query as route='catalog' (latency=185ms)."}
{"timestamp": "2026-10-18 20:15:02,340", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "[RAG_SUBGRAPH] Retrieved 2 chunks from Chroma collection 'library_docs' (distance < 0.28)."}
{"timestamp": "2026-10-18 20:15:02,895", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "[CACHE_SET] Response cached safely under key '1:tell me about dune' (TTL=300s)."}
{"timestamp": "2026-10-18 20:15:02,905", "level": "INFO", "correlation_id": "cid_w8_capstone_7f9b821a4e0c", "logger": "ai_service", "message": "[AGENT_RUN_FINISHED] correlation_id=cid_w8_capstone_7f9b821a4e0c user_id=u_441 thread_id=thread_9a8f21b4 route=catalog outcome=Completed"}

========================================================================================================================
HOP 4: ASP.NET CORE 8 WEB API (Structured Summary Completion Log)
Time: 2026-10-18T20:15:02.918Z
========================================================================================================================
info: libraryAPI.Controllers.AssistantController[0]
      [CorrelationScope: cid_w8_capstone_7f9b821a4e0c] [AGENT_RUN_SUMMARY] CorrelationId: cid_w8_capstone_7f9b821a4e0c | UserId: u_441 | ThreadId: thread_9a8f21b4 | Steps: 2 | Tokens: 350 | LatencyMs: 803 | Outcome: Completed
info: Microsoft.AspNetCore.Hosting.Diagnostics[2]
      Request finished HTTP/1.1 POST http://localhost:5000/api/assistant/agent/runs - 200 - text/event-stream 812.4ms

========================================================================================================================
HOP 5: ANGULAR 18 SPA (Stream Completion)
Time: 2026-10-18T20:15:02.924Z
========================================================================================================================
[ChatService] SSE stream completed. Final event received:
{
  "event": "final",
  "answer": "Dune is a seminal science fiction novel by Frank Herbert set on the desert planet Arrakis...",
  "sources": ["Dune", "Library Catalog"],
  "tokens": 350,
  "cached": false
}
```

---

## 🔍 Observability Takeaways

1. **Deterministic Request Stitching:** A single search query for `cid_w8_capstone_7f9b821a4e0c` retrieves the entire transaction lineage across client, API gateway, and Python AI containers.
2. **Zero Leaked Secrets in Structured Logs:** Neither user JWTs, database connection strings, nor model provider API keys appear anywhere in the logs. Only non-sensitive operational telemetry (`user_id`, `tokens`, `steps`, `latency_ms`, `outcome`) is preserved.
3. **Troubleshooting Velocity:** When an issue arises in production, support engineers can request the user's `X-Correlation-Id` from their HTTP response headers to identify the exact failing hop within seconds.
