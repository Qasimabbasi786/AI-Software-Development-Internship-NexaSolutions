# Week 7 - Part G: Testing, Evaluation & Tracing

## Executive Summary & Architecture Blueprint
Part G establishes two fundamentally different testing disciplines:
1. **Deterministic Testing**: Verifies components whose behavior is strictly reproducible and never calls an LLM (routing functions, retry thresholds, Pydantic boundaries, HTTP status code translation, ASP.NET Core endpoints).
2. **Non-Deterministic Evaluation**: Evaluates stochastic model trajectories across 10 structured scenarios to establish reliable pass rates, token metrics, and latency budgets.

---

## 1. Testing Architecture Overview

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

## 2. Deliverables Summary
- **Python Deterministic Suite**: [`ai-services/tests/test_deterministic_suite.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/tests/test_deterministic_suite.py) (15 tests covering schema boundaries, respx HTTP mocking, and guardrail filters - all passing).
- **.NET Integration Tests**: [`backend/tests/ReservationIntegrationTests.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/backend/tests/ReservationIntegrationTests.cs) and [`CustomWebApplicationFactory.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/backend/tests/CustomWebApplicationFactory.cs) (testing 401s, idempotency, and SQLite in-memory isolation).
- **Evaluation Runner**: [`ai-services/tests/eval_suite.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/tests/eval_suite.py) (benchmarking pass rates across 10 scenarios).
- **Official Evaluation Report**: Complete analysis and metrics matrix documented in [`docs/week7-eval-report.md`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/docs/week7-eval-report.md).
