using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using libraryAPI.Data;
using libraryAPI.Repositories;
using libraryAPI.Services;
using Polly;
using Polly.Extensions.Http;

// Load local .env file if present
var envPath = Path.Combine(Directory.GetCurrentDirectory(), ".env");
if (File.Exists(envPath))
{
    foreach (var line in File.ReadAllLines(envPath))
    {
        var parts = line.Split('=', 2, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        if (parts.Length == 2 && !parts[0].StartsWith('#'))
        {
            Environment.SetEnvironmentVariable(parts[0], parts[1]);
        }
    }
}

var builder = WebApplication.CreateBuilder(args);

// 1. Configure CORS Policy to allow Angular Frontend (http://localhost:4200)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngularApp", policy =>
    {
        policy.WithOrigins("http://localhost:4200", "https://localhost:4200")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

// 2. Add controllers with JSON circular reference handling
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });

// 3. Configure JWT Authentication
var jwtKey = builder.Configuration["Jwt:Key"] ?? "NexaSolutions_OriginSoft_SecureKey_2026_JWT_SecretKey_9876543210!";
var keyBytes = Encoding.UTF8.GetBytes(jwtKey);

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(keyBytes),
        ValidateIssuer = false,
        ValidateAudience = false,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();

// 4. Configure Swagger with JWT Bearer definition
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Nexa Solutions Library API - Week 4",
        Version = "v1",
        Description = "ASP.NET Core Web API with JWT Bearer Authentication & Role-Based Authorization."
    });

    // Add JWT Authentication Support in Swagger UI
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "Bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Enter JWT Bearer token format: Bearer <your_jwt_token>"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});

// 5. Register PostgreSQL DbContext
builder.Services.AddDbContext<LibraryDbContext>(options =>
    options.UseNpgsql(LibraryDbContext.GetConnectionString()));

// 6. Register Repository Dependency Injection
builder.Services.AddScoped<IBookRepository, BookRepository>();

// 7. Register Resilient Typed HttpClient for AI Service via Polly
var aiServiceUrl = Environment.GetEnvironmentVariable("FASTAPI_API_URL") 
                   ?? builder.Configuration["AiService:BaseUrl"] 
                   ?? "http://localhost:8000";

builder.Services.AddHttpClient<IAiServiceClient, AiServiceClient>(client =>
{
    client.BaseAddress = new Uri(aiServiceUrl);
    client.Timeout = TimeSpan.FromSeconds(10);
})
.AddPolicyHandler(GetRetryPolicy())
.AddPolicyHandler(GetCircuitBreakerPolicy());

static Polly.IAsyncPolicy<HttpResponseMessage> GetRetryPolicy() =>
    Polly.Extensions.Http.HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)));

static Polly.IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy() =>
    Polly.Extensions.Http.HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 3,
            durationOfBreak: TimeSpan.FromSeconds(30)
        );

var app = builder.Build();

// Automatically ensure PostgreSQL database and tables are created
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<LibraryDbContext>();
    dbContext.Database.EnsureCreated();
}

// Enable CORS Middleware
app.UseCors("AllowAngularApp");

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Week 4 Library API v1");
        c.RoutePrefix = string.Empty; // Serves Swagger UI at application root
    });
}

// Authentication MUST be called BEFORE Authorization
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();
