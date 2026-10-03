using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Polly.CircuitBreaker;
using libraryAPI.Services;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AssistantController : ControllerBase
{
    private readonly IAiServiceClient _aiServiceClient;
    private readonly HttpClient _httpClient;
    private readonly ILogger<AssistantController> _logger;

    public AssistantController(
        IAiServiceClient aiServiceClient, 
        IHttpClientFactory httpClientFactory,
        ILogger<AssistantController> logger)
    {
        _aiServiceClient = aiServiceClient;
        _httpClient = httpClientFactory.CreateClient(nameof(IAiServiceClient));
        _logger = logger;
    }

    /// <summary>
    /// POST: api/assistant/ask
    /// Proxies question to upstream FastAPI service through resilient Polly client.
    /// Returns 503 Service Unavailable with degraded notice if circuit is open.
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
            _logger.LogWarning(ex, "Circuit breaker is OPEN. Downstream AI service is struggling or unavailable.");
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
    /// Server-Sent Events (SSE) streaming proxy forwarding live tokens from FastAPI to client.
    /// CRITICAL: await Response.Body.FlushAsync() prevents TCP/socket buffering.
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
            // CRITICAL 1: ResponseHeadersRead prevents buffering entire body before returning
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

                // Forward SSE chunk onward to client
                await Response.WriteAsync(line + "\n\n", clientDisconnectToken);

                // CRITICAL 2: Body.FlushAsync() forces socket buffer to transmit immediately
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
