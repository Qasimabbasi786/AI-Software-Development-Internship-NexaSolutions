using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using libraryAPI.Data;
using libraryAPI.Services;
using System.Data.Common;

namespace libraryAPI.Tests;

public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    private DbConnection? _connection;

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remove existing DbContext registration
            var dbContextDescriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<LibraryDbContext>));
            if (dbContextDescriptor != null)
            {
                services.Remove(dbContextDescriptor);
            }

            var dbConnectionDescriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbConnection));
            if (dbConnectionDescriptor != null)
            {
                services.Remove(dbConnectionDescriptor);
            }

            // Create SQLite in-memory database connection
            _connection = new SqliteConnection("DataSource=:memory:");
            _connection.Open();

            services.AddDbContext<LibraryDbContext>((container, options) =>
            {
                options.UseSqlite(_connection);
            });

            // Replace IAiServiceClient with mock
            var aiServiceDescriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(IAiServiceClient));
            if (aiServiceDescriptor != null)
            {
                services.Remove(aiServiceDescriptor);
            }
            services.AddScoped<IAiServiceClient, FakeAiServiceClient>();

            // Seed test database
            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<LibraryDbContext>();
            db.Database.EnsureCreated();

            if (!db.Books.Any())
            {
                var author = new Models.Author { AuthorId = 1, Name = "Frank Herbert" };
                db.Authors.Add(author);
                db.Books.Add(new Models.Book
                {
                    BookId = 1,
                    Title = "Dune",
                    AuthorId = 1,
                    Genre = "Science Fiction",
                    Description = "Desert planet",
                    IsAvailable = true
                });
                db.Books.Add(new Models.Book
                {
                    BookId = 2,
                    Title = "Unavailable Book",
                    AuthorId = 1,
                    Genre = "Science Fiction",
                    Description = "Reserved",
                    IsAvailable = false
                });
                db.SaveChanges();
            }
        });
    }

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        _connection?.Close();
    }
}

public class FakeAiServiceClient : IAiServiceClient
{
    public Task<string> AskAssistantAsync(string question) => Task.FromResult("Fake answer");
    public Task<string> SummarizeBookAsync(string title, string text) => Task.FromResult("Fake summary");
}
