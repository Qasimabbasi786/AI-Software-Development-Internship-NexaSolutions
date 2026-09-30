# Week 4 - Part F: Git & GitHub, Level Up

## 📌 Executive Summary
In **Week 4 - Part F**, we level up our DevOps and source control engineering discipline through:
1. **Deliberate Merge Conflict Creation & Resolution**: Understanding Git 3-way merge mechanics and resolving textual conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) by hand.
2. **Standardized Pull Request Architecture**: Adopting `.github/PULL_REQUEST_TEMPLATE.md` to enforce rigorous documentation, test plans, and architectural review checklists.
3. **Enterprise GitHub Branch Protection Strategies**: Implementing policy guardrails on `main` to safeguard against unreviewed regressions and accidental direct pushes.

---

## 🏗️ Directory Contents

```
Week_04_PartF_GitPractice/
├── conflict_exercise.txt        # Verified artifact resulting from resolved conflict simulation
└── README.md                    # In-depth technical guide & DevOps reference manual

.github/
└── PULL_REQUEST_TEMPLATE.md     # Production pull request template for GitHub repositories
```

---

## ⚔️ Merge Conflict Mechanics & Resolution Walkthrough

### 1. Why Do Merge Conflicts Occur?
Git tracks file changes as Directed Acyclic Graphs (DAGs) of commits. When two divergent branches modify the **exact same line** (or adjacent lines) of a file since their common ancestor (`merge-base`), Git cannot deterministically determine which version is authoritative. It pauses the merge operation and embeds standard **conflict markers**.

### 2. Anatomy of Git Conflict Markers
When Git halts an automatic merge, it writes conflict blocks directly into the working tree file:

```text
<<<<<<< HEAD
Project Status: Branch A updated status to ACTIVE_DEVELOPMENT with feature auth pipeline.
Team Lead: AI Core Architect (Branch A Lead)
=======
Project Status: Branch B changed status to SECURITY_HARDENED with JWT validation.
Team Lead: Security & DevOps Architect (Branch B Lead)
>>>>>>> practice/conflict-b
```

| Marker Segment | Meaning |
| :--- | :--- |
| `<<<<<<< HEAD` | Denotes the start of the conflicting section in the **currently checked out branch** (e.g. `feature/git-workflow-level-up` or `main`). |
| `=======` | The divider separating the conflicting changes from the two incoming branches. |
| `>>>>>>> <branch_name>` | Denotes the end of the conflict section, originating from the **incoming branch being merged** (`practice/conflict-b`). |

### 3. Step-by-Step Hands-on Exercise Performed
We executed an end-to-end conflict and resolution workflow:

```bash
# 1. Created baseline tracking file
git checkout -b feature/git-workflow-level-up
# created conflict_exercise.txt
git commit -m "chore: add baseline file for merge conflict simulation"

# 2. Branch A branch-off & modification
git checkout -b practice/conflict-a
# modified line 3 & 4
git commit -am "feat: update status from branch A"

# 3. Branch B branch-off & competing modification
git checkout feature/git-workflow-level-up
git checkout -b practice/conflict-b
# modified line 3 & 4 with conflicting text
git commit -am "feat: update status from branch B"

# 4. Merging Branch A (Clean Fast-Forward)
git checkout feature/git-workflow-level-up
git merge practice/conflict-a

# 5. Merging Branch B (Triggers CONFLICT)
git merge practice/conflict-b
# Output:
# Auto-merging Week_04_PartF_GitPractice/conflict_exercise.txt
# CONFLICT (content): Merge conflict in Week_04/Week_04_PartF_GitPractice/conflict_exercise.txt
# Automatic merge failed; fix conflicts and then commit the result.
```

### 4. Manual Resolution Process
1. Inspect conflicting files using `git status` (`both modified: conflict_exercise.txt`).
2. Open the file, evaluate both engineering intents, and combine them into a unified solution:
   ```text
   # Conflict Simulation Sandbox
   This file is used to demonstrate and resolve deliberate merge conflicts.
   Project Status: UNIFIED_ARCHITECTURE - Combines ACTIVE_DEVELOPMENT with SECURITY_HARDENED JWT validation.
   Team Lead: AI Core Architect & Security DevOps Architect (Joint Leadership)
   Maintainer: Nexa Solutions Software Engineering Team
   ```
3. Strip all `<<<<<<<`, `=======`, and `>>>>>>>` markers.
4. Mark resolved by staging the file:
   ```bash
   git add Week_04/Week_04_PartF_GitPractice/conflict_exercise.txt
   ```
5. Finalize the merge commit:
   ```bash
   git commit -m "fix: resolve merge conflict between branch practice/conflict-a and practice/conflict-b"
   ```

### 5. Verified Commit Graph (`git log --graph --oneline`)
```text
*   a3bec38 fix: resolve merge conflict between branch practice/conflict-a and practice/conflict-b
|\  
| * 650262b feat: update status from branch B
* | 679d559 feat: update status from branch A
|/  
* aed43a2 chore: add baseline file for merge conflict simulation
```

---

## 📋 Standardized Pull Request Template Architecture

The file [`.github/PULL_REQUEST_TEMPLATE.md`](file:///.github/PULL_REQUEST_TEMPLATE.md) ensures all contributors provide necessary architectural context before code review:

### Mandatory Sections:
1. **📌 What Changed**: Bulleted high-level summary of the features, bug fixes, or refactors.
2. **🎯 Related Branch & Part**: Identifies target branch, source feature branch, and sprint week.
3. **🧪 How It Was Tested**: Verification commands across .NET (`dotnet test`), Angular (`ng test` / `ng build`), and Python (`pytest`).
4. **📸 Screenshots & Evidence**: Visual proof of UI components, Postman/Swagger responses, or token stream output.
5. **🛡️ Pre-Merge Checklist**: Mandatory assertions guaranteeing no leaked API keys or credentials, clean build, and passing unit tests.

---

## 🛡️ Enterprise Branch Protection Rules for `main`

To maintain production stability in team and enterprise settings, direct pushes to `main` must be disabled.

### Recommended GitHub Branch Protection Configuration:
1. Navigate to: **Repository -> Settings -> Branches -> Add branch protection rule**.
2. **Branch name pattern**: `main`
3. **Enforce Core Guardrails**:
   - [x] **Require a pull request before merging**: Disallows accidental direct `git push origin main`.
   - [x] **Require approvals**: Set minimum required approvals to **1** (or 2 for production releases).
   - [x] **Dismiss stale pull request approvals when new commits are pushed**: Forces re-review if the author pushes changes after an initial approval.
   - [x] **Require status checks to pass before merging**: Blocks merge until CI builds (`dotnet build`, Angular build, Python lint) pass.
   - [x] **Require conversation resolution before merging**: All reviewer comments and change requests must be marked resolved.
   - [x] **Do not allow bypassing the above settings**: Applies rules strictly to Administrators as well.

---

## 🌿 Git Checkpoint Commit
```bash
git add .github/PULL_REQUEST_TEMPLATE.md Week_04/Week_04_PartF_GitPractice/
git commit -m "chore: add pull request template"
```
