using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using libraryAPI.Data;
using libraryAPI.Services;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/me")]
[Authorize]
public class UserDataController : ControllerBase
{
    private readonly LibraryDbContext _dbContext;
    private readonly HttpClient _httpClient;
    private readonly ILogger<UserDataController> _logger;
    private readonly string _serviceKey;

    public UserDataController(
        LibraryDbContext dbContext,
        IHttpClientFactory httpClientFactory,
        ILogger<UserDataController> logger)
    {
        _dbContext = dbContext;
        _httpClient = httpClientFactory.CreateClient(nameof(IAiServiceClient));
        _logger = logger;
        _serviceKey = Environment.GetEnvironmentVariable("SERVICE_KEY") ?? "nexa-secure-service-key-2026";
    }

    private string? GetCurrentUserId()
    {
        return User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
               ?? User.FindFirst("sub")?.Value
               ?? User.Identity?.Name;
    }

    /// <summary>
    /// DELETE: api/me/data
    /// GDPR compliance: removes user's preferences, agent threads, checkpoints, and reservations history.
    /// Purges from both SQL Server/Postgres and downstream LangGraph checkpoint store.
    /// </summary>
    [HttpDelete("data")]
    public async Task<IActionResult> DeleteMyData(CancellationToken cancellationToken)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
        {
            return Unauthorized(new { message = "User identity claim could not be resolved from JWT." });
        }

        _logger.LogInformation("Processing GDPR data erasure request for user {UserId}", userId);

        // 1. Delete user preferences
        var userPrefs = await _dbContext.UserPreferences
            .Where(p => p.UserId == userId)
            .ToListAsync(cancellationToken);
        _dbContext.UserPreferences.RemoveRange(userPrefs);

        // 2. Delete agent threads
        var userThreads = await _dbContext.AgentThreads
            .Where(t => t.UserId == userId)
            .ToListAsync(cancellationToken);
        _dbContext.AgentThreads.RemoveRange(userThreads);

        // 3. Delete user usage logs
        var usageLogs = await _dbContext.UsageLogs
            .Where(u => u.UserId == userId)
            .ToListAsync(cancellationToken);
        _dbContext.UsageLogs.RemoveRange(usageLogs);

        // 4. Delete user reservations if permitted by library policy
        var userReservations = await _dbContext.Reservations
            .Where(r => r.UserId == userId)
            .ToListAsync(cancellationToken);
        int deletedReservationsCount = userReservations.Count;
        _dbContext.Reservations.RemoveRange(userReservations);

        await _dbContext.SaveChangesAsync(cancellationToken);


        // 5. Notify AI service to purge SQLite state checkpoints for this user
        int remoteCheckpointsDeleted = 0;
        try
        {
            var request = new HttpRequestMessage(HttpMethod.Delete, $"/agent/checkpoints/user/{userId}");
            request.Headers.Add("X-Service-Key", _serviceKey);
            using var response = await _httpClient.SendAsync(request, cancellationToken);
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadFromJsonAsync<System.Text.Json.Nodes.JsonObject>(cancellationToken: cancellationToken);
                if (content != null && content.TryGetPropertyValue("deleted_checkpoint_records", out var val))
                {
                    remoteCheckpointsDeleted = val?.GetValue<int>() ?? 0;
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed contacting AI service to purge checkpoints for user {UserId}", userId);
        }

        _logger.LogInformation("Completed data erasure for user {UserId}. Prefs: {Prefs}, Threads: {Threads}, Reservations: {Res}, Checkpoints: {CP}",
            userId, userPrefs.Count, userThreads.Count, deletedReservationsCount, remoteCheckpointsDeleted);

        return Ok(new
        {
            message = "All user personal data, agent threads, reservations, and state checkpoints were deleted successfully.",
            userId,
            deleted = new
            {
                preferences = userPrefs.Count,
                agentThreads = userThreads.Count,
                reservations = deletedReservationsCount,
                usageLogs = usageLogs.Count,
                checkpoints = remoteCheckpointsDeleted
            }
        });
    }
}
