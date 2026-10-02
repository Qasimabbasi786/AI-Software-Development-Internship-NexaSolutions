# Week 5 — Part F: Git Safely Undoing a Commit (`git revert`)

## Theoretical Guide: `git revert` vs `git reset`

### 1. What is `git revert`?
`git revert <commit-hash>` creates an entirely **new commit** that introduces inverse diffs of the target commit. It neutralizes the changes of that previous commit without erasing the past.

```
Initial State:
(A) ---> (B: bad feature) ---> (C) [main / HEAD]

After `git revert B`:
(A) ---> (B: bad feature) ---> (C) ---> (D: Revert "bad feature") [main / HEAD]
```

### 2. Why `git revert` is Essential on Protected Branches (`main`)
- **Preserves Honest Commit History:** Clearly documents when an issue was introduced and when/why it was reverted.
- **Collaborator Safe:** Because `git revert` only moves the branch *forward* by appending a new commit, it never breaks or desynchronizes teammates' local clones.
- **Works with Branch Protection:** Protected branches forbid force-pushing (`git push --force`). `git revert` requires only a normal forward push / PR.

### 3. Comparison Table

| Feature | `git revert` | `git reset` |
|---|---|---|
| **Mechanism** | Appends a new commit that inverts previous changes. | Moves the branch pointer backward, discarding commits from history. |
| **History Effect** | Non-destructive (History is preserved). | Destructive (History is rewritten). |
| **Protected Branch Safety** | **100% Safe** (Standard PR workflow). | **Dangerous / Forbidden** (Requires force push). |
| **Use Case** | Undoing bugs on shared/main branches. | Cleaning up messy unpushed local work. |

---

## Step-by-Step Hands-On Practice

### Step 1: Create a throwaway branch
```bash
git checkout -b practice/git-revert-test
```

### Step 2: Make an intentionally broken change & commit
For example, change chunk size to 0 in a test file:
```bash
git commit -am "test: introduce broken chunk_size = 0 bug"
```

### Step 3: Inspect log to get the commit hash
```bash
git log --oneline -n 3
# Example output:
# a1b2c3d test: introduce broken chunk_size = 0 bug
# 9f8e7d6 feat: add manual RAG pipeline
```

### Step 4: Revert the commit
```bash
git revert a1b2c3d
# Save and close the editor for the commit message: Revert "test: introduce broken chunk_size = 0 bug"
```

### Step 5: Verify history
```bash
git log --oneline -n 3
# Notice both the bad commit AND the revert commit are present and visible!
```
