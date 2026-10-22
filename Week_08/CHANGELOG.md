# Changelog

All notable changes to the **Nexa Solutions Library System** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-23

### 🚀 Production Milestone Release (Week 8 Capstone)
This is the inaugural production release of the containerized, multi-agent AI Library Management System, culminating 8 weeks of architecture, implementation, hardening, observability, and evaluation.

### Added
- **Multi-Container Orchestration (`docker-compose.yml`):**
  - Fully containerized topology comprising PostgreSQL 16 Alpine (`db`), FastAPI AI Agent (`ai-service`), ASP.NET Core 8 Web API (`api`), and Angular 18 Nginx SPA (`web`).
  - Declarative readiness healthchecks (`depends_on: condition: service_healthy`) eliminating race conditions and deadlocks.
  - Persistent named volumes (`sqldata`, `aidata`) preserving database state, vector store embeddings, and LangGraph SQLite conversation checkpoints across container teardown.
- **Automated Database Seeding (`DatabaseSeeder.cs`):**
  - Instant initialization creating preconfigured `admin` and `demo_user` accounts.
  - 16 diverse catalog books across 6 technical and literary categories, linked to 10 renowned authors.
- **Performance & Caching Tier (Week 8 Part B):**
  - Content-hash incremental vector indexing avoiding unnecessary re-embedding of unchanged books.
  - Safe in-memory read-only catalog answer cache (`TTLCache`) returning instant responses with 0 token consumption for verified non-sensitive catalog questions.
  - Dynamic routing with lightweight router models (`gemini-1.5-flash`) and per-user daily token budgets (25,000 tokens/day).
- **Enterprise Reliability & Observability (Week 8 Part C):**
  - End-to-end distributed correlation tracking via `X-Correlation-Id` across Angular, .NET middleware, and FastAPI.
  - Polly HTTP resilience policies featuring exponential backoff retries and 3-strike circuit breaker on outbound AI calls.
  - Granular `/health/live` and `/health/ready` diagnostic probes reporting relational database and Chroma vector store reachability.
- **Security Hardening & Privacy (Week 8 Part D):**
  - Strict transport security headers (HSTS, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`).
  - Role-based authorization policies and IP/user rate limiting (5 login attempts/min, 15 agent runs/min).
  - GDPR-compliant data erasure endpoint (`DELETE /api/users/{id}/data`) purging relational history, preferences, and LangGraph SQLite checkpoints simultaneously.
- **Expanded Quality Gate (Week 8 Part F):**
  - 20-scenario automated evaluation harness running 3 iterations per scenario (60 total trials) covering happy paths, adversarial prompt injections, foreign language queries, and boundary conditions.
  - Pre-defined, signed-off release criteria distinguishing hard blockers from soft statistical quality metrics.

### Changed
- Refactored .NET backend startup to gate database migrations and seeding behind `RUN_MIGRATIONS=true`.
- Decoupled API and AI service bootstrapping to break circular dependency cycles (ADR-004).
- Hardened CORS policy to strictly whitelist authorized origins (`http://localhost:4200`).

### Security
- Verified zero secrets in repository history via deep `gitleaks` inspection.
- Fixed or mitigated all transitive package vulnerabilities across .NET (`dotnet list package --vulnerable`), Python (`pip-audit`), and Node (`npm audit`).
- Enforced non-root user execution across all application containers (`USER $APP_UID` in .NET, `USER app` in Python).

---

## [0.7.0] - 2026-10-16
### Week 7: Autonomous Multi-Agent Workflows & HITL
- Introduced LangGraph state machine with human-in-the-loop (HITL) approval cards for book reservation writes.
- Implemented untrusted document wrappers and boundary validation guardrails.
- Added session-scoped SQLite checkpointer for multi-turn state persistence.

## [0.6.0] - 2026-10-09
### Week 6: LCEL RAG Assistant & Streaming
- Implemented LangChain LCEL pipeline with `RecursiveCharacterTextSplitter` and `MultiQueryRetriever`.
- Built Server-Sent Events (SSE) live token streaming endpoint (`/ask/stream`).
- Integrated Chroma vector database for library knowledge retrieval.

## [0.5.0] - 2026-10-02
### Week 5: Angular Modern Frontend
- Developed reactive Angular 18 client with Signals, standalone components, and Tailwind styling.
- Created interactive catalog browser, reservation drawer, and real-time streaming chat drawer.

## [0.4.0] - 2026-09-25
### Week 4: ASP.NET Core Backend Web API
- Established clean architecture with Repository pattern, EF Core, and PostgreSQL persistence.
- Added JWT Bearer authentication and Swagger/OpenAPI documentation.
