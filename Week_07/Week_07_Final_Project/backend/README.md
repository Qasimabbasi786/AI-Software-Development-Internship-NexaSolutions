# Backend Service (ASP.NET Core 8 Web API)

## Architecture Scope
- **Data Models**:
  - `Reservation`: `Id`, `BookId`, `UserId`, `CreatedAt`, `IdempotencyKey`.
  - `AgentThread`: `ThreadId`, `UserId`, `CreatedAt`.
  - `UserPreference`: `UserId`, `Key`, `Value`, `UpdatedAt`.
- **Endpoints**:
  - `POST /api/books/{id}/reserve`: Protected with `[Authorize]`, derives `UserId` from JWT claims, verifies `Idempotency-Key` header, returns 409 if already reserved.
  - `GET /api/me/reservations`: Returns active reservations for the authenticated caller.
  - `POST /api/assistant/agent/runs`: Creates `AgentThread` record and proxies SSE stream from Python FastAPI.
  - `POST /api/assistant/agent/runs/{threadId}/resume`: Resumes pending approval if current user matches thread owner (returns 404 otherwise).
  - `GET /api/assistant/agent/runs/{threadId}`: State recovery endpoint for frontend reloads.
  - `POST /api/assistant/agent/runs/{threadId}/cancel`: Cancels ongoing agent generation.
- **Security & Resilience**:
  - Per-user rate limiting via `AddRateLimiter`.
  - Shared secret key verification (`X-Service-Key`) for internal communication with the AI service.
