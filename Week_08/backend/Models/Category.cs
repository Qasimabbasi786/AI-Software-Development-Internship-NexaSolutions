namespace libraryAPI.Models;

/// <summary>
/// Entity representing a Category/Genre in the Library system.
/// </summary>
public class Category
{
    public int CategoryId { get; set; }
    public string CategoryName { get; set; } = string.Empty;
    public string? Description { get; set; }

    // Navigation Property: Many-to-Many relationship with Books
    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();
}
