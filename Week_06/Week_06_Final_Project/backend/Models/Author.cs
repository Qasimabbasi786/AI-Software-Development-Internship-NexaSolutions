namespace libraryAPI.Models;

/// <summary>
/// Entity representing an Author in the Library system.
/// Maps to the "Authors" table in PostgreSQL.
/// </summary>
public class Author
{
    public int AuthorId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string City { get; set; } = "Islamabad";
    public string? Email { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Navigation Property: One Author has many Books
    public ICollection<Book> Books { get; set; } = new List<Book>();
}
