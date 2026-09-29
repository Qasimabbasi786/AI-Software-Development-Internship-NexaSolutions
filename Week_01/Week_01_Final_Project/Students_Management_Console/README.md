# Week 1 Final Project - Student Management System (C# Console App)

## 📌 Overview
This component is a strongly-typed **C# .NET Console Application** designed to manage student records, academic metadata, and grade tracking. It demonstrates core object-oriented programming (OOP) principles, generic collection handling (`List<T>`), LINQ querying, and clean console interface interactions.

---

## 🏗️ Architecture & Component Design

```text
Students_Management_Console/
├── Program.cs             # Application entry point & interactive menu CLI loop
├── Models/
│   └── Student.cs         # Domain entity model (StudentId, FullName, Age, Major, GPA)
└── Services/
    └── StudentManager.cs  # In-memory CRUD business logic & LINQ queries
```

### 1. Domain Entity Model (`Student.cs`)
Represents an individual student record:
- `StudentId` (`int`): Unique primary identifier.
- `FullName` (`string`): Student's name.
- `Age` (`int`): Student's age.
- `Major` (`string`): Academic department (e.g. Computer Science, Software Engineering).
- `GPA` (`double`): Academic grade point average (0.0 to 4.0).

### 2. Service Layer (`StudentManager.cs`)
Encapsulates data manipulation using C# Generics and LINQ:
- **Add Student**: Appends new `Student` instances to memory with validation.
- **View All Students**: Iterates through records displaying formatted output tables.
- **Search Students**: Utilizes LINQ (`.Where(s => s.FullName.Contains(...) || s.Major == ...)`).
- **Delete Student**: Locates student by ID via `.FirstOrDefault()` and removes them.
- **Calculate Average GPA**: Computes aggregate statistics using LINQ `.Average(s => s.GPA)`.

---

## 🚀 How to Run Locally

### Prerequisites
- .NET 8.0 SDK (or .NET 7.0+) installed on your machine.

### Execution Steps
1. Open terminal and navigate to this folder:
   ```bash
   cd Week_01/Week_01_Final_Project/Students_Management_Console
   ```
2. Build and run the console application:
   ```bash
   dotnet run
   ```
3. Follow the interactive menu prompts (1-6) to perform student operations.

---

## 📢 Git Checkpoint
```bash
git add .
git commit -m "docs: add C# console student manager README"
```
