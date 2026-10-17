# 🏛️ Library Agent: Find, Approve, Reserve (Week 7 Final Project)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 7 Final Project — Secure LangGraph Agents, Tool Execution, HITL, Persistence & CI  

[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-2E7D32?logo=diagram-project&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![.NET: 8.0](https://img.shields.io/badge/.NET-8.0_Web_API-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![Angular: 18/20](https://img.shields.io/badge/Angular-18_Standalone-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite Checkpointer](https://img.shields.io/badge/Checkpointer-SqliteSaver-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 📌 Executive Summary
The **Week 7 Final Project** elevates the Library AI system into an autonomous, stateful **LangGraph Agent** capable of searching catalog records, checking physical shelf availability, pausing for explicit Human-in-the-Loop (HITL) approval before executing book reservations, re-planning upon 409 conflict errors, and surviving browser refreshes via durable SQLite checkpoints.

---

## 🏗️ Multi-Tier Architecture & LangGraph Graph Topology

```mermaid
graph TD
    START([START]) --> Router[Router Node: Intent Classifier]

    Router -->|catalog| RAG[RAG Subgraph: Week 6 Knowledge Retrieval]
    Router -->|chitchat| Chitchat[Chitchat Node: Conversational Greetings]
    Router -->|action| Agent[Agent Action & Planning Node]

    RAG --> END([END])
    Chitchat --> END

    Agent --> StepLimitCheck{Steps >= 6?}
    StepLimitCheck -->|Yes| GiveUp[Give Up Node: Step Budget Exhausted]
    GiveUp --> END

    StepLimitCheck -->|No| ToolCallCheck{Tool Calls?}
    ToolCallCheck -->|None / Final Answer| END
    ToolCallCheck -->|Read-Only Tools| Tools[ToolNode: search_catalog, check_availability, list_reservations]
    ToolCallCheck -->|Risky Tool: reserve_book| Approval[Approval Node: interrupt]

    Approval -->|Human Approved| Tools
    Approval -->|Human Rejected| Agent

    Tools --> ErrorCheck{Tool Result Error Type?}
    ErrorCheck -->|ERROR_RETRYABLE & Retries < 2| RetryBackoff[Exponential Backoff] --> Agent
    ErrorCheck -->|ERROR_FINAL 409 Conflict| Replan[Re-plan Alternative Book] --> Agent
    ErrorCheck -->|Success OK| Agent
```

---

## 🛡️ Core Agent Tools & Least Privilege

All tools are implemented in [`ai-services/agent_tools.py`](ai-services/agent_tools.py) with Pydantic boundary validation:

1. **`search_catalog(query: str)`**:
   - Read-only tool searching catalog records. Safe for unbounded autonomous execution.
2. **`check_availability(book_id: int)`**:
   - Read-only tool validating that `book_id > 0` via `AvailabilityArgs(gt=0)`.
3. **`reserve_book(book_id: int)`**:
   - High-risk write tool creating reservations. Requires human approval intercept.
   - Extracts user JWT and idempotency keys strictly from `RunnableConfig` (never persisted in state).
4. **`list_my_reservations()`**:
   - Read-only account tool scoped to caller identity.

---

## 🔁 Typed Retries & Re-planning Path

- **Transient Failures (`ERROR_RETRYABLE`)**:
  - Automatically retried up to 2 times with exponential backoff ($0.5 \times (\text{retries} + 1)$ seconds).
- **Reservation Conflict (`ERROR_FINAL: 409 Conflict`)**:
  - The agent detects the conflict and does NOT loop. It immediately invokes `search_catalog` to recommend alternative available books in the same genre.
- **Global Step Limit**:
  - Hard limit of `MAX_STEPS = 6` routes to `give_up_node` preventing infinite tool execution loops.

---

## 🚀 Running the Project

### 1. Backend (.NET 8 Web API)
```bash
cd backend
dotnet run
```

### 2. AI Services (FastAPI + LangGraph)
```bash
cd ai-services
python main.py
```

### 3. Frontend (Angular 18/20)
```bash
cd frontend
npm start
```
