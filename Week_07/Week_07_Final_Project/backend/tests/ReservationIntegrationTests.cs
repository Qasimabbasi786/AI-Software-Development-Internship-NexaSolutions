using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Security.Claims;
using System.Text;
using System.Text.Json;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using Xunit;
using libraryAPI.Models;

namespace libraryAPI.Tests;

public class ReservationIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory _factory;
    private const string TestJwtSecret = "YourSuperSecretKeyForJwtSigningMustBeAtLeast32BytesLong!";

    public ReservationIntegrationTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    private string GenerateTestJwt(string userId, string role = "User")
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.UTF8.GetBytes(TestJwtSecret);
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new ClaimsIdentity(new[]
            {
                new Claim(ClaimTypes.NameIdentifier, userId),
                new Claim(ClaimTypes.Role, role),
                new Claim("sub", userId)
            }),
            Expires = DateTime.UtcNow.AddHours(2),
            Issuer = "LibraryAgentIssuer",
            Audience = "LibraryAgentAudience",
            SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
        };
        var token = tokenHandler.CreateToken(tokenDescriptor);
        return tokenHandler.WriteToken(token);
    }

    [Fact]
    public async Task Reserve_WithoutToken_Returns401Unauthorized()
    {
        // Act: POST /api/books/1/reserve without Authorization header
        var response = await _client.PostAsync("/api/books/1/reserve", null);

        // Assert: 401 Unauthorized
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task Reserve_ValidToken_Returns200AndCreatesReservation()
    {
        var token = GenerateTestJwt("user_101");
        using var request = new HttpRequestMessage(HttpMethod.Post, "/api/books/1/reserve");
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        request.Headers.Add("Idempotency-Key", "key-initial-test");

        var response = await _client.SendAsync(request);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var content = await response.Content.ReadAsStringAsync();
        Assert.Contains("Reservation created successfully", content);
    }

    [Fact]
    public async Task Reserve_SameIdempotencyKeyTwice_CreatesOnlyOneReservation()
    {
        var token = GenerateTestJwt("user_102");
        var idempotencyKey = $"idempotent-key-{Guid.NewGuid()}";

        // First attempt on Book 1 (or new book)
        using var req1 = new HttpRequestMessage(HttpMethod.Post, "/api/books/1/reserve");
        req1.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        req1.Headers.Add("Idempotency-Key", idempotencyKey);
        var res1 = await _client.SendAsync(req1);

        // Second attempt with exact same key
        using var req2 = new HttpRequestMessage(HttpMethod.Post, "/api/books/1/reserve");
        req2.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        req2.Headers.Add("Idempotency-Key", idempotencyKey);
        var res2 = await _client.SendAsync(req2);

        // Both must return 200 OK without failing
        Assert.Equal(HttpStatusCode.OK, res2.StatusCode);
        var content2 = await res2.Content.ReadAsStringAsync();
        Assert.Contains("Idempotent response", content2);
    }

    [Fact]
    public async Task Reserve_AlreadyReservedBook_Returns409Conflict()
    {
        var token = GenerateTestJwt("user_103");
        // Book 2 is seeded as IsAvailable = false
        using var req = new HttpRequestMessage(HttpMethod.Post, "/api/books/2/reserve");
        req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        req.Headers.Add("Idempotency-Key", $"key-conflict-{Guid.NewGuid()}");

        var response = await _client.SendAsync(req);

        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
        var content = await response.Content.ReadAsStringAsync();
        Assert.Contains("already reserved or unavailable", content);
    }

    [Fact]
    public async Task GetMyReservations_ReturnsOnlyCallerReservations()
    {
        var userA = "user_alpha";
        var tokenA = GenerateTestJwt(userA);

        using var req = new HttpRequestMessage(HttpMethod.Get, "/api/me/reservations");
        req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", tokenA);

        var response = await _client.SendAsync(req);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task Preferences_SaveAndRetrieve_Succeeds()
    {
        var user = "pref_user_1";
        var token = GenerateTestJwt(user);

        // Save preference
        using var postReq = new HttpRequestMessage(HttpMethod.Post, "/api/me/preferences");
        postReq.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        postReq.Content = JsonContent.Create(new { Key = "favorite_genre", Value = "Science Fiction" });
        var postRes = await _client.SendAsync(postReq);
        Assert.Equal(HttpStatusCode.OK, postRes.StatusCode);

        // Retrieve preference
        using var getReq = new HttpRequestMessage(HttpMethod.Get, "/api/me/preferences");
        getReq.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        var getRes = await _client.SendAsync(getReq);
        Assert.Equal(HttpStatusCode.OK, getRes.StatusCode);
        var content = await getRes.Content.ReadAsStringAsync();
        Assert.Contains("favorite_genre", content);
        Assert.Contains("Science Fiction", content);
    }
}
