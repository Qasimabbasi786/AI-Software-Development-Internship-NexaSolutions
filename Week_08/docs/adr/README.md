# Architecture Decision Records (ADRs)

This directory contains formal records of significant architectural choices made across the 8-week platform evolution and finalized during the **Week 8 Capstone**.

## Format
Each record follows the Michael Nygard Architecture Decision Record standard:
- **Title:** `ADR-00X: Short descriptive title`
- **Status:** Proposed / Accepted / Superseded / Deprecated
- **Context:** The engineering problem, system requirements, and constraints.
- **Decision Drivers:** The architectural and operational forces influencing the choice.
- **Options Considered:** Trade-offs of evaluated alternatives.
- **Decision:** The chosen path and the rationale behind it.
- **Consequences:** Positive benefits, negative trade-offs, and operational implications.
- **Counter-Argument & Reversal Criteria:** The strongest technical argument against this decision and the specific empirical evidence required to reverse it.

## Index of ADRs
- [`ADR-001-separate-fastapi-service.md`](./ADR-001-separate-fastapi-service.md) — Why a separate FastAPI + Python service instead of calling LLMs directly from ASP.NET Core.
- [`ADR-002-sqlite-checkpointer-vs-postgres.md`](./ADR-002-sqlite-checkpointer-vs-postgres.md) — Why SQLite checkpoint persistence was chosen now with PostgreSQL planned for cluster scale.
- [`ADR-003-chroma-vector-store-and-hitl-writes.md`](./ADR-003-chroma-vector-store-and-hitl-writes.md) — Why embedded ChromaDB for this scale and why Human-in-the-Loop approval is strictly required for write tools.
