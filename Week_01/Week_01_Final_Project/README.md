# 🎓 Student Management Portal & Interactive Directory
### Week 1 — Capstone Project: C#/.NET Console & Angular Web Client

**Author:** Muhammad Qasim  
**Program:** AI Software Development Internship (.NET + Angular + AI)  
**Milestone:** Week 1 Final Project — Dual Subsystem Architecture  

[![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![C# 12](https://img.shields.io/badge/C%23-12.0-239120?logo=csharp&logoColor=white)](https://learn.microsoft.com/dotnet/csharp/)
[![Angular](https://img.shields.io/badge/Angular-18-DD0031?logo=angular&logoColor=white)](https://angular.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Status: Completed](https://img.shields.io/badge/Status-Completed_%E2%9C%85-success)](https://github.com/)

---

Welcome to the **Week 1 Capstone Project** for the **Nexa Solutions Internship Program**. This capstone unites everything learned across Week 1: fundamental C# logic, Object-Oriented Programming, generic collections with LINQ, exception handling, and an interactive Angular/TypeScript frontend.

---

## Table of Contents
1. [Project Overview & Dual Architecture](#1-project-overview--dual-architecture)
2. [Module 1: C# Console Student Management Portal](#2-module-1-c-console-student-management-portal)
   - [Data Modeling (`Student.cs`)](#data-modeling-studentcs)
   - [Service Layer (`StudentManager.cs`)](#service-layer-studentmanagercs)
   - [LINQ Filtering, Sorting, and Analytics](#linq-filtering-sorting-and-analytics)
   - [CLI Interactive Loop (`Program.cs`)](#cli-interactive-loop-programcs)
3. [Module 2: Angular Student Directory & Analytics Portal](#3-module-2-angular-student-directory--analytics-portal)
   - [Architecture & Component Hierarchy](#architecture--component-hierarchy)
   - [Real-Time Search & Two-Way Binding](#real-time-search--two-way-binding)
   - [Parent-Child Data Flow (`@Input` and `@Output`)](#parent-child-data-flow-input-and-output)
   - [Modern Dark/Glassmorphic Presentation](#modern-darkglassmorphic-presentation)
4. [End-to-End Execution Guide](#4-end-to-end-execution-guide)
   - [Running the C# Console Application](#running-the-c-console-application)
   - [Running the Angular Web Application](#running-the-angular-web-application)
5. [Comparative Analysis: Backend C# vs. Frontend Angular](#5-comparative-analysis-backend-c-vs-frontend-angular)
6. [Learning Outcomes Summary](#6-learning-outcomes-summary)

---

## 1. Project Overview & Dual Architecture

The Week 1 Final Project consists of two complementary implementations of a student management domain:

```
┌────────────────────────────────────────────────────────────────────────┐
│               Week 1 Capstone: Student Management Suite                │
├───────────────────────────────────┬────────────────────────────────────┤
│   Backend / Console Subsystem     │      Frontend / Web Subsystem      │
│  (Students_Management_Console)    │      (Student_Page_Angular)        │
│                                   │                                    │
│  • .NET 8 Console Application     │  • Angular 22 Standalone App       │
│  • Strong In-Memory CRUD Engine   │  • Reactive Search & Filter Engine │
│  • Complex LINQ Performance Sort  │  • Master-Detail Glassmorphic UI   │
│  • Academic Analytics Dashboard   │  • Typed Component Event Binding   │
└───────────────────────────────────┴────────────────────────────────────┘
```

Both implementations operate on an identical core domain: managing student profiles (ID, Name, Department, Marks, and Calculated Grades).

---

## 2. Module 1: C# Console Student Management Portal

Located at: [`Students_Management_Console/`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_Final_Project/Students_Management_Console)

### Data Modeling (`Student.cs`)
The domain entity leverages C# pattern matching with switch expressions for automatic grade assignment based on numerical marks:

```csharp
public class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Department { get; set; }
    public double Marks { get; set; }

    // Computed property using C# 8+ pattern matching expression
    public string Grade => Marks switch
    {
        >= 85 => "A+",
        >= 75 => "A",
        >= 65 => "B",
        >= 50 => "C",
        _     => "F"
    };

    public Student(int id, string name, string department, double marks)
    {
        Id = id;
        Name = name;
        Department = department;
        Marks = marks;
    }
}
```

### Service Layer (`StudentManager.cs`)
The `StudentManager` encapsulates data management over a private `List<Student>`, exposing controlled operations:

1. **`AddStudent(Student s)`**: Verifies uniqueness using `.Any(x => x.Id == s.Id)`.
2. **`ViewStudents()`**: Prints formatted tabular output sorted ascending by ID (`.OrderBy(s => s.Id)`).
3. **`SearchStudent(string keyword)`**: Multi-attribute, case-insensitive match on Name or Department using `.Where()`.
4. **`UpdateStudent(...)`**: Locates records by key via `.FirstOrDefault(s => s.Id == id)`.
5. **`DeleteStudent(int id)`**: Removes items safely without index shifts.
6. **`SortByMarks()`**: Ranks students in descending performance order (`.OrderByDescending(s => s.Marks)`).
7. **`ShowAnalytics()`**: Calculates statistical metrics across the population.

### LINQ Filtering, Sorting, and Analytics
The analytics feature demonstrates aggregate and sorting capabilities in LINQ:

```csharp
public void ShowAnalytics()
{
    if (students.Count == 0) return;

    double avgMarks = students.Average(s => s.Marks);
    var topStudent = students.OrderByDescending(s => s.Marks).First();
    var lowStudent = students.OrderBy(s => s.Marks).First();

    Console.WriteLine("====== ACADEMIC ANALYTICS DASHBOARD ======");
    Console.WriteLine($" Total Students : {students.Count}");
    Console.WriteLine($" Average Marks  : {avgMarks:F2}");
    Console.WriteLine($" Top Performer  : {topStudent.Name} ({topStudent.Marks} Marks)");
    Console.WriteLine($" Needs Attention: {lowStudent.Name} ({lowStudent.Marks} Marks)");
    Console.WriteLine("==========================================");
}
```

### CLI Interactive Loop (`Program.cs`)
The console host provides an 8-option menu, wrapped in defensive `try/catch (FormatException)` blocks to prevent crashes on invalid user input:

```
=========================================
   STUDENT PORTAL & MANAGEMENT SYSTEM
=========================================
 1. Add New Student
 2. View All Students (Table View)
 3. Update Student Record
 4. Delete Student
 5. Search Student (Name/Dept)
 6. Sort Students by Performance
 7. View Analytics Dashboard (New!)
 8. Exit
```

---

## 3. Module 2: Angular Student Directory & Analytics Portal

Located at: [`Student_Page_Angular/`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_Final_Project/Student_Page_Angular)

### Architecture & Component Hierarchy
The Angular frontend implements a **Master-Detail** pattern structured as standalone components:

```
┌────────────────────────────────────────────────────────┐
│                   App Component (Root)                 │
│         Search Input (Two-Way [(ngModel)])             │
├───────────────────────────┬────────────────────────────┤
│   StudentList (Master)    │   StudentDetails (Detail)  │
│                           │                            │
│  • Receives [searchText]  │  • Receives [student]      │
│  • Computes filtered list │  • Displays full profile,   │
│  • Emits (studentSelect)  │    department, and badges  │
└───────────────────────────┴────────────────────────────┘
```

### Real-Time Search & Two-Way Binding
The search bar uses `[(ngModel)]` for two-way synchronization, dynamically filtering records as the user types:

```html
<input
  type="text"
  placeholder="Search by name or department..."
  [(ngModel)]="searchText"
  class="neon-search-input"
/>
```

Inside [`StudentList`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_Final_Project/Student_Page_Angular/src/app/student-list/student-list.ts):
```typescript
get filteredStudents() {
  return this.students.filter(student =>
    student.name.toLowerCase().includes(this.searchText.toLowerCase()) ||
    student.department.toLowerCase().includes(this.searchText.toLowerCase())
  );
}
```

### Parent-Child Data Flow (`@Input` and `@Output`)
- **Data Down (`@Input`):** Parent passes the current search string to child:
  ```html
  <app-student-list [searchText]="searchText" ...>
  ```
- **Events Up (`@Output`):** Child emits selections to update parent state:
  ```typescript
  @Output() studentSelect = new EventEmitter<any>();

  selectStudent(student: any) {
    this.studentSelect.emit(student);
  }
  ```
- **Displaying Details:** The parent routes the selected student to `app-student-details`:
  ```html
  <app-student-details [student]="selectedStudent"></app-student-details>
  ```

### Modern Dark/Glassmorphic Presentation
The frontend uses a modern dark aesthetic featuring:
- Glassmorphic translucent cards (`backdrop-filter: blur(16px)`).
- Neon accents and interactive row highlights.
- Responsive flexbox/grid layout that adapts from widescreen desktops to mobile devices.

---

## 4. End-to-End Execution Guide

### Running the C# Console Application
```bash
# Navigate to the console directory
cd "Week_01/Week_01_Final_Project/Students_Management_Console"

# Build and execute
dotnet run
```

### Running the Angular Web Application
```bash
# Navigate to the Angular directory
cd "Week_01/Week_01_Final_Project/Student_Page_Angular"

# Install dependencies (first time only)
npm install

# Start development server
npm start
# or: ng serve

# Open your browser at:
http://localhost:4200/
```

---

## 5. Comparative Analysis: Backend C# vs. Frontend Angular

| Dimension | C# .NET Subsystem | Angular / TypeScript Subsystem |
| :--- | :--- | :--- |
| **Primary Responsibility** | Data validation, business logic, persistence, and backend metrics. | Presentation, user experience, reactive search, and interactive navigation. |
| **Data Querying** | LINQ (`Where`, `OrderByDescending`, `Average`, `First`). | JavaScript Array Methods (`filter`, `map`, `find`). |
| **Type Verification** | Compile-time static type system compiled to IL. | TypeScript compiler (`tsc`) transpiled to modern JavaScript. |
| **Error Handling** | Structured `try/catch/finally` exception blocks. | Component input guards, null safety operators (`?.`), and structural fallbacks (`ng-template`). |
| **State Storage** | In-memory `List<Student>` managed by `StudentManager`. | In-memory array managed within component reactive state. |

---

## 6. Learning Outcomes Summary

By completing this capstone project, interns have demonstrated:
1. Translating domain models across backend (C#) and frontend (TypeScript) environments.
2. Writing defensive, resilient user input parsers.
3. Leveraging declarative querying (LINQ & Array filters) in place of procedural loops.
4. Architecting clean component boundaries using `@Input()` and `@Output()` in modern Angular.
5. Delivering a responsive, professional user interface with high aesthetic polish.

---

## 👤 Author

- **Name:** Muhammad Qasim  
- **Internship:** AI Software Development Internship (.NET + Angular + AI)

