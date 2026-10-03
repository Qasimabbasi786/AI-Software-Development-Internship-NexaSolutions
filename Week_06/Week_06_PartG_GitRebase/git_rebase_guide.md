# Week 6 — Part G: Cleaning History with Interactive Rebase

## 🌟 Overview & Purpose
In active software development, commit history is often messy. Developers commit incrementally with messages like `"wip"`, `"fix typo"`, `"try again"`, and `"actually works now"`. While this is normal during exploratory local development, shipping this messy commit clutter to the shared repository makes code review difficult, pollutes `git log`, and impairs `git bisect` automated debugging.

**Interactive Rebase** (`git rebase -i`) gives developers the power to rewrite local commit history on their private feature branches before opening a Pull Request, presenting a clean, linear, and well-documented narrative of the change.

---

## 🔒 Crucial Git Safety Policies

### 1. Rebase is strictly for Private / Unshared Feature Branches
> [!CAUTION]
> **NEVER rebase `main`, `master`, or any public shared branch!**
> Rebase fundamentally recalculates SHA-1 commit hashes. When you rebase commits that other developers have already cloned or pulled, their local repositories will diverge from the remote branch, resulting in repeated merge conflicts and accidental commit resurrection when they push.
>
> **Golden Rule of Git Rebase:** Only rebase commits that exist solely on your private local branch and have not been built upon by teammates.

### 2. Pushing Rebased Branches: `--force-with-lease` vs `--force`
Once a branch history is rewritten locally, standard `git push` will fail with `[rejected - non-fast-forward]` because the commit tree diverged.

- ❌ **`git push --force` (Destructive):** Blindly overwrites the remote branch with your local history. If a collaborator pushed a commit to your branch in the interim, their work is permanently destroyed.
- ✅ **`git push --force-with-lease` (Safe & Protected):** Checks that the remote branch matches your local tracking ref (`origin/branch`) before overwriting. If anyone else pushed commits to the branch while you were rebasing, Git aborts the push, preventing accidental data loss.

---

## 🛠️ Interactive Rebase Commands & Options

When executing:
```bash
git rebase -i HEAD~N
```
Git launches an interactive editor listing commits from oldest to newest with command verbs:

| Command | Shorthand | Description | Use Case |
| :--- | :--- | :--- | :--- |
| `pick` | `p` | Keep commit as-is | Baseline commits you want to preserve |
| `reword` | `r` | Keep commit contents, but edit message | Fix typos or apply conventional commit formatting |
| `edit` | `e` | Stop for amending before continuing | Add forgotten files or split a large commit |
| `squash` | `s` | Melt commit into previous commit & combine messages | Fold WIP or typo fixes into the main feature commit |
| `fixup` | `f` | Melt commit into previous commit & discard message | Fold small tweaks silently into the parent commit |
| `drop` | `d` | Delete commit entirely | Remove accidental experiments or debug logs |

---

## 📋 Step-by-Step Hands-On Rebase & Squash Workflow

### Scenario:
You made 4 messy commits while implementing a feature:
1. `9c66a02 wip: start draft implementation`
2. `6b91f51 try again: tweak logic`
3. `7a08a6b fix: typo in comments`
4. `18654ce actually works now`

### Execution Sequence:
1. **Start Interactive Rebase:**
   ```bash
   git rebase -i HEAD~4
   ```

2. **Configure Commit Actions in the Editor:**
   ```text
   pick 9c66a02 wip: start draft implementation
   squash 6b91f51 try again: tweak logic
   squash 7a08a6b fix: typo in comments
   squash 18654ce actually works now
   ```

3. **Synthesize Final Conventional Commit Message:**
   In the second editor that appears, replace all messy comments with one clean, unified message:
   ```text
   feat(git-rebase): implement interactive rebase workflow and document best practices
   ```

4. **Verify Clean History:**
   ```bash
   git log --oneline -n 3
   ```
   All 4 messy commits are now collapsed into a single clean commit with a single unified diff!

5. **Safe Push to Remote:**
   ```bash
   git push origin feature/my-feature --force-with-lease
   ```

---

## ⚠️ Handling Rebase Conflicts

When Git applies each commit sequentially during a rebase, conflicts may occur:

1. **Check Status:**
   ```bash
   git status
   ```
   Git will report `rebase in progress` and list the conflicting files under `Unmerged paths:`.

2. **Resolve Conflicted Files:**
   Open each conflicted file, resolve the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), and save.

3. **Stage Resolved Files:**
   ```bash
   git add <resolved_file>
   ```
   > [!NOTE]
   > Do **NOT** run `git commit` during a rebase!

4. **Continue Rebase:**
   ```bash
   git rebase --continue
   ```

5. **Abort if Needed:**
   If the rebase becomes tangled and you want to safely restore your branch to its exact initial state:
   ```bash
   git rebase --abort
   ```

---

## 🎯 Verification & Evidence
For Week 6 Part G, the clean, squashed commit on the feature branch serves as permanent proof of mastering interactive rebasing and commit history hygiene.
