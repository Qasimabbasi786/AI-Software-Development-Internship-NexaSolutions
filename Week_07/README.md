# 🤖 Enterprise Autonomous AI Agent Platform (LangGraph, HITL, Security & Full-Stack)

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 7 — Secure LangGraph Agents • Tool Execution • Human-in-the-Loop • Persistence & CI  

[![Python: 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-2E7D32?logo=diagram-project&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![.NET: 8.0](https://img.shields.io/badge/.NET-8.0_Web_API-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![Angular: 18/20](https://img.shields.io/badge/Angular-18_Standalone-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite Checkpointer](https://img.shields.io/badge/Checkpointer-SqliteSaver-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Google Gemini](https://img.shields.io/badge/AI_Engine-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

## 🌟 Overview

This repository represents the production-ready autonomous agent platform built during **Week 7**. Where Week 6 established declarative streaming RAG pipelines, Week 7 steps into **Autonomous AI Agents** powered by **LangGraph**. The moment an AI system can decide its own next step and take real-world actions with side effects (reserving a physical book on a user's behalf), engineering priorities fundamentally shift toward:

- **Autonomy & Termination Guarantees**: Directed cyclic state graphs, conditional routing, step limits, and give-up handling.
- **Secure Tool Design**: Typed argument validation (Pydantic), read vs. write tool classification, server-side authorization using user JWTs (never passed in state), and idempotency keys.
- **Persistence & Human-in-the-Loop (HITL)**: Durable SQLite state checkpoints (`SqliteSaver`), state resumption across process restarts, `interrupt()` pauses for high-risk write actions, and long-term user preferences.
- **Agent Red-Teaming & Security**: 7-point adversarial attack harness (direct/indirect prompt injection via poisoned catalog RAG data, argument abuse, secret extraction, thread hijacking) and defense-in-depth mitigations.
- **Full-Stack End-to-End Integration**: ASP.NET Core Agent Run APIs, SSE typed event streams, Angular timeline UI with interactive Human Approval Cards.
- **DevOps Quality Gates**: GitHub Actions CI workflow (three parallel jobs: .NET, Angular, Python) and automated `git bisect` regression troubleshooting.

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 LangGraph Agent Pipeline               │
                  │                                                        │
   User Query ──> │   Router Node ──> Catalog Subgraph / Action Agent      │
   + JWT Token    │   (Intent Classifier)     (Plan-and-Execute)           │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │          Secure Tool Execution & Guardrails            │
                  │                                                        │
                  │  ┌───────────────────────┐   ┌───────────────────────┐ │
                  │  │ Pydantic Validation   │   │ Ephemeral ContextVar  │ │
                  │  │ (gt=0, Injection-Free)│   │ (Zero JWTs in State)  │ │
                  │  └───────────────────────┘   └───────────────────────┘ │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │         Human-in-the-Loop (HITL) Approval Gate         │
                  │                                                        │
                  │  Write Operation Detected? ──> interrupt() & Pause     │
                  │  Resumed via Command(resume={approved: True/False})   │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │ Typed SSE Stream to UI  │ ──> Timeline & Cards
                                 │ (/agent/runs endpoint)  │
                                 └─────────────────────────┘
```

---

## 📂 Repository Structure

| Directory / File | Description |
| :--- | :--- |
| **`Week_07_PartA_AgentFundamentals/`** | LangGraph core state machine: typed state, tool nodes, conditional edges, and step budget limits. |
| **`Week_07_PartB_SecureTools/`** | Secure tool design: Pydantic schemas (`ReserveArgs`), ephemeral credential injection, and idempotency. |
| **`Week_07_PartC_RoutingPlanning/`** | Structured intent routing (`RouteClassification`), dynamic plan/re-plan on 409 conflict, and typed retries. |
| **`Week_07_PartD_PersistenceHITL/`** | SQLite checkpointing (`SqliteSaver`), state durability, `interrupt()` approval gates, and long-term preferences. |
| **`Week_07_PartE_MultiAgent/`** | Multi-agent supervisor coordinating specialized Catalog and Circulation agents under least-privilege principles. |
| **`Week_07_PartF_SecurityRedTeam/`** | 7-vector adversarial security harness (indirect injection, overrides, secret extraction, thread hijacking). |
| **`Week_07_PartG_TestingEval/`** | Quality assurance: 15-test deterministic pytest suite, 10-scenario x 3-run evaluation matrix, and LangSmith traces. |
| **`Week_07_PartH_FullStackIntegration/`** | Full-stack architecture: ASP.NET Core Agent Run APIs, SSE proxying, and Angular execution timeline with approval cards. |
| **`Week_07_PartI_Ecosystem/`** | Ecosystem analysis: Model Context Protocol (MCP) and Microsoft Semantic Kernel (.NET) deep dives. |
| **`Week_07_PartJ_CI_GitBisect/`** | CI workflow setup (.github/workflows/ci.yml) and automated regression troubleshooting using `git bisect`. |
| **`Week_07_Final_Project/`** | Full-stack production capstone connecting Angular UI, ASP.NET Core 8 Web API, and FastAPI LangGraph agent. |
| **`docs/`** | Technical reports: Agent loop notes, tool risk table, red-team audit, eval metrics, and architectural write-ups. |

---

## 🚀 Quickstart & Execution

### 1. Configure Local Environment (`.env`)
Create `.env` in `ai-services` or the root workspace configured for Google Gemini:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DOTNET_URL=http://localhost:5000
SERVICE_KEY=nexa-secure-service-key-2026
```

### 2. Run Module Demos

#### Part A: Agent Loop & Step Limits
```bash
python Week_07_PartA_AgentFundamentals/agent_demo.py
```

#### Part C: Intent Router & Conflict Re-planning
```bash
python Week_07_PartC_RoutingPlanning/test_part_c.py
```

#### Part D: SQLite Persistence & HITL Approval
```bash
python Week_07_PartD_PersistenceHITL/test_part_d.py
```

#### Part E: Multi-Agent Supervisor Benchmark
```bash
python Week_07_PartE_MultiAgent/benchmark_part_e.py
```

#### Part F: 7-Vector Security Red-Team Suite
```bash
python Week_07_PartF_SecurityRedTeam/red_team_harness.py
```

#### Part G: 10-Scenario Evaluation Suite
```bash
python Week_07_PartG_TestingEval/eval_suite.py
```

#### Final Project: Full-Stack Verification
```bash
# 1. Start .NET Web API
cd Week_07_Final_Project/backend && dotnet run

# 2. Start Python FastAPI Agent
cd Week_07_Final_Project/ai-services && python main.py

# 3. Start Angular Client
cd Week_07_Final_Project/frontend && npm start
```

---

## 🔑 Core Architectural Axioms

1. **Explicit Graph Architecture**:
   State transitions are strictly governed via typed LangGraph State, using append-only reducers (`add_messages`) for conversation logs and overwrite fields for counters (`steps`, `retries`).
2. **Never Put Secrets or Auth Tokens in Checkpointed State**:
   User JWTs travel strictly inside `RunnableConfig["configurable"]["user_token"]` or ephemeral Python `ContextVar`, ensuring persistent storage files (`agent_checkpoints.sqlite`) contain zero credentials or sensitive authorization tokens.
3. **Defense in Depth Over Prompt Reliance**:
   Prompt guidelines are the first layer, but security guarantees are enforced server-side via ASP.NET Core JWT claims extraction, Pydantic argument boundaries (`gt=0`), and cryptographic idempotency keys.
4. **Resilience & Interruptibility**:
   Risky actions trigger `interrupt()`. Pauses survive server restarts, and human decisions are bound strictly to exact tool call IDs and arguments before database mutations can execute.
