using Microsoft.EntityFrameworkCore;
using Week_03_PartB_EFCore.Data;
using Week_03_PartB_EFCore.Models;

// 1. Load local .env file if present
var envPath = Path.Combine(Directory.GetCurrentDirectory(), ".env");
if (File.Exists(envPath))
{
    foreach (var line in File.ReadAllLines(envPath))
    {
        var parts = line.Split('=', 2, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        if (parts.Length == 2 && !parts[0].StartsWith('#'))
        {
            Environment.SetEnvironmentVariable(parts[0], parts[1]);
        }
    }
}

Console.WriteLine("==========================================================");
Console.WriteLine(" Week 3 - Part B: EF Core with PostgreSQL (Console Demo)");
Console.WriteLine("==========================================================");

using var context = new LibraryDbContext();

Console.WriteLine("\n[1] Ensuring Database Connection...");
bool canConnect = await context.Database.CanConnectAsync();
Console.WriteLine($"-> Database connection status: {(canConnect ? "SUCCESS" : "FAILED")}");

if (canConnect)
{
    // --- 1. INSERT DEMO RECORD (Create) ---
    Console.WriteLine("\n[2] Inserting a new Author and Book using EF Core...");
    var newAuthor = new Author
    {
        FullName = "Munirom Hashmi",
        City = "Islamabad",
        Email = "munir.hashmi@literature.pk"
    };

    context.Authors.Add(newAuthor);
    await context.SaveChangesAsync();

    var newBook = new Book
    {
        Title = "Modern Urdu Literature Trends",
        ISBN = "978-969-0-99999-9",
        PublicationYear = 2024,
        AuthorId = newAuthor.AuthorId
    };

    context.Books.Add(newBook);
    await context.SaveChangesAsync();
    Console.WriteLine($"-> Inserted Book ID: {newBook.BookId} linked to Author ID: {newAuthor.AuthorId}");

    // --- 2. FILTERED LINQ QUERY (Read) ---
    Console.WriteLine("\n[3] Executing Filtered LINQ Query (b => b.AuthorId == newAuthor.AuthorId)...");
    var authorBooks = await context.Books
        .Include(b => b.Author)
        .Where(b => b.AuthorId == newAuthor.AuthorId)
        .ToListAsync();

    foreach (var b in authorBooks)
    {
        Console.WriteLine($"-> Found Book: '{b.Title}' (Year: {b.PublicationYear}) | Author: {b.Author?.FullName}");
    }

    // --- 3. UPDATE RECORD (Update) ---
    Console.WriteLine("\n[4] Updating Book Publication Year...");
    var bookToUpdate = await context.Books.FirstOrDefaultAsync(b => b.BookId == newBook.BookId);
    if (bookToUpdate != null)
    {
        bookToUpdate.PublicationYear = 2025;
        await context.SaveChangesAsync();
        Console.WriteLine($"-> Updated Book ID {bookToUpdate.BookId} PublicationYear to 2025.");
    }

    // --- 4. DELETE RECORD (Delete) ---
    Console.WriteLine("\n[5] Cleaning up created demo book...");
    var bookToDelete = await context.Books.FirstOrDefaultAsync(b => b.BookId == newBook.BookId);
    if (bookToDelete != null)
    {
        context.Books.Remove(bookToDelete);
        await context.SaveChangesAsync();
        Console.WriteLine($"-> Successfully deleted Book ID: {bookToDelete.BookId}");
    }

    // Cleanup demo author
    context.Authors.Remove(newAuthor);
    await context.SaveChangesAsync();
}

Console.WriteLine("\n==========================================================");
Console.WriteLine(" EF Core CRUD Operations Completed Successfully!");
Console.WriteLine("==========================================================");
