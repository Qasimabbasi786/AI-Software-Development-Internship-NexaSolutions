using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;

namespace Week2_PartB_API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class GreetingController : ControllerBase
    {
        // In-memory storage for demonstration and testing via Postman/Swagger
        private static readonly List<GreetingModel> _greetings = new List<GreetingModel>
        {
            new GreetingModel { Id = 1, Name = "Muhammad Qasim", Message = "Welcome to Enterprise .NET Core API!" },
            new GreetingModel { Id = 2, Name = "Qasim Developer", Message = "Keep pushing forward with clean code!" }
        };

        // GET: api/greeting
        // Returns 200 OK with list of all greetings
        [HttpGet]
        public IActionResult GetAllGreetings()
        {
            var response = new
            {
                Status = "Success",
                Count = _greetings.Count,
                Data = _greetings
            };
            return Ok(response);
        }

        // GET: api/greeting/{id}
        // Returns 200 OK or 404 Not Found if resource doesn't exist
        [HttpGet("{id:int}")]
        public IActionResult GetGreetingById(int id)
        {
            var item = _greetings.FirstOrDefault(x => x.Id == id);
            if (item == null)
            {
                return NotFound(new { StatusCode = 404, Error = $"Greeting resource with ID {id} was not found." });
            }

            return Ok(new { StatusCode = 200, Data = item });
        }

        // POST: api/greeting
        // Returns 201 Created or 400 Bad Request
        [HttpPost]
        public IActionResult CreateGreeting([FromBody] GreetingRequest request)
        {
            if (request == null || string.IsNullOrWhiteSpace(request.Name) || string.IsNullOrWhiteSpace(request.Message))
            {
                return BadRequest(new { StatusCode = 400, Error = "Invalid payload. Both 'Name' and 'Message' fields are required." });
            }

            var newId = _greetings.Count > 0 ? _greetings.Max(x => x.Id) + 1 : 1;
            var newEntry = new GreetingModel
            {
                Id = newId,
                Name = request.Name.Trim(),
                Message = request.Message.Trim()
            };

            _greetings.Add(newEntry);

            var resourceUri = Url.Action(nameof(GetGreetingById), new { id = newEntry.Id }) ?? $"/api/greeting/{newEntry.Id}";
            
            return Created(resourceUri, new 
            { 
                StatusCode = 201, 
                Message = "Greeting resource successfully created!",
                Data = newEntry 
            });
        }
    }

    public class GreetingModel
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
    }

    public class GreetingRequest
    {
        public string Name { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
    }
}