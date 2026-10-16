# Week 7: Secure LangGraph Agents, Tool Execution, Human-in-the-Loop, Persistence & CI

Welcome to **Week 7** of the AI Software Development Internship. 

Where Week 6 delivered a fixed-path streaming RAG chain, Week 7 steps into **Autonomous AI Agents** powered by **LangGraph**. The moment an AI system can decide its own next step and take real-world actions with side effects (reserving a book on a user's behalf), engineering priorities fundamentally shift to:
- **Autonomy & Termination Guarantees**: Graph states, nodes, conditional edges, cycle termination, and give-up handling.
- **Secure Tool Design**: Typed argument validation (Pydantic), read vs. write tool classification, server-side authorization using user JWTs (never passed in state), and idempotency.
- **Routing & Re-planning Workflows**: Intent routing, plan-then-execute architectures, retry handling with backoff, and dynamic re-planning on conflicts (409 Conflict).
- **Persistence & Human-in-the-Loop (HITL)**: SQLite checkpointer (`SqliteSaver`), state resumption across process restarts, `interrupt()` pauses for high-risk write actions, and long-term user preferences.
- **Multi-Agent Systems (Stretch)**: Specialized supervisor-worker patterns (Catalog Agent + Circulation Agent).
- **Agent Red-Teaming & Security**: 7-point attack harness (direct/indirect prompt injection via poisoned catalog RAG data, argument abuse, secret extraction, thread hijacking) and defense-in-depth mitigations.
- **Deterministic Testing & LLM Evaluation**: Pytest and xUnit test suites, respx HTTP mocking, 10-scenario x 3-run trajectory evaluations, and LangSmith observability traces.
- **Full-Stack End-to-End Integration**: ASP.NET Core Agent Run APIs, SSE typed event streams, Angular timeline UI with interactive Human Approval Cards.
- **DevOps Quality Gates**: GitHub Actions CI workflow (three jobs: .NET, Angular, Python) and `git bisect` regression troubleshooting.

---

## Directory Structure Overview

```text
Week_07/
├── .github/workflows/ci.yml               # Multi-platform CI pipeline (.NET, Angular, Python)
├── docs/                                  # Technical reports & write-ups
│   ├── week7-agent-loop-notes.md          # Agent loop termination & error recovery notes
│   ├── week7-tool-risk-table.md           # Tool risk classification & justification table
│   ├── week7-red-team-report.md           # 7-attack red-team findings & residual risk report
│   ├── week7-eval-report.md               # 10-scenario x 3-run evaluation matrix & LangSmith traces
│   ├── week7-single-vs-multi-agent.md     # Single vs. multi-agent comparative analysis (Stretch)
│   ├── week7-mcp-vs-langchain-tools.md    # MCP vs. LangChain tools ecosystem analysis (Stretch)
│   ├── week7-semantic-kernel-comparison.md# Semantic Kernel (.NET) vs. LangGraph comparison (Stretch)
│   └── README.md                          # Documentation index and delivery criteria
├── Week_07_PartA_AgentFundamentals/       # LangGraph core: state, nodes, edges, cycle limits
├── Week_07_PartB_SecureTools/             # Pydantic schemas, write tools, JWT via config, idempotency
├── Week_07_PartC_RoutingPlanning/         # Intent routing, plan-then-execute, replanning on conflict
├── Week_07_PartD_PersistenceHITL/         # SQLiteSaver checkpointing, interrupt/resume, memory
├── Week_07_PartE_MultiAgent/              # Multi-agent supervisor with catalog & circulation specialists
├── Week_07_PartF_SecurityRedTeam/         # 7 security attack tests, untrusted document wrapping
├── Week_07_PartG_TestingEval/             # Pytest, xUnit tests, 10-scenario evaluation suite
├── Week_07_PartH_FullStackIntegration/    # .NET Agent API, SSE events, Angular approval timeline
├── Week_07_PartI_Ecosystem/               # MCP, Semantic Kernel, and local model analysis
├── Week_07_PartJ_CI_GitBisect/            # CI configuration verification, git bisect logs
├── Week_07_Final_Project/                 # Capstone end-to-end full-stack agent implementation
│   ├── backend/                           # ASP.NET Core 8 Web API (Reservations, Preferences, Rate limiting)
│   │   ├── Controllers/                   # Books, Auth, Assistant, Preferences
│   │   ├── Data/                          # LibraryDbContext (Reservations, Threads, Preferences)
│   │   ├── Models/                        # Entity models (Reservation, AgentThread, UserPreference, etc.)
│   │   ├── Repositories/                  # BookRepository & abstraction
│   │   └── Services/                      # AiServiceClient & abstraction
│   ├── ai-services/                       # FastAPI + LangGraph Agent service with SQLite checkpointer
│   │   ├── security/                      # Untrusted document wrapping, guardrails, red-team harness
│   │   ├── agent_graph.py                 # Core state machine, router, subgraphs, HITL interrupt, retries
│   │   ├── agent_tools.py                 # Pydantic-validated read/write tools & JWT forwarding
│   │   ├── model_factory.py               # Multi-provider LLM factory (Gemini, OpenAI, Anthropic)
│   │   ├── test_part_c.py                 # Part C router & re-planning verification suite
│   │   └── test_part_d.py                 # Part D persistence & secret audit verification suite
│   └── frontend/                          # Angular 17+ Chat & Agent timeline with HITL cards
├── requirements.txt                       # Python dependencies for Week 7
└── README.md                              # This root guide
```

---

## Core Architecture Principles

1. **Explicit Graph Architecture**:
   State transitions are strictly governed via typed LangGraph State, using append-only reducers (`add_messages`) for conversation logs and overwrite fields for counters (`steps`, `retries`).
2. **Never Put Secrets or Auth Tokens in Checkpointed State**:
   User JWTs travel strictly inside `RunnableConfig["configurable"]["user_token"]`, ensuring persistent storage files (`agent_checkpoints.sqlite`) contain zero credentials or sensitive authorization tokens.
3. **Defense in Depth Over Prompt Reliance**:
   Prompt guidelines are the first layer, but security guarantees are enforced server-side via ASP.NET Core JWT claims extraction, Pydantic argument boundaries, and cryptographic idempotency keys.
4. **Resilience & Interruptibility**:
   Risky actions trigger `interrupt()`. Pauses survive server restarts, and human decisions are bound strictly to exact tool call IDs and arguments.
