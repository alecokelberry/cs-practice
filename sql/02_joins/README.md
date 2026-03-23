# 02 — JOINs

A JOIN combines rows from two tables based on a related column. This is the core of relational databases — data is split across tables to avoid duplication, and JOINs reassemble it at query time.

---

## The Mental Model

Think of two tables side by side. A JOIN asks: "for each row in table A, find the matching rows in table B based on this condition." What happens to rows that don't match depends on the join type.

```
users                    orders
id | name                id | user_id | amount
---+-------              ---+---------+-------
1  | Alice               1  | 1       | 50.00
2  | Bob                 2  | 1       | 30.00
3  | Carol               3  | 2       | 75.00
                         4  | 99      | 10.00  ← no matching user
```

---

## INNER JOIN — Only Matching Rows

Returns rows only when there's a match in both tables. Non-matching rows are excluded from both sides.

```sql
SELECT users.name, orders.amount
FROM users
INNER JOIN orders ON users.id = orders.user_id;

-- Result: Alice + 50, Alice + 30, Bob + 75
-- Carol (no orders) and order 4 (no user) are excluded
```

`JOIN` without a keyword means `INNER JOIN` — they're identical.

---

## LEFT JOIN — All Left Rows, Matching Right Rows

Returns all rows from the left table. If no match in the right table, the right columns are NULL.

```sql
SELECT users.name, orders.amount
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

-- Result:
-- Alice  | 50.00
-- Alice  | 30.00
-- Bob    | 75.00
-- Carol  | NULL   ← Carol has no orders, but she appears
```

Use `LEFT JOIN` when you want all records from one table regardless of whether the other has matching data — e.g., "show all users and their orders, including users with no orders."

---

## RIGHT JOIN — All Right Rows, Matching Left Rows

The mirror of LEFT JOIN. All rows from the right table appear; left table NULLs where there's no match.

```sql
SELECT users.name, orders.amount
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;

-- Result:
-- Alice  | 50.00
-- Alice  | 30.00
-- Bob    | 75.00
-- NULL   | 10.00  ← order 4 has no matching user
```

`RIGHT JOIN` is rarely used — you can always rewrite it as a `LEFT JOIN` by swapping the table order. Most developers stick to `LEFT JOIN` for consistency.

---

## FULL OUTER JOIN — All Rows from Both Tables

Returns all rows from both tables. NULLs appear on whichever side has no match.

```sql
SELECT users.name, orders.amount
FROM users
FULL OUTER JOIN orders ON users.id = orders.user_id;

-- Result: all of the above — Alice (2 rows), Bob, Carol (NULL), order 4 (NULL)
```

---

## CROSS JOIN — Every Combination

Returns every combination of rows from both tables (cartesian product). Rarely what you want accidentally.

```sql
SELECT colors.name, sizes.label
FROM colors
CROSS JOIN sizes;

-- 3 colors × 4 sizes = 12 rows
```

Useful for generating combinations (e.g., all possible product variants).

---

## Self-Join — Joining a Table to Itself

Used when rows in a table relate to other rows in the same table (e.g., employees with managers).

```sql
-- employees table: id, name, manager_id (FK to same table)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

Aliases are required here to distinguish the two "copies" of the table.

---

## Joining Multiple Tables

```sql
SELECT u.name, o.amount, p.name AS product
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE u.city = 'Austin';
```

Each `JOIN` adds another table. Aliases (`u`, `o`, `oi`, `p`) keep it readable.

---

## Filtering After a JOIN

```sql
-- Filter on joined table
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.amount > 50;

-- Find users with NO orders (anti-join pattern)
SELECT users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
```

The anti-join pattern (LEFT JOIN + WHERE right side IS NULL) is common and worth memorizing.

---

## Common Pitfalls

**Forgetting the ON condition**
```sql
-- This is a CROSS JOIN — every combination, often not what you want
SELECT * FROM users JOIN orders;

-- Always specify the join condition
SELECT * FROM users JOIN orders ON users.id = orders.user_id;
```

**Ambiguous column names**
```sql
-- Error: column "id" is ambiguous
SELECT id, name FROM users JOIN orders ON users.id = orders.user_id;

-- Fix: qualify with table name or alias
SELECT users.id, users.name FROM users JOIN orders ON users.id = orders.user_id;
```

**INNER JOIN hiding missing data**
If your results are missing rows you expect, you might need `LEFT JOIN` instead of `INNER JOIN`.

**Row multiplication in one-to-many joins**
```sql
-- If a user has 5 orders, they appear 5 times
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
-- Alice appears twice (she has 2 orders) — this is correct behavior, not a bug
```

---

## Quick Reference

```
JOIN Types (all use ON table_a.col = table_b.col)

  INNER JOIN     — only matching rows from both tables
  LEFT JOIN      — all left rows + matching right rows (NULL if no match)
  RIGHT JOIN     — all right rows + matching left rows (NULL if no match)
  FULL OUTER JOIN — all rows from both tables (NULLs where no match)
  CROSS JOIN     — every combination (no ON condition)

Common Patterns

  -- Basic join
  SELECT a.col, b.col
  FROM a
  JOIN b ON a.id = b.a_id;

  -- Anti-join: rows in A with no match in B
  SELECT a.*
  FROM a
  LEFT JOIN b ON a.id = b.a_id
  WHERE b.id IS NULL;

  -- Self-join
  FROM employees e
  LEFT JOIN employees m ON e.manager_id = m.id

  -- Multiple joins
  FROM a
  JOIN b ON a.id = b.a_id
  JOIN c ON b.id = c.b_id

Rules
  Always use table aliases when joining
  Always qualify column names (table.column) when ambiguous
  Prefer LEFT JOIN over RIGHT JOIN for consistency
```
