# 04 — Subqueries & CTEs

A subquery is a query nested inside another query. A CTE (Common Table Expression) is a named subquery defined before the main query with `WITH`. Both let you break complex queries into logical steps.

---

## Subqueries in WHERE

The most common use: filter rows based on the result of another query.

```sql
-- Users who have placed at least one order
SELECT name FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- Users who have never ordered (NOT IN)
SELECT name FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM orders WHERE user_id IS NOT NULL);

-- Users whose order total exceeds the average order total
SELECT name FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
    GROUP BY user_id
    HAVING SUM(amount) > (SELECT AVG(amount) FROM orders)
);
```

**Caution with NOT IN and NULLs:** If the subquery returns any NULL, `NOT IN` returns no rows at all. Use `NOT EXISTS` instead when NULLs are possible.

```sql
-- Safer: NOT EXISTS instead of NOT IN
SELECT name FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

---

## Subqueries in FROM (Derived Tables)

A subquery in `FROM` creates a temporary table for the outer query to select from.

```sql
-- Top spenders: first aggregate, then filter and sort
SELECT name, total_spent
FROM (
    SELECT user_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY user_id
) AS user_totals
JOIN users ON users.id = user_totals.user_id
WHERE total_spent > 100
ORDER BY total_spent DESC;
```

The subquery must be given an alias (`user_totals` above).

---

## Correlated Subqueries

A correlated subquery references columns from the outer query. It runs once per row of the outer query — can be slow on large tables.

```sql
-- Each user's most recent order amount
SELECT u.name, (
    SELECT o.amount
    FROM orders o
    WHERE o.user_id = u.id        -- references outer u.id
    ORDER BY o.created_at DESC
    LIMIT 1
) AS last_order_amount
FROM users u;
```

The `u.id` inside the subquery changes for each row of the outer query — that's what makes it correlated.

---

## Subqueries in SELECT

Return a single value per row.

```sql
-- Show each user's order count inline
SELECT
    u.name,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```

Must return exactly one row and one column per outer row, or it errors.

---

## EXISTS and NOT EXISTS

`EXISTS` is faster than `IN` for large datasets because it stops scanning as soon as it finds one match.

```sql
-- Users who have placed at least one order
SELECT name FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- Users with no orders
SELECT name FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

The `SELECT 1` is convention — `EXISTS` only cares whether any row exists, not what the subquery returns.

---

## CTEs — Common Table Expressions

CTEs use `WITH` to name a subquery before the main query. They make complex queries dramatically more readable.

```sql
WITH user_totals AS (
    SELECT user_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY user_id
)
SELECT u.name, ut.total_spent
FROM users u
JOIN user_totals ut ON u.id = ut.user_id
WHERE ut.total_spent > 100
ORDER BY ut.total_spent DESC;
```

The CTE `user_totals` acts like a temporary view — it exists only for the duration of this query.

---

## Multiple CTEs

Chain multiple CTEs with commas.

```sql
WITH
monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(amount) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', created_at)
),
avg_monthly AS (
    SELECT AVG(revenue) AS avg_revenue FROM monthly_revenue
)
SELECT month, revenue, avg_revenue,
       revenue - avg_revenue AS delta
FROM monthly_revenue
CROSS JOIN avg_monthly
ORDER BY month;
```

---

## Recursive CTEs

Recursive CTEs process hierarchical data (trees, org charts, paths). They reference themselves.

```sql
-- Walk an employee org chart from the top down
WITH RECURSIVE org AS (
    -- Base case: top-level employees (no manager)
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees whose manager is already in org
    SELECT e.id, e.name, e.manager_id, org.level + 1
    FROM employees e
    JOIN org ON e.manager_id = org.id
)
SELECT name, level FROM org ORDER BY level, name;
```

The `UNION ALL` separates the base case from the recursive step. The query keeps running until no new rows are added.

---

## CTE vs Subquery — When to Use Each

| | Subquery | CTE |
|--|---------|-----|
| Readability | Gets messy when nested deeply | Very readable — named and separated |
| Reusability | Must repeat the SQL | Can reference the CTE multiple times |
| Debugging | Hard to isolate and test | Can run the CTE alone to inspect it |
| Performance | Same in most databases | Same in most databases |

**Rule of thumb:** Use a CTE whenever the subquery would need a meaningful name to be understood. If it's trivial (e.g., `WHERE id IN (SELECT id FROM...)`), a subquery is fine.

---

## Common Pitfalls

**NOT IN with NULLs returns no rows**
```sql
-- If orders has any row where user_id IS NULL, this returns nothing
WHERE id NOT IN (SELECT user_id FROM orders)

-- Safe alternative
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id)
```

**Correlated subqueries in SELECT are slow at scale**
They run once per row. For large tables, rewrite as a JOIN or a CTE with a JOIN.

**CTE name shadowing**
If your CTE has the same name as a real table, the CTE wins inside that query.

---

## Quick Reference

```
Subquery in WHERE
  WHERE col IN (SELECT col FROM ...)
  WHERE col NOT IN (SELECT col FROM ...)   -- careful with NULLs
  WHERE EXISTS (SELECT 1 FROM ... WHERE ...)
  WHERE NOT EXISTS (SELECT 1 FROM ... WHERE ...)

Subquery in FROM
  FROM (SELECT ... FROM ...) AS alias

Subquery in SELECT
  SELECT (SELECT COUNT(*) FROM ... WHERE ...) AS count_col

CTE (Common Table Expression)
  WITH cte_name AS (
      SELECT ...
  )
  SELECT ... FROM cte_name;

Multiple CTEs
  WITH
  cte1 AS (SELECT ...),
  cte2 AS (SELECT ... FROM cte1)
  SELECT ... FROM cte2;

Recursive CTE
  WITH RECURSIVE cte AS (
      -- base case
      SELECT ...
      UNION ALL
      -- recursive case referencing cte
      SELECT ... FROM table JOIN cte ON ...
  )
  SELECT * FROM cte;

EXISTS vs IN
  EXISTS  — stops at first match, handles NULLs safely, often faster
  IN      — evaluates all rows, dangerous with NULLs in subquery
```
