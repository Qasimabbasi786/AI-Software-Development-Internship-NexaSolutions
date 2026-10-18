using libraryAPI.Models;

namespace libraryAPI.Repositories;

/// <summary>
/// Repository Interface abstraction maintaining the contract between Service layer and Data persistence.
/// </summary>
public interface IBookRepository
{
    Task<IEnumerable<Book>> GetAllAsync();
    Task<Book?> GetByIdAsync(int id);
    Task<Book> AddAsync(Book book);
    Task<bool> UpdateAsync(Book book);
    Task<bool> DeleteAsync(int id);
}
