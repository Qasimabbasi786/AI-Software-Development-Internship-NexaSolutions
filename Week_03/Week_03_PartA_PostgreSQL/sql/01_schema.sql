-- =============================================================================
-- Week 3 - Part A: Relational Database Design (PostgreSQL)
-- File: 01_schema.sql
-- Description: DDL Script for creating tables, constraints, and relationships.
-- Tech Stack: PostgreSQL 12+
-- Context: Islamabad Library System (LibraryDb_Week3)
-- =============================================================================

-- Database Creation Notes:
-- Run `CREATE DATABASE librarydb_week3;` as superuser/postgres before running this script if starting fresh.
-- Ensure you are connected to `librarydb_week3` before executing the DDL commands below.

-- Drop existing tables if re-running script (respecting foreign key hierarchy)
DROP TABLE IF EXISTS "BookCategories" CASCADE;
DROP TABLE IF EXISTS "Books" CASCADE;
DROP TABLE IF EXISTS "Categories" CASCADE;
DROP TABLE IF EXISTS "Authors" CASCADE;

-- -----------------------------------------------------------------------------
-- 1. Authors Table (One-to-Many with Books)
-- -----------------------------------------------------------------------------
CREATE TABLE "Authors" (
    "AuthorId" SERIAL PRIMARY KEY,
    "FullName" VARCHAR(150) NOT NULL,
    "City" VARCHAR(100) DEFAULT 'Islamabad',
    "Email" VARCHAR(150) UNIQUE,
    "CreatedAt" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "Authors" IS 'Stores author profiles including Islamabad-based literature figures.';
COMMENT ON COLUMN "Authors"."AuthorId" IS 'Primary Key - Auto-incrementing integer identity.';

-- -----------------------------------------------------------------------------
-- 2. Books Table (Many-to-One with Authors)
-- -----------------------------------------------------------------------------
CREATE TABLE "Books" (
    "BookId" SERIAL PRIMARY KEY,
    "Title" VARCHAR(255) NOT NULL,
    "ISBN" VARCHAR(20) UNIQUE,
    "PublicationYear" INT CHECK ("PublicationYear" >= 1800 AND "PublicationYear" <= 2100),
    "AuthorId" INT NOT NULL,
    "CreatedAt" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint (Prevents orphaned books)
    CONSTRAINT "FK_Books_Authors_AuthorId" 
        FOREIGN KEY ("AuthorId") 
        REFERENCES "Authors" ("AuthorId") 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE "Books" IS 'Stores published titles referenced to an Author.';
COMMENT ON COLUMN "Books"."AuthorId" IS 'Foreign Key referencing Authors(AuthorId). RESTRICT prevents author deletion with active books.';

-- -----------------------------------------------------------------------------
-- 3. Categories Table
-- -----------------------------------------------------------------------------
CREATE TABLE "Categories" (
    "CategoryId" SERIAL PRIMARY KEY,
    "CategoryName" VARCHAR(100) NOT NULL UNIQUE,
    "Description" TEXT
);

COMMENT ON TABLE "Categories" IS 'Lookup table for literature genres and topics.';

-- -----------------------------------------------------------------------------
-- 4. BookCategories Table (Many-to-Many Link / Junction Table)
-- -----------------------------------------------------------------------------
CREATE TABLE "BookCategories" (
    "BookId" INT NOT NULL,
    "CategoryId" INT NOT NULL,
    "AssignedAt" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    -- Composite Primary Key to avoid duplicate assignments
    PRIMARY KEY ("BookId", "CategoryId"),

    -- Foreign Keys
    CONSTRAINT "FK_BookCategories_Books_BookId" 
        FOREIGN KEY ("BookId") 
        REFERENCES "Books" ("BookId") 
        ON DELETE CASCADE,

    CONSTRAINT "FK_BookCategories_Categories_CategoryId" 
        FOREIGN KEY ("CategoryId") 
        REFERENCES "Categories" ("CategoryId") 
        ON DELETE CASCADE
);

COMMENT ON TABLE "BookCategories" IS 'Junction table creating many-to-many relationship between Books and Categories.';

-- Indexes for optimized JOIN queries
CREATE INDEX "IX_Books_AuthorId" ON "Books" ("AuthorId");
CREATE INDEX "IX_BookCategories_CategoryId" ON "BookCategories" ("CategoryId");
