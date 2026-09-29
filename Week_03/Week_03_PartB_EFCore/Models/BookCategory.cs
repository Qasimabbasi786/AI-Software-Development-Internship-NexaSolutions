namespace Week_03_PartB_EFCore.Models;

/// <summary>
/// Explicit Join Entity representing the Many-to-Many link between Book and Category.
/// </summary>
public class BookCategory
{
    public int BookId { get; set; }
    public Book? Book { get; set; }

    public int CategoryId { get; set; }
    public Category? Category { get; set; }

    public DateTime AssignedAt { get; set; } = DateTime.UtcNow;
}
