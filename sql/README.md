# SQL Reference Course

A practical reference for SQL, focused on PostgreSQL. These lessons cover the core query language you'll use day-to-day as a backend developer — not database administration or vendor-specific internals.

---

## Requirements

- PostgreSQL 15+ (or any SQL database — syntax is mostly portable)
- Optional: [pgAdmin](https://www.pgadmin.org/) or [DBeaver](https://dbeaver.io/) for a GUI
- Optional: `psql` CLI for running queries directly

All examples use standard SQL with PostgreSQL-specific notes where dialects differ.

---

## Lessons

| # | Topic | What You'll Learn |
|---|-------|------------------|
| 01 | [Basic Queries — SELECT & WHERE](01_basic_queries_select_where/README.md) | Selecting columns, filtering rows, sorting, NULL handling |
| 02 | [JOINs](02_joins/README.md) | Combining data from multiple tables |
| 03 | [GROUP BY, Aggregates & HAVING](03_group_by_aggregates_having/README.md) | Counting, summing, averaging, grouping results |
| 04 | [Subqueries & CTEs](04_subqueries_ctes/README.md) | Nested queries, WITH clauses, readable complex queries |
| 05 | [INSERT, UPDATE, DELETE & Transactions](05_insert_update_delete_transactions/README.md) | Modifying data, ACID guarantees, rollbacks |
| 06 | [Window Functions Basics](06_window_functions_basics/README.md) | Row numbering, ranking, running totals, LAG/LEAD |
| 07 | [Indexes, Primary & Foreign Keys](07_indexes_primary_foreign_keys/README.md) | Constraints, indexes, referential integrity |
| 08 | [Basic Optimization & Normalization](08_basic_optimization_normalization/README.md) | EXPLAIN, query performance, 1NF/2NF/3NF |

---

## Recommended Order

Read them in order — each lesson builds on the previous one. Lessons 1–3 are the foundation; the rest build on top.

---

## How to Practice

Create a local PostgreSQL database and run the examples. A minimal schema for most examples:

```sql
CREATE TABLE users (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    email   TEXT UNIQUE NOT NULL,
    age     INT,
    city    TEXT
);

CREATE TABLE orders (
    id         SERIAL PRIMARY KEY,
    user_id    INT REFERENCES users(id),
    amount     NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## SQL Dialect Notes

These lessons use standard SQL, which works across PostgreSQL, MySQL, SQLite, and SQL Server with minor differences:

| Feature | PostgreSQL | MySQL | SQLite | SQL Server |
|---------|-----------|-------|--------|-----------|
| Auto-increment | `SERIAL` or `GENERATED ALWAYS AS IDENTITY` | `AUTO_INCREMENT` | `INTEGER PRIMARY KEY` | `IDENTITY(1,1)` |
| String concat | `\|\|` or `concat()` | `concat()` | `\|\|` | `+` |
| Limit rows | `LIMIT n` | `LIMIT n` | `LIMIT n` | `TOP n` or `FETCH FIRST n ROWS ONLY` |
| True/False | `TRUE` / `FALSE` | `1` / `0` | `1` / `0` | `1` / `0` |
| Explain | `EXPLAIN ANALYZE` | `EXPLAIN` | Not available | `SET SHOWPLAN_ALL ON` |
