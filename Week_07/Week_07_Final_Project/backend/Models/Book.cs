namespace libraryAPI.Models;

/// <summary>
/// Entity representing a Book in the Library system.
/// </summary>
public class Book
{
    public int BookId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? ISBN { get; set; }
    public int? PublicationYear { get; set; }
    public bool IsAvailable { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Foreign Key
    public int AuthorId { get; set; }
    
    // Navigation Property: Many-to-One relationship with Author
    public Author? Author { get; set; }

    // Navigation Property: Many-to-Many relationship with Category via BookCategory
    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();

    // Convenience / Compatibility properties for Week 2 controllers and clients
    [System.ComponentModel.DataAnnotations.Schema.NotMapped]
    public int Id
    {
        get => BookId;
        set => BookId = value;
    }

    [System.ComponentModel.DataAnnotations.Schema.NotMapped]
    public string? AuthorName
    {
        get => Author?.FullName;
        set { }
    }
}
