using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace libraryAPI.Services;

/// <summary>
/// Health check probing the FastAPI AI service /health endpoint with a strict short timeout.
/// </summary>
public class AiServiceHealthCheck : IHealthCheck
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<AiServiceHealthCheck> _logger;

    public AiServiceHealthCheck(IHttpClientFactory httpClientFactory, ILogger<AiServiceHealthCheck> logger)
    {
        _httpClient = httpClientFactory.CreateClient("HealthCheckClient");
        _logger = logger;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        try
        {
            var baseUrl = Environment.GetEnvironmentVariable("FASTAPI_API_URL") 
                          ?? Environment.GetEnvironmentVariable("AiService__BaseUrl")
                          ?? "http://localhost:8000";

            using var cts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            cts.CancelAfter(TimeSpan.FromSeconds(2.0)); // Strict 2.0s health timeout

            var response = await _httpClient.GetAsync($"{baseUrl.TrimEnd('/')}/health", cts.Token);
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync(cts.Token);
                return HealthCheckResult.Healthy($"AI service healthy. Details: {content}");
            }

            return HealthCheckResult.Unhealthy($"AI service returned status code {(int)response.StatusCode}");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "AiServiceHealthCheck probe failed.");
            return HealthCheckResult.Unhealthy($"AI service unreachable: {ex.Message}");
        }
    }
}
