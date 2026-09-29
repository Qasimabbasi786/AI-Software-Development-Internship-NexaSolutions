using libraryAPI.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace libraryAPI.Repositories
{
    public class BookRepository : IBookRepository
    {
        private readonly List<Book> _books;

        public BookRepository()
        {
            _books = new List<Book>
            {
                new Book { Id = 1, Title = "C# Fundamentals", Author = "Muhammad Qasim", Category = "Programming", CreatedAt = DateTime.Now.AddDays(-1) },
                new Book { Id = 2, Title = "Core Architecture", Author = "Qasim Abbasi", Category = "Software Design", CreatedAt = DateTime.Now.AddDays(-1) }
            };
        }

        public Task<IEnumerable<Book>> GetAllAsync()
        {
            return Task.FromResult(_books.AsEnumerable());
        }

        public Task<Book?> GetByIdAsync(int id)
        {
            return Task.FromResult(_books.FirstOrDefault(b => b.Id == id));
        }

        public Task<Book> AddAsync(Book book)
        {
            book.Id = _books.Count > 0 ? _books.Max(b => b.Id) + 1 : 1;
            book.CreatedAt = DateTime.Now;
            _books.Add(book);
            return Task.FromResult(book);
        }

        public Task<bool> UpdateAsync(Book book)
        {
            var existing = _books.FirstOrDefault(b => b.Id == book.Id);
            if (existing == null) return Task.FromResult(false);

            existing.Title = book.Title;
            existing.Author = book.Author;
            existing.Category = book.Category;
            return Task.FromResult(true);
        }

        public Task<bool> DeleteAsync(int id)
        {
            var existing = _books.FirstOrDefault(b => b.Id == id);
            if (existing == null) return Task.FromResult(false);

            _books.Remove(existing);
            return Task.FromResult(true);
        }
    }
}