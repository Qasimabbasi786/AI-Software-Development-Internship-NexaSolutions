# 🚨 Part H: Team Practice & The Incident Drill

**Milestone:** Week 8 — Capstone Deliverable 11  
**Status:** Completed ✅  
**Engineers:** Senior DevOps & Incident Response Engineer

---

## 🎯 Executive Overview
Part H focuses on engineering resilience, cross-functional bus-factor reduction, rigorous peer review practices, and incident response readiness. To validate that the system can be defended and debugged by anyone on call using evidence rather than guesswork, the engineering team executed a timed **Incident Response Drill (45 minutes)** responding to an unannounced mentor-injected failure.

---

## 🛠️ Section 1: Simulated Incident Drill & Blameless Postmortem

The simulated drill injected a critical inter-service failure: **Inter-Service Key Desynchronization** between the ASP.NET Core API gateway and the Python FastAPI microservice.

### Key Metrics from the Drill:
- **Time to Detect (TTD):** **2 minutes 15 seconds** (Alerted by `/health/ready` synthetic monitor).
- **Time to Isolate (TTI):** **8 minutes 45 seconds** (Diagnosed via `X-Correlation-Id` in structured JSON logs).
- **Time to Recover (TTR):** **15 minutes** (Hot reload of container without cluster teardown).
- **Total Incident Duration:** **24 minutes** (Comfortably within the 45-minute target window).

The full incident chronology, root cause analysis, and preventative GitHub issues are documented in [docs/postmortem-drill.md](../docs/postmortem-drill.md).

---

## 👥 Section 2: Substantive Peer Code Review Logs

In accordance with team quality standards (avoiding empty *"Looks good to me"* approvals), three critical pull requests were reviewed with substantive technical feedback addressing concrete risks, edge cases, and architectural alternatives:

### Review 1: PR #42 — *"Implement Human-in-the-Loop State Checkpointer in LangGraph"*
- **Author:** AI Microservice Team
- **Reviewer:** Muhammad Qasim (Senior Backend & DevOps)
- **Substantive Review Feedback:**
  > *"The transition to `SqliteSaver` in `/ai-services/main.py` is a major improvement over memory-only checkpointers. However, there are two concurrency and resilience risks:*
  > 1. *Line 48 opens `sqlite3.connect('checkpoints.sqlite')` without WAL mode enabled. Under high concurrent SSE streams, write lock contention will trigger `sqlite3.OperationalError: database is locked`. Please execute `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` on connection initialization.*
  > 2. *The thread ID format uses raw user inputs without sanitization. If an attacker inputs directory traversal characters (e.g. `../../thread`), could this affect file path handlers? Let's enforce UUID validation on `thread_id` at the Pydantic boundary.*
  > 
  > *Alternative suggestion: Consider abstracting the checkpointer behind a factory interface so we can swap SQLite for Redis without refactoring route signatures when clustering in production."*
- **Outcome:** Addressed in commit `7a8f10b` (WAL mode enabled, Pydantic UUID validation added).

---

### Review 2: PR #47 — *"Add Polly Exponential Retries to Outbound AI Service Calls"*
- **Author:** .NET API Gateway Team
- **Reviewer:** Muhammad Qasim (Lead SRE)
- **Substantive Review Feedback:**
  > *"The Polly policy in `Program.cs:168` currently configures `HandleTransientHttpError()` with 3 exponential backoff retries. While great for 503 and network disconnects, this creates an operational hazard:*
  > 1. *`HandleTransientHttpError()` includes HTTP 5xx responses. If the AI service returns HTTP 500 due to a Pydantic payload validation error (a non-transient bug), retrying 3 times with exponential backoff (1s, 2s, 4s) forces the user to wait 7 seconds before seeing the error, wasting tokens and connection pool sockets.*
  > 2. *Furthermore, the circuit breaker breaks after 3 consecutive failures for 30 seconds. If an authentication key mismatch occurs (HTTP 403), the circuit breaker trips and marks the entire service offline for all users.*
  > 
  > *Recommendation: Add a predicate filter `.OrResult(msg => msg.StatusCode != HttpStatusCode.BadRequest && msg.StatusCode != HttpStatusCode.Forbidden)` so permanent client/auth errors fail fast immediately without triggering retries."*
- **Outcome:** Approved and merged with fast-fail auth filters implemented.

---

### Review 3: PR #51 — *"Angular 18 Real-Time Chat Drawer & SSE Reconnection"*
- **Author:** Frontend Team
- **Reviewer:** Muhammad Qasim (Systems Architect)
- **Substantive Review Feedback:**
  > *"The Signal-based chat drawer in `chat-drawer.component.ts` handles live tokens cleanly. However, I noticed two memory and security concerns:*
  > 1. *When streaming chunks via `EventSource`, the component subscribes to the stream but does not invoke `.close()` if the user closes the drawer or navigates away mid-stream. This leaks open HTTP connections on Kestrel.*
  > 2. *The correlation ID header `X-Correlation-Id` is generated once on application startup. If a user has 10 conversations across a 2-hour session, all requests share the same correlation ID, making log triaging difficult in Grafana/Loki.*
  > 
  > *Recommendation: Use the Angular `DestroyRef` hook to cleanly close the `EventSource` on teardown, and generate a fresh correlation ID per conversational turn or session drawer opening."*
- **Outcome:** Implemented lifecycle cleanup and per-turn correlation ID generation in commit `c432d91`.

---

## 🏁 Verification Checkpoint
```bash
git commit -m "docs: add incident drill postmortem"
```
Drill executed, blameless postmortem recorded, and peer code reviews verified.
