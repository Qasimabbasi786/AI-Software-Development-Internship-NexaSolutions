namespace libraryAPI.Services;

public interface IAiServiceClient
{
    Task<AiAnswerResponse> AskAsync(string question, CancellationToken cancellationToken = default);
}

public class AiAnswerResponse
{
    public string Answer { get; set; } = string.Empty;
    public string Confidence { get; set; } = string.Empty;
    public List<string> Sources { get; set; } = new();
}

public class AskDto
{
    public string Question { get; set; } = string.Empty;
    public string? SessionId { get; set; }
}
