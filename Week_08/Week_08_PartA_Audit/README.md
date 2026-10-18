# 🔍 Part A: System Audit, Backlog Triage & Architecture Decisions

**Milestone:** Week 8 — Capstone Deliverable 1  
**Status:** Completed ✅  
**Author:** Muhammad Qasim (Senior Systems Architect & DevOps Engineer)  

[![Status: Completed](https://img.shields.io/badge/Part_A-Completed_%E2%9C%85-success)](https://github.com/)
[![ADRs](https://img.shields.io/badge/ADRs-3_Accepted-blue)](../docs/adr/)
[![Risk Triage](https://img.shields.io/badge/Backlog_Triaged-16_Items-orange)](./backlog-triage-risk-matrix.md)
[![Pre-Mortem](https://img.shields.io/badge/Pre--Mortem-5_Scenarios-red)](../docs/pre-mortem.md)

---

## 🎯 Executive Summary & Objectives

Strong engineers do not fix everything blindly; they decide what matters by evaluating the whole system honestly. In Part A, we conducted a rigorous architectural audit of the entire AI-powered library system developed across Weeks 1–7.

### Primary Objectives:
- **Target Architecture Definition:** Map the complete end-to-end topology (`Angular → .NET API → FastAPI + LangGraph → RAG & Tools → SQL Server / Chroma / SQLite / External LLM`) and establish trust boundaries at every hop.
- **Backlog Triage & Risk Scoring:** Consolidate Week 7 residual risks, red-team findings, and unfinished stretch goals into a prioritized backlog scored by $\text{Impact} \times \text{Likelihood} = \text{Risk}$, estimating effort ($S/M/L$).
- **Architecture Decision Records (ADRs):** Record defensible architectural decisions using the Nygard format, including explicit counter-arguments and reversal conditions.
- **Pre-Mortem Failure Analysis:** Anticipate production failure modes 6 months post-deployment and formulate proactive engineering controls.

---

## 📦 Deliverables & Documentation Index

| Deliverable | Location | Description & Focus |
| :--- | :--- | :--- |
| **Backlog Triage & Risk Matrix** | [`backlog-triage-risk-matrix.md`](./backlog-triage-risk-matrix.md) | 16 audited items scored by risk ($1–9$) and effort ($S/M/L$); 11 sprint items picked vs. 5 deferred with written justifications. |
| **Target Architecture & Trust Boundaries** | [`../README.md#system-architecture--trust-boundaries`](../README.md) | Comprehensive Mermaid diagram and 6-row trust boundary matrix defining protocols and auth mechanisms. |
| **ADR-001: Separate FastAPI Service** | [`../docs/adr/ADR-001-separate-fastapi-service.md`](../docs/adr/ADR-001-separate-fastapi-service.md) | Why a dedicated Python FastAPI service is used instead of in-process .NET LLM orchestration. |
| **ADR-002: SQLite Checkpoints vs. Postgres** | [`../docs/adr/ADR-002-sqlite-checkpointer-vs-postgres.md`](../docs/adr/ADR-002-sqlite-checkpointer-vs-postgres.md) | Why embedded SQLite with WAL mode is used for capstone and criteria for PostgreSQL migration. |
| **ADR-003: ChromaDB & Mandatory HITL Writes** | [`../docs/adr/ADR-003-chroma-vector-store-and-hitl-writes.md`](../docs/adr/ADR-003-chroma-vector-store-and-hitl-writes.md) | Why embedded ChromaDB fits catalog scale and why human approval (`interrupt()`) is mandatory for write tools. |
| **Production Pre-Mortem** | [`../docs/pre-mortem.md`](../docs/pre-mortem.md) | 5 realistic production disaster scenarios evaluated with likelihood, impact, and preventive controls. |

---

## 🚦 Backlog Triage Summary

```
Total Audited Items: 16
├── 🟢 Sprint Backlog (Picked for Week 8): 11 Items
│   ├── ISSUE-01 (Risk 9): Outbound Network Timeouts & Resiliency
│   ├── ISSUE-02 (Risk 6): Incremental Vector Indexing (SHA-256 Hashes)
│   ├── ISSUE-03 (Risk 6): TTL & Versioned Catalog Answer Cache
│   ├── ISSUE-04 (Risk 6): User Daily Token Budget Quotas (25k)
│   ├── ISSUE-05 (Risk 6): Distributed Correlation ID Tracing
│   ├── ISSUE-06 (Risk 6): Differentiated Liveness & Readiness Probes
│   ├── ISSUE-07 (Risk 6): Strict Origin CORS & Security Headers
│   ├── ISSUE-08 (Risk 6): Brute-Force Rate Limiting on Login
│   ├── ISSUE-09 (Risk 6): GDPR DELETE /api/me/data Endpoint
│   ├── ISSUE-10 (Risk 9): 4-Tier Docker Compose Packaging
│   └── ISSUE-11 (Risk 6): 20-Scenario x 3 Evaluation Suite
└── 🟡 Consciously Deferred Backlog: 5 Items
    ├── DEF-01 (Risk 2): PostgreSQL Checkpoint Cluster (Single-node capstone does not need multi-master clustering)
    ├── DEF-02 (Risk 2): Distributed Qdrant/Milvus Vector Store (Corpus < 500 books optimally handled by Chroma)
    ├── DEF-03 (Risk 2): Hardware FIDO2/WebAuthn MFA (JWT expiry and account lockout provide sufficient baseline)
    ├── DEF-04 (Risk 4): Multi-Model Dynamic Fallback (Single-provider optimization prioritized before multi-vendor routing)
    └── DEF-05 (Risk 2): Automated PDF File Ingestion (Deferred to Post-Internship Extension Roadmap)
```

---

## 🛡️ Trust Boundaries & Architecture Overview

The system architecture enforces strict trust boundaries at every communication interface:

```
[ Browser / Angular SPA (Untrusted Edge) ]
               │
               ▼  (Hop 1: HTTPS / Strict CORS / Bearer JWT / X-Correlation-Id)
┌────────────────────────────────────────────────────────┐
│ Trust Boundary 1: API Gateway (ASP.NET Core 8 Web API) │
│ - Token Budgeting, Login Rate Limiting, Health Probes  │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
               │ (EF Core / TDS)          │ (Hop 2: HTTP / Internal Docker Network)
               ▼                          │ (X-Service-Key + Forwarded User JWT Context)
    [( SQL Server 2022 )]                 ▼
                       ┌────────────────────────────────────────────────────────┐
                       │ Trust Boundary 2: AI Orchestrator (FastAPI + LangGraph)│
                       │ - Service-Key Auth, Safe Caching, Non-Root Linux User  │
                       └──────────────┬──────────────────────────┬──────────────┘
                                      │                          │
                                      ▼                          ▼
                          [( Chroma Vector Store )]   [( SQLite Checkpoints )]
                                      │
                                      ▼  (Hop 3: HTTPS Outbound / 10s Hard Timeout)
                       ┌────────────────────────────────────────────────────────┐
                       │ Trust Boundary 3: External LLM Cloud (Gemini / OpenAI) │
                       └────────────────────────────────────────────────────────┘
```

---

## 🔮 Pre-Mortem High-Priority Hazards & Controls

| Failure Scenario | Risk Score | Pre-Emptive Control Implemented |
| :--- | :---: | :--- |
| **LLM Provider Outage / 429 Throttle Freezes Threads** | **9 (High)** | 10s hard client timeout + circuit breaker fast-failing with polite retry message. |
| **Indirect Prompt Injection in Catalog Ingestion** | **6 (Medium)** | `<untrusted_document>` boundary tags + Mandatory HITL approval gate (`interrupt()`). |
| **SQLite Checkpoint Lock Contention Under Load** | **6 (Medium)** | `PRAGMA journal_mode=WAL;` and busy timeout (5000ms); ADR-002 scaling bridge. |
| **Shared Answer Cache Leaks Personal User Data** | **6 (Medium)** | Route-level cache segregation (`route == "catalog"` only; write tools never cached). |
| **Circular Startup Deadlock in Multi-Container Setup** | **6 (Medium)** | Asynchronous lazy index syncing with exponential backoff; decoupled liveness vs. readiness. |

---

## 🧪 Verification & Acceptance Criteria

- [x] **Backlog Triage Matrix Complete:** All Week 7 residual risks, red-team issues, and evaluation gaps scored with impact, likelihood, and effort in [`backlog-triage-risk-matrix.md`](./backlog-triage-risk-matrix.md).
- [x] **Architecture Diagram & Boundaries:** Complete Mermaid diagram and 6-row authentication matrix documented in [`../README.md`](../README.md).
- [x] **3 Formal ADRs Authored:** Nygard format records written in [`../docs/adr/`](../docs/adr/) with counter-arguments and reversal criteria.
- [x] **Pre-Mortem Analysis Authored:** 5 realistic production disaster scenarios evaluated with preventive controls in [`../docs/pre-mortem.md`](../docs/pre-mortem.md).
- [x] **Git Checkpoint Committed:** Cleanly staged and committed with message `docs: add architecture diagram, ADRs and pre-mortem for Week 8 Part A` (`451b578`).
