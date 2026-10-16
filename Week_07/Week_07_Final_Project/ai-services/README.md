# AI Services (FastAPI + LangGraph)

## Architecture Scope
- **Framework**: FastAPI + Uvicorn hosting compiled LangGraph state machines.
- **State Management**:
  - `AgentState`: `messages: Annotated[list, add_messages]`, `steps: int`, `retries: int`, `route: str`.
  - Checkpointer: `SqliteSaver` storing serialized checkpoints to `agent_checkpoints.sqlite` (gitignored).
- **Security Boundaries**:
  - Enforce internal `X-Service-Key` header authentication on all routes.
  - Read end-user JWT strictly from `RunnableConfig["configurable"]["user_token"]` to avoid persisting credentials in checkpoints.
  - Wrap catalog RAG context inside `<untrusted_document>` tags.
- **Tools**:
  - `search_catalog`: Semantic book search.
  - `check_availability`: Real-time stock status check.
  - `reserve_book`: Pydantic validated, marked as risky for HITL approval, forwards `Idempotency-Key` and Bearer JWT to .NET backend.
  - `list_my_reservations`: Retrieves caller's active reservations.
- **Human-in-the-Loop**:
  - `approval_node`: Triggers `interrupt()` whenever write tools are detected in pending calls.
