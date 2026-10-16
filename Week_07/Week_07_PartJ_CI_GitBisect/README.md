# Part J: Git & GitHub: Continuous Integration and git bisect

## Objectives
- Implement GitHub Actions CI pipeline (`.github/workflows/ci.yml`) covering:
  - `.NET 8` build and unit/integration test execution
  - `Angular 20` dependency installation and compilation
  - `Python 3.12` test suite execution via `pytest`
- Configure branch protection rules enforcing required status checks on `main`.
- Master `git bisect` for binary-search bug isolation across commit history:
  - `git bisect start`
  - `git bisect bad <commit>`
  - `git bisect good <commit>`
  - `git bisect run pytest -q`
  - `git bisect reset`
- Maintain secret hygiene: zero API keys, JWT tokens, or SQLite database files committed to source control.

## Deliverables
- Validated CI workflow definition in `.github/workflows/ci.yml`.
- `git bisect` run log demonstrating automated isolation of regression commits.
- Interactive rebase documentation before opening Pull Requests.
