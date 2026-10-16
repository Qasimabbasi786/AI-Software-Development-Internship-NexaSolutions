# Part A: Agent Fundamentals & LangGraph Core

## Objectives
- Understand Chatbot vs. Chain vs. Agent autonomy.
- Implement explicit LangGraph state graphs with `StateGraph`, `START`, and `END`.
- Use append reducers (`add_messages`) for conversation history and scalar overwrite fields for `steps`.
- Enforce hard loop termination with `MAX_STEPS` and a dedicated `give_up_node`.

## Deliverables
- `agent_fundamentals.py`: Core LangGraph agent loop with step limit counter and give-up node.
- Generated Mermaid diagram comparing hand-drawn vs. compiled graph.
- Practice challenges documented in `../docs/week7-agent-loop-notes.md`.
