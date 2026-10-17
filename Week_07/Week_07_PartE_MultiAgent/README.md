# Week 7 — Part E: Multi-Agent Systems (Stretch Tier)

## 📌 Executive Summary
Part E explores the **Multi-Agent Supervisor Pattern**, decomposing the assistant into specialized domain agents coordinated by a centralized supervisor:
1. **Supervisor Node**: Orchestrator dynamically delegating work via `SupervisorDecision(next: Literal["catalog_agent", "circulation_agent", "FINISH"])`.
2. **Catalog Specialist**: Read-only worker agent scoped strictly to `search_catalog` and `check_availability`. Write tools are omitted from its tool registry to enforce least privilege.
3. **Circulation Specialist**: Transactional worker agent with `reserve_book` and `list_my_reservations`, guarded by human approval.
4. **Coordination Ceiling**: Enforces `MAX_SUPERVISOR_STEPS = 6` to terminate infinite worker-supervisor ping-pong cycles.

---

## 🏗️ Architecture & Graph Topology

```mermaid
graph TD;
    __start__([START]):::first --> supervisor;
    
    supervisor -. "next == 'catalog_agent'" .-> catalog_agent;
    supervisor -. "next == 'circulation_agent'" .-> circulation_agent;
    supervisor -. "next == 'FINISH' || steps >= 6" .-> __end__([END]):::last;
    
    catalog_agent -. "tool call" .-> catalog_tools[Catalog Tools: search, availability];
    catalog_tools --> catalog_agent;
    catalog_agent -. "findings complete" .-> supervisor;
    
    circulation_agent -. "tool call" .-> circulation_tools[Circulation Tools: reserve, list];
    circulation_tools --> circulation_agent;
    circulation_agent -. "reservation action complete" .-> supervisor;

    classDef default fill:#f2f0ff,line-height:1.2;
    classDef first fill-opacity:0;
    classDef last fill:#bfb6fc;
```

---

## 🔑 Core Concepts Mastered

### 1. Multi-Agent Roles & Least Privilege

| Agent Name | Scope | Available Tools | Mutation Rights |
| :--- | :--- | :--- | :---: |
| **Supervisor** | Orchestration & Intent Handoff | None | None |
| **Catalog Agent** | Catalog Search & Availability Reads | `search_catalog`, `check_availability` | **No** (Read-Only) |
| **Circulation Agent**| Reservations & Personal Loan Queries| `reserve_book`, `list_my_reservations`| **Yes** (HITL Protected) |

### 2. The "Multi-Agent Tax" Benchmark
Quantitative metrics comparing Single-Agent vs. Multi-Agent architectures are documented in [`docs/week7-single-vs-multi-agent.md`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/docs/week7-single-vs-multi-agent.md):
- **Latency**: Multi-Agent is **+141% slower** (5.80s vs 2.40s) due to repetitive supervisor delegation round-trips.
- **Model Calls**: Increased from 2 calls to 5 calls (**+150%**).
- **Token Overhead**: Increased from 620 tokens to 1,420 tokens (**+129%**).
- **Production Verdict**: Single-agent with explicit subgraphs and deterministic guardrails is the superior architectural choice for this domain.

---

## 🛠️ Implementation Details (`benchmark_part_e.py`)

- **Multi-Agent Graph:** [`Week_07_Final_Project/ai-services/multi_agent_system.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/multi_agent_system.py)
- **Comparative Benchmark:** [`Week_07_PartE_MultiAgent/benchmark_part_e.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_PartE_MultiAgent/benchmark_part_e.py)
- **Verification Command:**
  ```bash
  python Week_07_PartE_MultiAgent/benchmark_part_e.py
  ```

---

## ✅ Verification Checklist
- [x] Multi-agent supervisor compiled using `SupervisorDecision` structured output schema.
- [x] Catalog Agent tool surface area strictly confined to non-mutating search and availability tools.
- [x] Circulation Agent manages reservations with human approval interrupts.
- [x] `MAX_SUPERVISOR_STEPS` bounds ping-pong cycles and enforces reliable graph termination.
