# Part E: Multi-Agent Systems (Stretch Tier)

## Objectives
- Decompose complex domains into specialized sub-agents:
  - **Catalog Agent**: Read-only specialist for querying catalog metadata and availability.
  - **Circulation Agent**: Write-specialist for managing reservations and renewals (requiring approval).
- Implement a **Supervisor Node** using structured output (`Next(BaseModel)`) to dynamically orchestrate worker agents.
- Enforce least privilege by agent (Catalog Agent has no access to write tools).
- Prevent infinite worker ping-pong by enforcing a global step limit counter.

## Deliverables
- Multi-agent supervisor implementation in LangGraph.
- Comparative benchmarks measuring tokens, model calls, and latency versus single-agent workflows.
- Technical analysis documented in `../docs/week7-single-vs-multi-agent.md`.
