using Microsoft.EntityFrameworkCore;
using libraryAPI.Data;
using libraryAPI.Models;

namespace libraryAPI.Repositories;

/// <summary>
/// EF Core / PostgreSQL implementation of IBookRepository.
/// Injects LibraryDbContext via Dependency Injection and replaces in-memory List<Book> operations.
/// </summary>
public class BookRepository : IBookRepository
{
    private readonly LibraryDbContext _context;
    private readonly ILogger<BookRepository> _logger;

    public BookRepository(LibraryDbContext context, ILogger<BookRepository> logger)
    {
        _context = context ?? throw new ArgumentNullException(nameof(context));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<IEnumerable<Book>> GetAllAsync()
    {
        try
        {
            return await _context.Books
                .Include(b => b.Author)
                .AsNoTracking()
                .ToListAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while retrieving all books from PostgreSQL database.");
            throw;
        }
    }

    public async Task<Book?> GetByIdAsync(int id)
    {
        try
        {
            return await _context.Books
                .Include(b => b.Author)
                .FirstOrDefaultAsync(b => b.BookId == id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while fetching book ID {BookId} from PostgreSQL.", id);
            throw;
        }
    }

    public async Task<Book> AddAsync(Book book)
    {
        try
        {
            await _context.Books.AddAsync(book);
            await _context.SaveChangesAsync();
            return book;
        }
        catch (DbUpdateException dbEx)
        {
            _logger.LogError(dbEx, "Database error adding new book '{Title}'. Check foreign keys or constraints.", book.Title);
            throw new InvalidOperationException("Failed to save book to PostgreSQL due to database constraint rules.", dbEx);
        }
    }

    public async Task<bool> UpdateAsync(Book book)
    {
        try
        {
            var existing = await _context.Books.FindAsync(book.BookId);
            if (existing == null) return false;

            existing.Title = book.Title;
            existing.ISBN = book.ISBN;
            existing.PublicationYear = book.PublicationYear;
            existing.AuthorId = book.AuthorId;

            await _context.SaveChangesAsync();
            return true;
        }
        catch (DbUpdateException dbEx)
        {
            _logger.LogError(dbEx, "Database error updating book ID {BookId}.", book.BookId);
            throw;
        }
    }

    public async Task<bool> DeleteAsync(int id)
    {
        try
        {
            var book = await _context.Books.FindAsync(id);
            if (book == null) return false;

            _context.Books.Remove(book);
            await _context.SaveChangesAsync();
            return true;
        }
        catch (DbUpdateException dbEx)
        {
            _logger.LogError(dbEx, "Database error deleting book ID {BookId}.", id);
            throw;
        }
    }
}
