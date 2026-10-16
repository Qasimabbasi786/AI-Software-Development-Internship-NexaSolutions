# Part B: Tool Design & Secure Tool Execution

## Objectives
- Treat tool descriptions as prompts: precise parameter semantics and boundary constraints.
- Define typed, validated arguments with Pydantic (`args_schema`) to reject malformed inputs before HTTP execution.
- Classify read vs. write tools; enforce server-side authorization on write operations.
- Return errors as data (`ERROR_RETRYABLE`, `ERROR_FINAL`) rather than unhandled graph-crashing exceptions.
- Ensure the agent acts *as* the user, not *above* the user: pass JWT via `RunnableConfig` (never in checkpointed state).
- Implement idempotency keys (`Idempotency-Key` header) to prevent double reservation on retry.

## Deliverables
- ASP.NET Core entity migrations: `Reservation` and `AgentThread`.
- `POST /api/books/{id}/reserve` with idempotency verification and JWT claims-based user resolution.
- `GET /api/me/reservations` for personal reservation retrieval.
- Python tool definitions (`reserve_book`, `check_availability`, `list_my_reservations`).
