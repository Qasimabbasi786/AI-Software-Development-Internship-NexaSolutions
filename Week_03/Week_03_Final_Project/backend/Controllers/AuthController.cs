using Microsoft.AspNetCore.Mvc;
using libraryAPI.Data;
using libraryAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly LibraryDbContext _context;

    public AuthController(LibraryDbContext context)
    {
        _context = context;
    }

    public record LoginRequest(string Email, string Password);
    public record RegisterRequest(string Username, string Email, string Password);

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            return BadRequest(new { message = "Email and password are required." });
        }

        var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == request.Email);
        if (user == null || user.PasswordHash != request.Password)
        {
            return Unauthorized(new { message = "Invalid email or password (Auth Skeleton)." });
        }

        return Ok(new
        {
            message = "Login successful (Skeleton Mode: Real JWT issuance scheduled for Week 4)",
            user = new { user.UserId, user.Username, user.Email, user.Role },
            token = "skeleton-mock-jwt-token-week-3"
        });
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            return BadRequest(new { message = "Email and password are required." });
        }

        var exists = await _context.Users.AnyAsync(u => u.Email == request.Email);
        if (exists)
        {
            return BadRequest(new { message = "User with this email already exists." });
        }

        var newUser = new User
        {
            Username = request.Username,
            Email = request.Email,
            PasswordHash = request.Password,
            Role = "Member"
        };

        _context.Users.Add(newUser);
        await _context.SaveChangesAsync();

        return Ok(new { message = "User registered successfully.", userId = newUser.UserId });
    }
}

