# Architecture Decision Records (ADRs)

This directory contains records of significant architectural choices made across the 8-week system evolution and finalized during the Week 8 Capstone.

## Format
Each record follows the standard Michael Nygard ADR format:
- **Title:** `ADR-00X: Short descriptive title`
- **Status:** Proposed / Accepted / Superseded / Deprecated
- **Context:** The engineering problem, system requirements, and constraints.
- **Options Considered:** Trade-offs of evaluated alternatives.
- **Decision:** The chosen path and the rationale behind it.
- **Consequences:** Positive benefits, negative trade-offs, and operational implications.

## Index of ADRs
- [`ADR-001-separate-fastapi-service.md`](./ADR-001-separate-fastapi-service.md) — Why a separate FastAPI + Python service instead of calling LLMs directly from ASP.NET Core.
- [`ADR-002-sqlite-checkpointer-vs-postgres.md`](./ADR-002-sqlite-checkpointer-vs-postgres.md) — Why SQLite checkpoint persistence was chosen now with PostgreSQL planned for cluster scale.
- [`ADR-003-human-in-the-loop-for-writes.md`](./ADR-003-human-in-the-loop-for-writes.md) — Why mandatory interactive approval gates (`interrupt()`) are enforced on write tools.
- [`ADR-004-database-migrations-in-containers.md`](./ADR-004-database-migrations-in-containers.md) — Startup automated migrations vs. dedicated migration jobs in containerized deployments.
