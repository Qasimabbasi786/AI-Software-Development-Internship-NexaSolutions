# 🔒 Part D: Security Hardening & Peer Review

**Milestone:** Week 8 — Capstone Deliverable 6 & 7  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Run automated vulnerability audits across all 3 technology stacks (`dotnet list package --vulnerable`, `npm audit`, `pip-audit`) and resolve or justify all findings.
- Perform deep Git history secret scanning using `gitleaks` across all commits and branches to ensure no credentials or API keys were ever committed.
- Harden transport and edge security: enforce strict CORS policies allowing only the designated Angular origin (no wildcards with credentials), enable HSTS, and add security headers.
- Implement brute-force defense on authentication: login rate limiting and exponential lockout.
- Enforce request payload and question size limits to defend against prompt injection DOS and token inflation.
- Implement GDPR-compliant `DELETE /api/me/data` completely removing user preferences, checkpoints, and chat histories.

---

## 📦 Key Deliverables
1. **Security Scan Audit:** Clean outputs for .NET, npm, and pip dependency scans documented in [`/docs/week8-security-review.md`](../docs/week8-security-review.md).
2. **Gitleaks Report:** Full history scan output confirming zero un-rotated secrets in Git history.
3. **Hardened Auth & CORS:** Origin-bound CORS policies, login lockout configuration, and request size filters.
4. **Data Deletion API:** Functional endpoint purging user thread checkpoints and DB entries with verification scripts.
5. **Peer Security Review:** 5-question peer review checklist completed and tracked in GitHub issues.

---

## 🧪 Verification & Acceptance Criteria
- [ ] No high/critical unmitigated vulnerabilities across dotnet, npm, and pip packages.
- [ ] Gitleaks scan returns zero active un-rotated secrets.
- [ ] Calling `DELETE /api/me/data` purges all related entries from SQL Server and LangGraph SQLite checkpoints.
- [ ] Questions exceeding character limit are rejected with HTTP 400 (not silently truncated).
