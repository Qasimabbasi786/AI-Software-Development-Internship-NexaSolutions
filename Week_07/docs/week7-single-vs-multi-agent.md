# Week 7 Architectural Tradeoffs: Single-Agent vs. Multi-Agent Systems

## Executive Summary
This document analyzes the engineering tradeoffs between a single unified LangGraph agent versus a multi-agent supervisor pattern for enterprise domain assistants.

---

## 1. Architectural Comparison

### Single-Agent Architecture (Parts A–D)
- **Model Calls**: Typically 1 to 3 LLM calls per user request.
- **Complexity**: Single graph state, shared message history, one tool execution node.
- **Latency & Tokens**: Minimal overhead, high cache hit rates, fast response times.

### Multi-Agent Supervisor Architecture (Part E)
- **Model Calls**: 3 to 6 LLM calls (Supervisor -> Specialist 1 -> Supervisor -> Specialist 2 -> Supervisor -> Synthesis).
- **Complexity**: Multiple prompt contexts, delegation routing, worker state aggregation, complex cycle termination safeguards.
- **Latency & Tokens**: Noticeable latency increase (+150-250%) and token consumption multiplier.

---

## 2. Production Recommendation
For our Library Assistant application, we recommend deploying a **Single-Agent Architecture with explicit subgraphs and strict tool partitioning**, rather than a full multi-agent supervisor. 

**Justification**:
1. The domain scope is focused (catalog search and reservation).
2. Pydantic schemas and LangGraph conditional edges already provide deterministic guardrails.
3. Multi-agent delegation introduces compounding non-deterministic failure modes and unnecessary operational latency for this tier of business complexity.
