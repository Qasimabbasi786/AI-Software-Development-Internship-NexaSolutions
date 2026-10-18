# 📚 Week 8 Capstone Documentation Suite

This directory contains complete architectural, operational, security, evaluation, and retrospective documentation required by the **Week 8 Capstone Definition of Done**.

## 📑 Core Documentation Index

| Document | Audience & Purpose | Key Contents |
| :--- | :--- | :--- |
| **[`architecture.md`](./architecture.md)** | System Architects & Developers | Component topology, data flow, trust boundary definitions, sequence diagrams. |
| **[`runbook.md`](./runbook.md)** | DevOps / SRE / On-Call Engineers | Start/stop commands, health endpoints, log aggregation, key rotation, disaster recovery. |
| **[`user-guide.md`](./user-guide.md)** | End Users & Stakeholders | System features, conversational commands, human approval flow, GDPR data deletion. |
| **[`release-criteria.md`](./release-criteria.md)** | Quality Assurance & Mentors | Pre-defined hard and soft release gates for production promotion. |
| **[`week8-performance-report.md`](./week8-performance-report.md)** | Performance & FinOps Engineers | 20-scenario before/after benchmarks: median/p95 latency, token counts, cost models. |
| **[`week8-security-review.md`](./week8-security-review.md)** | Security Engineers & Auditors | Dependency vulnerability audits, gitleaks findings, CORS lockdown, rate-limiting proofs. |
| **[`week8-trace-example.md`](./week8-trace-example.md)** | SRE & Support Engineers | End-to-end distributed trace sample traversing Angular, .NET API, and FastAPI using `X-Correlation-Id`. |
| **[`postmortem-incident-drill.md`](./postmortem-incident-drill.md)** | Engineering Team & Mentors | Blameless postmortem analysis of the mentor-injected production incident. |
| **[`reflection-candidate.md`](./reflection-candidate.md)** | Mentor & Candidate Review | Written reflection, hardest bugs, design trade-offs, and 90-day learning roadmap. |
| **[`adr/`](./adr/)** | Architecture Decision Records | Formal records documenting key architectural choices and trade-offs. |
