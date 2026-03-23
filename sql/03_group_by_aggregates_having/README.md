# 03 — GROUP BY, Aggregates & HAVING

Aggregate functions collapse multiple rows into a single value. `GROUP BY` lets you aggregate within groups (e.g., one row per city, one row per user). `HAVING` filters those groups.

---

## Aggregate Functions

These operate on a set of rows and return one value.

```sql
-- COUNT rows
SELECT COUNT(*) FROM orders;            -- total rows (includes NULLs)
SELECT COUNT(amount) FROM orders;       -- rows where amount is NOT NULL
SELECT COUNT(DISTINCT user_id) FROM orders;  -- unique users who ordered

-- SUM and AVG
SELECT SUM(amount) FROM orders;
SELECT AVG(amount) FROM orders;

-- MIN and MAX
SELECT MIN(amount), MAX(amount) FROM orders;

-- All together
SELECT
    COUNT(*)          AS total_orders,
    SUM(amount)       AS total_revenue,
    AVG(amount)       AS avg_order,
    MIN(amount)       AS smallest,
    MAX(amount)       AS largest
FROM orders;
```

---

## GROUP BY — Aggregate Within Groups

Without `GROUP BY`, aggregates collapse *all* rows to one. With `GROUP BY`, they collapse rows *within each group*.

```sql
-- Orders per user
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id;

-- Revenue per user
SELECT user_id, SUM(amount) AS total_spent
FROM orders
GROUP BY user_id;

-- Orders per city (joining first)
SELECT u.city, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.city;
```

**Rule:** Every column in `SELECT` that isn't an aggregate must appear in `GROUP BY`.

```sql
-- Error: name not in GROUP BY and not an aggregate
SELECT user_id, name, COUNT(*) FROM orders GROUP BY user_id;

-- Fix: include name in GROUP BY
SELECT user_id, name, COUNT(*) FROM orders GROUP BY user_id, name;
```

---

## GROUP BY with Multiple Columns

```sql
-- Orders per user per month
SELECT
    user_id,
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS order_count,
    SUM(amount) AS monthly_total
FROM orders
GROUP BY user_id, DATE_TRUNC('month', created_at)
ORDER BY user_id, month;
```

---

## HAVING — Filter Groups

`WHERE` filters rows before grouping. `HAVING` filters groups after aggregating.

```sql
-- Only users with more than 3 orders
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 3;

-- Only cities with average order > $50
SELECT u.city, AVG(o.amount) AS avg_order
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.city
HAVING AVG(o.amount) > 50;

-- WHERE and HAVING together
SELECT user_id, SUM(amount) AS total
FROM orders
WHERE created_at >= '2024-01-01'   -- filter rows first
GROUP BY user_id
HAVING SUM(amount) > 100;          -- then filter groups
```

---

## Query Execution Order

SQL clauses execute in this order (not the order you write them):

```
1. FROM / JOIN     — which tables
2. WHERE           — filter rows
3. GROUP BY        — form groups
4. HAVING          — filter groups
5. SELECT          — compute output columns
6. ORDER BY        — sort
7. LIMIT / OFFSET  — paginate
```

This explains why you can't use a `SELECT` alias in `WHERE` or `HAVING` — the alias doesn't exist yet when those clauses run.

```sql
-- Error: total not defined yet when HAVING runs
SELECT user_id, SUM(amount) AS total
FROM orders
GROUP BY user_id
HAVING total > 100;

-- Fix: repeat the expression
HAVING SUM(amount) > 100;
```

---

## NULL in Aggregates

Aggregates (except `COUNT(*)`) ignore NULL values automatically.

```sql
-- If 3 of 10 rows have NULL amount:
COUNT(*)       -- 10
COUNT(amount)  -- 7
SUM(amount)    -- sum of the 7 non-null values
AVG(amount)    -- average of the 7 non-null values (not divided by 10)
```

`GROUP BY` treats NULL as its own group — all NULL values in a grouping column land in the same bucket.

---

## Common Pitfalls

**Using WHERE instead of HAVING for aggregate conditions**
```sql
-- Error: can't use aggregate in WHERE
SELECT user_id FROM orders WHERE COUNT(*) > 3 GROUP BY user_id;

-- Fix: use HAVING
SELECT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 3;
```

**Column not in GROUP BY**
```sql
-- Error (in strict SQL mode)
SELECT user_id, name, COUNT(*) FROM orders GROUP BY user_id;

-- Fix: every non-aggregate SELECT column must be in GROUP BY
SELECT user_id, name, COUNT(*) FROM orders GROUP BY user_id, name;
```

**COUNT(*) vs COUNT(col)**
```sql
COUNT(*)     -- counts all rows including NULLs
COUNT(col)   -- counts only non-NULL values in that column
```

---

## Quick Reference

```
Aggregate Functions
  COUNT(*)              -- total rows
  COUNT(col)            -- non-null values
  COUNT(DISTINCT col)   -- unique non-null values
  SUM(col)              -- total (ignores NULL)
  AVG(col)              -- average (ignores NULL)
  MIN(col)              -- minimum
  MAX(col)              -- maximum

GROUP BY
  GROUP BY col                       -- one group per unique value
  GROUP BY col1, col2                -- one group per unique combination
  Rule: every non-aggregate SELECT column must be in GROUP BY

HAVING
  HAVING COUNT(*) > 3                -- filter groups by count
  HAVING SUM(amount) > 100           -- filter groups by aggregate
  HAVING AVG(amount) BETWEEN 10 AND 50

WHERE vs HAVING
  WHERE  — filters rows before grouping
  HAVING — filters groups after aggregating

Execution Order
  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```
