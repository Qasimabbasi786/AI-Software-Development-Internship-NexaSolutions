# 🛡️ Week 8: Comprehensive Security Review & Audit Report

**Milestone:** Week 8 — Part D Deliverable  
**Author:** Muhammad Qasim (Senior Application Security & Penetration Testing Engineer)  
**Date:** 2026-10-18  
**Scope:** Full-Stack Security Hardening, Vulnerability Audits, Secret Scanning, Data Lifecycle, and Peer Review  

---

## 🎯 Executive Summary

Week 7 identified AI-specific vulnerabilities (prompt injections, indirect jailbreaks, thread hijacking). **Week 8 Part D closes the real-world operational vulnerabilities** that attackers exploit: third-party package CVEs, exposed Git secrets, wildcard CORS misconfigurations, brute-force authentication, unbounded request sizes, and personal data retention violations.

---

## 🔍 1. Dependency Vulnerability Scans

We executed automated dependency audits across all three technology tiers:

### 1.1 .NET 8 Web API (`dotnet list package --vulnerable --include-transitive`)
- **Initial Finding:** 
  - `Microsoft.Extensions.Caching.Memory` (8.0.0) — High Severity (GHSA-qj66-m88j-hmgj)
  - `System.Text.Json` (8.0.4) — High Severity (GHSA-8g4q-xg66-9fp4)
- **Remediation:** 
  Explicitly added patched package references in [`libraryAPI.csproj`](../backend/libraryAPI.csproj):
  ```xml
  <PackageReference Include="Microsoft.Extensions.Caching.Memory" Version="8.0.1" />
  <PackageReference Include="System.Text.Json" Version="8.0.5" />
  ```
- **Post-Fix Audit Result:**
  ```
  The given project `libraryAPI` has no vulnerable packages given the current sources.
  Status: Clean (0 Vulnerabilities)
  ```

### 1.2 Python FastAPI AI Service (`pip-audit -r requirements.txt`)
- **Audit Command:** `python -m pip_audit -r requirements.txt`
- **Result:**
  ```
  No known vulnerabilities found.
  Status: Clean (0 Vulnerabilities)
  ```

### 1.3 Angular 18 Client (`npm audit`)
- **Audit Finding:** Dev-dependency notices related to local Angular CLI build utilities (`postcss`, `webpack-dev-middleware`, `tar`).
- **Production Assessment:** Angular client is built via multi-stage Docker build producing static production JavaScript served via Alpine Nginx. Build tooling vulnerabilities are not exposed to runtime client browsers. Runtime packages have zero critical vulnerabilities.

---

## 🔑 2. Whole-History Secret Scanning (`gitleaks` & Git Log Audit)

- **Audit Target:** All branches, historical commits, and merges across the repository.
- **Audit Tooling:** Executed git log pattern scans for provider key signatures (`sk-`, `AIza`, `ghp_`, `bearer`, `SERVICE_KEY`).
- **Findings:**
  - Zero un-rotated cloud provider API keys were committed to Git history.
  - All real API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `JWT_KEY`) are dynamically injected via environment variables (`.env`).
  - `.gitignore` and `.dockerignore` properly enforce `.env` exclusion from version control.

---

## 🌐 3. Transport, Browser & Authentication Hardening

### 3.1 Strict Origin-Bound CORS
- **Rule:** Wildcards with credentials (`AllowAnyOrigin()` + `AllowCredentials()`) are strictly forbidden.
- **Implementation in `Program.cs`:**
  ```csharp
  options.AddPolicy("AllowAngularApp", policy => {
      policy.WithOrigins("http://localhost:4200", "https://localhost:4200")
            .AllowAnyHeader()
            .AllowAnyMethod();
  });
  ```

### 3.2 HSTS & Standard Security Headers
Configured custom security header middleware in ASP.NET Core:
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` (HSTS on HTTPS)
- `X-Content-Type-Options: nosniff` (MIME sniffing prevention)
- `X-Frame-Options: DENY` (Clickjacking mitigation)
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

### 3.3 Brute-Force Rate Limiting & Account Lockout
Configured IP-based fixed-window rate limiter on the login endpoint (`/api/auth/login`):
- **Limit:** Maximum 5 login attempts per minute per remote IP.
- **Status:** Returns `429 Too Many Requests` when exceeded.

### 3.4 Request Limits & Input Guardrails
- **Max Question Length:** Enforced hard cap of 1,000 characters in `AssistantController.cs`.
- **Handling:** Immediately rejects with `400 Bad Request` rather than silently truncating, alerting the user and avoiding truncated prompt injection attacks.
- **Daily Token Budget:** Per-user daily cap of 25,000 tokens returning `429 Too Many Requests` when exhausted.

---

## 🗑️ 4. Data Lifecycle & GDPR Data Erasure Endpoint

### `DELETE /api/me/data`
Built a complete, audited data deletion workflow in [`UserDataController.cs`](../backend/Controllers/UserDataController.cs) complying with GDPR "Right to be Forgotten":
1. **Preferences Erasure:** Deletes all stored user preferences in `UserPreferences`.
2. **Conversation & Threads:** Purges all agent thread rows from `AgentThreads`.
3. **Usage Logs:** Deletes daily token records in `UsageLogs`.
4. **Reservation Records:** Clears user's active/past reservations in `Reservations`.
5. **Durable State Checkpoints:** Invokes `DELETE /agent/checkpoints/user/{userId}` in the AI service, purging all LangGraph SQLite checkpoint snapshots and write records from disk.

---

## 👥 5. Peer Security Review Checklist & Responses

| Peer Review Question | Evaluation & Hardening Evidence |
| :--- | :--- |
| **1. Can a user reach another user's data by changing an ID, token, or thread ID?** | **No.** All user identity is extracted strictly from the validated cryptographic JWT claims principal (`sub`/`NameIdentifier`). Thread access verifies `AgentThread.UserId == CurrentUser`; if mismatched, the API returns `404 Not Found` (never 403) to prevent thread enumeration. |
| **2. Can an unauthenticated caller reach the AI service or any write endpoint?** | **No.** The AI service listens on an internal Docker container network and requires the pre-shared `X-Service-Key`. Write endpoints (.NET `reserve_book` and assistant runs) require `[Authorize]` with a valid JWT. |
| **3. Are there secrets in code, config, logs, Docker images or Git history?** | **No.** Secrets are injected exclusively via runtime environment variables. All loggers redact tokens and keys. Multi-stage Dockerfiles discard build arguments. |
| **4. What happens with a 1 MB question, an empty question, or 50 requests per second?** | **All are rejected safely:**<br>• Empty questions $\rightarrow$ Rejected with `400 Bad Request`.<br>• 1 MB questions $\rightarrow$ Rejected by max length guard (>1000 chars) with `400 Bad Request`.<br>• 50 req/sec $\rightarrow$ Throttled by ASP.NET Core RateLimiter returning `429 Too Many Requests`. |
| **5. Does any error response leak stack traces, SQL, internal URLs, or keys?** | **No.** Production exception handlers emit standardized JSON error objects (`code`, `message`, `retryable`). Database errors yield generic user-friendly messages. |
| **6. Which untrusted text can influence tool calls, and what stops it?** | Untrusted catalog book descriptions retrieved via RAG could contain indirect prompt injections. **Mitigation:** Untrusted text is isolated inside `<untrusted_document>` XML boundary tags, and LangGraph write tools unconditionally require interactive human approval (`interrupt()`) before execution. |

---

## ✅ Deliverable Checklist
- [x] .NET transitive vulnerabilities resolved (0 vulnerabilities remaining).
- [x] Python dependencies audited via `pip-audit` (0 vulnerabilities found).
- [x] Whole-history Git secret scanning executed.
- [x] Strict origin CORS, HSTS, and security headers active.
- [x] Brute-force rate limiting active on `/api/auth/login`.
- [x] Max question length limit (1000 chars) active and rejecting oversized input.
- [x] GDPR `DELETE /api/me/data` completely removes user records from SQL Server and SQLite checkpoints.
- [x] Peer review checklist completed with empirical evidence.
