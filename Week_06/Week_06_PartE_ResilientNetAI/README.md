# Week 6 — Part E: Resilient .NET $\rightarrow$ AI Service Integration (Production-Grade)

## 📌 Executive Summary
Service-to-service communication between the **ASP.NET Core Web API** and the **FastAPI AI Microservice** is susceptible to network jitter, transient downstream failures, and model latency spikes. 

Rather than relying on unhandled `HttpClient` calls that hang and crash with HTTP 500 errors, Part E integrates **Polly** resilience policies with `IHttpClientFactory` to provide:
1. **Typed HttpClient**: `IAiServiceClient` / `AiServiceClient`.
2. **Transient Error Retry**: Exponential backoff with jitter.
3. **Timeout Enforcement**: Prevents slow upstream AI calls from exhausting the ASP.NET Core thread pool.
4. **Circuit Breaker**: Trips open after consecutive failures to protect downstream infrastructure.
5. **Graceful Degradation**: Catches `BrokenCircuitException` and responds with HTTP 503 rather than an unhandled crash.

---

## 🏗️ Architecture: Resilient Service-to-Service Flow

```
                      ┌──────────────────────────────────────┐
                      │    Angular Frontend / Client Request │
                      └──────────────────┬───────────────────┘
                                         │ POST /api/assistant/ask
                                         ▼
                      ┌──────────────────────────────────────┐
                      │  ASP.NET Core: AssistantController   │
                      └──────────────────┬───────────────────┘
                                         │ Injects IAiServiceClient
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    Resilient Polly Policy Pipeline   │
                      │ ┌──────────────────────────────────┐ │
                      │ │  1. Timeout Policy (10s max)     │ │
                      │ └────────────────┬─────────────────┘ │
                      │                  ▼                   │
                      │ ┌──────────────────────────────────┐ │
                      │ │  2. Retry Policy (3x Backoff)    │ │
                      │ └────────────────┬─────────────────┘ │
                      │                  ▼                   │
                      │ ┌──────────────────────────────────┐ │
                      │ │  3. Circuit Breaker (3 fails/30s)│ │
                      │ └────────────────┬─────────────────┘ │
                      └──────────────────┼───────────────────┘
                                         │ Upstream HTTP Call
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    FastAPI AI Microservice (:8000)   │
                      └──────────────────────────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Polly Policies in ASP.NET Core 8
- **Exponential Backoff:** `WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)))` (delays of 2s, 4s, 8s).
- **Circuit Breaker:** `CircuitBreakerAsync(3, TimeSpan.FromSeconds(30))` isolates failing dependencies.

### 2. Error Boundary Handling
When the circuit is broken, `AssistantController` catches `BrokenCircuitException` and immediately returns:
```json
{
  "message": "The AI assistant is temporarily unavailable. Please try again shortly.",
  "status": "CircuitBreakerOpen",
  "retryAfterSeconds": 30
}
```

---

## 🛠️ Verification & Build Commands

```powershell
# Build verification in backend project
cd "Week_06/Week_06_Final_Project/backend"
& "D:\Software\dotnet\dotnet.exe" build --no-restore
```
