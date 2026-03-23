# 07 — Indexes, Primary & Foreign Keys

Constraints enforce data integrity — they prevent bad data from entering the database. Indexes make queries fast by letting the database find rows without scanning the entire table.

---

## Primary Keys

A primary key uniquely identifies each row. Every table should have one.

```sql
-- Primary key defined inline
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,   -- SERIAL = auto-incrementing integer
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Or as a table constraint (required for composite primary keys)
CREATE TABLE order_items (
    order_id   INT,
    product_id INT,
    quantity   INT,
    PRIMARY KEY (order_id, product_id)   -- composite primary key
);
```

A primary key implicitly creates a unique index on that column. You can't insert NULL or a duplicate value.

### Modern alternative to SERIAL

```sql
-- PostgreSQL 10+: preferred over SERIAL
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

`GENERATED ALWAYS AS IDENTITY` is the SQL standard. `SERIAL` is PostgreSQL-specific shorthand.

---

## UNIQUE Constraints

Ensures all values in a column (or combination of columns) are distinct.

```sql
CREATE TABLE users (
    id    SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL    -- no two users can have the same email
);

-- Unique across multiple columns
CREATE TABLE memberships (
    user_id  INT,
    group_id INT,
    UNIQUE (user_id, group_id)    -- a user can only join a group once
);
```

`UNIQUE` allows NULL — and multiple NULL values are allowed even in a UNIQUE column (NULLs are never equal to each other).

---

## NOT NULL

```sql
CREATE TABLE users (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL,          -- required
    bio  TEXT                    -- optional (NULL allowed)
);
```

---

## Foreign Keys — Referential Integrity

A foreign key ensures that a value in one table exists in another table. It prevents orphaned records.

```sql
CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),  -- must exist in users.id
    amount  NUMERIC(10, 2)
);
```

If you try to insert an order with `user_id = 999` and no user with `id = 999` exists, the database rejects it.

### ON DELETE and ON UPDATE Behavior

What happens to orders when a user is deleted?

```sql
CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE
    -- ON DELETE RESTRICT  -- (default) error if user has orders
    -- ON DELETE CASCADE   -- delete orders when user is deleted
    -- ON DELETE SET NULL  -- set user_id to NULL when user is deleted
    -- ON DELETE SET DEFAULT  -- set to column default
);
```

| Option | Behavior |
|--------|---------|
| `RESTRICT` (default) | Error — can't delete the user if orders exist |
| `CASCADE` | Delete orders automatically when user is deleted |
| `SET NULL` | Set `user_id` to NULL (requires column to be nullable) |
| `SET DEFAULT` | Set `user_id` to the column's default value |

---

## Indexes

An index is a separate data structure that the database maintains to speed up lookups. Without an index, the database reads every row (a "sequential scan"). With an index, it jumps directly to matching rows.

### Creating Indexes

```sql
-- Index on a single column (most common)
CREATE INDEX idx_users_email ON users(email);

-- Index on multiple columns (useful for queries filtering on both)
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Unique index (equivalent to UNIQUE constraint)
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index — only index rows matching a condition (smaller, faster)
CREATE INDEX idx_orders_large ON orders(amount) WHERE amount > 1000;

-- Drop an index
DROP INDEX idx_users_email;
```

Indexes are used automatically by the query planner. You don't reference them in queries.

---

## Primary Keys and Foreign Keys Create Indexes Automatically

- `PRIMARY KEY` — always creates a unique index
- `UNIQUE` constraint — always creates a unique index
- `FOREIGN KEY` — does **not** create an index on the referencing column (you should add one manually)

```sql
-- The foreign key column user_id is NOT automatically indexed
-- Add it manually to speed up joins and cascades
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

---

## B-Tree Indexes (Default)

The default index type in PostgreSQL. Works for `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `IN`, and `ORDER BY`.

```sql
-- This query can use the index on email
WHERE email = 'alice@example.com'

-- This cannot (function applied to the column defeats the index)
WHERE LOWER(email) = 'alice@example.com'

-- Fix: create a functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

---

## When to Add an Index

| Add an index when... | Avoid an index when... |
|----------------------|----------------------|
| A column appears frequently in `WHERE` | The table is small (full scan is fast) |
| A column is used in `JOIN` conditions | The column has few distinct values (e.g., boolean, status with 3 options) |
| A column appears in `ORDER BY` on large result sets | The table has very frequent writes (indexes slow down INSERT/UPDATE/DELETE) |
| A column is a foreign key | — |

Every index speeds up reads but slows down writes — the database must update the index on every INSERT, UPDATE, or DELETE.

---

## Adding Constraints to Existing Tables

```sql
-- Add a foreign key to an existing table
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_user
    FOREIGN KEY (user_id) REFERENCES users(id);

-- Add a unique constraint
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE (email);

-- Add NOT NULL
ALTER TABLE users ALTER COLUMN name SET NOT NULL;

-- Drop a constraint
ALTER TABLE orders DROP CONSTRAINT fk_orders_user;
```

---

## CHECK Constraints

Enforce custom rules on column values.

```sql
CREATE TABLE products (
    id    SERIAL PRIMARY KEY,
    price NUMERIC CHECK (price >= 0),       -- inline
    stock INT,
    CONSTRAINT chk_stock_non_negative CHECK (stock >= 0)  -- named
);
```

---

## Common Pitfalls

**Missing index on foreign key columns**
Every foreign key column should usually have an index. Otherwise, deleting a user requires a full table scan of orders to find orphaned rows.

**Index on low-cardinality columns**
An index on a `status` column with only 3 values ('pending', 'active', 'closed') is often useless — the database may scan the whole table anyway.

**Function calls defeating indexes**
```sql
WHERE UPPER(name) = 'ALICE'   -- can't use index on name
WHERE name LIKE '%alice%'     -- leading wildcard defeats the index
WHERE name LIKE 'alice%'      -- trailing wildcard is fine, uses the index
```

**Forgetting ON DELETE behavior**
The default is `RESTRICT`. If you delete a parent row and it has children, you get a foreign key violation error — not a cascade. Be explicit about which behavior you want.

---

## Quick Reference

```
Constraints
  col SERIAL PRIMARY KEY                      -- auto-increment PK
  col INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY  -- SQL standard PK
  col TEXT NOT NULL                           -- required
  col TEXT UNIQUE                             -- no duplicates (NULLs exempt)
  col INT REFERENCES other_table(id)          -- foreign key
  col INT REFERENCES other_table(id) ON DELETE CASCADE
  CHECK (col > 0)                             -- custom rule
  PRIMARY KEY (col1, col2)                    -- composite PK

Indexes
  CREATE INDEX idx_name ON table(col);                -- basic
  CREATE INDEX idx_name ON table(col1, col2);         -- composite
  CREATE UNIQUE INDEX idx_name ON table(col);         -- unique
  CREATE INDEX idx_name ON table(col) WHERE condition; -- partial
  CREATE INDEX idx_name ON table(LOWER(col));          -- functional
  DROP INDEX idx_name;

Alter Existing Tables
  ALTER TABLE t ADD CONSTRAINT name FOREIGN KEY (col) REFERENCES other(id);
  ALTER TABLE t ADD CONSTRAINT name UNIQUE (col);
  ALTER TABLE t ALTER COLUMN col SET NOT NULL;
  ALTER TABLE t DROP CONSTRAINT name;

When to Index
  ✓ Frequent WHERE columns
  ✓ JOIN columns (especially FK columns)
  ✓ ORDER BY columns on large tables
  ✗ Small tables
  ✗ Low-cardinality columns
  ✗ Write-heavy tables (index overhead)
```
