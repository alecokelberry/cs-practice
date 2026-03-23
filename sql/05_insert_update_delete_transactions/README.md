# 05 — INSERT, UPDATE, DELETE & Transactions

These are the data-modification statements. `SELECT` reads data; `INSERT`, `UPDATE`, and `DELETE` change it. Transactions group changes so they either all succeed or all fail.

---

## INSERT

```sql
-- Insert one row
INSERT INTO users (name, email, age, city)
VALUES ('Alice', 'alice@example.com', 30, 'Austin');

-- Insert multiple rows at once (more efficient than one at a time)
INSERT INTO users (name, email, age, city)
VALUES
    ('Bob',   'bob@example.com',   25, 'Dallas'),
    ('Carol', 'carol@example.com', 35, 'Houston');

-- Insert and return the new row (PostgreSQL — useful to get auto-generated id)
INSERT INTO users (name, email)
VALUES ('Dave', 'dave@example.com')
RETURNING id, name;
```

Columns with defaults (like `SERIAL` primary keys or `DEFAULT NOW()` timestamps) don't need to be listed.

---

## INSERT ... ON CONFLICT (Upsert)

Insert a row, but if a unique constraint would be violated, update instead.

```sql
-- If the email already exists, update the name
INSERT INTO users (name, email)
VALUES ('Alice Updated', 'alice@example.com')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name;

-- If it already exists, do nothing (ignore the duplicate)
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com')
ON CONFLICT (email)
DO NOTHING;
```

`EXCLUDED` refers to the row that was attempted but conflicted.

---

## UPDATE

```sql
-- Update one column for a specific row
UPDATE users
SET city = 'San Antonio'
WHERE id = 1;

-- Update multiple columns
UPDATE users
SET city = 'San Antonio', age = 31
WHERE id = 1;

-- Update based on another column
UPDATE orders
SET amount = amount * 1.1   -- 10% increase
WHERE created_at < '2024-01-01';

-- Update and return the modified row
UPDATE users
SET city = 'San Antonio'
WHERE id = 1
RETURNING id, name, city;
```

**Always use WHERE with UPDATE.** An `UPDATE` without `WHERE` updates every row in the table.

---

## DELETE

```sql
-- Delete specific rows
DELETE FROM users WHERE id = 1;

-- Delete with a subquery
DELETE FROM orders
WHERE user_id IN (
    SELECT id FROM users WHERE city = 'Austin'
);

-- Delete and return what was deleted
DELETE FROM users WHERE id = 1 RETURNING *;
```

**Always use WHERE with DELETE.** A `DELETE` without `WHERE` deletes every row.

---

## TRUNCATE — Fast Delete All Rows

```sql
-- Delete all rows (much faster than DELETE FROM table for large tables)
TRUNCATE TABLE orders;

-- Truncate multiple tables
TRUNCATE TABLE order_items, orders;

-- Reset auto-increment counter
TRUNCATE TABLE users RESTART IDENTITY;
```

`TRUNCATE` can't be rolled back in most databases (it's DDL, not DML). In PostgreSQL it can be rolled back inside a transaction.

---

## Transactions

A transaction groups multiple statements into a single unit. All succeed, or none do — the database never ends up in a half-updated state.

```sql
-- Start a transaction
BEGIN;

-- Move $100 from Alice to Bob
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Alice
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Bob

-- Commit: make changes permanent
COMMIT;
```

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- Something went wrong — undo everything
ROLLBACK;
```

Without transactions, if the second `UPDATE` fails, Alice loses $100 and Bob gets nothing.

---

## SAVEPOINT — Partial Rollback

```sql
BEGIN;

INSERT INTO orders (user_id, amount) VALUES (1, 50.00);

SAVEPOINT after_order;

INSERT INTO order_items (order_id, product_id) VALUES (1, 99);
-- This failed — roll back only to the savepoint, not the whole transaction
ROLLBACK TO SAVEPOINT after_order;

-- The order insert is still intact
COMMIT;
```

---

## ACID Properties

Transactions guarantee ACID:

| Property | Meaning |
|----------|---------|
| **Atomicity** | All statements in the transaction succeed, or none do |
| **Consistency** | The database moves from one valid state to another (constraints are enforced) |
| **Isolation** | Concurrent transactions don't see each other's uncommitted changes |
| **Durability** | Once committed, changes survive crashes |

---

## INSERT/UPDATE with SELECT (INSERT INTO ... SELECT)

```sql
-- Copy rows from one table to another
INSERT INTO archived_orders (id, user_id, amount, created_at)
SELECT id, user_id, amount, created_at
FROM orders
WHERE created_at < '2023-01-01';

-- Update using a join
UPDATE orders o
SET amount = amount * 0.9
FROM users u
WHERE o.user_id = u.id
  AND u.city = 'Austin';
```

---

## Common Pitfalls

**UPDATE or DELETE without WHERE**
```sql
-- Deletes every row in the table
DELETE FROM orders;

-- Updates every row in the table
UPDATE users SET city = 'Austin';
```

Always double-check your WHERE clause before running destructive statements. Run a `SELECT` with the same `WHERE` first to see what will be affected.

**Forgetting to COMMIT**
In most database clients, you're auto-committed by default. But if you explicitly `BEGIN` a transaction, you must `COMMIT` — otherwise the changes are rolled back when the connection closes.

**TRUNCATE is not the same as DELETE**
`TRUNCATE` resets sequences, is faster, and (in most databases) can't be rolled back. Use `DELETE FROM table` if you need the changes to be transactional and reversible.

**Upsert conflicts only on equality**
`ON CONFLICT` triggers only on exact unique/primary key violations. It doesn't trigger for range constraints or check constraints.

---

## Quick Reference

```
INSERT
  INSERT INTO table (col1, col2) VALUES (val1, val2);
  INSERT INTO table (col1, col2) VALUES (...), (...);       -- multiple rows
  INSERT INTO table (...) VALUES (...) RETURNING id;        -- get generated id
  INSERT INTO table (...) VALUES (...)
    ON CONFLICT (col) DO UPDATE SET col = EXCLUDED.col;     -- upsert
  INSERT INTO table (...) VALUES (...)
    ON CONFLICT (col) DO NOTHING;                           -- ignore duplicate

UPDATE
  UPDATE table SET col = val WHERE condition;
  UPDATE table SET col1 = v1, col2 = v2 WHERE condition;
  UPDATE table SET col = val WHERE condition RETURNING *;

DELETE
  DELETE FROM table WHERE condition;
  DELETE FROM table WHERE condition RETURNING *;
  TRUNCATE TABLE table;                         -- fast, resets sequences

Transactions
  BEGIN;                          -- start
  COMMIT;                         -- save changes
  ROLLBACK;                       -- undo all changes
  SAVEPOINT name;                 -- checkpoint
  ROLLBACK TO SAVEPOINT name;     -- undo to checkpoint

ACID
  Atomicity — all or nothing
  Consistency — constraints enforced
  Isolation — concurrent transactions don't interfere
  Durability — committed changes survive crashes
```
