# ⚡ Part B: Performance, Cost & Safe Caching

**Milestone:** Week 8 — Capstone Deliverable 2 & 3  
**Status:** Initialized 📌  

---

## 🎯 Objectives
- Benchmark baseline system performance across 20 evaluation scenarios, measuring median and p95 latency, token counts, and cost per run.
- Implement incremental vector re-indexing (`sync_index`) using content hashing (`SHA-256`) so only modified catalog records incur embedding computation.
- Implement a thread-safe, TTL and versioned answer cache for read-only catalog queries (`current_catalog_version`).
- Enforce strict cache safety: personal user data and state-mutating write actions must never be cached across users.
- Enforce token budgets per user per day in .NET alongside max question length constraints to prevent resource exhaustion and cost blowups.

---

## 📦 Key Deliverables
1. **Incremental Indexing Engine:** SHA-256 hash comparison against Chroma collection metadata before calling embeddings API.
2. **Safe Answer Cache:** Normalized query keying combined with active catalog version, strictly guarding read-only operations.
3. **Daily Token Budget Enforcement:** EF Core query tracking user token usage against quota, returning HTTP 429 when exceeded.
4. **Before/After Performance Report:** Comprehensive comparative metrics table saved in [`/docs/week8-performance-report.md`](../docs/week8-performance-report.md).

---

## 🧪 Verification & Acceptance Criteria
- [ ] Evaluation pass rate must not regress between baseline and optimized runs.
- [ ] Modifying a book description invalidates cache and returns fresh data via catalog version increment.
- [ ] User-specific answers ("What books have I reserved?") are never cached or served to other users.
- [ ] Writing actions are strictly excluded from answer caching.
