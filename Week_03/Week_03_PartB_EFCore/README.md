# Week 3 - Part B: Entity Framework Core with PostgreSQL

## 📌 Overview
This module demonstrates object-relational mapping (ORM) using **Entity Framework Core 8.0** configured with the **Npgsql PostgreSQL provider** (`Npgsql.EntityFrameworkCore.PostgreSQL`). 

Instead of writing raw SQL statements by hand, EF Core allows C# applications to interact with PostgreSQL using strongly-typed C# domain models, `DbContext` session management, LINQ expressions, and versioned schema migrations.

---

## 🛠️ Environment Setup & Custom Configuration
- **.NET SDK Location**: Configured at `D:\Software\dotnet` (System `PATH`).
- **NuGet Packages Directory**: Redirected to `D:\Software\VS_Code_Related\dotnet-packages` (`NUGET_PACKAGES`).
- **Environment Security**: Database credentials are kept out of source code by utilizing a `.env` file (`.gitignore` protected) and mapped dynamically in `LibraryDbContext.cs`.

---

## 🔒 Connection String & `.env` Security

A `.env.example` template is committed to Git while the active `.env` file is ignored:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=librarydb_week3
POSTGRES_USER=postgres
POSTGRES_PASSWORD=private
```

In [`LibraryDbContext.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/Data/LibraryDbContext.cs), the context dynamically reads these environment variables:

```csharp
public static string GetConnectionString()
{
    var host = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "localhost";
    var port = Environment.GetEnvironmentVariable("POSTGRES_PORT") ?? "5432";
    var db = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "librarydb_week3";
    var user = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
    var pass = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "private";

    return $"Host={host};Port={port};Database={db};Username={user};Password={pass}";
}
```

---

## 🏗️ Domain Entity Models & Relationships

| Entity Class | PostgreSQL Table | Primary Key | Key Relationships / Mapping |
| :--- | :--- | :--- | :--- |
| [`Author.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/Models/Author.cs) | `"Authors"` | `AuthorId` | One-to-Many (`1:N`) with `Book` |
| [`Book.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/Models/Book.cs) | `"Books"` | `BookId` | Many-to-One with `Author`, Foreign Key `AuthorId` |
| [`Category.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/Models/Category.cs) | `"Categories"` | `CategoryId` | Many-to-Many (`M:N`) with `Book` via `BookCategory` |
| [`BookCategory.cs`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartB_EFCore/Models/BookCategory.cs) | `"BookCategories"` | Composite (`BookId`, `CategoryId`) | Junction entity table |

---

## ⚡ EF Core CRUD & LINQ Snippets

### 1. Add Record (`INSERT`)
```csharp
var newAuthor = new Author { FullName = "Faiz Ahmed Faiz", City = "Islamabad" };
context.Authors.Add(newAuthor);
await context.SaveChangesAsync();
```

### 2. Filtered LINQ Query (`SELECT ... WHERE`)
```csharp
var authorBooks = await context.Books
    .Include(b => b.Author)
    .Where(b => b.AuthorId == 2)
    .ToListAsync();
```

### 3. Update Record (`UPDATE`)
```csharp
var book = await context.Books.FindAsync(1);
if (book != null) {
    book.PublicationYear = 2025;
    await context.SaveChangesAsync();
}
```

### 4. Delete Record (`DELETE`)
```csharp
var book = await context.Books.FindAsync(1);
if (book != null) {
    context.Books.Remove(book);
    await context.SaveChangesAsync();
}
```

---

## 🔄 EF Core Migration Commands

To generate and apply database schema changes in PostgreSQL using EF Core CLI tools:

1. **Generate Initial Migration**:
   ```bash
   dotnet ef migrations add InitialCreate
   ```
2. **Apply Migration to PostgreSQL Database**:
   ```bash
   dotnet ef database update
   ```

---

## 📢 Git Checkpoint
```bash
git add Week_03_PartB_EFCore/
git commit -m "feat: add EF Core models, LibraryDbContext, Npgsql PostgreSQL provider, and .env security integration"
```
