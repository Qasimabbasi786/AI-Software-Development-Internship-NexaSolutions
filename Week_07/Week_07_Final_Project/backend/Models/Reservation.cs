using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace libraryAPI.Models
{
    [Table("Reservations")]
    public class Reservation
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }

        [Required]
        public int BookId { get; set; }

        [ForeignKey("BookId")]
        public Book? Book { get; set; }

        [Required]
        [MaxLength(100)]
        public string UserId { get; set; } = string.Empty;

        [Required]
        [MaxLength(200)]
        public string IdempotencyKey { get; set; } = string.Empty;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [MaxLength(50)]
        public string Status { get; set; } = "Active"; // Active, Cancelled, Completed
    }
}
