using Microsoft.EntityFrameworkCore;
using Week_03_PartC_API_Integration.Models;

namespace Week_03_PartC_API_Integration.Data;

/// <summary>
/// PostgreSQL DbContext for Part C Web API integration.
/// Maps Author, Book, Category domain models and loads connection strings dynamically.
/// </summary>
public class LibraryDbContext : DbContext
{
    public LibraryDbContext() { }

    public LibraryDbContext(DbContextOptions<LibraryDbContext> options) : base(options) { }

    public DbSet<Author> Authors => Set<Author>();
    public DbSet<Book> Books => Set<Book>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<BookCategory> BookCategories => Set<BookCategory>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseNpgsql(GetConnectionString());
        }
    }

    public static string GetConnectionString()
    {
        var envConn = Environment.GetEnvironmentVariable("CONNECTION_STRING") ?? 
                      Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        if (!string.IsNullOrEmpty(envConn)) return envConn;

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

        modelBuilder.Entity<Author>().ToTable("Authors");
        modelBuilder.Entity<Book>().ToTable("Books");
        modelBuilder.Entity<Category>().ToTable("Categories");
        modelBuilder.Entity<BookCategory>().ToTable("BookCategories");

        modelBuilder.Entity<BookCategory>()
            .HasKey(bc => new { bc.BookId, bc.CategoryId });

        modelBuilder.Entity<Book>()
            .HasOne(b => b.Author)
            .WithMany(a => a.Books)
            .HasForeignKey(b => b.AuthorId)
            .OnDelete(DeleteBehavior.Restrict);

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
