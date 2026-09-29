# Week 1 Final Project - Student Management Portal (Angular Frontend)

## 📌 Overview
This component is an **Angular Single-Page Application (SPA)** providing an interactive web interface for managing student records. It showcases Angular component architecture, two-way data binding (`ngModel`), reactive forms, service layer abstraction, and responsive Bootstrap styling.

---

## 🏗️ Architecture & Component Layout

```text
Student_Page_Angular/
├── package.json               # Angular dependencies & npm scripts
├── angular.json               # Angular CLI configuration
├── src/
│   ├── main.ts                # Application entry point
│   ├── index.html             # Base HTML template with Bootstrap 5
│   └── app/
│       ├── app.component.ts   # Root layout shell
│       ├── models/
│       │   └── student.model.ts # Student TypeScript interface
│       ├── services/
│       │   └── student.service.ts # State management & CRUD operations
│       └── components/
│           └── student-list/  # Student table, search filter, and add form
```

### Key Technical Features
- **Component Architecture**: Standalone component layout featuring modular UI separation.
- **Data Binding**: Interactivity via property binding (`[ngClass]`, `[disabled]`), event binding (`(click)`, `(ngSubmit)`), and structural directives (`*ngFor`, `*ngIf`).
- **Student Service**: Centralized RxJS / BehaviorSubject reactive state management for real-time list updates.
- **Filtering & Search**: Dynamic client-side filtering by student name or major.

---

## 🚀 How to Run Locally

### Prerequisites
- Node.js (v18+ or v20+) and `npm` installed.

### Execution Steps
1. Open terminal and navigate to this folder:
   ```bash
   cd Week_01/Week_01_Final_Project/Student_Page_Angular
   ```
2. Install project dependencies:
   ```bash
   npm install
   ```
3. Start the local development server:
   ```bash
   ng serve --open
   # or: npm start
   ```
4. Access the web portal in your browser at `http://localhost:4200/`.

---

## 📢 Git Checkpoint
```bash
git add .
git commit -m "docs: add Angular student portal README"
```
