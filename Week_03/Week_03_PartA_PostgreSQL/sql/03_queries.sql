-- =============================================================================
-- Week 3 - Part A: Relational Database Design (PostgreSQL)
-- File: 03_queries.sql
-- Description: DQL Queries & Foreign Key Violation Demonstration Scripts
-- Context: Querying Books, Authors, and Categories in PostgreSQL
-- =============================================================================

-- -----------------------------------------------------------------------------
-- TASK 1: INNER JOIN Query (Books + Authors)
-- Goal: Retrieve every book along with its author's full name, ordered by author name.
-- -----------------------------------------------------------------------------
SELECT 
    b."BookId",
    b."Title",
    b."ISBN",
    b."PublicationYear",
    a."FullName" AS "AuthorName",
    a."City" AS "AuthorCity"
FROM "Books" b
INNER JOIN "Authors" a ON b."AuthorId" = a."AuthorId"
ORDER BY a."FullName" ASC, b."Title" ASC;


-- -----------------------------------------------------------------------------
-- TASK 2: Many-to-Many JOIN Query (Categories for a Specific Book)
-- Goal: Return all category names and descriptions for 'Ice Candy Man' (BookId = 3)
-- -----------------------------------------------------------------------------
SELECT 
    b."Title" AS "BookTitle",
    c."CategoryName",
    c."Description" AS "CategoryDescription"
FROM "Books" b
INNER JOIN "BookCategories" bc ON b."BookId" = bc."BookId"
INNER JOIN "Categories" c ON bc."CategoryId" = c."CategoryId"
WHERE b."Title" = 'Ice Candy Man' -- Or filter by b."BookId" = 3
ORDER BY c."CategoryName" ASC;


-- -----------------------------------------------------------------------------
-- TASK 3: Foreign Key Constraint Violation Test & Explanation
-- Goal: Demonstrate PostgreSQL's referential integrity enforcement when attempting 
-- to delete an Author who still has dependent child rows in the "Books" table.
-- -----------------------------------------------------------------------------

-- TRY THIS DELETE COMMAND:
DELETE FROM "Authors" WHERE "AuthorId" = 1;

/*
================================================================================
EXPLANATION OF THE EXPECTED POSTGRESQL ERROR:
================================================================================

When executing the DELETE query above, PostgreSQL aborts the transaction and throws:

ERROR: update or delete on table "Authors" violates foreign key constraint 
       "FK_Books_Authors_AuthorId" on table "Books"
DETAIL: Key (AuthorId)=(1) is still referenced from table "Books".

WHY DOES THIS HAPPEN?
1. In `01_schema.sql`, we defined the constraint:
   `CONSTRAINT "FK_Books_Authors_AuthorId" FOREIGN KEY ("AuthorId") REFERENCES "Authors" ("AuthorId") ON DELETE RESTRICT`

2. `ON DELETE RESTRICT` (or `NO ACTION`) prevents orphaned records. If we were allowed to delete 
   Faiz Ahmed Faiz (AuthorId = 1), the books "Nuskha-Hai-Wafa" and "Naqsh-e-Faryadi" would point to an AuthorId 
   that no longer exists in the database.

3. HOW TO RESOLVE IN PRODUCTION PRACTICE:
   - Option A (Explicit cleanup): First reassign or delete the associated books from the "Books" table:
     `DELETE FROM "Books" WHERE "AuthorId" = 1;`
     `DELETE FROM "Authors" WHERE "AuthorId" = 1;`
   - Option B (Cascade): If defined with `ON DELETE CASCADE`, deleting the author would automatically delete all 6 linked books.
================================================================================
*/
