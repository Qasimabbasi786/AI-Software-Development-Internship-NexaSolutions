# ⚡ Part B: Performance, Cost & Safe Caching

**Milestone:** Week 8 — Capstone Deliverables 2 & 3  
**Status:** Completed ✅  
**Author:** Muhammad Qasim (Lead AI Performance & Caching Engineer)  

[![Status: Completed](https://img.shields.io/badge/Part_B-Completed_%E2%9C%85-success)](https://github.com/)
[![Latency](https://img.shields.io/badge/Median_Latency-1.15s_(-56%25)-brightgreen)](../docs/week8-performance-report.md)
[![Cost](https://img.shields.io/badge/Cost_Savings--71%25-blue)](../docs/week8-performance-report.md)
[![Pytest](https://img.shields.io/badge/Tests-3_Passed_%E2%9C%85-success)](../ai-services/tests/test_caching_perf.py)
[![Token Budget](https://img.shields.io/badge/Daily_Budget-25k_Tokens-orange)](../backend/Controllers/AssistantController.cs)

---

## 🎯 Executive Summary & Objectives

AI features carry direct financial running costs and noticeable user latency. The strict guiding principle for Part B was:  
$$\textbf{Measure First} \longrightarrow \textbf{Optimize Second} \longrightarrow \textbf{Measure Again}$$

### Core Accomplishments:
1. **Incremental Indexing Engine:** Implemented SHA-256 book content hashing in [`safe_cache.py`](../ai-services/safe_cache.py) so unchanged books skip re-embedding upon synchronization.
2. **Safe Answer Cache (`TTLCache`):** Configured a thread-safe 5-minute TTL cache storing normalized catalog queries, invalidated automatically upon catalog version changes (`current_catalog_version`).
3. **Cache Safety & Guardrails:** Strictly prohibited caching across users, write tool executions, and personal reservation records.
4. **Model Selection Optimization:** Routed intent classification to a cheaper, high-speed model (`gemini-1.5-flash`), reserving powerful models for complex multi-step reasoning.
5. **Budget Enforcement:** Implemented per-user daily token budgets ($25{,}000$ tokens/day) and max question length limits ($1{,}000$ characters) in ASP.NET Core with HTTP 429 status codes.

---

## 📦 Key Deliverables & Code Artifacts

| Component | File Location | Purpose & Implementation |
| :--- | :--- | :--- |
| **Safe Caching & Indexer** | [`../ai-services/safe_cache.py`](../ai-services/safe_cache.py) | SHA-256 text hashing, `IncrementalCatalogIndexer`, `TTLCache`, normalized cache keys, and safety predicates. |
| **Model Selection Optimization** | [`../ai-services/model_factory.py`](../ai-services/model_factory.py)<br>[`../ai-services/agent_graph.py`](../ai-services/agent_graph.py) | `get_router_model()` wiring lightweight model to `create_router_runnable()`. |
| **Token Budget & Quota Guard** | [`../backend/Controllers/AssistantController.cs`](../backend/Controllers/AssistantController.cs)<br>[`../backend/Models/UsageLog.cs`](../backend/Models/UsageLog.cs) | Enforces 1,000 char question limit and checks `UsageLogs` against `DAILY_TOKEN_BUDGET` returning HTTP 429. |
| **Automated Test Suite** | [`../ai-services/tests/test_caching_perf.py`](../ai-services/tests/test_caching_perf.py) | Pytest suite verifying incremental indexing, catalog version invalidation, and cross-user cache isolation. |
| **Performance Benchmark Report** | [`../docs/week8-performance-report.md`](../docs/week8-performance-report.md) | Exhaustive before/after benchmark table, cost breakdown, and challenge answers. |

---

## 📊 Performance & Cost Summary Table

| Metric | Baseline | Optimized | Delta | Why it Improved |
| :--- | :---: | :---: | :---: | :--- |
| **Median Latency** | $2.65\text{ s}$ | **$1.15\text{ s}$** | **$-56.6\%$** | Fast-path catalog cache hits ($<15\text{ms}$) + faster inference on cheaper router. |
| **p95 Latency** | $4.85\text{ s}$ | **$2.40\text{ s}$** | **$-50.5\%$** | Elimination of redundant embeddings and trimmed prompt history context. |
| **Model Calls Per Run** | $2.45$ | **$1.35$** | **$-44.9\%$** | Read-only catalog hits bypass LLM; small talk/chitchat resolves in 1 call. |
| **Tokens In / Out** | $740 / 185$ | **$310 / 85$** | **$-57.3\%$** | Focused router system prompt, history trimming, zero-cost cache hits. |
| **Estimated Cost Per Run** | $\$0.00062$ | **$\$0.00018$** | **$-71.0\%$** | Cheaper model pricing for routing + token reduction + zero-cost cache hits. |
| **Evaluation Pass Rate** | $100\%$ | **$100\%$** | **$0.0\%$ (No regression)** | Exact deterministic quality preserved; zero unapproved writes or misroutes. |

---

## 🧪 Verification & Acceptance Criteria

- [x] **Incremental Indexing Verified:** Only modified books trigger embedding generation (`test_incremental_indexing_skips_unchanged` passing).
- [x] **Cache Invalidation Verified:** Bumping catalog version invalidates cached answers, eliminating stale data (`test_cache_invalidation_on_catalog_version_change` passing).
- [x] **Cache Safety Verified:** User-specific reservation queries and write tool invocations are rejected from cache (`test_cache_safety_user_specific_and_write_tools_never_cached` passing).
- [x] **Daily Token Budgeting Verified:** ASP.NET Core checks and writes to `UsageLogs`, returning HTTP 429 when budget is exceeded.
- [x] **All Builds & Tests Green:** .NET project builds with 0 errors; pytest passes all test cases.
