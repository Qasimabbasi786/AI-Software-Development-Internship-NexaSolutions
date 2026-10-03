# Week 6 — Part G: Git — Cleaning History with Interactive Rebase

## 🌟 Executive Summary
Interactive rebase (`git rebase -i`) is an essential engineering tool for maintaining clean, readable, and professional commit histories before merging code into shared branches. This module covers interactive rebasing techniques, squash workflows, safety rules, and conflict resolution protocols.

For the complete technical blueprint, commands reference, and step-by-step walkthrough, refer to:
👉 **[Comprehensive Git Rebase Guide (git_rebase_guide.md)](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_06/Week_06_PartG_GitRebase/git_rebase_guide.md)**

---

## 🔑 Key Principles at a Glance

1. **Why Interactive Rebase?**
   - Collapses intermediate work-in-progress (`wip`, `fix typo`, `test fix`) commits into cohesive, logical commits.
   - Preserves high signal-to-noise ratio in repository history for easier code reviews and automated bisecting.

2. **Branch Safety Policy:**
   - **Allowed:** Only unshared, private local feature branches prior to PR merge.
   - **Forbidden:** Never rebase `main`, `master`, or any shared upstream branch.

3. **Safe Remote Updates:**
   - Always use `git push --force-with-lease` rather than `git push --force` to prevent overwriting collaborators' recent commits.

4. **Conflict Resolution:**
   - Resolve conflicts $\rightarrow$ `git add <file>` $\rightarrow$ `git rebase --continue`.
   - Never run `git commit` mid-rebase. Use `git rebase --abort` to safely rollback if needed.
