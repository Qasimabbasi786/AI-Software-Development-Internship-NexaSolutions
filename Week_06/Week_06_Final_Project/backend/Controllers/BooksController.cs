using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using libraryAPI.Models;
using libraryAPI.Repositories;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookRepository _repository;
    private readonly ILogger<BooksController> _logger;

    public BooksController(IBookRepository repository, ILogger<BooksController> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    /// <summary>
    /// GET: api/books
    /// Public endpoint. Fetches all books from PostgreSQL.
    /// </summary>
    [HttpGet]
    [AllowAnonymous]
    public async Task<ActionResult<IEnumerable<Book>>> GetAll()
    {
        var books = await _repository.GetAllAsync();
        return Ok(books);
    }

    /// <summary>
    /// GET: api/books/{id}
    /// Public endpoint. Fetches a single book. Returns 404 Not Found if non-existent.
    /// </summary>
    [HttpGet("{id:int}")]
    [AllowAnonymous]
    public async Task<ActionResult<Book>> GetById(int id)
    {
        var book = await _repository.GetByIdAsync(id);
        if (book == null)
        {
            return NotFound(new { message = $"Book with ID {id} was not found." });
        }
        return Ok(book);
    }

    /// <summary>
    /// GET: api/books/{id}/availability
    /// Public endpoint. Checks whether a book is available to borrow.
    /// </summary>
    [HttpGet("{id:int}/availability")]
    [AllowAnonymous]
    public async Task<IActionResult> GetAvailability(int id)
    {
        var book = await _repository.GetByIdAsync(id);
        if (book == null)
        {
            return NotFound(new { message = $"Book with ID {id} was not found.", isAvailable = false });
        }
        return Ok(new { bookId = id, isAvailable = book.IsAvailable, title = book.Title });
    }

    /// <summary>
    /// POST: api/books
    /// Protected endpoint. Requires authenticated user (Admin or User role).
    /// </summary>
    [HttpPost]
    [Authorize]
    public async Task<ActionResult<Book>> Create([FromBody] Book book)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        try
        {
            var created = await _repository.AddAsync(book);
            return CreatedAtAction(nameof(GetById), new { id = created.BookId }, created);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /// <summary>
    /// PUT: api/books/{id}
    /// Protected endpoint. Requires authenticated user (Admin or User role).
    /// </summary>
    [HttpPut("{id:int}")]
    [Authorize]
    public async Task<IActionResult> Update(int id, [FromBody] Book book)
    {
        if (id != book.BookId)
        {
            return BadRequest(new { message = "URL ID does not match body BookId." });
        }

        var updated = await _repository.UpdateAsync(book);
        if (!updated)
        {
            return NotFound(new { message = $"Book with ID {id} was not found for update." });
        }

        return NoContent();
    }

    /// <summary>
    /// DELETE: api/books/{id}
    /// Highly protected endpoint. Requires "Admin" role only.
    /// Non-admin authenticated users receive 403 Forbidden.
    /// </summary>
    [HttpDelete("{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _repository.DeleteAsync(id);
        if (!deleted)
        {
            return NotFound(new { message = $"Book with ID {id} was not found for deletion." });
        }

        return NoContent();
    }
}
