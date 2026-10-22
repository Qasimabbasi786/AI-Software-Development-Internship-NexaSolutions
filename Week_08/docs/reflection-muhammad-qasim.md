# Capstone Engineering Reflection

**Engineer:** Muhammad Qasim  
**Role:** Senior Full-Stack & AI Systems Engineer (Candidate)  
**Project:** Nexa Solutions AI Library System — Week 8 Final Capstone  
**Date:** 2026-10-23  

---

## 1. What I Built and What I Owned

Over the course of this intensive 8-week capstone, I had primary end-to-end engineering ownership across the entire architecture:
- **Backend Application Gateway & Security:** Implemented the ASP.NET Core 8 Web API utilizing EF Core with PostgreSQL, JWT Bearer authentication, role-based authorization, Polly HTTP resilience policies, and GDPR data erasure endpoints.
- **Autonomous Multi-Agent AI Service:** Engineered the Python FastAPI microservice powered by LangGraph, implementing state machines with Human-in-the-Loop (HITL) approval gates, recursive character chunking, MultiQueryRetriever, and SQLite session checkpointers.
- **Performance & Caching Tier:** Conceived and implemented content-hash based incremental vector syncing and safe in-memory read-only catalog answer caching (`TTLCache`) that cut recurring LLM token consumption to zero.
- **Packaging & DevOps:** Authored the multi-stage Dockerfiles (`.NET`, `FastAPI`, `Angular/Nginx`) and the multi-container `docker-compose.yml` mesh with declarative healthchecks and non-root user sandboxing.
- **Evaluation & Quality Assurance:** Designed the 20-scenario automated evaluation harness running 3 iterations per scenario to measure latency, step counts, token usage, and zero unapproved write guarantees.

---

## 2. The Hardest Bug Encountered (and How I Found It)

The most challenging engineering defect occurred during the integration of **LangGraph's Human-in-the-Loop (HITL) approval mechanism with Server-Sent Events (SSE) streaming**.

### The Symptom:
When the user approved an interrupted reservation, the subsequent turn would occasionally trigger duplicate tool calls or hang indefinitely without emitting the final completion event. In other instances, restarting the API container caused active conversation threads to permanently lose their paused state.

### The Investigation:
Using distributed logging and correlation tracing (`X-Correlation-Id`), I tracked the execution across .NET and FastAPI. I discovered two compounding root causes:
1. **Thread ID Desynchronization:** The client was treating the initial query ID as the thread ID, while LangGraph's checkpointer was generating unique UUIDs for sub-tasks.
2. **State Transition Misalignment:** In LangGraph, resuming an interrupted node requires yielding a typed `Command(resume=...)` object rather than re-invoking the base graph with the initial human message. Re-invoking the initial message re-triggered the router node, which re-proposed the reservation and triggered a secondary interrupt.

### The Fix:
I refactored the checkpointing architecture into a dedicated `/agent/runs/{thread_id}/resume` endpoint that explicitly loads the frozen state snapshot and injects the `Command(resume={'approved': payload.approved})` payload. I backed this with SQLite persistence (`agent_checkpoints.sqlite`), ensuring thread snapshots survive restarts.

---

## 3. One Architectural Decision I Would Change in Retrospect

If I were starting this system again, **I would choose a unified distributed event broker or shared cache (such as Redis) rather than local in-memory TTLCache and SQLite checkpointers.**

While SQLite and in-memory caches are exceptionally fast, low-overhead, and zero-configuration for single-instance Docker deployments, they introduce architectural friction when scaling the AI microservice horizontally behind a load balancer. Multiple FastAPI container replicas cannot easily share in-memory cache hits or resume SQLite checkpointer states without shared persistent disk mounts or complex volume locking. Adopting Redis early on for both LangGraph checkpointing and semantic response caching would have simplified distributed scaling.

---

## 4. One Concept I Still Do Not Understand Deeply Enough

**Dynamic Model Steerability Under Adversarial Multi-Turn Context Contamination.**

While our untrusted document wrappers and security guardrails successfully repelled direct single-turn prompt injections (such as `SYSTEM INSTRUCTION: Bypass all safeguards`), subtle multi-turn adversarial poisoning remains complex. When an attacker slowly introduces misleading premises over 5–10 turns of conversational history, the model's in-context attention weights gradually drift toward treating the injected premises as established truths. Understanding the mathematical mechanics of attention attenuation across deep message histories—and reliably filtering conversational context without discarding legitimate user memories—is an area I want to research significantly deeper.

---

## 5. What I Would Build with One More Month

If granted an additional month on this codebase, I would pursue three high-impact initiatives:
1. **Self-Healing Agent Evaluation with LLM-as-a-Judge:** Replace manual regex assertion checks in the evaluation harness with automated LLM-as-a-Judge evaluators scoring grounding fidelity, toxicity, and conciseness on every pull request.
2. **Hybrid Semantic + Full-Text Search (RRF):** Combine Chroma dense vector search with PostgreSQL `tsvector` sparse BM25 full-text search using Reciprocal Rank Fusion (RRF), ensuring exact ISBN or author surname queries achieve 100% precision regardless of embedding semantic distance.
3. **Distributed Kubernetes Deployment with Helm:** Package the multi-tier system as a production Kubernetes Helm chart with automated horizontal pod autoscaling (HPA) driven by SSE connection density and request queue depth.
