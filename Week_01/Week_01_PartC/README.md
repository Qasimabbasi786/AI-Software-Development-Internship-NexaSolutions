# Week 1 - Part C: Generic Collections, Exception Handling, and LINQ

Welcome to **Part C** of Week 1 in the **Nexa Solutions Internship Program**. This module covers three fundamental enterprise C# capabilities: **Generic Collections** (`List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`), robust **Exception Handling** via `try/catch/finally`, and functional data querying with **LINQ (Language Integrated Query)**.

---

## Table of Contents
1. [Generic Collections in C# (.NET BCL)](#1-generic-collections-in-c-net-bcl)
   - [`List<T>`: Dynamic Array](#listt-dynamic-array)
   - [`Dictionary<TKey, TValue>`: Key-Value Hash Map](#dictionarytkey-tvalue-key-value-hash-map)
   - [`HashSet<T>`: Unique Set Collection](#hashsett-unique-set-collection)
   - [Collection Complexity & Characteristics](#collection-complexity--characteristics)
2. [Defensive Programming & Exception Handling](#2-defensive-programming--exception-handling)
   - [The Exception Pipeline (`try / catch / finally`)](#the-exception-pipeline-try--catch--finally)
   - [Exception Hierarchy & Specific Catch Blocks](#exception-hierarchy--specific-catch-blocks)
3. [Language Integrated Query (LINQ) Fundamentals](#3-language-integrated-query-linq-fundamentals)
   - [Core Operators Explained](#core-operators-explained)
   - [Deferred Execution vs. Immediate Execution](#deferred-execution-vs-immediate-execution)
4. [Domain Walkthrough: Student Records Processing](#4-domain-walkthrough-student-records-processing)
5. [Code Deep-Dive (`Program.cs`)](#5-code-deep-dive-programcs)
6. [How to Build and Run](#6-how-to-build-and-run)
7. [Enterprise Best Practices](#7-enterprise-best-practices)

---

## 1. Generic Collections in C# (.NET BCL)

Prior to generics in .NET 2.0, collections operated on `object`, incurring performance penalties from boxing/unboxing and exposing code to runtime type mismatches. Generics (`System.Collections.Generic`) provide compile-time type safety and maximum execution performance.

### `List<T>`: Dynamic Array
An ordered, zero-indexed list that expands its capacity dynamically as elements are appended.
```csharp
List<string> departments = new List<string> { "CS", "AI", "CyberSecurity" };
departments.Add("Data Science");
```

### `Dictionary<TKey, TValue>`: Key-Value Hash Map
An associative array linking unique keys to corresponding values, providing near $O(1)$ lookups based on key hashing.
```csharp
Dictionary<int, string> studentRoster = new Dictionary<int, string>
{
    { 101, "Muhammad Qasim" },
    { 102, "Minahil" }
};

if (studentRoster.TryGetValue(101, out string studentName))
{
    Console.WriteLine($"Student: {studentName}");
}
```

### `HashSet<T>`: Unique Set Collection
An unordered collection optimized for mathematical set operations (unions, intersections) and ensuring uniqueness without duplicate keys.
```csharp
HashSet<string> enrolledIds = new HashSet<string> { "S001", "S002", "S001" };
// Count is 2 because duplicates are automatically rejected
```

### Collection Complexity & Characteristics
| Collection | Access by Index | Search / Lookup | Insert / Add | Memory Overhead |
| :--- | :--- | :--- | :--- | :--- |
| `List<T>` | $O(1)$ | $O(n)$ | Amortized $O(1)$ | Low (contiguous memory buffer) |
| `Dictionary<TKey, TValue>` | N/A (Key lookup: $O(1)$) | $O(1)$ average | $O(1)$ average | Medium (hash buckets & entry arrays) |
| `HashSet<T>` | N/A | $O(1)$ average | $O(1)$ average | Medium (hash buckets) |

---

## 2. Defensive Programming & Exception Handling

Applications encounter unexpected conditions: missing files, network drops, malformed user input, or unparseable tokens. Robust software anticipates failures using structured exception handling.

### The Exception Pipeline (`try / catch / finally`)

```
   ┌────────────────────────────────────────────────────────┐
   │                       try Block                        │
   │  Execute risky operations (e.g. parsing, file I/O)     │
   └──────────────────────────┬─────────────────────────────┘
                              │
               Was an exception thrown?
               ├── Yes ──► Match against catch blocks
               └── No  ──► Skip catch blocks
                              │
   ┌──────────────────────────▼─────────────────────────────┐
   │                      catch Block                       │
   │  Specific: catch (FormatException ex)                  │
   │  Fallback: catch (Exception ex)                        │
   └──────────────────────────┬─────────────────────────────┘
                              │
   ┌──────────────────────────▼─────────────────────────────┐
   │                     finally Block                      │
   │  Always runs: Cleanup resources, close streams/sockets │
   └────────────────────────────────────────────────────────┘
```

### Exception Hierarchy & Specific Catch Blocks
Always order `catch` blocks from most specific to least specific. Catching raw `Exception` first causes unreachable code warnings because it intercepts all sub-types.

```csharp
try
{
    Console.Write("Enter Student ID: ");
    int id = int.Parse(Console.ReadLine()); // May throw FormatException
}
catch (FormatException fEx)
{
    // Specific: Non-numeric characters entered
    Console.WriteLine($"Format error: {fEx.Message}");
}
catch (OverflowException oEx)
{
    // Specific: Number entered is too large for Int32
    Console.WriteLine($"Overflow error: {oEx.Message}");
}
catch (Exception ex)
{
    // Catch-all fallback
    Console.WriteLine($"Unexpected error: {ex.Message}");
}
finally
{
    // Guaranteed cleanup step
    Console.WriteLine("Search operation terminated.");
}
```

---

## 3. Language Integrated Query (LINQ) Fundamentals

LINQ brings SQL-like declarative querying capabilities directly into C#. Instead of imperative nested loops, engineers express data filters and transformations with fluent, readable expressions.

### Core Operators Explained

| Method | Behavior | Return Type | Equivalent SQL Concept |
| :--- | :--- | :--- | :--- |
| `Where(predicate)` | Filters elements satisfying a boolean condition. | `IEnumerable<T>` | `WHERE condition` |
| `Select(transform)` | Projects each element into a new form or shape. | `IEnumerable<TResult>` | `SELECT col1, col2` |
| `OrderBy(keySelector)` | Sorts elements ascending by a specified property. | `IOrderedEnumerable<T>` | `ORDER BY col ASC` |
| `OrderByDescending(keySelector)` | Sorts elements descending by a specified property. | `IOrderedEnumerable<T>` | `ORDER BY col DESC` |
| `FirstOrDefault(predicate)` | Returns the first matching element, or `default(T)` (`null` for reference types) if none found. | `T?` | `SELECT TOP 1 ...` |
| `Any(predicate)` | Returns `true` if at least one element matches. | `bool` | `EXISTS(...)` |
| `Count(predicate)` | Evaluates total matching elements. | `int` | `COUNT(*)` |

### Deferred Execution vs. Immediate Execution
* **Deferred (Lazy) Execution:** Methods such as `Where` and `Select` do not execute immediately when defined. They return an enumerable query object; the actual filtering occurs only when the collection is iterated over (e.g. in a `foreach` loop).
* **Immediate (Eager) Execution:** Methods like `ToList()`, `ToArray()`, `Count()`, and `FirstOrDefault()` force the query to evaluate immediately, capturing the current state in memory.

---

## 4. Domain Walkthrough: Student Records Processing

The `Week_01_PartC` sample models an academic departmental dataset:

```csharp
public class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Department { get; set; }
    public double Marks { get; set; }
}
```

The sample demonstrates:
1. Instantiating a `List<Student>` with five structured records.
2. Filtering records targeting the **CS Department** using `.Where()`.
3. Sorting students by **Marks (Highest to Lowest)** using `.OrderByDescending()`.
4. Searching a specific record by **ID** using `.FirstOrDefault()` wrapped in a defensive `try / catch` structure.

---

## 5. Code Deep-Dive (`Program.cs`)

Here is how the core queries are structured in [Program.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartC/Program.cs):

```csharp
// 1. Initialise the List
List<Student> students = new List<Student>
{
    new Student { Id = 1, Name = "Muhammad Qasim", Department = "CS", Marks = 82.0 },
    new Student { Id = 2, Name = "Minahil", Department = "AI", Marks = 82.0 },
    new Student { Id = 3, Name = "Asma", Department = "CS", Marks = 79.5 },
    new Student { Id = 4, Name = "Anoosha", Department = "AI", Marks = 80.0 },
    new Student { Id = 5, Name = "Azmat", Department = "CYS", Marks = 76.0 }
};

// 2. Department Filtering with LINQ
var csStudents = students.Where(s => s.Department == "CS").ToList();
foreach (var s in csStudents)
{
    Console.WriteLine($"{s.Name} ({s.Marks})");
}

// 3. Sorting with OrderByDescending
var sortedStudents = students.OrderByDescending(s => s.Marks).ToList();

// 4. Safe Search with FirstOrDefault and Exception Handling
Console.Write("Enter Student ID to search: ");
string inputId = Console.ReadLine();

try
{
    int id = int.Parse(inputId);
    var student = students.FirstOrDefault(s => s.Id == id);
    
    if (student != null)
        Console.WriteLine($"Found Student: {student.Name}, Dept: {student.Department}");
    else
        Console.WriteLine($"No student found with ID {id}.");
}
catch (FormatException)
{
    Console.WriteLine("Invalid input! Please enter a valid numeric ID.");
}
catch (Exception ex)
{
    Console.WriteLine($"An unexpected error occurred: {ex.Message}");
}
```

---

## 6. How to Build and Run

```bash
# Navigate to Part C
cd "Week_01/Week_01_PartC"

# Build the project
dotnet build

# Run the console demonstration
dotnet run
```

---

## 7. Enterprise Best Practices

1. **Avoid `.First()` when null is possible**: Prefer `.FirstOrDefault()` to prevent unhandled `InvalidOperationException` crashes if no matching element exists.
2. **Materialize Queries Intentionally**: Call `.ToList()` when you plan to reuse the results multiple times, avoiding duplicate query re-evaluations.
3. **Never swallow exceptions blindly**: Avoid empty `catch { }` blocks that suppress problems without logging or notifying the caller.
4. **Choose the Right Collection**:
   - Use `List<T>` for sequential, index-based data.
   - Use `Dictionary<TKey, TValue>` for key-based lookups.
   - Use `HashSet<T>` to guarantee uniqueness and evaluate memberships quickly.
