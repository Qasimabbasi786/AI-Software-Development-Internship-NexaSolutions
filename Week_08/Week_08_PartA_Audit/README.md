# 🔍 Part A: System Audit, Backlog Triage & Architecture Decisions

**Milestone:** Week 8 — Capstone Deliverable 1  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Conduct a complete system-wide audit of the platform built through Weeks 1–7.
- Triage the starting backlog comprising Week 7 residual risks, red-team findings, and unfinished stretch items.
- Score all backlog items with impact ($1-3$) and likelihood ($1-3$) matrix: $\text{Risk} = \text{Impact} \times \text{Likelihood}$, estimated by effort (S/M/L).
- Establish formal Architecture Decision Records (ADRs) explaining key design choices.
- Conduct a comprehensive pre-mortem failure mode analysis identifying at least 5 realistic production disaster scenarios with preventive controls.

---

## 📦 Key Deliverables
1. **GitHub Issues & Backlog Triage:** Labelled backlog issues (`security`, `reliability`, `performance`, `docs`, `tech-debt`) categorized into To do / Doing / Done.
2. **System Architecture Diagram:** Mermaid diagram documenting all service containers, datastores, protocols, and distinct trust boundaries.
3. **ADRs in `/docs/adr/`:**
   - Why a separate FastAPI service instead of in-process LLM calls from .NET.
   - Why SQLite checkpoint persistence now and PostgreSQL later.
   - Why interactive human approval (`interrupt()`) is mandatory for write operations.
4. **Pre-Mortem Failure Analysis:** Documented in `/docs/architecture.md` assessing 5+ failure modes with likelihood, impact, and controls.

---

## 🧪 Verification & Acceptance Criteria
- [ ] Every backlog item has an assigned risk score and effort estimate.
- [ ] At least one ADR includes the strongest counter-argument and conditions that would force a reversal.
- [ ] All trust boundaries and authentication hops are clearly documented.
