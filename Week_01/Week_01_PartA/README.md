# Week 1 - Part A: C# and .NET Programming Foundations

Welcome to **Part A** of Week 1 in the **Nexa Solutions Internship Program**. This module establishes core backend competencies in **C#** and modern cross-platform **.NET**, focusing on application architecture, language syntax, flow control, procedural logic, and elementary memory constructs.

---

## Table of Contents
1. [Architecture Overview: .NET SDK vs. .NET Runtime](#1-architecture-overview-net-sdk-vs-net-runtime)
2. [Console Applications & CLI Lifecycle](#2-console-applications--cli-lifecycle)
3. [C# Syntax, Type System & Variables](#3-c-syntax-type-system--variables)
4. [Control Flow: Branching & Iteration](#4-control-flow-branching--iteration)
5. [Procedural Logic: Methods & Defensive Parsing](#5-procedural-logic-methods--defensive-parsing)
6. [Basic Arrays & Bounds Traversal](#6-basic-arrays--bounds-traversal)
7. [Hands-On Practice Exercises](#7-hands-on-practice-exercises)
   - [Exercise 1: Robust Four-Operation Calculator](#exercise-1-robust-four-operation-calculator)
   - [Exercise 2: Even or Odd Checker](#exercise-2-even-or-odd-checker)
   - [Exercise 3: Classic FizzBuzz (1 to 100)](#exercise-3-classic-fizzbuzz-1-to-100)
   - [Exercise 4: Academic Grading System](#exercise-4-academic-grading-system)
   - [Exercise 5: Array Min / Max Traversal](#exercise-5-array-min--max-traversal)
8. [How to Build and Run](#8-how-to-build-and-run)
9. [Key Takeaways & Best Practices](#9-key-takeaways--best-practices)

---

## 1. Architecture Overview: .NET SDK vs. .NET Runtime

Understanding the .NET execution pipeline is fundamental for any software engineer working across modern web and enterprise platforms.

```
       Developer Machine / CI-CD                         Target Machine / Server
┌───────────────────────────────────────┐         ┌───────────────────────────────────┐
│              .NET SDK                 │         │           .NET Runtime            │
│  ┌───────────────┐ ┌────────────────┐ │         │  ┌──────────────────────────────┐ │
│  │   Compilers   │ │ Build Tools    │ │         │  │ Common Language Runtime (CLR)│ │
│  │  (Roslyn C#)  │ │ (MSBuild, CLI) │ │         │  │ ┌────────────┐ ┌───────────┐ │ │
│  └───────┬───────┘ └────────────────┘ │ Build   │  │ │ JIT Engine │ │  Garbage  │ │ │
│          ▼                            ├────────►│  │ │ (IL -> ASM)│ │ Collector │ │ │
│  Intermediate Language (.dll assembly)│         │  │ └────────────┘ └───────────┘ │ │
│                                       │         │  │ Base Class Libraries (BCL)   │ │
└───────────────────────────────────────┘         │  └──────────────────────────────┘ │
                                                  └───────────────────────────────────┘
```

* **.NET SDK (Software Development Kit):**
  The complete toolset required to write, compile, test, and package applications. It includes the Roslyn C# compiler (`csc`), project build engine (`MSBuild`), package client (`NuGet`), and the `dotnet` CLI.
* **.NET Runtime (CLR - Common Language Runtime):**
  The lightweight execution engine required only to run compiled code. It houses:
  - **JIT (Just-In-Time) Compiler:** Translates machine-agnostic Common Intermediate Language (CIL/IL) into native CPU machine instructions upon execution.
  - **Garbage Collector (GC):** Automates memory allocation and reclamation on the managed heap.
  - **BCL (Base Class Library):** Standardized, foundational runtime classes (e.g., `System`, `System.IO`, `System.Collections`).

---

## 2. Console Applications & CLI Lifecycle

Modern .NET console applications target single or multiple platforms via a unified project specification file (`.csproj`):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
```

### Essential CLI Lifecycle Commands
| Command | Purpose |
| :--- | :--- |
| `dotnet new console -n Week_01_PartA` | Scaffolds a new C# console project template. |
| `dotnet restore` | Resolves and downloads external NuGet packages and tool references. |
| `dotnet build` | Compiles source files into an intermediate assembly (`.dll`) under `/bin/Debug/`. |
| `dotnet run` | Compiles incrementally (if needed) and launches the application entry point (`Main`). |
| `dotnet clean` | Purges build artifacts (`bin` and `obj` directories). |

---

## 3. C# Syntax, Type System & Variables

C# is a strongly typed, object-oriented language. Every variable has a defined type categorized as either a **Value Type** (allocated on the stack or inline within objects) or a **Reference Type** (stored on the managed heap with an address pointer on the stack).

### Core Primitive Data Types
| Type | Category | Size | Example Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| `int` | Value (Integer) | 4 bytes | `42` | Signed 32-bit integer (-2B to +2B). |
| `double` | Value (Floating) | 8 bytes | `3.14159` | 64-bit IEEE double-precision float. |
| `decimal`| Value (Financial)| 16 bytes| `19.99m` | High-precision 128-bit format for monetary calculations. |
| `bool` | Value (Boolean) | 1 byte | `true`, `false` | Logical boolean flag. |
| `char` | Value (Character)| 2 bytes | `'A'` | Single Unicode character. |
| `string` | Reference | Dynamic | `"Nexa Solutions"`| Immutable sequence of UTF-16 characters. |

```csharp
// Variable declarations
int studentCount = 35;
double defaultCutoff = 75.5;
bool isEnrollmentOpen = true;
string courseTitle = "Programming Foundations";

// String interpolation
string summary = $"Course: {courseTitle} | Capacity: {studentCount}";
```

---

## 4. Control Flow: Branching & Iteration

### Conditional Logic: `if / else if / else` vs. `switch`
- Use `if / else` chains when evaluating ranges or complex boolean expressions.
- Use `switch` statements (or C# switch expressions) when matching discrete constants, states, or menu selectors.

```csharp
// Range comparison using if/else
if (marks >= 85)
    grade = "A";
else if (marks >= 70)
    grade = "B";
else
    grade = "F";

// Discrete state matching using switch
switch (menuSelection)
{
    case "1":
        ExecuteCalculator();
        break;
    case "6":
        isExiting = true;
        break;
    default:
        Console.WriteLine("Invalid option.");
        break;
}
```

### Iteration Statements
- `for`: Counted loops where iteration bounds are predetermined.
- `while`: Condition-first loops where the termination state is evaluated before every cycle.
- `do-while`: Executes at least once before testing the loop predicate.
- `foreach`: Read-only, sequential enumeration over collections implementing `IEnumerable`.

---

## 5. Procedural Logic: Methods & Defensive Parsing

Writing resilient console code requires defensive input handling. The classical `int.Parse()` or `Convert.ToInt32()` methods throw unhandled exceptions (`FormatException`, `OverflowException`) on unexpected user input, crashing the process.

Modern C# applications leverage `TryParse`:

```csharp
Console.Write("Enter a number: ");
string input = Console.ReadLine();

// Safe evaluation without throwing exceptions
if (double.TryParse(input, out double validatedNumber))
{
    Console.WriteLine($"Parsed number: {validatedNumber}");
}
else
{
    Console.WriteLine("Error: Invalid numeric input.");
}
```

---

## 6. Basic Arrays & Bounds Traversal

An array in C# is a contiguous, fixed-size reference type holding elements of identical type:

```csharp
// Declaration and initialisation syntax
int[] numbers = new int[5] { 10, 20, 30, 40, 50 };

// Zero-based index bounds
int firstElement = numbers[0];
int lastElement = numbers[numbers.Length - 1];

// Traversal
for (int i = 0; i < numbers.Length; i++)
{
    Console.WriteLine($"Index {i}: {numbers[i]}");
}
```

---

## 7. Hands-On Practice Exercises

The implementation in `Week_01_PartA/Program.cs` encapsulates a command-line interactive runner featuring five core exercises:

### Exercise 1: Robust Four-Operation Calculator
Accepts two numeric operands and computes addition, subtraction, multiplication, and guarded division:

```csharp
static void Calculator()
{
    Console.WriteLine("--- Calculator ---");
    Console.Write("Enter first number: ");
    if (!double.TryParse(Console.ReadLine(), out double num1))
    {
        Console.WriteLine("Invalid input. Please enter a valid number.");
        return;
    }

    Console.Write("Enter second number: ");
    if (!double.TryParse(Console.ReadLine(), out double num2))
    {
        Console.WriteLine("Invalid input. Please enter a valid number.");
        return;
    }

    Console.WriteLine($"Addition: {num1 + num2}");
    Console.WriteLine($"Subtraction: {num1 - num2}");
    Console.WriteLine($"Multiplication: {num1 * num2}");
    
    // Guard against Divide-By-Zero
    if (num2 != 0)
        Console.WriteLine($"Division: {num1 / num2}");
    else
        Console.WriteLine("Division: Cannot divide by zero.");
}
```

### Exercise 2: Even or Odd Checker
Determines parity utilizing the modulus operator (`%`):

```csharp
static void EvenOrOdd()
{
    Console.WriteLine("--- Even Number or Odd Number ---");
    Console.Write("Enter a number: ");
    if (int.TryParse(Console.ReadLine(), out int input))
    {
        if (input % 2 == 0)
            Console.WriteLine($"{input} is an Even Number.");
        else
            Console.WriteLine($"{input} is an Odd Number.");
    }
}
```

### Exercise 3: Classic FizzBuzz (1 to 100)
Demonstrates loop iteration and nested compound boolean conditions:

```csharp
static void FizzBuzz()
{
    Console.WriteLine("--- FizzBuzz (1-100) ---");
    for (int i = 1; i <= 100; i++)
    {
        if (i % 3 == 0 && i % 5 == 0)
            Console.WriteLine("FizzBuzz");
        else if (i % 3 == 0)
            Console.WriteLine("Fizz");
        else if (i % 5 == 0)
            Console.WriteLine("Buzz");
        else
            Console.WriteLine(i);
    }
}
```

### Exercise 4: Academic Grading System
Evaluates student marks across segmented performance brackets:

```csharp
static void MarksToGrade()
{
    Console.WriteLine("--- Marks to Grade ---");
    Console.Write("Enter your marks (0-100): ");
    if (int.TryParse(Console.ReadLine(), out int marks))
    {
        if (marks >= 85 && marks <= 100)      Console.WriteLine("Grade: A");
        else if (marks >= 80 && marks < 85)   Console.WriteLine("Grade: A-");
        else if (marks >= 75 && marks < 80)   Console.WriteLine("Grade: B+");
        else if (marks >= 70 && marks < 75)   Console.WriteLine("Grade: B-");
        else if (marks >= 65 && marks < 70)   Console.WriteLine("Grade: C+");
        else if (marks >= 60 && marks < 65)   Console.WriteLine("Grade: C-");
        else if (marks >= 55 && marks < 60)   Console.WriteLine("Grade: D+");
        else if (marks >= 50 && marks < 55)   Console.WriteLine("Grade: D-");
        else                                  Console.WriteLine("Grade: F");
    }
}
```

### Exercise 5: Array Min / Max Traversal
Performs a single-pass $O(n)$ search across an integer array to detect extreme values:

```csharp
static void ArrayMinMax()
{
    Console.WriteLine("--- Array Min/Max ---");
    int[] array = { 2, 5, 4, 11, 78, 13, 5, 1, 9, 0 };
    int min = array[0];
    int max = array[0];

    for (int i = 1; i < array.Length; i++)
    {
        if (array[i] < min)
            min = array[i];
        if (array[i] > max)
            max = array[i];
    }

    Console.WriteLine($"Smallest value: {min}");
    Console.WriteLine($"Largest value:  {max}");
}
```

---

## 8. How to Build and Run

To execute the project from your terminal or command prompt:

```bash
# Navigate to the Part A project folder
cd "Week_01/Week_01_PartA"

# Restore dependencies
dotnet restore

# Build the project
dotnet build

# Launch the interactive menu application
dotnet run
```

---

## 9. Key Takeaways & Best Practices

1. **Prefer `TryParse` over `Parse`**: Eliminates unexpected runtime crashes caused by malformed input.
2. **Defend against Arithmetic Exceptions**: Always verify divisor values (`num2 != 0`) prior to floating-point or integer divisions.
3. **Array Boundaries**: Use `array.Length` instead of hardcoding bounds to prevent `IndexOutOfRangeException`.
4. **Clean Code Formatting**: Structure terminal menus with clear exits, helpful prompts, and clean feedback cycles.
