# 01 — Basic Queries: SELECT & WHERE

SQL is a declarative language — you describe *what* you want, not *how* to get it. The database figures out the how. Every query starts with `SELECT`.

---

## SELECT and FROM

```sql
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Rename columns in output (alias)
SELECT name AS full_name, email AS contact FROM users;

-- Computed column
SELECT name, age * 12 AS age_in_months FROM users;
```

`SELECT *` is fine for exploration but avoid it in production code — if the table schema changes, your query silently returns different columns.

---

## WHERE — Filtering Rows

```sql
-- Equality
SELECT * FROM users WHERE city = 'Austin';

-- Not equal
SELECT * FROM users WHERE city != 'Austin';
SELECT * FROM users WHERE city <> 'Austin';  -- same thing

-- Comparisons
SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE age >= 18 AND age <= 65;

-- BETWEEN (inclusive on both ends)
SELECT * FROM users WHERE age BETWEEN 18 AND 65;

-- Multiple conditions
SELECT * FROM users WHERE city = 'Austin' AND age > 21;
SELECT * FROM users WHERE city = 'Austin' OR city = 'Dallas';

-- IN — match any value in a list
SELECT * FROM users WHERE city IN ('Austin', 'Dallas', 'Houston');

-- NOT IN
SELECT * FROM users WHERE city NOT IN ('Austin', 'Dallas');
```

---

## LIKE — Pattern Matching

```sql
-- % matches any number of characters
SELECT * FROM users WHERE name LIKE 'A%';     -- starts with A
SELECT * FROM users WHERE name LIKE '%son';   -- ends with son
SELECT * FROM users WHERE name LIKE '%ali%';  -- contains ali

-- _ matches exactly one character
SELECT * FROM users WHERE name LIKE '_ob';    -- Bob, Rob, Job...

-- Case-insensitive (PostgreSQL)
SELECT * FROM users WHERE name ILIKE 'alice%';
```

`LIKE` uses a sequential scan — it's slow on large tables. For text search, use full-text indexes instead.

---

## NULL Handling

NULL means "unknown" — it's not a value, so you can't compare to it with `=`.

```sql
-- WRONG — always returns no rows
SELECT * FROM users WHERE age = NULL;

-- CORRECT
SELECT * FROM users WHERE age IS NULL;
SELECT * FROM users WHERE age IS NOT NULL;

-- COALESCE — return first non-null value
SELECT name, COALESCE(city, 'Unknown') AS city FROM users;

-- NULLIF — return NULL if two values are equal (useful to avoid divide-by-zero)
SELECT total / NULLIF(count, 0) AS average FROM stats;
```

---

## ORDER BY and LIMIT

```sql
-- Sort ascending (default)
SELECT * FROM users ORDER BY name;
SELECT * FROM users ORDER BY name ASC;

-- Sort descending
SELECT * FROM users ORDER BY age DESC;

-- Sort by multiple columns
SELECT * FROM users ORDER BY city ASC, name ASC;

-- Limit number of rows
SELECT * FROM users ORDER BY age DESC LIMIT 10;

-- Skip rows (pagination)
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;  -- rows 21–30
```

Always use `ORDER BY` with `LIMIT`. Without it, the database returns rows in an unpredictable order.

---

## DISTINCT — Remove Duplicate Rows

```sql
-- Unique cities
SELECT DISTINCT city FROM users;

-- Unique combinations
SELECT DISTINCT city, age FROM users;
```

`DISTINCT` can be slow — it has to sort all rows to find duplicates. Use it intentionally.

---

## Common Pitfalls

**String comparison is case-sensitive**
```sql
-- These return different rows in most databases
WHERE name = 'alice'
WHERE name = 'Alice'
```

**NULL comparisons always return NULL (not true or false)**
```sql
-- This never matches — NULL = NULL is NULL, not TRUE
WHERE manager_id = NULL

-- Use IS NULL instead
WHERE manager_id IS NULL
```

**BETWEEN is inclusive**
```sql
-- Includes age 18 AND age 65
WHERE age BETWEEN 18 AND 65
```

**ORDER BY without LIMIT gives inconsistent pagination**
If you paginate with `OFFSET` but don't `ORDER BY` a unique column, rows can shift between pages as data changes.

---

## Quick Reference

```
SELECT
  SELECT col1, col2 FROM table       -- specific columns
  SELECT * FROM table                -- all columns
  SELECT col AS alias FROM table     -- rename in output

WHERE
  WHERE col = 'value'                -- equality
  WHERE col != 'value'               -- not equal
  WHERE col > 10                     -- comparison
  WHERE col BETWEEN 10 AND 20        -- inclusive range
  WHERE col IN ('a', 'b', 'c')       -- match list
  WHERE col LIKE 'A%'                -- pattern: starts with A
  WHERE col IS NULL                  -- null check
  WHERE col IS NOT NULL              -- not null
  WHERE a AND b                      -- both conditions
  WHERE a OR b                       -- either condition

NULL
  IS NULL / IS NOT NULL              -- always use, never = NULL
  COALESCE(col, default)             -- first non-null value
  NULLIF(a, b)                       -- NULL if a = b, else a

ORDER & LIMIT
  ORDER BY col ASC / DESC            -- sort
  ORDER BY col1, col2                -- multi-column sort
  LIMIT n                            -- first n rows
  LIMIT n OFFSET m                   -- pagination

DISTINCT
  SELECT DISTINCT col FROM table     -- unique values
```
