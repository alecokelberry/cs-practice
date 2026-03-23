# 06 — Window Functions Basics

Window functions perform calculations across a set of rows *related to the current row*, without collapsing them into one row the way `GROUP BY` does. You get the aggregate value alongside the original row.

---

## The Mental Model

`GROUP BY` + aggregate: collapses 10 rows into 1.
Window function: keeps all 10 rows, but adds a computed column to each.

```sql
-- GROUP BY: one row per user
SELECT user_id, SUM(amount) AS total FROM orders GROUP BY user_id;

-- Window function: all order rows, with the user's total on each row
SELECT user_id, amount, SUM(amount) OVER (PARTITION BY user_id) AS user_total
FROM orders;
```

---

## The OVER Clause

`OVER()` is what makes a function a window function. Without it, `SUM()` is an aggregate. With it, it's a window function.

```sql
-- OVER() with nothing: the window is ALL rows
SELECT name, amount, SUM(amount) OVER () AS grand_total
FROM orders;

-- PARTITION BY: one window per group (like GROUP BY, but keeps all rows)
SELECT user_id, amount, SUM(amount) OVER (PARTITION BY user_id) AS user_total
FROM orders;

-- ORDER BY inside OVER: running total (cumulative sum)
SELECT user_id, created_at, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total
FROM orders;
```

---

## ROW_NUMBER, RANK, DENSE_RANK

These number or rank rows within a window.

```sql
SELECT
    user_id,
    amount,
    ROW_NUMBER()  OVER (PARTITION BY user_id ORDER BY amount DESC) AS row_num,
    RANK()        OVER (PARTITION BY user_id ORDER BY amount DESC) AS rank,
    DENSE_RANK()  OVER (PARTITION BY user_id ORDER BY amount DESC) AS dense_rank
FROM orders;
```

| Function | Ties | Gap after ties |
|----------|------|---------------|
| `ROW_NUMBER()` | Arbitrary order (no true tie) | Always sequential |
| `RANK()` | Same rank | Yes — next rank skips |
| `DENSE_RANK()` | Same rank | No — no gaps |

Example with tied amounts of $50:

```
amount | ROW_NUMBER | RANK | DENSE_RANK
50     | 1          | 1    | 1
50     | 2          | 1    | 1
30     | 3          | 3    | 2   ← RANK skips 2, DENSE_RANK doesn't
```

---

## Getting the Top N Per Group

A common use of `ROW_NUMBER()`: get the top 1 (or top N) rows per group.

```sql
-- Largest order per user
WITH ranked AS (
    SELECT user_id, amount,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn
    FROM orders
)
SELECT user_id, amount
FROM ranked
WHERE rn = 1;
```

You can't use a window function in `WHERE` directly — that's why the CTE is needed.

---

## LAG and LEAD — Access Adjacent Rows

`LAG` looks at the previous row; `LEAD` looks at the next row (within the window).

```sql
SELECT
    user_id,
    created_at,
    amount,
    LAG(amount)  OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order,
    LEAD(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS next_order,
    amount - LAG(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS change
FROM orders;
```

The first row has NULL for `LAG` (no previous row). `LEAD` and `LAG` accept a default:

```sql
LAG(amount, 1, 0) OVER (...)   -- use 0 if there's no previous row
```

---

## FIRST_VALUE and LAST_VALUE

Return the first or last value in the window.

```sql
SELECT
    user_id,
    amount,
    FIRST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS first_order,
    LAST_VALUE(amount)  OVER (
        PARTITION BY user_id
        ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order
FROM orders;
```

`LAST_VALUE` requires the explicit frame clause (`ROWS BETWEEN ...`) — by default, the window frame only goes up to the current row, so `LAST_VALUE` would just return the current row's value.

---

## NTILE — Divide Rows into Buckets

```sql
-- Divide users into 4 quartiles by total spending
WITH totals AS (
    SELECT user_id, SUM(amount) AS total FROM orders GROUP BY user_id
)
SELECT user_id, total,
       NTILE(4) OVER (ORDER BY total DESC) AS quartile
FROM totals;
```

`NTILE(4)` assigns 1–4. Quartile 1 = highest spenders.

---

## Frame Clauses

By default, `ORDER BY` inside `OVER` sets the frame to "all preceding rows up to current." You can override this:

```sql
-- Rolling 7-row average
AVG(amount) OVER (
    ORDER BY created_at
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)

-- All rows in the partition (explicitly)
SUM(amount) OVER (
    PARTITION BY user_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

`ROWS` counts physical rows; `RANGE` counts rows with the same `ORDER BY` value (relevant for ties).

---

## Common Pitfalls

**Using window functions in WHERE**
```sql
-- Error: window functions not allowed in WHERE
WHERE ROW_NUMBER() OVER (...) = 1

-- Fix: wrap in a CTE or subquery
WITH ranked AS (SELECT *, ROW_NUMBER() OVER (...) AS rn FROM ...)
SELECT * FROM ranked WHERE rn = 1;
```

**LAST_VALUE returning the current row**
The default frame for `ORDER BY` inside `OVER` ends at the current row. Always add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` for `LAST_VALUE`.

**Not partitioning when you should**
`SUM(amount) OVER ()` sums the entire table. `SUM(amount) OVER (PARTITION BY user_id)` sums per user. Forgetting `PARTITION BY` gives wrong results without an error.

---

## Quick Reference

```
OVER Clause
  OVER ()                                    -- whole result set as window
  OVER (PARTITION BY col)                    -- one window per group
  OVER (ORDER BY col)                        -- running/cumulative (ordered)
  OVER (PARTITION BY col ORDER BY col2)      -- per-group running total

Ranking Functions
  ROW_NUMBER() OVER (...)   -- unique sequential number, no ties
  RANK()       OVER (...)   -- tied rows get same rank, gaps after
  DENSE_RANK() OVER (...)   -- tied rows get same rank, no gaps
  NTILE(n)     OVER (...)   -- divide into n buckets (1..n)

Offset Functions
  LAG(col, n, default)  OVER (...)   -- n rows before current (default: 1)
  LEAD(col, n, default) OVER (...)   -- n rows after current
  FIRST_VALUE(col)      OVER (...)   -- first value in window
  LAST_VALUE(col)       OVER (...)   -- last value in window (needs frame clause)

Aggregates as Window Functions
  SUM(col)  OVER (...)     -- running or partitioned sum
  AVG(col)  OVER (...)     -- running or partitioned average
  COUNT(*)  OVER (...)     -- running or partitioned count
  MIN/MAX   OVER (...)     -- min/max in window

Frame Clause
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW     -- default with ORDER BY
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- whole partition
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW              -- rolling 7

Top N per group pattern
  WITH ranked AS (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY sort_col DESC) AS rn
      FROM table
  )
  SELECT * FROM ranked WHERE rn <= n;
```
