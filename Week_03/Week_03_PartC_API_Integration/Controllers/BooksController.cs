using Microsoft.AspNetCore.Mvc;
using Week_03_PartC_API_Integration.Models;
using Week_03_PartC_API_Integration.Repositories;

namespace Week_03_PartC_API_Integration.Controllers;

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
    /// Fetches all books from PostgreSQL.
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Book>>> GetAll()
    {
        var books = await _repository.GetAllAsync();
        return Ok(books);
    }

    /// <summary>
    /// GET: api/books/{id}
    /// Fetches a single book. Returns 404 Not Found if non-existent instead of a raw 500 exception.
    /// </summary>
    [HttpGet("{id:int}")]
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
    /// POST: api/books
    /// Creates a new book record in PostgreSQL.
    /// </summary>
    [HttpPost]
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
    /// Updates a book. Returns 404 if not found.
    /// </summary>
    [HttpPut("{id:int}")]
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
    /// Deletes a book. Returns 404 if not found.
    /// </summary>
    [HttpDelete("{id:int}")]
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
