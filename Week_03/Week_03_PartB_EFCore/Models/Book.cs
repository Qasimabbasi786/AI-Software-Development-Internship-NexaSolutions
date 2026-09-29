namespace Week_03_PartB_EFCore.Models;

/// <summary>
/// Entity representing a Book in the Library system.
/// </summary>
public class Book
{
    public int BookId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? ISBN { get; set; }
    public int? PublicationYear { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Foreign Key
    public int AuthorId { get; set; }
    
    // Navigation Property: Many-to-One relationship with Author
    public Author? Author { get; set; }

    // Navigation Property: Many-to-Many relationship with Category via BookCategory
    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();
}
