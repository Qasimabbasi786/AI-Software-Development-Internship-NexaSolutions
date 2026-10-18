# 🛡️ Part C: Reliability, Observability & Fault Tolerance

**Milestone:** Week 8 — Capstone Deliverable 4 & 5  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Establish distributed request tracing using `X-Correlation-Id` originating at Angular or API edge and propagating through every hop to FastAPI and database calls.
- Enforce structured JSON logging across all services capturing correlation ID, user ID, route, step count, token consumption, latency, and status outcome.
- Implement differentiated `/health/live` (process alive) and `/health/ready` (dependencies like SQL Server and FastAPI/Chroma healthy) endpoints in .NET and FastAPI.
- Configure explicit timeouts on every outbound network call (FastAPI HTTP client, database connection, LLM inference calls) to prevent thread pool exhaustion.
- Conduct a formal Failure-Injection Matrix, deliberately injecting 6 severe production faults and validating graceful handling.

---

## 📦 Key Deliverables
1. **Correlation Middleware:** .NET correlation middleware + FastAPI correlation middleware ensuring header continuity.
2. **Health Check Probes:** ASP.NET Core Health Check extensions and FastAPI `/health` endpoint verifying vector store connectivity.
3. **End-to-End Trace Example:** Verified trace log demonstrating unified correlation ID across all 3 tiers in [`/docs/week8-trace-example.md`](../docs/week8-trace-example.md).
4. **Failure Injection Test Suite:** Completed failure matrix covering stopped SQL, stopped FastAPI, artificial latency, invalid LLM keys, simulated HTTP 429, and empty vector store.

---

## 🧪 Verification & Acceptance Criteria
- [ ] Single correlation ID appears in Angular console, .NET logs, and FastAPI logs for the same transaction.
- [ ] Readiness check fails immediately if SQL Server or AI service is unresponsive, while liveness remains green.
- [ ] Outbound network calls fail fast at their timeout without freezing the Angular UI.
