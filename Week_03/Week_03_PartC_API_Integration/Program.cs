using Microsoft.EntityFrameworkCore;
using Week_03_PartC_API_Integration.Data;
using Week_03_PartC_API_Integration.Repositories;

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

// Add services to the container.
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        // Fix circular dependency serialization error between Book <-> Author navigation properties
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Register PostgreSQL DbContext
builder.Services.AddDbContext<LibraryDbContext>(options =>
    options.UseNpgsql(LibraryDbContext.GetConnectionString()));

// Register Repository Dependency Injection
builder.Services.AddScoped<IBookRepository, BookRepository>();

var app = builder.Build();

// Enable CORS Middleware (Must be before UseAuthorization and MapControllers)
app.UseCors("AllowAngularApp");

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Week 3 Library API v1");
        c.RoutePrefix = string.Empty; // Serves Swagger UI at application root (http://localhost:5000/)
    });
}

app.UseAuthorization();
app.MapControllers();

app.Run();
