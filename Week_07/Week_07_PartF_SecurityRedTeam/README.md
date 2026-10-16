# Week 7 - Part F: Agent Safety & AI Security (Red-Team Your Own Agent)

## Executive Summary & Architecture Blueprint
Part F enforces defense-in-depth security principles across the autonomous agent lifecycle. The governing philosophy is simple: **assume the model will occasionally be fooled, and design deterministic external controls so that damage is strictly bounded.**

```mermaid
graph TD;
    User[User Input] --> InputGuard[SecurityGuardrails: validate_input];
    InputGuard -. "Malicious override detected" .-> RejectInput[Reject / Flag Input];
    InputGuard --> Agent[Agent LLM Node];
    
    Catalog[(Catalog DB)] --> UntrustedWrapper[wrap_untrusted: XML Delimiters];
    UntrustedWrapper --> Agent;
    
    Agent --> ToolChoice{Tool Calling Decision};
    ToolChoice -. "Risky Write Tool (reserve_book)" .-> ApprovalNode[approval_node: interrupt];
    ApprovalNode -. "Human Approval Rejected" .-> RejectionMsg[ToolMessage: REJECTED_BY_USER];
    ApprovalNode -. "Human Approved" .-> NetAPI[.NET Web API: [Authorize] + JWT];
    
    NetAPI --> CheckIdempotency{Verify IdempotencyKey};
    CheckIdempotency --> SQLServer[(SQL Server DB)];
    
    Agent --> OutputFilter[SecurityGuardrails: sanitize_output];
    OutputFilter --> RenderUI[Angular UI Stream];

    classDef default fill:#f2f0ff,line-height:1.2;
    classDef reject fill:#ffdede;
    class RejectInput reject;
```

---

## 1. Clean Security Architecture Subdirectory
All Part F security components are organized inside [`ai-services/security/`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/security):
- [`untrusted_wrapper.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/security/untrusted_wrapper.py): Implements `wrap_untrusted()`, encapsulating retrieved database text inside `<untrusted_document>` tags.
- [`guardrails.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/security/guardrails.py): Implements input prompt injection detection and output regex-based secret sanitization (`sanitize_output`).
- [`red_team_harness.py`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/Week_07_Final_Project/ai-services/security/red_team_harness.py): The 7-attack automated test harness verifying all defense layers.

---

## 2. The 7-Attack Test Suite Summary
Detailed results, before/after analysis, and residual risks are documented in [`docs/week7-red-team-report.md`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_07/docs/week7-red-team-report.md):
1. **Indirect Injection via Data**: Neutralized by XML delimiters and mandatory `approval_node` interrupt.
2. **Direct Override**: Blocked by input guardrails and per-turn step limits.
3. **Cross-User Access**: Neutralized by ASP.NET Core deriving user identity strictly from cryptographically verified JWT claims.
4. **Secret Extraction**: Neutralized by regex sanitization and omitting secrets from graph state.
5. **Argument Abuse**: Neutralized by Pydantic `args_schema` (`gt=0`) and EF Core parameterization.
6. **Resource Exhaustion**: Neutralized by LangGraph `MAX_STEPS = 6` and ASP.NET Core `AddRateLimiter`.
7. **Thread Hijacking**: Neutralized by `AgentThread` ownership cross-checks returning `404 Not Found`.
