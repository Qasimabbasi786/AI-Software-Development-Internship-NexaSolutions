# Week 4 - Part F: Git & GitHub, Level Up

## 🎯 Objectives
- Understand why merge conflicts happen and how Git demarcates conflicts (`<<<<<<<`, `=======`, `>>>>>>>`).
- Practice resolving real merge conflicts manually by hand.
- Configure repository **Branch Protection Rules** on `main` to require Pull Requests and approvals before merging.
- Create and adopt `.github/PULL_REQUEST_TEMPLATE.md` to standardize PR descriptions, testing checklists, and review quality.

---

## 🛠️ Step-by-Step Merge Conflict Practice

### 1. Create two parallel branches from `main`
```bash
git checkout main
git checkout -b practice/conflict-a

# Edit line in a practice file, commit
git commit -am "test: update description in conflict-a"

git checkout main
git checkout -b practice/conflict-b

# Edit the SAME line differently, commit
git commit -am "test: update description in conflict-b"
```

### 2. Merge Branch A into Main
```bash
git checkout main
git merge practice/conflict-a   # Merges cleanly!
```

### 3. Merge Branch B into Main (Triggers Conflict)
```bash
git merge practice/conflict-b   # Git reports CONFLICT
```

### 4. Resolve the Conflict
Open the conflicting file, inspect the markers:
```text
<<<<<<< HEAD
Version from branch A (currently on main)
=======
Version from branch B
>>>>>>> practice/conflict-b
```
1. Manually edit the file to the unified intended state.
2. Remove all conflict marker lines (`<<<<<<<`, `=======`, `>>>>>>>`).
3. Stage and commit:
```bash
git add .
git commit -m "fix: resolve merge conflict between branch A and B"
```

---

## 🔒 Branch Protection Setup on GitHub
1. Go to your GitHub repository -> **Settings** -> **Branches**.
2. Click **Add branch protection rule**.
3. Set Branch name pattern: `main`.
4. Enable:
   - [x] **Require a pull request before merging**
   - [x] **Require approvals** (minimum 1 approval)
   - [x] **Do not allow bypassing the above settings**
5. Save changes.

---

## 🌿 Git Checkpoint
```bash
git checkout -b chore/pull-request-template
git add .github/PULL_REQUEST_TEMPLATE.md
git commit -m "chore: add pull request template"
```
