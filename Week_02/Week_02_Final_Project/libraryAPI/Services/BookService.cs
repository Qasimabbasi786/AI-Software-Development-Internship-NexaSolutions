using libraryAPI.Models;
using libraryAPI.Repositories;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace libraryAPI.Services
{
    public class BookService : IBookService
    {
        private readonly IBookRepository _repository;

        public BookService(IBookRepository repository)
        {
            _repository = repository;
        }

        public Task<IEnumerable<Book>> GetAllBooksAsync()
        {
            return _repository.GetAllAsync();
        }

        public Task<Book?> GetBookByIdAsync(int id)
        {
            return _repository.GetByIdAsync(id);
        }

        public Task<Book> AddBookAsync(Book book)
        {
            return _repository.AddAsync(book);
        }

        public Task<bool> UpdateBookAsync(Book book)
        {
            return _repository.UpdateAsync(book);
        }

        public Task<bool> DeleteBookAsync(int id)
        {
            return _repository.DeleteAsync(id);
        }
    }
}