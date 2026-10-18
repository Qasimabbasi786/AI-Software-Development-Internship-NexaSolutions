# Architecture Decision Record

## ADR-002: SQLite Checkpointer Now vs. Relational / Postgres Scaling Later

- **Status:** Accepted
- **Deciders:** Muhammad Qasim (Lead Architect), Engineering Team
- **Date:** 2026-10-18
- **Scope:** Agent State Persistence & Checkpoint Store

---

### Context & Problem Statement
LangGraph autonomous agents require durable state persistence across turn executions, process restarts, and interactive human-in-the-loop pauses. When an agent requests user approval for a write tool (`reserve_book`), the execution halts via `interrupt()`, serializing the entire conversation state, pending tool calls, and execution counters into a checkpointer keyed by `thread_id`.

We needed to decide how and where to store these state checkpoints during Week 8 capstone and establish clear migration criteria for enterprise production scale.

### Decision Drivers
- **Operational Simplicity for Single-Node / Compose Deployment:** The capstone must clone, build, and run with a single `docker compose up` command on any reviewer's machine without managing multiple complex relational database clusters.
- **Embedded Performance:** SQLite (`SqliteSaver`) requires zero network roundtrips for checkpoint serialization and deserialization, offering sub-millisecond writes directly to a mounted volume.
- **State Isolation:** Agent graph execution state contains semi-structured message payloads, tool call identifiers, and LangGraph-internal metadata that does not require relational foreign key joins with core transactional library tables.

---

### Considered Options
1. **Option 1: Memory Saver (`MemorySaver`)**
   - *Pros:* Zero disk footprint; instantaneous reads/writes.
   - *Cons:* Complete state loss upon container restart; impossible to resume human approval flows across deployments or multi-process workers. Unacceptable for production.
2. **Option 2: Embedded SQLite Checkpointer (`SqliteSaver`) (Chosen for Capstone)**
   - *Pros:* Durable persistence across container restarts using a mounted Docker volume (`aidata:/data`); zero operational setup or database migration overhead; embedded file I/O with ACID transactions.
   - *Cons:* File-level locking limits concurrent write scalability; single point of failure; does not support horizontal scaling across multiple container replicas without shared distributed network storage (NFS/EFS).
3. **Option 3: External PostgreSQL / SQL Server Checkpointer (`PostgresSaver`)**
   - *Pros:* Fully concurrent; supports horizontally scaled, multi-replica AI service clusters; unified enterprise backup and failover.
   - *Cons:* Adds heavy dependency overhead and schema migration requirements to the capstone environment; introduces network latency to every graph step state transition.

---

### Decision Outcome
**Chosen Option:** **Option 2 (Embedded SQLite Checkpointer via `SqliteSaver` mounted on a persistent Docker volume)** for the capstone deployment, with an explicit architectural bridge to **Option 3 (PostgreSQL)** for horizontal clustering.

All checkpoint data is stored at `/data/checkpoints/agent_checkpoints.sqlite`, which maps to the persistent named volume `aidata`. This guarantees that if the AI container restarts or crashes during a human approval wait, the user's thread state and pending action card resume seamlessly.

#### Consequences
- **Positive:**
  - Zero external service configuration required for running the agent state machine.
  - Sub-millisecond state reads and writes without saturating SQL Server connection pools.
  - Easy offline inspection using standard SQLite tooling (`sqlite3`).
- **Negative / Trade-offs:**
  - The AI service cannot be scaled horizontally beyond 1 replica without SQLite database lock contention (`database is locked` error under concurrent multi-process writes).
  - Checkpoint cleanup requires scheduled vacuuming or explicit GDPR deletion routines (`DELETE /api/me/data`).

---

### Strongest Counter-Argument & Conditions for Reversal
> **Strongest Counter-Argument:**
> Because the application already deploys Microsoft SQL Server for entity persistence, introducing SQLite creates a two-database architecture with split persistence. State and business data live in different engines, complicating disaster recovery, consistent point-in-time restores, and unified auditing. Furthermore, any horizontal scaling test will immediately fail due to SQLite's single-writer limitation.

> **Evidence That Would Reverse This Decision:**
> 1. Concurrency requirements exceed 50 simultaneous agent writes per second, triggering SQLite `busy_timeout` exceptions.
> 2. Infrastructure requirements mandate deploying multiple stateless AI service replicas behind a load balancer (Kubernetes Deployment with HPA > 1).
> 3. Enterprise audit compliance requires checkpointer tables to reside within the primary encrypted SQL Server / PostgreSQL enterprise cluster.
