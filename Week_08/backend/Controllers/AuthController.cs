using Microsoft.AspNetCore.Mvc;
using libraryAPI.Data;
using libraryAPI.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace libraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly LibraryDbContext _context;
    private readonly IConfiguration _configuration;
    private readonly PasswordHasher<User> _passwordHasher;

    public AuthController(LibraryDbContext context, IConfiguration configuration)
    {
        _context = context;
        _configuration = configuration;
        _passwordHasher = new PasswordHasher<User>();
    }

    public record RegisterDto(string Username, string? Email, string Password, string? Role);
    public record LoginDto(string Username, string Password);

    /// <summary>
    /// POST: api/auth/register
    /// Registers a new user, hashes password using PBKDF2 with HMAC-SHA256.
    /// </summary>
    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.Username) || string.IsNullOrWhiteSpace(dto.Password))
        {
            return BadRequest(new { message = "Username and password are required." });
        }

        var normalizedUsername = dto.Username.Trim();
        var exists = await _context.Users.AnyAsync(u => u.Username.ToLower() == normalizedUsername.ToLower());
        if (exists)
        {
            return BadRequest(new { message = $"Username '{normalizedUsername}' is already taken." });
        }

        var role = string.IsNullOrWhiteSpace(dto.Role) ? "User" : dto.Role.Trim();
        // Standardize roles: Only "Admin" or "User"
        if (!string.Equals(role, "Admin", StringComparison.OrdinalIgnoreCase) &&
            !string.Equals(role, "User", StringComparison.OrdinalIgnoreCase))
        {
            role = "User";
        }

        var user = new User
        {
            Username = normalizedUsername,
            Email = dto.Email?.Trim() ?? $"{normalizedUsername.ToLower()}@library.local",
            Role = role,
            CreatedAt = DateTime.UtcNow
        };

        // Hash password securely using ASP.NET Core PasswordHasher
        user.PasswordHash = _passwordHasher.HashPassword(user, dto.Password);

        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        return Ok(new
        {
            message = "User registered successfully.",
            userId = user.UserId,
            username = user.Username,
            role = user.Role
        });
    }

    /// <summary>
    /// POST: api/auth/login
    /// Validates user credentials against stored password hash and issues a signed JWT token.
    /// </summary>
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto dto)
    {
        if (string.IsNullOrWhiteSpace(dto.Username) || string.IsNullOrWhiteSpace(dto.Password))
        {
            return BadRequest(new { message = "Username and password are required." });
        }

        var normalized = dto.Username.Trim();
        var user = await _context.Users.SingleOrDefaultAsync(u =>
            u.Username.ToLower() == normalized.ToLower() ||
            u.Email.ToLower() == normalized.ToLower());

        if (user == null)
        {
            return Unauthorized(new { message = "Invalid username or password." });
        }

        var verificationResult = _passwordHasher.VerifyHashedPassword(user, user.PasswordHash, dto.Password);
        if (verificationResult == PasswordVerificationResult.Failed)
        {
            return Unauthorized(new { message = "Invalid username or password." });
        }

        var token = GenerateJwtToken(user);

        return Ok(new
        {
            message = "Login successful.",
            token,
            user = new
            {
                user.UserId,
                user.Username,
                user.Email,
                user.Role
            }
        });
    }

    /// <summary>
    /// Generates a cryptographically signed JWT token embedding user claims (id, username, role).
    /// </summary>
    private string GenerateJwtToken(User user)
    {
        var jwtKey = _configuration["Jwt:Key"] ?? "NexaSolutions_OriginSoft_SecureKey_2026_JWT_SecretKey_9876543210!";
        var issuer = _configuration["Jwt:Issuer"] ?? "LibraryAPI";
        var audience = _configuration["Jwt:Audience"] ?? "LibraryAppUsers";
        var expiryMinutes = int.TryParse(_configuration["Jwt:ExpiryMinutes"], out var exp) ? exp : 120;

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.UserId.ToString()),
            new Claim(ClaimTypes.NameIdentifier, user.UserId.ToString()),
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            notBefore: DateTime.UtcNow,
            expires: DateTime.UtcNow.AddMinutes(expiryMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
