# 🚨 Part H: Team Practice & The Incident Drill

**Milestone:** Week 8 — Capstone Deliverable 11  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Minimize the bus factor by conducting cross-stack walkthroughs and pairing across frontend, backend, and AI orchestration.
- Conduct high-quality, substantive peer code reviews across at least 3 pull requests pointing out specific risks and alternatives.
- Execute a timed live Incident Response Drill (45 minutes) responding to a mentor-injected production failure.
- Diagnose and remediate the injected fault exclusively utilizing health check probes, structured correlation logs, traces, and automated tests.
- Produce an exhaustive, blameless postmortem report detailing timeline, impact, root cause, contributing factors, and preventive action items.

---

## 📦 Key Deliverables
1. **Peer Review Log:** Documentation of 3+ substantive PR reviews with technical feedback.
2. **Incident Drill Playbook:** Diagnostic cheat sheet mapping symptoms (401/403, 503, query latency) to evidence sources.
3. **Blameless Postmortem Report:** Completed postmortem report in [`docs/postmortem-incident-drill.md`](../docs/postmortem-incident-drill.md) adhering to Google SRE postmortem standards.
4. **Action Item Tracking:** Preventative enhancements and healthcheck additions filed as GitHub issues.

---

## 🧪 Verification & Acceptance Criteria
- [ ] Injected failure successfully isolated and remediated within the 45-minute drill window.
- [ ] Postmortem focuses on systemic and architectural factors rather than human error.
- [ ] Action items have defined owners and explicit acceptance criteria.
