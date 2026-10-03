# Week 6 — Part E: Resilient .NET $\rightarrow$ AI Service Integration (Production-Grade)

## 🌟 Overview
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
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │       IAiServiceClient (Polly)       │
                      │                                      │
                      │   [Circuit Breaker Policy]           │
                      │   - 3 consecutive failures trips     │
                      │   - 30-second cooldown period        │
                      │   - Fail-fast BrokenCircuitException │
                      │                                      │
                      │   [Wait & Retry Policy]              │
                      │   - 3 attempts                       │
                      │   - Exponential backoff: 2^attempt   │
                      │                                      │
                      │   [Timeout Policy]                   │
                      │   - 10s per request attempt          │
                      └──────────────────┬───────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │ Success                                       │ Upstream Down / Tripped
                 ▼                                               ▼
  ┌──────────────────────────────┐                ┌──────────────────────────────┐
  │  FastAPI Upstream AI Service │                │  Catch BrokenCircuitException│
  │    (POST /ask -> Gemini)     │                │   -> Returns HTTP 503        │
  └──────────────────────────────┘                │  "AI Assistant is temporarily│
                                                  │   unavailable. Try shortly." │
                                                  └──────────────────────────────┘
```

---

## 💻 .NET Implementation Details

### 1. Polly Policy Configuration ([Program.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_06/Week_06_Final_Project/backend/Program.cs))
```csharp
builder.Services.AddHttpClient<IAiServiceClient, AiServiceClient>(client =>
{
    client.BaseAddress = new Uri(aiServiceUrl);
    client.Timeout = TimeSpan.FromSeconds(10);
})
.AddPolicyHandler(GetRetryPolicy())
.AddPolicyHandler(GetCircuitBreakerPolicy());

static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy() =>
    HttpPolicyExtensions.HandleTransientHttpError()
        .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)));

static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy() =>
    HttpPolicyExtensions.HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 3,
            durationOfBreak: TimeSpan.FromSeconds(30)
        );
```

### 2. Graceful Degradation Controller ([AssistantController.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_06/Week_06_Final_Project/backend/Controllers/AssistantController.cs))
```csharp
[HttpPost("ask")]
[AllowAnonymous]
public async Task<IActionResult> Ask([FromBody] AskDto dto, CancellationToken cancellationToken)
{
    try
    {
        var result = await _aiServiceClient.AskAsync(dto.Question, cancellationToken);
        return Ok(result);
    }
    catch (BrokenCircuitException ex)
    {
        _logger.LogWarning(ex, "Circuit breaker is OPEN. Fast-failing with 503.");
        return StatusCode(StatusCodes.Status503ServiceUnavailable, new
        {
            message = "The AI assistant is temporarily unavailable. Please try again shortly.",
            status = "CircuitBreakerOpen",
            retryAfterSeconds = 30
        });
    }
}
```

---

## 🔬 Challenge & Failure Analysis

### 1. Why Immediate Retries Without Backoff Make Outages Worse
When a downstream microservice or LLM provider experiences elevated load, memory saturation, or thread pool exhaustion, incoming requests take longer to complete or time out. 
- **The Retry Storm (Thundering Herd):** If 100 client requests fail and every caller immediately retries 3 times with 0 delay, the struggling service instantly receives 300 additional requests right when its CPU or connection pool is already at 100% capacity.
- **Why Exponential Backoff Matters:** Backing off ($2^1 = 2s$, $2^2 = 4s$, $2^3 = 8s$) introduces progressive delays that give the downstream service idle time to drain buffers, garbage collect, and stabilize before the next request arrives.

### 2. Transient vs. Non-Transient Failures: The Danger of Non-Idempotent Retries
- **Transient Failures (Safe to Retry):**
  - TCP handshake timeouts, dropped packets, DNS resolution glitches, HTTP 503 Service Unavailable, or HTTP 429 Rate Limit. These errors indicate that the downstream service has not begun processing the request payload and no state mutations or billable tokens have been consumed.
- **Non-Transient / Stateful Failures (Dangerous to Retry):**
  - HTTP 400 Bad Request or HTTP 422 Unprocessable Entity will *never* succeed on retry because the payload is semantically invalid.
  - If a POST request has *already partially succeeded* on the AI server (e.g., embedding creation started or paid Gemini API tokens were dispatched), retrying the entire HTTP request duplicates upstream API credit consumption and risks generating conflicting records.

---

## 🛠️ Verifying Resilience Under Failure
To observe the circuit breaker in action:
1. Stop the FastAPI microservice (`Ctrl + C` or shut down port 8000).
2. Call `POST http://localhost:5000/api/assistant/ask` 4 times in rapid succession:
   - **Attempts 1 to 3:** Notice execution pauses according to exponential backoff ($2s, 4s, 8s$) before returning failure.
   - **Attempt 4+:** The circuit breaker trips into the **OPEN** state. The response returns in under 5ms with **HTTP 503 (CircuitBreakerOpen)**, completely skipping outbound network calls.
