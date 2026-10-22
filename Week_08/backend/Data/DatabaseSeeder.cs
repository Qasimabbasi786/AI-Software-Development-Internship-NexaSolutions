using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using libraryAPI.Models;

namespace libraryAPI.Data;

/// <summary>
/// Week 8 Part E: Database Seeding Service
/// Automatically seeds demo user, admin user, authors, categories, and 15+ catalog books across categories.
/// </summary>
public static class DatabaseSeeder
{
    public static async Task SeedAsync(LibraryDbContext context)
    {
        // 1. Seed Users (Admin & Demo User)
        if (!await context.Users.AnyAsync())
        {
            var hasher = new PasswordHasher<User>();

            var adminUser = new User
            {
                Username = "admin",
                Email = "admin@library.nexa",
                Role = "Admin",
                CreatedAt = DateTime.UtcNow
            };
            adminUser.PasswordHash = hasher.HashPassword(adminUser, "Admin123!");

            var demoUser = new User
            {
                Username = "demo_user",
                Email = "demouser@library.nexa",
                Role = "User",
                CreatedAt = DateTime.UtcNow
            };
            demoUser.PasswordHash = hasher.HashPassword(demoUser, "DemoUser123!");

            context.Users.AddRange(adminUser, demoUser);
            await context.SaveChangesAsync();
        }

        // 2. Seed Authors & Categories & Books
        if (!await context.Books.AnyAsync())
        {
            var authors = new List<Author>
            {
                new() { FullName = "Robert C. Martin", City = "Chicago", Email = "unclebob@cleancoder.com" },
                new() { FullName = "Martin Kleppmann", City = "Cambridge", Email = "martin@kleppmann.com" },
                new() { FullName = "David Thomas", City = "Dallas", Email = "pragdave@pragmaticprogrammer.com" },
                new() { FullName = "Frank Herbert", City = "Tacoma", Email = "frank@herbert.org" },
                new() { FullName = "Jane Austen", City = "Steventon", Email = "jane@austenclassic.org" },
                new() { FullName = "William Gibson", City = "Vancouver", Email = "william@matrix.cyberpunk" },
                new() { FullName = "Andrew Ng", City = "Palo Alto", Email = "andrew@deeplearning.ai" },
                new() { FullName = "Arthur Conan Doyle", City = "Edinburgh", Email = "arthur@sherlock.org" },
                new() { FullName = "George Orwell", City = "Motihari", Email = "george@orwell1984.org" },
                new() { FullName = "J.R.R. Tolkien", City = "Oxford", Email = "tolkien@middleearth.org" }
            };
            context.Authors.AddRange(authors);
            await context.SaveChangesAsync();

            var categories = new List<Category>
            {
                new() { CategoryName = "Software Engineering", Description = "Best practices, architecture, clean code" },
                new() { CategoryName = "Distributed Systems", Description = "Consensus, replication, databases, event streaming" },
                new() { CategoryName = "Science Fiction", Description = "Cyberpunk, space exploration, planetary epics" },
                new() { CategoryName = "Classic Literature", Description = "Historical, societal, and classic romance fiction" },
                new() { CategoryName = "Artificial Intelligence", Description = "Deep learning, neural networks, agents, and RAG" },
                new() { CategoryName = "Mystery & Detective", Description = "Crime, deduction, forensic investigations" }
            };
            context.Categories.AddRange(categories);
            await context.SaveChangesAsync();

            var books = new List<Book>
            {
                // 1
                new() { Title = "Clean Code: A Handbook of Agile Software Craftsmanship", AuthorId = authors[0].AuthorId, PublicationYear = 2008, IsAvailable = true, ISBN = "978-0132350884" },
                // 2
                new() { Title = "Designing Data-Intensive Applications", AuthorId = authors[1].AuthorId, PublicationYear = 2017, IsAvailable = true, ISBN = "978-1449373320" },
                // 3
                new() { Title = "The Pragmatic Programmer: Your Journey to Mastery", AuthorId = authors[2].AuthorId, PublicationYear = 2019, IsAvailable = true, ISBN = "978-0135957059" },
                // 4
                new() { Title = "Dune", AuthorId = authors[3].AuthorId, PublicationYear = 1965, IsAvailable = true, ISBN = "978-0441172719" },
                // 5
                new() { Title = "Pride and Prejudice", AuthorId = authors[4].AuthorId, PublicationYear = 1813, IsAvailable = true, ISBN = "978-0141439518" },
                // 6
                new() { Title = "Neuromancer", AuthorId = authors[5].AuthorId, PublicationYear = 1984, IsAvailable = true, ISBN = "978-0441569595" },
                // 7
                new() { Title = "Machine Learning Yearning", AuthorId = authors[6].AuthorId, PublicationYear = 2018, IsAvailable = true, ISBN = "978-0999999901" },
                // 8
                new() { Title = "The Adventures of Sherlock Holmes", AuthorId = authors[7].AuthorId, PublicationYear = 1892, IsAvailable = true, ISBN = "978-0140437713" },
                // 9
                new() { Title = "1984", AuthorId = authors[8].AuthorId, PublicationYear = 1949, IsAvailable = true, ISBN = "978-0451524935" },
                // 10
                new() { Title = "The Fellowship of the Ring", AuthorId = authors[9].AuthorId, PublicationYear = 1954, IsAvailable = true, ISBN = "978-0547928210" },
                // 11
                new() { Title = "Clean Architecture: A Craftsman's Guide", AuthorId = authors[0].AuthorId, PublicationYear = 2017, IsAvailable = true, ISBN = "978-0134494166" },
                // 12
                new() { Title = "Animal Farm", AuthorId = authors[8].AuthorId, PublicationYear = 1945, IsAvailable = true, ISBN = "978-0451526342" },
                // 13
                new() { Title = "Dune Messiah", AuthorId = authors[3].AuthorId, PublicationYear = 1969, IsAvailable = true, ISBN = "978-0441172696" },
                // 14
                new() { Title = "Count Zero", AuthorId = authors[5].AuthorId, PublicationYear = 1986, IsAvailable = true, ISBN = "978-0441117734" },
                // 15
                new() { Title = "Sense and Sensibility", AuthorId = authors[4].AuthorId, PublicationYear = 1811, IsAvailable = true, ISBN = "978-0141439662" },
                // 16
                new() { Title = "The Return of the King", AuthorId = authors[9].AuthorId, PublicationYear = 1955, IsAvailable = true, ISBN = "978-0547928197" }
            };
            context.Books.AddRange(books);
            await context.SaveChangesAsync();

            // Link categories to books
            var bookCategories = new List<BookCategory>
            {
                new() { BookId = books[0].BookId, CategoryId = categories[0].CategoryId },
                new() { BookId = books[1].BookId, CategoryId = categories[1].CategoryId },
                new() { BookId = books[2].BookId, CategoryId = categories[0].CategoryId },
                new() { BookId = books[3].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[4].BookId, CategoryId = categories[3].CategoryId },
                new() { BookId = books[5].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[6].BookId, CategoryId = categories[4].CategoryId },
                new() { BookId = books[7].BookId, CategoryId = categories[5].CategoryId },
                new() { BookId = books[8].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[9].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[10].BookId, CategoryId = categories[0].CategoryId },
                new() { BookId = books[11].BookId, CategoryId = categories[3].CategoryId },
                new() { BookId = books[12].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[13].BookId, CategoryId = categories[2].CategoryId },
                new() { BookId = books[14].BookId, CategoryId = categories[3].CategoryId },
                new() { BookId = books[15].BookId, CategoryId = categories[2].CategoryId }
            };
            context.BookCategories.AddRange(bookCategories);
            await context.SaveChangesAsync();
        }
    }
}
