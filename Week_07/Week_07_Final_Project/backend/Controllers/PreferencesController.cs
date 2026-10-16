using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using libraryAPI.Data;
using libraryAPI.Models;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/me/preferences")]
[Authorize]
public class PreferencesController : ControllerBase
{
    private readonly LibraryDbContext _dbContext;
    private readonly ILogger<PreferencesController> _logger;

    public PreferencesController(LibraryDbContext dbContext, ILogger<PreferencesController> logger)
    {
        _dbContext = dbContext;
        _logger = logger;
    }

    private string? GetCurrentUserId()
    {
        return User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
               ?? User.FindFirst("sub")?.Value
               ?? User.Identity?.Name;
    }

    /// <summary>
    /// GET: api/me/preferences
    /// Retrieves all stored preferences for the authenticated caller.
    /// </summary>
    [HttpGet]
    public async Task<IActionResult> GetMyPreferences()
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
            return Unauthorized(new { message = "User identity claim could not be resolved from JWT." });

        var prefs = await _dbContext.UserPreferences
            .Where(p => p.UserId == userId)
            .OrderBy(p => p.Key)
            .ToListAsync();

        return Ok(prefs);
    }

    /// <summary>
    /// POST: api/me/preferences
    /// Saves or updates a specific preference key/value pair.
    /// </summary>
    [HttpPost]
    public async Task<IActionResult> SavePreference([FromBody] PreferenceDto request)
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
            return Unauthorized(new { message = "User identity claim could not be resolved from JWT." });

        if (string.IsNullOrWhiteSpace(request.Key))
            return BadRequest(new { message = "Preference Key is required." });

        var existing = await _dbContext.UserPreferences
            .FirstOrDefaultAsync(p => p.UserId == userId && p.Key == request.Key);

        if (existing != null)
        {
            existing.Value = request.Value ?? string.Empty;
            existing.UpdatedAt = DateTime.UtcNow;
        }
        else
        {
            _dbContext.UserPreferences.Add(new UserPreference
            {
                UserId = userId,
                Key = request.Key,
                Value = request.Value ?? string.Empty,
                UpdatedAt = DateTime.UtcNow
            });
        }

        await _dbContext.SaveChangesAsync();
        _logger.LogInformation("Saved user preference {Key} for user {UserId}", request.Key, userId);
        return Ok(new { message = "Preference saved successfully.", key = request.Key, value = request.Value });
    }

    /// <summary>
    /// DELETE: api/me/preferences
    /// Deletes all preferences for the current user ("Forget My Preferences" path).
    /// </summary>
    [HttpDelete]
    public async Task<IActionResult> ForgetMyPreferences()
    {
        var userId = GetCurrentUserId();
        if (string.IsNullOrEmpty(userId))
            return Unauthorized(new { message = "User identity claim could not be resolved from JWT." });

        var userPrefs = await _dbContext.UserPreferences.Where(p => p.UserId == userId).ToListAsync();
        _dbContext.UserPreferences.RemoveRange(userPrefs);
        await _dbContext.SaveChangesAsync();

        _logger.LogInformation("Deleted all preferences for user {UserId}", userId);
        return Ok(new { message = $"Successfully cleared {userPrefs.Count} preferences." });
    }
}

public class PreferenceDto
{
    public string Key { get; set; } = string.Empty;
    public string Value { get; set; } = string.Empty;
}
