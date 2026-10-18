using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace libraryAPI.Models;

/// <summary>
/// Daily token consumption record per user for AI budget enforcement.
/// </summary>
public class UsageLog
{
    [Key]
    public int Id { get; set; }

    [Required]
    public string UserId { get; set; } = string.Empty;

    [Required]
    public DateOnly Day { get; set; }

    [Required]
    public int Tokens { get; set; }

    public DateTime RecordedAt { get; set; } = DateTime.UtcNow;
}
