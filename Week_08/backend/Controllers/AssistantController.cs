using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.EntityFrameworkCore;
using Polly.CircuitBreaker;
using libraryAPI.Services;
using libraryAPI.Data;
using libraryAPI.Models;
using System.Text.Json;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AssistantController : ControllerBase
{
    private readonly IAiServiceClient _aiServiceClient;
    private readonly HttpClient _httpClient;
    private readonly LibraryDbContext _dbContext;
    private readonly ILogger<AssistantController> _logger;
    private readonly string _serviceKey;

    public AssistantController(
        IAiServiceClient aiServiceClient, 
        IHttpClientFactory httpClientFactory,
        LibraryDbContext dbContext,
        ILogger<AssistantController> logger)
    {
        _aiServiceClient = aiServiceClient;
        _httpClient = httpClientFactory.CreateClient(nameof(IAiServiceClient));
        _dbContext = dbContext;
        _logger = logger;
        _serviceKey = Environment.GetEnvironmentVariable("SERVICE_KEY") ?? "nexa-secure-service-key-2026";
    }

    private string? GetCurrentUserId()
    {
        return User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
               ?? User.FindFirst("sub")?.Value
               ?? User.Identity?.Name;
    }

    public record AgentRunRequest(string Question, string? ThreadId);
    public record ResumeRequest(bool Approved);

    /// <summary>
    /// POST: api/assistant/agent/runs
    /// Starts an agent run, streams typed SSE events, creates AgentThread row, returns threadId in first event.
    /// Rate limited per-user using AddRateLimiter policy.
    /// </summary>
    [HttpPost("agent/runs")]
    [Authorize]
    [EnableRateLimiting("PerUserAgentPolicy")]
    public async Task StartAgentRun([FromBody] AgentRunRequest request, CancellationToken clientDisconnectToken)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
        {
            Response.StatusCode = StatusCodes.Status401Unauthorized;
            await Response.WriteAsync("data: {\"error\": \"Unauthorized\"}\n\n", clientDisconnectToken);
            return;
        }

        if (string.IsNullOrWhiteSpace(request.Question))
        {
            Response.StatusCode = StatusCodes.Status400BadRequest;
            await Response.WriteAsync("data: {\"error\": \"Question cannot be empty.\"}\n\n", clientDisconnectToken);
            return;
        }

        // Week 8 Part B: Max question length check (reject, do not silently truncate)
        const int maxQuestionLength = 1000;
        if (request.Question.Length > maxQuestionLength)
        {
            Response.StatusCode = StatusCodes.Status400BadRequest;
            await Response.WriteAsync($"data: {{\"error\": \"Question exceeds maximum allowed length of {maxQuestionLength} characters.\"}}\n\n", clientDisconnectToken);
            return;
        }

        // Week 8 Part B: Daily token budget check per user
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        var dailyBudget = int.TryParse(Environment.GetEnvironmentVariable("DAILY_TOKEN_BUDGET"), out var budget) ? budget : 25000;
        var usedTokensToday = await _dbContext.UsageLogs
            .Where(u => u.UserId == userId && u.Day == today)
            .SumAsync(u => (int?)u.Tokens, clientDisconnectToken) ?? 0;

        if (usedTokensToday >= dailyBudget)
        {
            Response.StatusCode = StatusCodes.Status429TooManyRequests;
            await Response.WriteAsync("data: {\"error\": \"Daily AI token usage limit reached. Try again tomorrow.\", \"status\": 429}\n\n", clientDisconnectToken);
            return;
        }

        var threadId = string.IsNullOrWhiteSpace(request.ThreadId) ? $"thread_{Guid.NewGuid():N}" : request.ThreadId.Trim();

        // Retrieve or create AgentThread row with strict ownership
        var existingThread = await _dbContext.AgentThreads.FirstOrDefaultAsync(t => t.ThreadId == threadId, clientDisconnectToken);
        if (existingThread != null)
        {
            if (existingThread.UserId != userId)
            {
                // Strict ownership: return 404 so thread IDs cannot be probed
                Response.StatusCode = StatusCodes.Status404NotFound;
                await Response.WriteAsync("data: {\"error\": \"Thread not found.\"}\n\n", clientDisconnectToken);
                return;
            }
            existingThread.LastActiveAt = DateTime.UtcNow;
            existingThread.Status = "Active";
        }
        else
        {
            existingThread = new AgentThread
            {
                ThreadId = threadId,
                UserId = userId,
                CreatedAt = DateTime.UtcNow,
                LastActiveAt = DateTime.UtcNow,
                Status = "Active"
            };
            _dbContext.AgentThreads.Add(existingThread);
        }
        await _dbContext.SaveChangesAsync(clientDisconnectToken);

        // Setup SSE response headers
        Response.ContentType = "text/event-stream";
        Response.Headers["Cache-Control"] = "no-cache";
        Response.Headers["Connection"] = "keep-alive";
        Response.Headers["X-Accel-Buffering"] = "no";

        // Forward JWT and X-Service-Key to FastAPI upstream
        var userJwt = Request.Headers.Authorization.ToString().Replace("Bearer ", "").Trim();
        var upstreamRequest = new HttpRequestMessage(HttpMethod.Post, "/agent/run")
        {
            Content = JsonContent.Create(new
            {
                thread_id = threadId,
                user_id = userId,
                question = request.Question
            })
        };
        upstreamRequest.Headers.Add("X-Service-Key", _serviceKey);
        if (!string.IsNullOrEmpty(userJwt))
        {
            upstreamRequest.Headers.Add("X-Forwarded-User-Token", userJwt);
        }

        try
        {
            using var upstreamResponse = await _httpClient.SendAsync(
                upstreamRequest,
                HttpCompletionOption.ResponseHeadersRead,
                clientDisconnectToken
            );

            if (!upstreamResponse.IsSuccessStatusCode)
            {
                Response.StatusCode = (int)upstreamResponse.StatusCode;
                var errPayload = JsonSerializer.Serialize(new
                {
                    @event = "error",
                    code = (int)upstreamResponse.StatusCode,
                    message = $"Upstream AI service error: {upstreamResponse.StatusCode}",
                    retryable = upstreamResponse.StatusCode == System.Net.HttpStatusCode.ServiceUnavailable
                });
                await Response.WriteAsync($"data: {errPayload}\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);
                return;
            }

            await using var upstreamStream = await upstreamResponse.Content.ReadAsStreamAsync(clientDisconnectToken);
            using var reader = new StreamReader(upstreamStream);

            while (!reader.EndOfStream && !clientDisconnectToken.IsCancellationRequested)
            {
                var line = await reader.ReadLineAsync(clientDisconnectToken);
                if (string.IsNullOrEmpty(line)) continue;

                if (line.Contains("\"approval_required\""))
                {
                    existingThread.Status = "Paused";
                    await _dbContext.SaveChangesAsync(CancellationToken.None);
                }
                else if (line.Contains("\"final\""))
                {
                    existingThread.Status = "Completed";
                    
                    // Week 8 Part B: Record token usage in database
                    try
                    {
                        int tokensToRecord = 450; // default estimated baseline per turn
                        var jsonStart = line.IndexOf('{');
                        if (jsonStart >= 0)
                        {
                            using var doc = JsonDocument.Parse(line.Substring(jsonStart));
                            if (doc.RootElement.TryGetProperty("tokens", out var tokensProp))
                            {
                                tokensToRecord = tokensProp.GetInt32();
                            }
                        }

                        _dbContext.UsageLogs.Add(new UsageLog
                        {
                            UserId = userId,
                            Day = today,
                            Tokens = tokensToRecord,
                            RecordedAt = DateTime.UtcNow
                        });
                    }
                    catch { /* fallback gracefully if event line is not json */ }

                    await _dbContext.SaveChangesAsync(CancellationToken.None);
                }

                await Response.WriteAsync(line + "\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);

            }
        }
        catch (BrokenCircuitException ex)
        {
            _logger.LogWarning(ex, "Circuit breaker is OPEN during agent run streaming.");
            var errPayload = JsonSerializer.Serialize(new
            {
                @event = "error",
                code = 503,
                message = "The AI agent service is temporarily unavailable (Circuit Breaker Open).",
                retryable = true
            });
            await Response.WriteAsync($"data: {errPayload}\n\n", clientDisconnectToken);
            await Response.Body.FlushAsync(clientDisconnectToken);
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("Client closed connection mid-run for thread {ThreadId}.", threadId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Streaming error proxying agent run.");
            var errPayload = JsonSerializer.Serialize(new
            {
                @event = "error",
                code = 500,
                message = $"Agent run error: {ex.Message}",
                retryable = false
            });
            await Response.WriteAsync($"data: {errPayload}\n\n", clientDisconnectToken);
            await Response.Body.FlushAsync(clientDisconnectToken);
        }
    }

    /// <summary>
    /// POST: api/assistant/agent/runs/{threadId}/resume
    /// Resumes a paused agent run after user approval or rejection.
    /// Strict ownership check: returns 404 for non-owners (never 403). Idempotent.
    /// </summary>
    [HttpPost("agent/runs/{threadId}/resume")]
    [Authorize]
    public async Task ResumeAgentRun(string threadId, [FromBody] ResumeRequest request, CancellationToken clientDisconnectToken)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
        {
            Response.StatusCode = StatusCodes.Status401Unauthorized;
            return;
        }

        var thread = await _dbContext.AgentThreads.FirstOrDefaultAsync(t => t.ThreadId == threadId, clientDisconnectToken);
        if (thread == null || thread.UserId != userId)
        {
            // Strict security requirement: anyone else gets 404, not 403, so thread IDs cannot be probed
            Response.StatusCode = StatusCodes.Status404NotFound;
            await Response.WriteAsync("data: {\"error\": \"Thread not found.\"}\n\n", clientDisconnectToken);
            return;
        }

        Response.ContentType = "text/event-stream";
        Response.Headers["Cache-Control"] = "no-cache";
        Response.Headers["Connection"] = "keep-alive";
        Response.Headers["X-Accel-Buffering"] = "no";

        var userJwt = Request.Headers.Authorization.ToString().Replace("Bearer ", "").Trim();
        var upstreamRequest = new HttpRequestMessage(HttpMethod.Post, $"/agent/runs/{threadId}/resume")
        {
            Content = JsonContent.Create(new
            {
                thread_id = threadId,
                user_id = userId,
                approved = request.Approved
            })
        };
        upstreamRequest.Headers.Add("X-Service-Key", _serviceKey);
        if (!string.IsNullOrEmpty(userJwt))
        {
            upstreamRequest.Headers.Add("X-Forwarded-User-Token", userJwt);
        }

        try
        {
            using var upstreamResponse = await _httpClient.SendAsync(
                upstreamRequest,
                HttpCompletionOption.ResponseHeadersRead,
                clientDisconnectToken
            );

            if (!upstreamResponse.IsSuccessStatusCode)
            {
                Response.StatusCode = (int)upstreamResponse.StatusCode;
                var errPayload = JsonSerializer.Serialize(new
                {
                    @event = "error",
                    code = (int)upstreamResponse.StatusCode,
                    message = $"Upstream resume error: {upstreamResponse.StatusCode}",
                    retryable = false
                });
                await Response.WriteAsync($"data: {errPayload}\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);
                return;
            }

            thread.Status = "Active";
            thread.LastActiveAt = DateTime.UtcNow;
            await _dbContext.SaveChangesAsync(CancellationToken.None);

            await using var upstreamStream = await upstreamResponse.Content.ReadAsStreamAsync(clientDisconnectToken);
            using var reader = new StreamReader(upstreamStream);

            while (!reader.EndOfStream && !clientDisconnectToken.IsCancellationRequested)
            {
                var line = await reader.ReadLineAsync(clientDisconnectToken);
                if (string.IsNullOrEmpty(line)) continue;

                if (line.Contains("\"final\""))
                {
                    thread.Status = "Completed";
                    await _dbContext.SaveChangesAsync(CancellationToken.None);
                }

                await Response.WriteAsync(line + "\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error resuming agent thread {ThreadId}", threadId);
            var errPayload = JsonSerializer.Serialize(new
            {
                @event = "error",
                code = 500,
                message = $"Resume error: {ex.Message}",
                retryable = false
            });
            await Response.WriteAsync($"data: {errPayload}\n\n", clientDisconnectToken);
            await Response.Body.FlushAsync(clientDisconnectToken);
        }
    }

    /// <summary>
    /// GET: api/assistant/agent/runs/{threadId}
    /// Returns current state for page refresh, including pending approval if paused.
    /// Strict ownership check: returns 404 for non-owners.
    /// </summary>
    [HttpGet("agent/runs/{threadId}")]
    [Authorize]
    public async Task<IActionResult> GetAgentRunState(string threadId, CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId)) return Unauthorized();

        var thread = await _dbContext.AgentThreads.FirstOrDefaultAsync(t => t.ThreadId == threadId, cancellationToken);
        if (thread == null || thread.UserId != userId)
        {
            // Strict ownership requirement: 404 Not Found
            return NotFound(new { message = $"Thread '{threadId}' not found." });
        }

        // Query upstream FastAPI for graph snapshot if available
        try
        {
            var upstreamRequest = new HttpRequestMessage(HttpMethod.Get, $"/agent/runs/{threadId}/state");
            upstreamRequest.Headers.Add("X-Service-Key", _serviceKey);
            var upstreamResponse = await _httpClient.SendAsync(upstreamRequest, cancellationToken);

            if (upstreamResponse.IsSuccessStatusCode)
            {
                var stateData = await upstreamResponse.Content.ReadFromJsonAsync<object>(cancellationToken: cancellationToken);
                return Ok(new
                {
                    threadId = thread.ThreadId,
                    userId = thread.UserId,
                    status = thread.Status,
                    lastActiveAt = thread.LastActiveAt,
                    state = stateData
                });
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Could not fetch state snapshot from FastAPI for thread {ThreadId}", threadId);
        }

        return Ok(new
        {
            threadId = thread.ThreadId,
            userId = thread.UserId,
            status = thread.Status,
            lastActiveAt = thread.LastActiveAt,
            pendingApproval = thread.Status == "Paused"
        });
    }

    /// <summary>
    /// POST: api/assistant/agent/runs/{threadId}/cancel
    /// Cancels a running thread and aborts upstream token generation.
    /// Strict ownership check: returns 404 for non-owners.
    /// </summary>
    [HttpPost("agent/runs/{threadId}/cancel")]
    [Authorize]
    public async Task<IActionResult> CancelAgentRun(string threadId, CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId)) return Unauthorized();

        var thread = await _dbContext.AgentThreads.FirstOrDefaultAsync(t => t.ThreadId == threadId, cancellationToken);
        if (thread == null || thread.UserId != userId)
        {
            return NotFound(new { message = $"Thread '{threadId}' not found." });
        }

        thread.Status = "Cancelled";
        thread.LastActiveAt = DateTime.UtcNow;
        await _dbContext.SaveChangesAsync(cancellationToken);

        // Inform upstream FastAPI to stop generation
        try
        {
            var upstreamRequest = new HttpRequestMessage(HttpMethod.Post, $"/agent/runs/{threadId}/cancel");
            upstreamRequest.Headers.Add("X-Service-Key", _serviceKey);
            await _httpClient.SendAsync(upstreamRequest, cancellationToken);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Notification of cancel to upstream FastAPI returned warning for thread {ThreadId}", threadId);
        }

        return Ok(new
        {
            message = "Agent run cancelled successfully.",
            threadId = thread.ThreadId,
            status = thread.Status
        });
    }

    /// <summary>
    /// POST: api/assistant/ask
    /// Proxies question to upstream FastAPI service through resilient Polly client.
    /// </summary>
    [HttpPost("ask")]
    [AllowAnonymous]
    public async Task<IActionResult> Ask([FromBody] AskDto dto, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(dto.Question))
        {
            return BadRequest(new { message = "Question cannot be empty." });
        }

        try
        {
            var result = await _aiServiceClient.AskAsync(dto.Question, cancellationToken);
            return Ok(result);
        }
        catch (BrokenCircuitException ex)
        {
            _logger.LogWarning(ex, "Circuit breaker is OPEN.");
            return StatusCode(StatusCodes.Status503ServiceUnavailable, new
            {
                message = "The AI assistant is temporarily unavailable. Please try again shortly.",
                status = "CircuitBreakerOpen",
                retryAfterSeconds = 30
            });
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "HTTP failure contacting AI service after retry exhaustion.");
            return StatusCode(StatusCodes.Status503ServiceUnavailable, new
            {
                message = "The AI assistant is temporarily unavailable. Please try again shortly.",
                status = "ServiceUnavailable"
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error in AssistantController.");
            return StatusCode(StatusCodes.Status500InternalServerError, new
            {
                message = "An unexpected error occurred while communicating with the AI service."
            });
        }
    }

    /// <summary>
    /// POST: api/assistant/ask/stream
    /// Backward-compatible SSE stream for Week 6 clients.
    /// </summary>
    [HttpPost("ask/stream")]
    [AllowAnonymous]
    public async Task AskStream([FromBody] AskDto dto, CancellationToken clientDisconnectToken)
    {
        if (string.IsNullOrWhiteSpace(dto.Question))
        {
            Response.StatusCode = StatusCodes.Status400BadRequest;
            await Response.WriteAsync("data: Error: Question cannot be empty.\n\n", clientDisconnectToken);
            return;
        }

        Response.ContentType = "text/event-stream";
        Response.Headers["Cache-Control"] = "no-cache";
        Response.Headers["Connection"] = "keep-alive";
        Response.Headers["X-Accel-Buffering"] = "no";

        var upstreamRequest = new HttpRequestMessage(HttpMethod.Post, "/ask/stream")
        {
            Content = JsonContent.Create(new { question = dto.Question, session_id = dto.SessionId ?? "default_session" })
        };

        try
        {
            using var upstreamResponse = await _httpClient.SendAsync(
                upstreamRequest,
                HttpCompletionOption.ResponseHeadersRead,
                clientDisconnectToken
            );

            if (!upstreamResponse.IsSuccessStatusCode)
            {
                Response.StatusCode = (int)upstreamResponse.StatusCode;
                await Response.WriteAsync($"data: Upstream AI service returned error: {upstreamResponse.StatusCode}\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);
                return;
            }

            await using var upstreamStream = await upstreamResponse.Content.ReadAsStreamAsync(clientDisconnectToken);
            using var reader = new StreamReader(upstreamStream);

            while (!reader.EndOfStream && !clientDisconnectToken.IsCancellationRequested)
            {
                var line = await reader.ReadLineAsync(clientDisconnectToken);
                if (string.IsNullOrEmpty(line)) continue;

                await Response.WriteAsync(line + "\n\n", clientDisconnectToken);
                await Response.Body.FlushAsync(clientDisconnectToken);
            }
        }
        catch (BrokenCircuitException ex)
        {
            _logger.LogWarning(ex, "Circuit breaker is OPEN during streaming request.");
            await Response.WriteAsync("data: The AI assistant is temporarily unavailable. Please try again shortly.\n\n", clientDisconnectToken);
            await Response.WriteAsync("data: [DONE]\n\n", clientDisconnectToken);
            await Response.Body.FlushAsync(clientDisconnectToken);
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("Client closed connection mid-stream. Upstream request aborted.");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Streaming error proxying AI response.");
            await Response.WriteAsync($"data: Streaming error: {ex.Message}\n\n", clientDisconnectToken);
            await Response.WriteAsync("data: [DONE]\n\n", clientDisconnectToken);
            await Response.Body.FlushAsync(clientDisconnectToken);
        }
    }
}

