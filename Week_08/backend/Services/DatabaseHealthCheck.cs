using Microsoft.Extensions.Diagnostics.HealthChecks;
using libraryAPI.Data;

namespace libraryAPI.Services;

/// <summary>
/// Health check probing the primary relational database connectivity.
/// </summary>
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly LibraryDbContext _dbContext;
    private readonly ILogger<DatabaseHealthCheck> _logger;

    public DatabaseHealthCheck(LibraryDbContext dbContext, ILogger<DatabaseHealthCheck> logger)
    {
        _dbContext = dbContext;
        _logger = logger;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        try
        {
            var canConnect = await _dbContext.Database.CanConnectAsync(cancellationToken);
            if (canConnect)
            {
                return HealthCheckResult.Healthy("Database connection is healthy and responsive.");
            }
            return HealthCheckResult.Unhealthy("Cannot connect to relational database.");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "DatabaseHealthCheck failed.");
            return HealthCheckResult.Unhealthy($"Database health check failed: {ex.Message}");
        }
    }
}
