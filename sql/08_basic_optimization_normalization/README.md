# 08 — Basic Optimization & Normalization

Normalization is the process of organizing database tables to reduce redundancy and avoid update anomalies. Optimization is understanding why queries are slow and fixing them. Both are about designing schemas and queries that are correct *and* efficient.

---

## EXPLAIN — See the Query Plan

Before optimizing, understand what the database is actually doing. `EXPLAIN` shows the query plan without running the query. `EXPLAIN ANALYZE` runs it and shows actual timing.

```sql
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
```

### Reading the Output

```
Seq Scan on users  (cost=0.00..1.05 rows=1 width=68)
  Filter: (email = 'alice@example.com')
```

- **Seq Scan** — reading every row (no index used)
- **Index Scan** — using an index (fast)
- **cost=0.00..1.05** — estimated startup cost .. total cost (in arbitrary units)
- **rows=1** — estimated rows returned
- **Actual time=0.012..0.013** — real execution time in milliseconds (with ANALYZE)

### Common Plan Nodes

| Node | Meaning |
|------|---------|
| `Seq Scan` | Full table scan — no index |
| `Index Scan` | Uses an index, fetches rows from table |
| `Index Only Scan` | Uses index only, never touches the table (fastest) |
| `Hash Join` | Joins using a hash table (good for large tables) |
| `Nested Loop` | For each outer row, scan inner (good for small inner sets) |
| `Sort` | Sorting rows (expensive if no index to pre-sort) |

---

## Common Query Performance Problems

### 1. Sequential Scans on Large Tables

```sql
-- Problem: no index on email
SELECT * FROM users WHERE email = 'alice@example.com';  -- Seq Scan

-- Fix: add an index
CREATE INDEX idx_users_email ON users(email);  -- now uses Index Scan
```

### 2. Function Calls Defeating Indexes

```sql
-- Problem: index on name can't be used
WHERE LOWER(name) = 'alice'

-- Fix: create a functional index
CREATE INDEX idx_users_name_lower ON users(LOWER(name));
```

### 3. Leading Wildcard in LIKE

```sql
-- Problem: can't use a B-tree index with a leading %
WHERE name LIKE '%alice%'

-- Trailing wildcard is fine
WHERE name LIKE 'alice%'

-- For full-text search, use PostgreSQL's full-text features
WHERE to_tsvector('english', name) @@ to_tsquery('alice')
```

### 4. SELECT * When You Need a Few Columns

```sql
-- Problem: transfers all columns across the network + prevents index-only scans
SELECT * FROM orders WHERE user_id = 1;

-- Better: only select what you need
SELECT id, amount, created_at FROM orders WHERE user_id = 1;
```

### 5. N+1 Queries (SQL equivalent)

The N+1 problem in SQL: a query returns N rows, then you loop and run N more queries for related data. Fix with a JOIN.

```sql
-- Problem: 1 query for users + N queries for each user's order count
SELECT * FROM users;                                  -- query 1
SELECT COUNT(*) FROM orders WHERE user_id = 1;       -- query 2
SELECT COUNT(*) FROM orders WHERE user_id = 2;       -- query 3 ... etc.

-- Fix: one query with a JOIN
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

---

## Normalization

Normalization organizes tables to reduce redundancy. Each normal form eliminates a specific type of problem.

### First Normal Form (1NF)

**Rule:** Every column holds one atomic value. No repeating groups, no arrays in a column.

```sql
-- Violates 1NF: storing multiple values in one column
INSERT INTO orders (id, user_id, products) VALUES (1, 1, 'apple,banana,cherry');

-- Correct: each value in its own row
CREATE TABLE order_items (
    order_id   INT REFERENCES orders(id),
    product    TEXT,
    PRIMARY KEY (order_id, product)
);
```

### Second Normal Form (2NF)

**Rule:** Must be in 1NF. Every non-key column must depend on the *entire* primary key (not just part of it). Only matters for composite primary keys.

```sql
-- Violates 2NF: product_name depends only on product_id, not the full key
CREATE TABLE order_items (
    order_id     INT,
    product_id   INT,
    product_name TEXT,  -- depends only on product_id, not (order_id, product_id)
    quantity     INT,
    PRIMARY KEY (order_id, product_id)
);

-- Correct: move product_name to a products table
CREATE TABLE products (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE order_items (
    order_id   INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity   INT,
    PRIMARY KEY (order_id, product_id)
);
```

### Third Normal Form (3NF)

**Rule:** Must be in 2NF. No transitive dependencies — non-key columns must depend directly on the primary key, not on other non-key columns.

```sql
-- Violates 3NF: zip_code determines city, but zip_code is not the key
CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    name     TEXT,
    zip_code TEXT,
    city     TEXT   -- depends on zip_code, not on id
);

-- Correct: extract the zip → city relationship
CREATE TABLE zip_codes (
    zip  TEXT PRIMARY KEY,
    city TEXT NOT NULL
);

CREATE TABLE users (
    id       SERIAL PRIMARY KEY,
    name     TEXT,
    zip_code TEXT REFERENCES zip_codes(zip)
);
```

---

## Normal Forms Summary

| Form | Rule | Eliminates |
|------|------|-----------|
| 1NF | Atomic values, no repeating groups | Arrays/lists in columns |
| 2NF | Full dependency on entire PK | Partial key dependency |
| 3NF | No transitive dependency | Non-key to non-key dependency |

Most production schemas aim for 3NF. "Normalize until it hurts, denormalize until it works."

---

## Denormalization — Intentional Redundancy

Sometimes you store redundant data intentionally for performance.

```sql
-- Normalized: to get the order total, sum all order_items
SELECT SUM(quantity * price) FROM order_items WHERE order_id = 1;

-- Denormalized: store the total directly on the order
ALTER TABLE orders ADD COLUMN total NUMERIC(10, 2);
-- Update it whenever order_items change (usually via trigger or application logic)
```

Trade-off: reads are faster, but writes are more complex and data can get out of sync.

Common denormalization patterns:
- Storing `order_total` on orders instead of computing from items
- Storing `user_name` on orders to avoid joining users
- Storing pre-aggregated counts (e.g., `post.comment_count`)

---

## Common Pitfalls

**Not running EXPLAIN before optimizing**
Don't guess — measure. An index you think should help might not be used. `EXPLAIN ANALYZE` shows you exactly what's happening.

**Over-normalizing**
Full normalization can require many JOINs for simple queries. If a table is small and rarely changes (like a zip code lookup), a JOIN is overkill. Practical schemas balance normalization with query simplicity.

**Adding indexes to everything**
Every index has a write cost. A table with 10 indexes pays 10x the write cost. Add indexes based on actual query patterns, not preemptively.

**Not analyzing tables**
The query planner uses statistics about data distribution. In PostgreSQL, `VACUUM ANALYZE` (runs automatically, but can be run manually) updates these statistics so the planner makes good decisions.

```sql
ANALYZE users;   -- update statistics for this table
```

---

## Quick Reference

```
EXPLAIN
  EXPLAIN query;                    -- show plan without running
  EXPLAIN ANALYZE query;            -- run and show actual timings

  Plan nodes to watch for:
    Seq Scan   → no index (slow on large tables)
    Index Scan → using index (fast)
    Sort       → may need an index to avoid

Optimization Checklist
  ✓ Run EXPLAIN ANALYZE — confirm the problem before fixing
  ✓ Add index on frequently filtered columns (WHERE, JOIN, ORDER BY)
  ✓ Avoid functions on indexed columns in WHERE
  ✓ Avoid leading wildcards in LIKE
  ✓ Select only needed columns (avoid SELECT *)
  ✓ Use JOINs instead of loops (avoid N+1)
  ✓ Run ANALYZE after large data changes

Normal Forms
  1NF  — atomic values, no lists in a column
  2NF  — no partial key dependency (composite PKs)
  3NF  — no transitive dependency (A→B→C becomes A→B, A→C removed)

Denormalization Tradeoffs
  + Faster reads (fewer JOINs)
  - Data can become inconsistent
  - Writes are more complex
  Use when: hot read paths, reporting tables, pre-aggregated counts
```
