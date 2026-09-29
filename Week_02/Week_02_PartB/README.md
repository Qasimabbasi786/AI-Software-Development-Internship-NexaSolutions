# Week 2 - Part B: ASP.NET Core Web API Fundamentals

Welcome to **Part B** of Week 2 in the **Nexa Solutions Internship Program**. Having solidified intermediate C# design principles, this module steps into modern backend server architecture using **ASP.NET Core Web API**. You will learn the mechanics of the HTTP protocol, controller routing, HTTP verbs, status codes, dependency injection containers, app configuration, and automated Swagger/OpenAPI documentation.

---

## Table of Contents
1. [REST & HTTP API Fundamentals](#1-rest--http-api-fundamentals)
2. [ASP.NET Core Request/Response Pipeline & Middleware](#2-aspnet-core-requestresponse-pipeline--middleware)
3. [HTTP Verbs & REST Semantics (CRUD Mapping)](#3-http-verbs--rest-semantics-crud-mapping)
4. [Standard HTTP Status Codes](#4-standard-http-status-codes)
5. [Controllers, Routing & Parameter Binding](#5-controllers-routing--parameter-binding)
6. [Dependency Injection in ASP.NET Core](#6-dependency-injection-in-aspnet-core)
7. [Application Configuration & `appsettings.json`](#7-application-configuration--appsettingsjson)
8. [Swagger & OpenAPI Specification](#8-swagger--openapi-specification)
9. [Code Walkthrough: `GreetingController.cs`](#9-code-walkthrough-greetingcontrollercs)
10. [How to Build, Run & Test](#10-how-to-build-run--test)
11. [Enterprise API Best Practices](#11-enterprise-api-best-practices)

---

## 1. REST & HTTP API Fundamentals

A **Web API** provides programmatic access to server resources over HTTP. In REST (Representational State Transfer) architecture:
- **Resources** are modeled as discrete URIs (e.g., `/api/greeting`, `/api/greeting/1`).
- **Representations** are typically formatted in JSON.
- **Operations** utilize standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **State** is stateless; every request contains all authentication and payload information necessary to execute.

---

## 2. ASP.NET Core Request/Response Pipeline & Middleware

When an HTTP request enters an ASP.NET Core application, it traverses a chain of **Middleware** components before reaching the controller:

```
HTTP Request
     │
     ▼
┌────────────────────────────────────────────────────────┐
│  Developer Exception Page / Exception Handler          │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  Swagger & Swagger UI Middleware (API Docs)            │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  HTTPS Redirection & CORS Policy                       │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  Routing & Endpoint Selection                          │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  Authentication & Authorization                        │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│  Controller Action Execution & Model Binding           │
│  (GreetingController -> Returns IActionResult)          │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
HTTP Response (JSON + Status Code)
```

In [Program.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_PartB/Program.cs):
```csharp
var builder = WebApplication.CreateBuilder(args);

// Register controllers and Swagger generator
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the pipeline order
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Week 2 Part B API V1");
        c.RoutePrefix = string.Empty; // Serve Swagger at root URL
    });
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## 3. HTTP Verbs & REST Semantics (CRUD Mapping)

| HTTP Verb | Operation | Idempotent | Request Body | Typical Success Code |
| :--- | :--- | :--- | :--- | :--- |
| **`GET`** | Retrieve resource(s) | Yes | None | `200 OK` |
| **`POST`** | Create a new resource | No | JSON Payload | `201 Created` |
| **`PUT`** | Completely replace/update an existing resource | Yes | JSON Payload | `200 OK` or `204 No Content` |
| **`DELETE`**| Remove an existing resource | Yes | None | `200 OK` or `204 No Content` |

---

## 4. Standard HTTP Status Codes

REST APIs communicate result states using standard status code categories:

```
1xx Informational ──► Protocol negotiation
2xx Success       ──► 200 OK (Read/Update), 201 Created (Post), 204 No Content (Delete)
3xx Redirection   ──► 301 Moved Permanently, 304 Not Modified (Caching)
4xx Client Error  ──► 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
5xx Server Error  ──► 500 Internal Server Error, 503 Service Unavailable
```

---

## 5. Controllers, Routing & Parameter Binding

ASP.NET Core controllers inherit from `ControllerBase` and use attributes to declare route endpoints and binding rules:

### Controller Level Attributes
```csharp
[ApiController] // Enforces automatic model validation and inferring parameter sources
[Route("api/[controller]")] // Resolves to 'api/greeting'
public class GreetingController : ControllerBase
```

### Parameter Binding Sources
- `[FromRoute]`: Matches tokens from the URI path (e.g., `api/greeting/{id}`).
- `[FromBody]`: Deserializes the incoming JSON HTTP body into a C# DTO.
- `[FromQuery]`: Extracts key-value query string parameters (e.g., `api/greeting?category=design`).
- `[FromHeader]`: Binds HTTP request headers.

---

## 6. Dependency Injection in ASP.NET Core

ASP.NET Core provides a built-in Inversion of Control (IoC) container to manage object lifecycles:

| Lifetime | Method | Description | Common Use Case |
| :--- | :--- | :--- | :--- |
| **Transient** | `AddTransient<TService, TImpl>()` | A fresh instance is created every time it is requested. | Lightweight, stateless services. |
| **Scoped** | `AddScoped<TService, TImpl>()` | One instance per HTTP request lifecycle. Disposed at request completion. | Entity Framework Database Contexts, unit of work services. |
| **Singleton** | `AddSingleton<TService, TImpl>()` | Created once on application startup; reused for all subsequent requests across all users. | Caches, in-memory state stores, background workers. |

---

## 7. Application Configuration & `appsettings.json`

Configuration data is managed hierarchically using JSON configuration files and environment overrides:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

Values are injected using the `IConfiguration` abstraction or the strongly-typed **Options Pattern** (`IOptions<T>`).

---

## 8. Swagger & OpenAPI Specification

OpenAPI provides a machine-readable JSON description of your API endpoints. **Swagger UI** renders this specification as an interactive web page where engineers can inspect models and execute live HTTP requests.

In this project, Swagger UI is configured to load directly at the root URL (`http://localhost:<port>/`):
```csharp
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "Week 2 Part B API V1");
    c.RoutePrefix = string.Empty;
});
```

---

## 9. Code Walkthrough: `GreetingController.cs`

Located at [Controllers/GreetingController.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_02/Week_02_PartB/Controllers/GreetingController.cs):

```csharp
[ApiController]
[Route("api/[controller]")]
public class GreetingController : ControllerBase
{
    private static readonly List<GreetingModel> _greetings = new List<GreetingModel>
    {
        new GreetingModel { Id = 1, Name = "Muhammad Qasim", Message = "Welcome to Enterprise .NET Core API!" },
        new GreetingModel { Id = 2, Name = "Qasim Developer", Message = "Keep pushing forward with clean code!" }
    };

    // GET: api/greeting
    [HttpGet]
    public IActionResult GetAllGreetings()
    {
        return Ok(new
        {
            Status = "Success",
            Count = _greetings.Count,
            Data = _greetings
        });
    }

    // GET: api/greeting/1
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
```

---

## 10. How to Build, Run & Test

```bash
# Navigate to the Part B directory
cd "Week_02/Week_02_PartB"

# Restore dependencies & build
dotnet build

# Launch the Web API
dotnet run
```

Once running:
- Open your browser to the console output URL (typically `http://localhost:5xxx/` or `https://localhost:7xxx/`).
- Swagger UI will appear immediately at the root.
- Test `GET /api/greeting`, `GET /api/greeting/1`, and `POST /api/greeting` directly inside Swagger or using Postman/curl:

```bash
# Example curl POST request:
curl -X POST "http://localhost:5000/api/greeting" \
     -H "Content-Type: application/json" \
     -d '{"name": "Nexa Intern", "message": "Building scalable APIs!"}'
```

---

## 11. Enterprise API Best Practices

1. **Always Return Standardized Status Codes**: Return `201 Created` with a `Location` header upon entity creation; return `404 Not Found` for missing resources.
2. **Defensive Model Validation**: Check for empty or malformed inputs and return `400 Bad Request` with descriptive error details.
3. **Use Explicit Routing Constraints**: Constrain path parameters (e.g. `{id:int}`) to prevent route conflicts and early-reject invalid types.
4. **Use DTOs (Data Transfer Objects)**: Do not expose raw database entities directly to API clients. Use dedicated request/response models (`GreetingRequest`, `GreetingModel`).
