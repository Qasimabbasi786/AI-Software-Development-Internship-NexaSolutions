-- =============================================================================
-- Week 3 - Part A: Relational Database Design (PostgreSQL)
-- File: 02_seed_data.sql
-- Description: DML Seed Script for inserting initial data.
-- Context: Pakistani Authors (Islamabad & Rawalpindi region) & Literature
-- =============================================================================

-- Clear existing data (in correct sequence for foreign key constraints)
TRUNCATE TABLE "BookCategories", "Books", "Categories", "Authors" RESTART IDENTITY CASCADE;

-- -----------------------------------------------------------------------------
-- 1. Insert Pakistani Authors
-- -----------------------------------------------------------------------------
INSERT INTO "Authors" ("FullName", "City", "Email") VALUES
('Faiz Ahmed Faiz', 'Islamabad', 'faiz.ahmed@literature.pk'),
('Bapsi Sidhwa', 'Islamabad', 'bapsi.sidhwa@authors.pk'),
('Dr. Tariq Rahman', 'Islamabad', 'tariq.rahman@numl.edu.pk');

-- -----------------------------------------------------------------------------
-- 2. Insert Books (Linked to Authors via AuthorId)
-- Author 1: Faiz Ahmed Faiz (IDs: 1, 2)
-- Author 2: Bapsi Sidhwa (IDs: 3, 4)
-- Author 3: Dr. Tariq Rahman (IDs: 5, 6)
-- -----------------------------------------------------------------------------
INSERT INTO "Books" ("Title", "ISBN", "PublicationYear", "AuthorId") VALUES
('Nuskha-Hai-Wafa', '978-969-0-01501-1', 1984, 1),
('Naqsh-e-Faryadi', '978-969-0-01502-8', 1941, 1),
('Ice Candy Man', '978-014-0-11756-1', 1988, 2),
('The Crow Eaters', '978-086-1-44321-5', 1978, 2),
('Language and Politics in Pakistan', '978-019-5-77644-7', 1996, 3),
('Names and Naming Practices in Pakistan', '978-019-9-40810-8', 2020, 3);

-- -----------------------------------------------------------------------------
-- 3. Insert Categories
-- -----------------------------------------------------------------------------
INSERT INTO "Categories" ("CategoryName", "Description") VALUES
('Urdu Poetry', 'Classic and modern Urdu poetic collections and ghazals'),
('Pakistani Fiction', 'Fictional novels and narratives centered on South Asian themes'),
('Linguistics & History', 'Academic research on languages, socio-political dynamics, and culture'),
('Historical Classics', 'Literary works reflecting significant historical epochs');

-- -----------------------------------------------------------------------------
-- 4. Insert BookCategories (Many-to-Many Linking)
-- -----------------------------------------------------------------------------
INSERT INTO "BookCategories" ("BookId", "CategoryId") VALUES
-- 'Nuskha-Hai-Wafa' -> Urdu Poetry, Historical Classics
(1, 1),
(1, 4),

-- 'Naqsh-e-Faryadi' -> Urdu Poetry
(2, 1),

-- 'Ice Candy Man' -> Pakistani Fiction, Historical Classics
(3, 2),
(3, 4),

-- 'The Crow Eaters' -> Pakistani Fiction
(4, 2),

-- 'Language and Politics in Pakistan' -> Linguistics & History, Historical Classics
(5, 3),
(5, 4),

-- 'Names and Naming Practices in Pakistan' -> Linguistics & History
(6, 3);
