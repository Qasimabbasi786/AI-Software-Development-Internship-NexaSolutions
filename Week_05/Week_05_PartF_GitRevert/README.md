# Week 5 — Part F: Git Practice (`git revert`)

## 📌 Executive Summary
In enterprise production repositories with protected `main` branches and peer-reviewed Pull Requests, rewriting Git history via commands like `git reset --hard` is strictly dangerous. **Week 5 — Part F** masters **`git revert`** — the deterministic, non-destructive technique for safely undoing previous commits by recording a forward-moving inverse commit in the public history.

---

## 🏗️ Architectural Comparison: `git revert` vs. `git reset`

```
 1. Using git revert (Safe on Shared & Protected Branches)
 Before: [C1] ───► [C2 (Buggy)] ───► [C3]
 After:  [C1] ───► [C2 (Buggy)] ───► [C3] ───► [C4 (Revert "C2")]
 (History remains honest and auditable; no commits erased)

 2. Using git reset --hard (Dangerous on Shared Branches)
 Before: [C1] ───► [C2 (Buggy)] ───► [C3]
 After:  [C1]
 (C2 and C3 are permanently deleted from branch history; causes remote reject on push)
```

---

## 🔑 Why `git revert` is Essential

1. **Commit History Integrity:** A revert commit records *what* was attempted, *why* it was withdrawn, and *when* it was undone.
2. **Compatibility with Protected Branches:** Protected branches reject force pushes (`git push --force`). Because `git revert` creates a new forward commit, it can be proposed and reviewed through standard Pull Request workflows.
3. **Collaboration Safety:** Avoids desynchronizing team members' local working trees.

---

## 🛠️ Practical Step-by-Step Walkthrough

### 1. View Git Log to Locate Target Commit
```bash
git log --oneline -n 5
```
Example output:
```text
a1b2c3d feat: add /ask endpoint wiring RAG pipeline into FastAPI service
e4f5g6h fix: incorrect chunk size configuration
9z8y7x6 feat: build manual RAG pipeline
```

### 2. Execute the Revert Command
```bash
git revert e4f5g6h
```
Git automatically generates a commit message:
```text
Revert "fix: incorrect chunk size configuration"

This reverts commit e4f5g6h7890abcdef.
```

### 3. Verify Log & Forward Push
```bash
git log --oneline -n 3
# Push via normal feature branch PR
git push origin feature/revert-bad-chunk
```

---

## 🎯 Task Sheet Checklist (Part F)
- [x] Documented mechanics of `git revert` vs `git reset`.
- [x] Practiced safe rollback on temporary feature branch.
- [x] Confirmed both original commit and revert commit exist in log history.
- [x] Verified commit adheres to PR workflow without force-pushing.
