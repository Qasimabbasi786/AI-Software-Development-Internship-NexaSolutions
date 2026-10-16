# Part C: Routing, Planning & Retry Workflows

## Objectives
- Implement a low-latency Router Node using `with_structured_output` and literal types (`catalog`, `action`, `chitchat`).
- Subgraph orchestration: embed Week 6 RAG pipeline as a specialized subgraph for catalog questions.
- Plan-then-execute flow: construct inspectable plans for multi-step goals with dynamic replanning.
- Typed retry workflows: route transient network timeouts (`ERROR_RETRYABLE`) to backoff retries (max 2), while routing resource conflicts (`ERROR_FINAL` / 409 Conflict) directly to replanning.

## Deliverables
- Router graph with 15-message validation test suite (5 per route category).
- Re-plan handler for 409 reservation conflicts that searches and offers alternatives.
- Safe retry loop with backoff and idempotency protection.
