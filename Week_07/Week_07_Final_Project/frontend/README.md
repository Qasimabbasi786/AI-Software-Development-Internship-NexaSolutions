# Frontend Client (Angular 17+ Standalone)

## Architecture Scope
- **Framework**: Angular 17/18 Standalone Components with Signals and RxJS.
- **Components**:
  - `AgentChatComponent`: Main conversational container with chat input and streaming message view.
  - `AgentTimelineComponent`: Visual step-by-step reasoning feed displaying tool calls, tool results, thoughts, and status transitions.
  - `ApprovalCardComponent`: Interactive Human-in-the-Loop approval card showing tool name, arguments, and Approve/Reject buttons with double-click disabling.
- **Services**:
  - `AgentRunService`: Manages Server-Sent Events (SSE) connections, dispatches typed events (`step`, `token`, `approval_required`, `final`, `error`), and issues resume commands.
  - `ReservationService`: Manages user reservations and badge counters.
- **State Resilience**:
  - Restores active thread state and pending approval cards upon browser refresh using `GET /api/assistant/agent/runs/{threadId}`.
