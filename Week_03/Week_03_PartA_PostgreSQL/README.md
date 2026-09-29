# Week 3 - Part A: Relational Database Design (PostgreSQL)

## 📌 Overview
This module demonstrates core **Relational Database Design** principles using **PostgreSQL**, moving from simple flat files or single-table CRUD to normalized, multi-table database architectures with referential integrity. 

All sample data is localized to **Islamabad, Pakistan**, featuring prominent authors (e.g., Faiz Ahmed Faiz, Bapsi Sidhwa, Dr. Tariq Rahman) and their literary works.

---

## 🧠 Key Technical Concepts

### 1. Database Normalization (1NF to 3NF)
- **Problem**: Storing all book and author details in one table leads to data duplication (e.g., repeating `AuthorName` and `AuthorEmail` across every book row).
- **Solution**: Normalization isolates entity concepts into dedicated tables (`Authors`, `Books`, `Categories`), linked via unique key identifiers.

### 2. Primary Keys (PK) vs. Foreign Keys (FK)
- **Primary Key (`PK`)**: Uniquely identifies each record in a table (e.g., `"AuthorId"` SERIAL PRIMARY KEY).
- **Foreign Key (`FK`)**: References a Primary Key in another table to establish relationships (e.g., `"Books"."AuthorId"` pointing to `"Authors"."AuthorId"`).

### 3. Relationship Types
- **One-to-Many (`1:N`)**: One author can write multiple books, but each book has one primary author (`Authors` -> `Books`).
- **Many-to-Many (`M:N`)**: A book can belong to multiple categories, and a category can contain multiple books. Implemented via a junction/link table (`BookCategories`).

### 4. Referential Integrity & Foreign Key Constraints
- Declaring `ON DELETE RESTRICT` guarantees that an Author cannot be deleted if child rows exist in `Books`, protecting data integrity.

---

## 📁 Repository Structure
```text
Week_03_PartA_PostgreSQL/
├── README.md
└── sql/
    ├── 01_schema.sql      # DDL: Table creation, primary/foreign keys, indexes
    ├── 02_seed_data.sql    # DML: Seed data (Islamabad authors, books, categories)
    └── 03_queries.sql     # DQL: JOIN queries and FK error demonstration
```

---

## 🚀 Execution & Verification Instructions

### Option 1: Execution via `psql` CLI
1. Open terminal and connect to your local PostgreSQL server:
   ```bash
   psql -U postgres
   ```
2. Create the database:
   ```sql
   CREATE DATABASE librarydb_week3;
   \c librarydb_week3
   ```
3. Execute the SQL scripts in sequence:
   ```bash
   psql -U postgres -d librarydb_week3 -f sql/01_schema.sql
   psql -U postgres -d librarydb_week3 -f sql/02_seed_data.sql
   psql -U postgres -d librarydb_week3 -f sql/03_queries.sql
   ```

### Option 2: Execution via GUI Tools (pgAdmin / DBeaver / Azure Data Studio)
1. Open your database client and connect to PostgreSQL.
2. Create and switch to `librarydb_week3`.
3. Open and run [`sql/01_schema.sql`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartA_PostgreSQL/sql/01_schema.sql).
4. Open and run [`sql/02_seed_data.sql`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartA_PostgreSQL/sql/02_seed_data.sql).
5. Execute queries in [`sql/03_queries.sql`](file:///d:/Courses%20and%20Internship/Internship/Completed/Internship-by-azeem/Week_wise_sol/Week-03_and_04/Week_03/Week_03_PartA_PostgreSQL/sql/03_queries.sql) to inspect JOIN results and referential integrity checks.

---

## 🔍 Verification Output

### Task 1: Inner Join Query Result
```sql
SELECT b."Title", a."FullName" AS "AuthorName"
FROM "Books" b
JOIN "Authors" a ON b."AuthorId" = a."AuthorId"
ORDER BY a."FullName";
```
| Title | AuthorName |
| :--- | :--- |
| Ice Candy Man | Bapsi Sidhwa |
| The Crow Eaters | Bapsi Sidhwa |
| Language and Politics in Pakistan | Dr. Tariq Rahman |
| Names and Naming Practices in Pakistan | Dr. Tariq Rahman |
| Naqsh-e-Faryadi | Faiz Ahmed Faiz |
| Nuskha-Hai-Wafa | Faiz Ahmed Faiz |

### Task 3: Foreign Key Error Verification
When running `DELETE FROM "Authors" WHERE "AuthorId" = 1;`:
```text
ERROR: update or delete on table "Authors" violates foreign key constraint "FK_Books_Authors_AuthorId" on table "Books"
DETAIL: Key (AuthorId)=(1) is still referenced from table "Books".
```
This confirms that referential integrity is functioning as designed.

---

## 📢 Git Checkpoint
```bash
git add sql/ README.md
git commit -m "feat: add Week 3 PostgreSQL relational schema, seed data, and join queries"
```
