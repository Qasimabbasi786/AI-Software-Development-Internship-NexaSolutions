using System.Net.Http.Json;

namespace libraryAPI.Services;

public class AiServiceClient : IAiServiceClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<AiServiceClient> _logger;

    public AiServiceClient(HttpClient httpClient, ILogger<AiServiceClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<AiAnswerResponse> AskAsync(string question, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Dispatching /ask request to upstream FastAPI service for question: {Question}", question);
        
        var response = await _httpClient.PostAsJsonAsync("/ask", new { question }, cancellationToken);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<AiAnswerResponse>(cancellationToken: cancellationToken);
        return result ?? new AiAnswerResponse { Answer = "Empty response received from AI service.", Confidence = "low" };
    }
}
