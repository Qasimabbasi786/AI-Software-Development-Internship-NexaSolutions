# Incident Postmortem: Inter-Service Key Desynchronization (INC-20261023-01)

**Incident Date:** 2026-10-23  
**Incident Duration:** 24 minutes (Detection to Full Recovery)  
**Severity:** SEV-1 (Critical Feature Outage — AI Assistant and Autonomous Agent Runs Unavailable)  
**Lead Incident Commander:** Muhammad Qasim (Senior DevOps & SRE)  
**Scribe & Communications:** Nexa Solutions QA Team  
**Status:** Resolved & Closed  

---

## 1. Executive Summary

On 2026-10-23 between 14:02 UTC and 14:26 UTC, the Nexa Solutions Library System experienced a partial service outage affecting the AI assistant and book reservation workflows. While the catalog browsing and user authentication services remained operational, 100% of natural language assistant inquiries and agent runs failed with HTTP 500 errors and timeout notices.

The incident was secretly introduced as a blind engineering drill to test on-call diagnostic capabilities under pressure. The on-call engineering team successfully isolated the fault within 11 minutes by following the distributed correlation ID trace (`X-Correlation-Id`), identified an inter-service authentication mismatch (`X-Service-Key`), remediated the configuration drift, and restored full service health within 24 minutes without restarting unaffected database or web containers.

---

## 2. User & Business Impact

| Metric | Measured Impact |
| :--- | :--- |
| **User Experience** | Users clicking the "Ask AI Assistant" drawer received immediate error toasts: *"Assistant temporarily unavailable. Please retry shortly."* |
| **Request Failure Rate** | 100% of requests to `POST /api/agent/run` and `POST /ask/stream` failed (142 failed requests recorded during the drill window). |
| **Unaffected Systems** | PostgreSQL relational database, Angular SPA browsing, book catalog search, and standard JWT user login remained 100% healthy. |
| **Data Integrity Impact** | **Zero data corruption or loss.** Zero unapproved writes or half-committed reservation records occurred. |

---

## 3. Incident Timeline (UTC)

| Timestamp | Elapsed | Phase | Action / Event Description |
| :--- | :--- | :--- | :--- |
| **14:02:00** | +00m | **Fault Injection** | Mentor introduced failure: modified `SERVICE_KEY` environment variable inside `.NET API` to `sec-auth-token-bad-key-mismatch`, creating a key discrepancy with `FastAPI`. |
| **14:04:15** | +02m | **Detection** | Synthetic health check monitor reported readiness probe failure: `GET http://localhost:5000/health/ready` returned HTTP 503 `Unhealthy` with sub-check `ai-service: Degraded`. |
| **14:06:30** | +04m | **Alert & Escalation** | Automated alert fired on `#alerts-production` Slack channel. On-call incident response drill initiated. |
| **14:08:45** | +06m | **Triage & Log Inspection** | Engineer queried API logs with correlation ID: `docker compose logs api --tail=50`. Found Polly Circuit Breaker tripping due to repeated HTTP 403 Forbidden responses from `http://ai-service:8000/agent/run`. |
| **14:13:20** | +11m | **Root Cause Isolated** | Inspected AI service logs: `docker compose logs ai-service`. Confirmed log entry: `{"level": "WARNING", "message": "Forbidden: Invalid or missing X-Service-Key"}`. Discovered that .NET was forwarding a stale/mismatched key. |
| **14:17:00** | +15m | **Fix Applied** | Realigned `.env` configuration; synchronized `SERVICE_KEY` across `.NET` and `FastAPI` service blocks in `docker-compose.yml`. |
| **14:20:10** | +18m | **Container Reload** | Executed targeted hot reload without cluster teardown: `docker compose up -d --no-deps api`. |
| **14:23:45** | +21m | **Verification** | Verified `GET http://localhost:5000/health/ready` returned HTTP 200 OK. Executed synthetic agent query; verified SSE tokens streamed cleanly. |
| **14:26:00** | +24m | **All Clear** | Incident Commander declared incident resolved. Normal operations resumed. |

---

## 4. Root Cause & Contributing Factors

### 4.1 Proximate Root Cause
The ASP.NET Core API failed to authenticate against the FastAPI AI microservice because the pre-shared secret header (`X-Service-Key`) dispatched by .NET did not match the expected `SERVICE_KEY` enforced by FastAPI's endpoint security dependency. FastAPI rejected all inbound proxy requests with HTTP 403 Forbidden.

### 4.2 Contributing & Compounding Architectural Factors
1. **Polly Circuit Breaker Tripping:** When .NET received 3 consecutive HTTP 403 Forbidden responses from FastAPI, the Polly Circuit Breaker transitioned to `Open` state for 30 seconds. While designed to protect downstream servers from cascading traffic, it caused immediate fast-failing of all subsequent user queries.
2. **Generic User-Facing Error Messages:** The Angular client received HTTP 500 from .NET and displayed a generic toast rather than an informative status message indicating a downstream authentication handshake error.
3. **Configuration Drift Risk:** `SERVICE_KEY` was declared in multiple container definition blocks rather than referencing a single centralized variable anchor in `.env`.

---

## 5. What Went Well vs. What Went Poorly

### What Went Well:
- **Correlation ID Tracking:** The presence of `X-Correlation-Id` across both .NET and FastAPI log streams enabled the on-call engineer to pinpoint the exact 403 Forbidden response within 5 minutes without guessing.
- **Granular Health Checks:** The `/health/ready` probe immediately isolated the fault to the `ai-service` dependency while confirming the PostgreSQL relational database remained fully healthy.
- **Zero Lateral Impact:** Database tables, user sessions, and persistent vector store files were completely unaffected throughout the outage.

### What Went Poorly:
- **Circuit Breaker Masked Underlying Code:** The Polly circuit breaker reported `BrokenCircuitException` in the higher-level logs, which initially looked like a network connectivity drop rather than an HTTP 403 authentication error until the engineer filtered deeper into the innermost exception.
- **Dual Secret Source of Truth:** Having two separate environment keys in local development created an easy opportunity for configuration divergence.

---

## 6. Corrective Actions & Preventative GitHub Issues

| Issue ID | Action Item Description | Type | Owner | Target Date |
| :--- | :--- | :--- | :--- | :--- |
| **#108** | **Centralize Docker Compose Environment Anchors:** Refactor `docker-compose.yml` to utilize YAML extension fields (`&common-env`) to guarantee single-source environment keys. | Architecture | DevOps | 2026-10-25 |
| **#109** | **Distinguish 403 vs 500 in Circuit Breaker Policy:** Modify Polly `HandleTransientHttpError` to exclude HTTP 401/403 (unauthorized/forbidden) so permanent configuration errors don't trip transient circuit breakers. | Reliability | .NET Lead | 2026-10-26 |
| **#110** | **Add Inter-Service Auth Diagnostic Probe:** Update `/health/ready` in .NET API to explicitly test the `X-Service-Key` handshake on startup and emit a warning log on key mismatch. | Observability | AI Lead | 2026-10-27 |
| **#111** | **Improve Client Error Categorization:** Update Angular HTTP interceptor to display actionable toast notifications when downstream microservices report auth or maintenance states. | Frontend | UI Lead | 2026-10-28 |
