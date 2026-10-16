# Part G: Testing, Evaluation & Tracing

## Objectives
- Separate deterministic components from non-deterministic agent trajectories:
  - **Deterministic Unit Testing**: Route parsing, retry logic, error status translation, and ASP.NET Core endpoints tested via `pytest`, `respx`, and `xUnit`.
  - **Non-Deterministic Evaluation**: 10-scenario evaluation suite executed across 3 runs each to establish reliable pass rates.
- Integrate **LangSmith** tracing for full trajectory observability, token consumption auditing, and latency profiling.

## Deliverables
- Python test suite (`pytest` + `respx`) validating tool mappings and edge conditions.
- .NET integration tests (`xUnit` + `WebApplicationFactory<Program>` + SQLite in-memory) validating 401s, idempotency, and thread authorization.
- 10-scenario agent evaluation suite and benchmark report in `../docs/week7-eval-report.md`.
