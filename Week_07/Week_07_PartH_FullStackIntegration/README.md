# Part H: Full-Stack Integration (.NET Agent API & Angular Agent UI)

## Objectives
- Build resilient ASP.NET Core Run Management APIs:
  - `POST /api/assistant/agent/runs`: Start an agent run, stream typed SSE events.
  - `POST /api/assistant/agent/runs/{threadId}/resume`: Approve or reject pending HITL actions.
  - `GET /api/assistant/agent/runs/{threadId}`: State recovery on page reload.
  - `POST /api/assistant/agent/runs/{threadId}/cancel`: Cancel active runs upstream.
- Implement Typed Server-Sent Events (SSE): `step`, `token`, `approval_required`, `final`, and `error`.
- Build Angular Agent UI:
  - Agent activity timeline showing thought steps and tool results.
  - Interactive Human Approval Card for write operations with double-click protection.
  - Automatic state recovery on browser refresh.
- Enforce trust boundaries: Browser -> .NET (user JWT) -> FastAPI (shared `X-Service-Key` + forwarded user token).

## Deliverables
- ASP.NET Core controllers and middleware with rate limiting (`AddRateLimiter`).
- Angular agent timeline components and resume/approval services.
- Verification scripts for browser reload, rate limits, and cross-user hijacking attempts (expecting 404).
