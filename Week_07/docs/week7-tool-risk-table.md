# Week 7 Tool Risk & Classification Table

This document establishes the risk taxonomy, execution safety constraints, idempotency enforcement, and human approval gates across all tools available to the assistant.

---

## Tool Classification Matrix

| Tool Name | Type (Read/Write) | Side Effects | Needs Approval? | Idempotent? | Retryable? | Primary Defense & Justification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `search_catalog` | **Read** | None | No | Yes | Yes (on network timeout) | Pure retrieval. Does not alter system state or leak private user data. |
| `check_availability` | **Read** | None | No | Yes | Yes (on network timeout) | Verifies book inventory count. Safe for unbounded calls. |
| `list_my_reservations` | **Read** | None | No | Yes | Yes (on network timeout) | Scoped strictly to current user's JWT identity. Cannot access other users' reservations. |
| `reserve_book` | **Write** | Modifies DB, creates reservation | **YES** | Yes (via `Idempotency-Key`) | Only on transient 5xx/timeout (Never on 409/401/403/404) | High risk. Modifies inventory and commits user records. Pauses for human confirmation via `interrupt()`. |
| `cancel_reservation` | **Write** | Modifies DB, releases reservation | **YES** | Yes (via `Idempotency-Key`) | Only on transient 5xx/timeout (Never on 404/403) | Irreversible side-effect without user confirmation. Requires HITL approval. |

---

## Security Justification for Non-Approved Tools
- `search_catalog` and `check_availability` are classified as read-only. Leaving them without human approval is safe because:
  1. They have no write side-effects on persistent storage.
  2. The database operations execute with read-only query semantics.
  3. No financial or inventory commitments occur.

---

## Why JWT Must Never Live in Graph State
- LangGraph checkpointers (such as `SqliteSaver`) serialize and store graph state directly onto disk or database tables for every step.
- If an authorization token (JWT) is stored in the state, it becomes permanently recorded in checkpoint databases, log files, and trace history.
- **Solution**: Pass the JWT exclusively inside `RunnableConfig["configurable"]["user_token"]`. It is available for execution of the current turn, but excluded from serialized graph state snapshots.
