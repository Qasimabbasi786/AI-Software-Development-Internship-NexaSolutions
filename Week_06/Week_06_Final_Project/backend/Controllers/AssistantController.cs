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
    private readonly ILogger<AssistantController> _logger;

    public AssistantController(IAiServiceClient aiServiceClient, ILogger<AssistantController> logger)
    {
        _aiServiceClient = aiServiceClient;
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
}
