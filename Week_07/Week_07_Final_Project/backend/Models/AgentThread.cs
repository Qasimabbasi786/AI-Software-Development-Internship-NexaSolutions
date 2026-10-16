using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace libraryAPI.Models
{
    [Table("AgentThreads")]
    public class AgentThread
    {
        [Key]
        [MaxLength(100)]
        public string ThreadId { get; set; } = string.Empty;

        [Required]
        [MaxLength(100)]
        public string UserId { get; set; } = string.Empty;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime LastActiveAt { get; set; } = DateTime.UtcNow;

        [MaxLength(50)]
        public string Status { get; set; } = "Active"; // Active, Paused, Completed, Cancelled
    }
}
