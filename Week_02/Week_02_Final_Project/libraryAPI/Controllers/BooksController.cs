using libraryAPI.Models;
using libraryAPI.Services;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace libraryAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BooksController : ControllerBase
    {
        private readonly IBookService _bookService;

        public BooksController(IBookService bookService)
        {
            _bookService = bookService;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Book>>> GetBooks()
        {
            var books = await _bookService.GetAllBooksAsync();
            return Ok(new { StatusCode = 200, Message = "Books retrieved successfully", Data = books });
        }

        [HttpGet("{id:int}")]
        public async Task<ActionResult<Book>> GetBook(int id)
        {
            var book = await _bookService.GetBookByIdAsync(id);
            if (book == null)
            {
                return NotFound(new { StatusCode = 404, Error = $"Book with ID {id} was not found." });
            }
            return Ok(new { StatusCode = 200, Data = book });
        }

        [HttpPost]
        public async Task<ActionResult<Book>> CreateBook([FromBody] Book book)
        {
            if (string.IsNullOrWhiteSpace(book.Title) || string.IsNullOrWhiteSpace(book.Author))
            {
                return BadRequest(new { StatusCode = 400, Error = "Title and Author are required fields." });
            }

            var createdBook = await _bookService.AddBookAsync(book);
            return CreatedAtAction(nameof(GetBook), new { id = createdBook.Id }, new { StatusCode = 201, Message = "Book registered successfully", Data = createdBook });
        }

        [HttpPut("{id:int}")]
        public async Task<IActionResult> UpdateBook(int id, [FromBody] Book book)
        {
            if (id != book.Id)
            {
                return BadRequest(new { StatusCode = 400, Error = "ID mismatch between route and payload." });
            }

            var result = await _bookService.UpdateBookAsync(book);
            if (!result)
            {
                return NotFound(new { StatusCode = 404, Error = $"Book with ID {id} could not be found for update." });
            }

            return Ok(new { StatusCode = 200, Message = "Book updated successfully" });
        }

        [HttpDelete("{id:int}")]
        public async Task<IActionResult> DeleteBook(int id)
        {
            var result = await _bookService.DeleteBookAsync(id);
            if (!result)
            {
                return NotFound(new { StatusCode = 404, Error = $"Book with ID {id} could not be found for deletion." });
            }

            return Ok(new { StatusCode = 200, Message = "Book deleted successfully" });
        }
    }
}