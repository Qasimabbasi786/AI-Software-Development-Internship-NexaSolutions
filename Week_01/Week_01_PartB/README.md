# Week 1 - Part B: Object-Oriented Programming (OOP) in C#

Welcome to **Part B** of Week 1 in the **Nexa Solutions Internship Program**. This module advances your engineering skills from procedural scripting to robust **Object-Oriented Design (OOD)** in C#. You will master encapsulation, class abstraction, inheritance, polymorphism, interface contracts, and architectural decisions between inheritance and composition.

---

## Table of Contents
1. [Core Principles of Object-Oriented Programming](#1-core-principles-of-object-oriented-programming)
2. [Classes vs. Objects (Reference Allocation)](#2-classes-vs-objects-reference-allocation)
3. [Properties, Auto-Properties & Encapsulation](#3-properties-auto-properties--encapsulation)
4. [Constructors & Object Lifecycle](#4-constructors--object-lifecycle)
5. [Access Modifiers & Visibility Scopes](#5-access-modifiers--visibility-scopes)
6. [Inheritance (`base` and derived classes)](#6-inheritance-base-and-derived-classes)
7. [Polymorphism: Method Overriding vs Overloading](#7-polymorphism-method-overriding-vs-overloading)
8. [Interface Contracts (`IPrintable`)](#8-interface-contracts-iprintable)
9. [Inheritance vs. Composition: Architectural Trade-Offs](#9-inheritance-vs-composition-architectural-trade-offs)
10. [Domain Implementation in This Project](#10-domain-implementation-in-this-project)
11. [How to Build and Run](#11-how-to-build-and-run)
12. [Summary Checklist](#12-summary-checklist)

---

## 1. Core Principles of Object-Oriented Programming

C# is an object-oriented language architected around four foundational pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Four Pillars of Object-Oriented C#                   │
├───────────────────┬───────────────────┬────────────────┬───────────────┤
│   Encapsulation   │    Abstraction    │  Inheritance   │ Polymorphism  │
│                   │                   │                │               │
│ Hide state and    │ Expose essential  │ Share common   │ Provide many  │
│ guard invariants  │ capabilities via  │ attributes and │ forms behind  │
│ via properties    │ clean interfaces  │ behaviors from │ common base   │
│ & private fields. │ or base classes.  │ parent types.  │ or interface. │
└───────────────────┴───────────────────┴────────────────┴───────────────┘
```

---

## 2. Classes vs. Objects (Reference Allocation)

* **Class (Blueprint):** A declared type that specifies the fields, properties, methods, and events that instances will possess. Classes are defined in source code and compiled into metadata.
* **Object (Instance):** A tangible, runtime instantiation of a class. When instantiated with the `new` keyword:
  - An instance payload is allocated on the **Managed Heap**.
  - A variable holding the memory reference (pointer) is placed on the **Stack**.

```csharp
// Definition (Class)
public class Person
{
    public string Name { get; set; }
}

// Instantiation (Object)
Person personInstance = new Person(); 
// personInstance on stack points to heap memory
```

---

## 3. Properties, Auto-Properties & Encapsulation

Encapsulation ensures that an object’s internal state cannot be corrupted by external callers. In C#, properties mediate access to fields:

### Classical Field with Guarded Property
```csharp
public class BankAccount
{
    private double _balance; // Private backing field

    public double Balance
    {
        get { return _balance; }
        private set 
        { 
            if (value >= 0) 
                _balance = value; 
        }
    }
}
```

### Auto-Implemented Properties
When no custom validation is required, auto-properties provide concise syntax while maintaining API stability:
```csharp
public class Person
{
    public string Name { get; set; } = string.Empty;
    public int Age { get; set; }
}
```

---

## 4. Constructors & Object Lifecycle

Constructors initialize an object into a valid state upon instantiation. If no explicit constructor is provided, C# supplies a default parameterless constructor.

Derived classes invoke base constructors via the `base(...)` keyword:

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person() { }

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

public class Student : Person
{
    public string StudentId { get; set; }

    public Student(string name, int age, string studentId) 
        : base(name, age) // Delegates to Person constructor
    {
        StudentId = studentId;
    }
}
```

---

## 5. Access Modifiers & Visibility Scopes

C# provides rich scoping to enforce encapsulation:

| Modifier | Accessibility Scope |
| :--- | :--- |
| `public` | Accessible from any assembly or external caller. |
| `private` | Accessible only within the declaring class/struct. |
| `protected` | Accessible within the declaring class and derived types. |
| `internal` | Accessible anywhere within the current assembly (`.dll`/`.exe`), but hidden externally. |
| `protected internal` | Accessible within the current assembly OR any derived class across assemblies. |
| `private protected` | Accessible only by derived classes within the same assembly. |

---

## 6. Inheritance (`base` and derived classes)

Inheritance models an **"is-a"** relationship, facilitating code reuse and logical taxonomies.

In this project:
- `Person` acts as the generalized base class containing shared human characteristics (`Name`, `Age`).
- `Student` and `Teacher` specialize `Person` by adding domain-specific fields:

```
               ┌──────────────────────┐
               │    Person (Base)     │
               │  - Name: string      │
               │  - Age: int          │
               │  + PrintDetails()    │
               └──────────┬───────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
┌───────────────────────┐   ┌───────────────────────┐
│   Student (Derived)   │   │   Teacher (Derived)   │
│  - Grade: int         │   │  - Subject: string    │
│  - StudentId: string  │   │  + PrintDetails()     │
│  + PrintDetails()     │   └───────────────────────┘
└───────────────────────┘
```

---

## 7. Polymorphism: Method Overriding vs Overloading

Polymorphism allows objects of different concrete classes to be treated uniformly through a shared interface or base type.

### 1. Compile-Time Polymorphism (Method Overloading)
Methods share the same identifier but differ in parameter signatures:
```csharp
public void Enroll(string courseCode) { ... }
public void Enroll(string courseCode, int semester) { ... }
```

### 2. Runtime Polymorphism (Method Overriding)
Base classes declare `virtual` methods, which derived classes override with custom behaviors using the `override` keyword:
```csharp
public class Person
{
    public virtual void PrintDetails()
    {
        Console.WriteLine($"Name: {Name}, Age: {Age}");
    }
}

public class Student : Person
{
    public override void PrintDetails()
    {
        base.PrintDetails();
        Console.WriteLine($"Grade: {Grade}, StudentId: {StudentId}");
    }
}
```

---

## 8. Interface Contracts (`IPrintable`)

An **Interface** is a pure behavioral contract. It defines *what* an implementing class must do, rather than *how*. Unlike class inheritance (where C# permits only single inheritance), a class may implement **multiple interfaces**.

```csharp
namespace Week1_PartB_Exercises
{
    public interface IPrintable
    {
        void PrintDetails();
    }
}
```

Implementing classes:
```csharp
public class Student : Person, IPrintable
{
    public int Grade { get; set; }
    public string StudentId { get; set; }

    public void PrintDetails()
    {
        Console.WriteLine($"Name: {Name}, Age: {Age}, Grade: {Grade}, StudentId: {StudentId}");
    }
}
```

---

## 9. Inheritance vs. Composition: Architectural Trade-Offs

A common software architecture trap is overuse of deep inheritance hierarchies. Modern system design recommends: **"Favor object composition over class inheritance."**

```
Inheritance ("is-a"):
Student ────► is a ────► Person

Composition ("has-a"):
Student ────► has a ───► ContactProfile
        ────► has a ───► TranscriptRecord
```

### Comparison Matrix
| Architectural Aspect | Inheritance ("is-a") | Composition ("has-a") |
| :--- | :--- | :--- |
| **Coupling** | **Tight coupling**: Changes to base classes ripple down to every derived class. | **Loose coupling**: Components can be swapped, mocked, or altered independently. |
| **Flexibility** | Static, locked at compile time. | Dynamic, behaviors can be injected or reconfigured at runtime. |
| **Testability** | Harder to isolate; requires subclassing or complex mock setups. | Highly testable via dependency injection (mocking interfaces). |
| **When to Use** | When there is an unmistakable, universal hierarchical relationship (`Dog is an Animal`). | When combining modular capabilities (`Car has an Engine`, `Order has a PaymentProcessor`). |

---

## 10. Domain Implementation in This Project

The `Week_01_PartB` codebase implements this object model:

* **[IPrintable.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/IPrintable.cs):** The reporting contract defining `void PrintDetails()`.
* **[Person.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/Person.cs):** Root entity encapsulating `Name`, `Age`, and basic details printing.
* **[Student.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/Student.cs):** Extends `Person` with `Grade` and `StudentId`.
* **[Teacher.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/Teacher.cs):** Extends `Person` with teaching `Subject`.
* **[Program.cs](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/All%20Week%20Tasks%20Sol/Week_01/Week_01_PartB/Program.cs):** Entry point demonstrating object initialization and formatted terminal output.

---

## 11. How to Build and Run

```bash
# Navigate to the Part B directory
cd "Week_01/Week_01_PartB"

# Build assemblies
dotnet build

# Execute the console driver
dotnet run
```

---

## 12. Summary Checklist

- [x] Clearly distinguish between Stack references and Heap object instances.
- [x] Protect object state using properties and appropriate access modifiers (`private`, `public`, `protected`).
- [x] Model hierarchies cleanly with `base` class inheritance.
- [x] Decouple consumers by declaring polymorphic interface contracts (`IPrintable`).
- [x] Evaluate whether an architectural scenario calls for inheritance ("is-a") or modular composition ("has-a").
