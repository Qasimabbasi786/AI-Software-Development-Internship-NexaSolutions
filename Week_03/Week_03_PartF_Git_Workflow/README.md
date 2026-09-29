# Week 3 - Part F: Professional Git & GitHub Workflow

## 📌 Overview
This part establishes industry-standard Git version control practices, feature branching, standard commit conventions, Pull Request (PR) reviews, and repository secret management.

## 🎯 Technical Concepts
- **Git Branching Strategy**: Isolated feature branches off `main` (e.g. `feature/relational-schema`, `feature/ef-core-setup`).
- **Conventional Commits**:
  - `feat:` (new feature)
  - `fix:` (bug fix)
  - `docs:` (documentation)
  - `chore:` (configuration/migrations)
  - `refactor:` (restructuring code without behavior changes)
- **Pull Requests & Code Reviews**: Reviewing code diffs prior to merging into `main`.
- **Secret Hygiene**: Strict exclusion of `.env`, connection strings, and API keys using `.gitignore`.
- **Milestone Tagging**: Tagging final releases (e.g. `git tag -a v0.3-week3`).

## 📁 Branching Plan for Week 3
| Branch Name | Scope / Target Part |
| :--- | :--- |
| `feature/relational-schema` | Part A - PostgreSQL SQL Scripts |
| `feature/ef-core-setup` | Part B - EF Core Models, DbContext & Migrations |
| `feature/api-db-integration` | Part C - API Repository Swap |
| `feature/angular-http-integration` | Part E - Angular Client HTTP Services |
| `feature/ai-summary-script` | Part G - Python AI Foundation Script |

## 📝 Execution Checklist & Verification
- [ ] Verify root `.gitignore` excludes binaries, `.env`, `appsettings.Development.json`, `node_modules`, `.venv`
- [ ] Maintain clean linear history with PR descriptions
- [ ] Ensure zero secrets committed in Git history
