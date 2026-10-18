# 🛡️ Part C: Reliability, Observability & Fault Tolerance

**Milestone:** Week 8 — Capstone Deliverables 4 & 5  
**Status:** Completed ✅  
**Author:** Muhammad Qasim (Senior Reliability & Observability Engineer)  

[![Status: Completed](https://img.shields.io/badge/Part_C-Completed_%E2%9C%85-success)](https://github.com/)
[![Correlation ID](https://img.shields.io/badge/Tracing-X--Correlation--Id-blue)](../docs/week8-trace-example.md)
[![Health Probes](https://img.shields.io/badge/HealthChecks-/live_%26_/ready-brightgreen)](../backend/Program.cs)
[![Timeouts](https://img.shields.io/badge/Timeouts-Everywhere_Guaranteed-orange)](./README.md#explicit-outbound-network-timeouts)
[![Failure Matrix](https://img.shields.io/badge/Failure_Injection-6_Scenarios_Tested-success)](./README.md#challenge--failure-injection-matrix-required)

---

## 🎯 Executive Summary & Objectives

When an issue occurs at 2:00 a.m. in production, structured logs, correlation IDs, and differentiated health checks are all an on-call engineer has. 

### Core Accomplishments:
1. **Unified Correlation ID (`X-Correlation-Id`):** Created at the edge (Angular HTTP interceptor), propagated through ASP.NET Core middleware into logging scopes, and forwarded downstream to FastAPI via `X-Correlation-Id` headers.
2. **Structured JSON Logging:** Implemented structured logging capturing `CorrelationId`, `UserId`, `ThreadId`, `Steps`, `Tokens`, `LatencyMs`, and `Outcome`. Zero secrets, JWTs, or PII are logged.
3. **Differentiated Liveness vs. Readiness:**
   - `/health/live`: Probes process health only (returns 200 OK if Kestrel is running).
   - `/health/ready`: Probes all critical dependencies (relational database connection + AI service reachability).
   - FastAPI `/health`: Checks Chroma vector store collection accessibility and document count.
4. **Timeouts Everywhere:** Hard timeouts configured on every network boundary (database, FastAPI proxy, and LLM calls).
5. **Failure-Injection Matrix:** Deliberately injected 6 production failures and validated resilience.

---

## 📦 Deliverables & File Index

| Deliverable | Location | Description & Focus |
| :--- | :--- | :--- |
| **.NET Correlation & Health Checks** | [`../backend/Program.cs`](../backend/Program.cs) | Correlation ID middleware, `DatabaseHealthCheck`, `AiServiceHealthCheck`, `/health/live`, `/health/ready`. |
| **FastAPI Correlation & Vector Health** | [`../ai-services/main.py`](../ai-services/main.py) | `CorrelationIdFilter`, FastAPI correlation middleware, and vector store reachability in `/health`. |
| **Angular Correlation Interceptor** | [`../frontend/src/app/auth.interceptor.ts`](../frontend/src/app/auth.interceptor.ts) | Generates and forwards `X-Correlation-Id` on all outbound browser requests. |
| **End-to-End Trace Example** | [`../docs/week8-trace-example.md`](../docs/week8-trace-example.md) | Full real-world multi-tier trace demonstrating unified request lineage across all 3 tiers. |
| **Failure-Injection Report** | [`./README.md#challenge--failure-injection-matrix-required`](./README.md) | Completed 6-scenario failure injection matrix with expected, observed, and remediation actions. |

---

## ⏱️ Explicit Outbound Network Timeouts

Every network dependency is bounded by an explicit timeout to prevent thread exhaustion:

| Outbound Network Hop | Source Container | Destination Service | Configured Timeout | Implementation / Mechanism |
| :--- | :--- | :--- | :---: | :--- |
| **Database Query** | `api` (.NET) | Relational Database | **5.0 s** | Npgsql command timeout / EF Core `CommandTimeout(5)` |
| **AI Service Proxy** | `api` (.NET) | `ai-service` (FastAPI) | **10.0 s** | `HttpClient.Timeout = TimeSpan.FromSeconds(10)` with Polly circuit breaker |
| **Health Check Probe** | `api` (.NET) | `ai-service` (`/health`) | **2.0 s** | `CancellationTokenSource.CancelAfter(TimeSpan.FromSeconds(2.0))` |
| **LLM Inference Call** | `ai-service` (Python) | Google Gemini / OpenAI | **10.0 s** | Model factory client timeout (`timeout=10.0`) |
| **Tool Execution Callback** | `ai-service` (Python) | `api` (.NET) | **3.0 s** | `httpx.Client(timeout=3.0)` in `agent_tools.py` |

---

## 💥 Challenge — Failure Injection Matrix (Required)

All 6 required production failures were deliberately injected and verified:

| Injected Failure | Expected Behavior | Observed Behavior | Fix / Remediation Applied |
| :--- | :--- | :--- | :--- |
| **1. Stop Relational Database** | Clear error logged; readiness check fails (`/health/ready` returns 503); liveness (`/health/live`) stays 200; no crash loop. | Readiness probe failed after 2s; API remained running without crashing container. | Implemented custom `DatabaseHealthCheck` returning `Unhealthy` while keeping process alive. |
| **2. Stop FastAPI** | Polly circuit breaker opens after 3 consecutive failures; returns 503 with clear user message; UI shows retry prompt. | Circuit breaker broke after 3 attempts, returned 503 Service Unavailable instantly without thread starvation. | Added Polly Circuit Breaker policy with 30s break duration in `Program.cs`. |
| **3. Add 10s Delay in AI Service** | Outbound HTTP timeout fires at 10s; client receives timeout error; Angular UI remains responsive and unfrozen. | .NET HttpClient threw `TaskCanceledException` at exactly 10s; SSE emitted retryable error event. | Enforced 10-second `HttpClient.Timeout` and async cancellation token propagation. |
| **4. Invalid LLM API Key** | Model initialization throws clean authentication error; API key is scrubbed and never leaked to logs or UI. | Error caught by guardrail node; generic error message emitted to user; logs contained 0 key fragments. | Sanitized error handlers in `main.py` stripping sensitive substrings matching `AIza...` / `sk-...`. |
| **5. Simulate Provider 429 Throttle** | Exponential backoff honors `Retry-After` header; if exhausted, displays informative user message rather than failing silently. | Caught 429; retried with exponential delay ($2^n$ backoff); returned graceful "AI provider busy" notification. | Added retry backoff in Polly HTTP pipeline and typed retry handler in LangGraph `route_after_tools`. |
| **6. Corrupt / Empty Vector Store** | RAG retriever handles zero matching chunks gracefully; assistant admits lack of information without hallucinations. | Model returned: *"I don't have that information in my library catalog."* Zero hallucinated books. | Updated RAG prompt with strict grounding rules: lack of context forces explicit admission of missing data. |

---

## 🧪 Verification & Acceptance Criteria

- [x] **Unified Correlation ID:** `X-Correlation-Id` appears in Angular HTTP inspector, .NET Kestrel console, and FastAPI JSON logs for every transaction.
- [x] **Readiness vs. Liveness Verified:** Stopping database marks `/health/ready` unhealthy (503) while `/health/live` remains healthy (200).
- [x] **FastAPI Vector Check:** Calling `GET /health` reports `vector_store_reachable: true` and indexed document counts.
- [x] **Structured Run Summary:** Single summary line logged per run containing correlation ID, user ID, steps, tokens, and latency.
- [x] **All Timeouts Configured:** Hard timeouts documented and active across all outbound network hops.
