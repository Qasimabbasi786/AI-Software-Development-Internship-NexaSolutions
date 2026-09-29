# Library Management API (ASP.NET Core Web API)
### Week 2 Final Project — Backend Service (`libraryAPI`)

Welcome to the backend service for the **Week 2 Capstone Project** in the **Nexa Solutions Internship Program**. This service is built with **ASP.NET Core 8 Web API** and implements the industry-standard **Controller-Service-Repository** pattern with in-memory persistence, CORS policy configuration, dependency injection, and interactive OpenAPI (Swagger) documentation.

---

## Table of Contents
1. [Architecture & Design Pattern](#1-architecture--design-pattern)
2. [Project Structure](#2-project-structure)
3. [Data Model (`Book.cs`)](#3-data-model-bookcs)
4. [Layer Breakdown](#4-layer-breakdown)
   - [Repository Layer (`IBookRepository` & `BookRepository`)](#repository-layer-ibookrepository--bookrepository)
   - [Service Layer (`IBookService` & `BookService`)](#service-layer-ibookservice--bookservice)
   - [Controller Layer (`BooksController.cs`)](#controller-layer-bookscontrollercs)
5. [CORS & Dependency Injection Configuration (`Program.cs`)](#5-cors--dependency-injection-configuration-programcs)
6. [API Endpoints & HTTP Status Contract](#6-api-endpoints--http-status-contract)
7. [How to Build, Run & Test](#7-how-to-build-run--test)
8. [Testing with Swagger and cURL](#8-testing-with-swagger-and-curl)

---

## 1. Architecture & Design Pattern

The application enforces strict separation of concerns using a 3-tier enterprise pattern:

```
 HTTP Request (from Angular / Postman / Swagger)
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│            Controllers (Presentation Layer)            │
│  - Routes HTTP requests & parses route/body inputs     │
│  - Returns standardized HTTP response status codes     │
└──────────────────────────┬─────────────────────────────┘
                           │ Calls IBookService
                           ▼
┌────────────────────────────────────────────────────────┐
│              Services (Business Logic Layer)           │
│  - Executes domain validation & business operations    │
│  - Coordinates between controllers and repository      │
└──────────────────────────┬─────────────────────────────┘
                           │ Calls IBookRepository
                           ▼
┌────────────────────────────────────────────────────────┐
│            Repositories (Data Persistence Layer)       │
│  - Manages in-memory List<Book> storage                │
│  - Encapsulates asynchronous Task-based data queries   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Project Structure

```
libraryAPI/
├── Controllers/
│   └── BooksController.cs         # RESTful HTTP endpoints & status codes
├── Models/
│   └── Book.cs                    # Domain entity model
├── Services/
│   ├── IBookService.cs            # Service contract interface
│   └── BookService.cs             # Business logic implementation
├── Repositories/
│   ├── IBookRepository.cs         # Repository contract interface
│   └── BookRepository.cs          # In-memory storage & CRUD operations
├── Properties/
│   └── launchSettings.json        # Local hosting profiles (Port 5184)
├── appsettings.json               # Application configuration
├── libraryAPI.csproj              # .NET 8 Project file
└── Program.cs                     # DI registration, CORS, middleware pipeline
```

---

## 3. Data Model (`Book.cs`)

Located in [`Models/Book.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Models/Book.cs):

```csharp
namespace libraryAPI.Models
{
    public class Book
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Author { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.Now;
    }
}
```

---

## 4. Layer Breakdown

### Repository Layer (`IBookRepository` & `BookRepository`)
Decouples storage mechanics from application logic. All methods return `Task` or `Task<T>` to maintain asynchronous architecture:

```csharp
public interface IBookRepository
{
    Task<IEnumerable<Book>> GetAllAsync();
    Task<Book?> GetByIdAsync(int id);
    Task<Book> AddAsync(Book book);
    Task<bool> UpdateAsync(Book book);
    Task<bool> DeleteAsync(int id);
}
```

Inside [`Repositories/BookRepository.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Repositories/BookRepository.cs):
- Seeded with initial mock records for immediate testing.
- Uses `_books.Max(b => b.Id) + 1` to generate auto-incrementing primary keys.
- Updates and deletions mutate the in-memory collection safely.

### Service Layer (`IBookService` & `BookService`)
Located in [`Services/BookService.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Services/BookService.cs). It acts as an intermediary, receiving the injected repository via constructor injection:

```csharp
public class BookService : IBookService
{
    private readonly IBookRepository _repository;

    public BookService(IBookRepository repository)
    {
        _repository = repository;
    }

    public Task<IEnumerable<Book>> GetAllBooksAsync() => _repository.GetAllAsync();
    public Task<Book?> GetBookByIdAsync(int id) => _repository.GetByIdAsync(id);
    public Task<Book> AddBookAsync(Book book) => _repository.AddAsync(book);
    public Task<bool> UpdateBookAsync(Book book) => _repository.UpdateAsync(book);
    public Task<bool> DeleteBookAsync(int id) => _repository.DeleteAsync(id);
}
```

### Controller Layer (`BooksController.cs`)
Located in [`Controllers/BooksController.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Controllers/BooksController.cs):
- `[ApiController]` enables automatic HTTP 400 responses on invalid models.
- `[Route("api/[controller]")]` maps to `/api/Books`.
- Uses semantic responses: `Ok()`, `CreatedAtAction()`, `BadRequest()`, and `NotFound()`.

---

## 5. CORS & Dependency Injection Configuration (`Program.cs`)

Located in [`Program.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_Final_Project/libraryAPI/Program.cs):

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Library Management Enterprise API",
        Version = "v1",
        Description = "An optimized backend service for managing library books."
    });
});

// Dependency Injection Lifetimes:
// 1. Singleton: Preserves in-memory book list across all client requests
builder.Services.AddSingleton<IBookRepository, BookRepository>();

// 2. Scoped: Created once per incoming HTTP request
builder.Services.AddScoped<IBookService, BookService>();

// Configure Cross-Origin Resource Sharing (CORS) for Angular
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngular", policy =>
    {
        policy.WithOrigins("http://localhost:4200")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Library API V1");
        c.RoutePrefix = string.Empty; // Loads Swagger at root http://localhost:<port>/
    });
}

app.UseCors("AllowAngular");
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## 6. API Endpoints & HTTP Status Contract

| Verb | Route | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **`GET`** | `/api/Books` | Retrieve all books | `200 OK` |
| **`GET`** | `/api/Books/{id}` | Retrieve single book by ID | `200 OK`, `404 Not Found` |
| **`POST`** | `/api/Books` | Register a new book | `201 Created` (includes Location header), `400 Bad Request` |
| **`PUT`** | `/api/Books/{id}` | Update existing book details | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **`DELETE`** | `/api/Books/{id}` | Delete book from system | `200 OK`, `404 Not Found` |

---

## 7. How to Build, Run & Test

```bash
# Navigate to libraryAPI directory
cd "Week_02/Week_02_Final_Project/libraryAPI"

# Restore NuGet dependencies
dotnet restore

# Build project
dotnet build

# Run the API
dotnet run
```

When started, note the port from the terminal (configured by default on `http://localhost:5184`). Open your browser to:
`http://localhost:5184/` to view the interactive **Swagger UI**.

---

## 8. Testing with Swagger and cURL

### Retrieve All Books
```bash
curl -X GET "http://localhost:5184/api/Books" -H "accept: application/json"
```

### Add a New Book
```bash
curl -X POST "http://localhost:5184/api/Books" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Clean Code in C#",
       "author": "Robert C. Martin",
       "category": "Software Architecture"
     }'
```

### Update a Book
```bash
curl -X PUT "http://localhost:5184/api/Books/1" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 1,
       "title": "C# Fundamentals (Updated)",
       "author": "Muhammad Qasim",
       "category": "Programming"
     }'
```

### Delete a Book
```bash
curl -X DELETE "http://localhost:5184/api/Books/1"
```
