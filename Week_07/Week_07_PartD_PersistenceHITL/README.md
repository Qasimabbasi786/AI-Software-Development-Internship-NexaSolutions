# Part D: Persistence, Human-in-the-Loop & Agent Memory

## Objectives
- Integrate `SqliteSaver` checkpointer for state durability across server restarts.
- Implement Human-in-the-Loop (HITL) execution pauses using LangGraph `interrupt()` on risky write tools.
- Resume interrupted runs using `Command(resume={"approved": True/False})` mapped precisely to pending tool calls.
- Implement short-term state inspection (`app.get_state_history`) and long-term user preferences (`UserPreference` table) with an explicit deletion path.
- Enforce strict exclusion of sensitive JWT tokens and API keys from checkpoint files.

## Deliverables
- SQLite checkpointing implementation demonstrating process interruption and resumption.
- Human approval flow handling both approval and rejection gracefully without illegal retries.
- Persistence leak test script verifying zero JWT tokens present in `.sqlite` checkpoint files.
