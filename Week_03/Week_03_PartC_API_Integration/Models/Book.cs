namespace Week_03_PartC_API_Integration.Models;

public class Author
{
    public int AuthorId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string City { get; set; } = "Islamabad";
    public string? Email { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<Book> Books { get; set; } = new List<Book>();
}

public class Book
{
    public int BookId { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? ISBN { get; set; }
    public int? PublicationYear { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public int AuthorId { get; set; }
    public Author? Author { get; set; }

    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();
}

public class Category
{
    public int CategoryId { get; set; }
    public string CategoryName { get; set; } = string.Empty;
    public string? Description { get; set; }

    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();
}

public class BookCategory
{
    public int BookId { get; set; }
    public Book? Book { get; set; }

    public int CategoryId { get; set; }
    public Category? Category { get; set; }

    public DateTime AssignedAt { get; set; } = DateTime.UtcNow;
}
