# 📋 Week 8 Backlog Triage, Risk Matrix & Prioritization

**Milestone:** Week 8 — Part A Deliverable 1  
**Author:** Muhammad Qasim (Lead Systems Architect & DevOps Engineer)  
**Date:** 2026-10-18  
**Scope:** Week 7 Residual Risks, Red-Team Findings, Stretch Goals & Production Deficiencies  

---

## 🎯 Executive Overview

To transform the prototype built in Weeks 1–7 into an enterprise-ready system, every known deficiency, residual risk, evaluation limitation, and unfinished item was audited and scored. 

### Scoring Formula:
$$\text{Risk Score} = \text{Impact } (1–3) \times \text{Likelihood } (1–3)$$
- **Impact (1–3):** $1 = \text{Cosmetic / Minor UX}$, $2 = \text{Performance degradation / Non-critical failure}$, $3 = \text{Security breach / Data loss / System crash}$
- **Likelihood (1–3):** $1 = \text{Unlikely / Rare edge case}$, $2 = \text{Occasional / Probable under load}$, $3 = \text{Frequent / Default behavior}$
- **Effort Estimate:** **S** (Small: <2h), **M** (Medium: 2–6h), **L** (Large: >6h)

---

## 🚦 Triage Matrix & Item Status

### 🟢 SPRINT BACKLOG: Work Picked for Week 8 Capstone (To Do / In Progress)

| Issue ID | Category | Title & Scope | Impact (1–3) | Likelihood (1–3) | Risk Score | Effort | Status | Justification & Resolution Path |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **ISSUE-01** | `reliability` | **Missing Explicit Outbound Network Timeouts** | 3 | 3 | **9** | **S** | **In Progress** | Slow LLM responses or unresponsive internal services freeze thread pools. Implement explicit 10s timeout on all HTTP calls. |
| **ISSUE-02** | `performance` | **Redundant Catalog Embeddings on Every Re-index** | 2 | 3 | **6** | **M** | **To Do** | Full re-embeddings cost tokens and latency on startup. Implement SHA-256 incremental content hashing (`sync_index`). |
| **ISSUE-03** | `performance` | **Uncached Repeated Read Queries Inflate Latency/Cost** | 2 | 3 | **6** | **M** | **To Do** | Frequent catalog search queries repeatedly invoke LLM. Implement thread-safe TTL catalog answer cache with version invalidation. |
| **ISSUE-04** | `security` | **Unbounded Daily User Token Consumption** | 3 | 2 | **6** | **M** | **To Do** | Abusive or compromised accounts can exhaust API quotas. Enforce per-user daily token budgets in .NET (`DailyTokenBudget = 25k`). |
| **ISSUE-05** | `reliability` | **Lack of End-to-End Distributed Request Tracing** | 2 | 3 | **6** | **S** | **In Progress** | Debugging errors across Angular, .NET, and FastAPI is impossible without a unified key. Add `X-Correlation-Id` middleware. |
| **ISSUE-06** | `reliability` | **Indistinguishable Liveness vs. Readiness Probes** | 3 | 2 | **6** | **S** | **To Do** | Orchestrators cannot differentiate whether container is booting vs. database is down. Implement `/health/live` and `/health/ready`. |
| **ISSUE-07** | `security` | **Overly Permissive CORS and Missing Security Headers** | 3 | 2 | **6** | **S** | **To Do** | Browser clients can be subject to CSRF or cross-origin exploitation. Lock down CORS strictly to Angular origin; add HSTS & headers. |
| **ISSUE-08** | `security` | **Missing Brute-Force Rate Limiting on Login** | 3 | 2 | **6** | **S** | **To Do** | Credential stuffing attacks could compromise user accounts. Implement IP/account rate limiting and temporary lockout in ASP.NET Core. |
| **ISSUE-09** | `security` | **Absence of User Data Deletion Endpoint (GDPR/Privacy)** | 3 | 2 | **6** | **M** | **To Do** | Personal data in SQL and SQLite checkpoints violates privacy compliance. Implement `DELETE /api/me/data` wiping threads and records. |
| **ISSUE-10** | `packaging` | **Non-Containerized Multi-Service Deployment Friction** | 3 | 3 | **9** | **L** | **To Do** | "Works on my machine" prevents clean stakeholder verification. Package all 4 services via multi-stage Dockerfiles & Docker Compose. |
| **ISSUE-11** | `evaluation` | **Limited 10-Scenario Evaluation Suite** | 2 | 3 | **6** | **M** | **To Do** | 10 scenarios do not cover extreme edge cases (5000-char queries, multilingual, empty catalog). Expand to 20 scenarios run 3x. |

---

### 🟡 DEFERRED BACKLOG: Items Consciously Deferred with Written Justification

| Issue ID | Category | Title & Scope | Impact (1–3) | Likelihood (1–3) | Risk Score | Effort | Status | One-Line Reason for Deferral |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **DEF-01** | `tech-debt` | **Migrate SQLite Checkpoints to PostgreSQL Cluster** | 2 | 1 | **2** | **L** | **Deferred** | Single-node Docker Compose for capstone evaluation has sufficient capacity with WAL mode; Postgres adds heavy container overhead. |
| **DEF-02** | `tech-debt` | **Replace ChromaDB with Distributed Qdrant/Milvus** | 2 | 1 | **2** | **L** | **Deferred** | Catalog scale (<500 books) is optimally handled by embedded ChromaDB; distributed vector cluster is premature optimization. |
| **DEF-03** | `security` | **Hardware Token MFA / FIDO2 WebAuthn for Login** | 2 | 1 | **2** | **L** | **Deferred** | High implementation complexity; JWT expiry and password lockout provide sufficient security baseline for capstone. |
| **DEF-04** | `stretch` | **Multi-Model Dynamic Fallback Routing (Claude/Ollama)** | 2 | 2 | **4** | **L** | **Deferred** | Cloud LLM latency/cost SLAs are stable; primary focus is single-provider hardening and prompt optimization before multi-model failover. |
| **DEF-05** | `stretch` | **Automated Multi-User Document Upload & PDF Ingestion** | 1 | 2 | **2** | **L** | **Deferred** | Catalog ingestion is managed via administrator API; document parsing is an extension project (Part I Roadmap). |

---

## 📌 Defense of Prioritization

1. **Why ISSUE-01 (Timeouts) and ISSUE-10 (Docker Packaging) are ranked at top priority (Risk 9):**
   - In distributed systems, missing timeouts are fatal: a single slow response locks worker threads, propagating failure across all layers until the whole system crashes. 
   - Docker packaging is the ultimate test of software delivery; without container reproducibility, no evaluator or mentor can verify the project independently.
2. **Why DEF-01 (PostgreSQL Checkpoints) was deferred:**
   - Although SQLite has known concurrency limits, enabling WAL mode (`PRAGMA journal_mode=WAL`) provides concurrent reader support and sub-millisecond writes for the single-node capstone demo. Introducing a dedicated PostgreSQL container would inflate memory consumption without providing observable functional benefits to the demo day evaluation.
