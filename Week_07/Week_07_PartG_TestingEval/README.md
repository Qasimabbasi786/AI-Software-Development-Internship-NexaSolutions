# Week 7 — Part G: Testing, Evaluation & Tracing

## 📌 Executive Summary
Part G establishes two fundamentally different testing disciplines:
1. **Deterministic Testing**: Verifies components whose behavior is strictly reproducible with zero LLM API dependency (routing functions, retry thresholds, Pydantic boundaries, HTTP status code translation, ASP.NET Core endpoints).
2. **Non-Deterministic Evaluation**: Evaluates stochastic model trajectories across 10 structured scenarios to establish reliable pass rates, token metrics, and latency budgets.

---

## 🏗️ Architecture & Dual Testing Pipeline

```mermaid
graph TD;
    subgraph Deterministic Testing (Every Commit / CI)
        Pytest[Pytest + respx] --> SchemaValidation[Pydantic Args Validation: gt=0]
        Pytest --> ErrorMapping[HTTP 409/404/401/Timeout -> Tool Data Strings]
        Pytest --> GuardrailsTest[Input/Output Security RegEx Filter]
        
        DotNetTests[xUnit + WebApplicationFactory] --> AuthTests[JWT Claim Extraction & 401 Rejections]
        DotNetTests --> IdempotencyTests[Same Idempotency-Key -> 1 DB Row]
        DotNetTests --> OwnershipTests[Thread Ownership Validation -> 404 on Hijack]
    end

    subgraph Non-Deterministic Evaluation (Scheduled & Monitored)
        EvalSuite[10-Scenario Evaluation Suite] --> TrajectoryCheck[Tool Call Sequence Inspection]
        EvalSuite --> TokenTracker[Token Count & Latency Benchmarks]
        EvalSuite --> LangSmith[LangSmith Tracing: Pass/Fail Traces]
    end
```

---

## 🔑 Core Concepts Mastered

### 1. Deterministic vs Non-Deterministic Testing

| Testing Tier | Technology | Execution Trigger | API Key Required? | Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **Python Unit/Mock Suite** | `pytest`, `respx` | Every Commit / PR | **No** (Mocked) | Pydantic boundaries, secret sanitization, error mapping. |
| **.NET Integration Suite**| `xUnit`, `WebApplicationFactory` | Every Commit / PR | **No** (In-Memory DB) | JWT auth claims, idempotency key replays, 404 isolation. |
| **LLM Evaluation Matrix** | Python Evaluation Suite | Nightly / Release Gate | **Yes** (Google Gemini) | 10-scenario trajectory accuracy, token usage, latency. |
| **Agent Observability** | LangSmith | Continuous Staging | **Yes** (LangSmith) | Visual node execution trees, failure and re-plan traces. |

### 2. 10-Scenario Evaluation Matrix Summary
- Full benchmark matrix documented in [`docs/week7-eval-report.md`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/docs/week7-eval-report.md).
- Verified trajectory compliance across Happy Path, 409 Conflict Re-planning, User Rejection handling, Prompt Injections, and Chitchat routing.

---

## 🛠️ Implementation Details & Commands

- **Python Deterministic Suite (15 tests):**
  ```bash
  D:\Software\PythonEnvironments\AI_env\Scripts\python.exe -m pytest Week_07_Final_Project/ai-services/tests/test_deterministic_suite.py
  ```
- **.NET Integration Suite (9 tests):**
  ```bash
  D:\Software\dotnet\dotnet.exe test Week_07_Final_Project/backend/tests/libraryAPI.Tests.csproj
  ```
- **Automated Evaluation Suite:**
  ```bash
  D:\Software\PythonEnvironments\AI_env\Scripts\python.exe Week_07_PartG_TestingEval/eval_suite.py
  ```

---

## ✅ Verification Checklist
- [x] 15/15 deterministic pytest tests passing in < 3s without external API dependencies.
- [x] 9/9 backend xUnit integration tests passing on in-memory SQLite.
- [x] 10-scenario trajectory evaluation executed across repeated runs.
- [x] LangSmith tracing configuration established for pass and conflict re-plan runs.
