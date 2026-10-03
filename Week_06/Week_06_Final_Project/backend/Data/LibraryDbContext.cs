using Microsoft.EntityFrameworkCore;
using libraryAPI.Models;

namespace libraryAPI.Data;

/// <summary>
/// Database context class representing session with PostgreSQL using EF Core.
/// Reads connection string dynamically from Environment Variables (.env) or configuration settings.
/// </summary>
public class LibraryDbContext : DbContext
{
    public LibraryDbContext() { }

    public LibraryDbContext(DbContextOptions<LibraryDbContext> options) : base(options) { }

    public DbSet<Author> Authors => Set<Author>();
    public DbSet<Book> Books => Set<Book>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<BookCategory> BookCategories => Set<BookCategory>();
    public DbSet<User> Users => Set<User>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            string connectionString = GetConnectionString();
            optionsBuilder.UseNpgsql(connectionString);
        }
    }

    /// <summary>
    /// Helper method to construct connection string securely from environment variables 
    /// or fallback default configuration.
    /// </summary>
    public static string GetConnectionString()
    {
        // 1. Check direct connection string environment variable
        var envConn = Environment.GetEnvironmentVariable("CONNECTION_STRING") ?? 
                      Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        if (!string.IsNullOrEmpty(envConn))
        {
            return envConn;
        }

        // 2. Check granular PostgreSQL environment variables
        var host = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "localhost";
        var port = Environment.GetEnvironmentVariable("POSTGRES_PORT") ?? "5432";
        var db = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "librarydb_week3";
        var user = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
        var pass = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "private";

        return $"Host={host};Port={port};Database={db};Username={user};Password={pass}";
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Map PostgreSQL table names explicitly
        modelBuilder.Entity<Author>().ToTable("Authors");
        modelBuilder.Entity<Book>().ToTable("Books");
        modelBuilder.Entity<Category>().ToTable("Categories");
        modelBuilder.Entity<BookCategory>().ToTable("BookCategories");
        modelBuilder.Entity<User>().ToTable("Users");

        // Composite Primary Key for BookCategory junction table
        modelBuilder.Entity<BookCategory>()
            .HasKey(bc => new { bc.BookId, bc.CategoryId });

        // One-to-Many: Author -> Books
        modelBuilder.Entity<Book>()
            .HasOne(b => b.Author)
            .WithMany(a => a.Books)
            .HasForeignKey(b => b.AuthorId)
            .OnDelete(DeleteBehavior.Restrict);

        // Many-to-Many setup: Book <-> Category via BookCategory
        modelBuilder.Entity<BookCategory>()
            .HasOne(bc => bc.Book)
            .WithMany(b => b.BookCategories)
            .HasForeignKey(bc => bc.BookId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<BookCategory>()
            .HasOne(bc => bc.Category)
            .WithMany(c => c.BookCategories)
            .HasForeignKey(bc => bc.CategoryId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
