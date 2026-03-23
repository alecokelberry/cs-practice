# Lesson 10 — Dynamic Programming

## What This Covers
What dynamic programming (DP) is and when to use it, memoization with `@functools.cache`,
bottom-up tabulation, and five classic DP problems: Fibonacci, Climbing Stairs, Coin Change,
Longest Common Subsequence (LCS), and 0/1 Knapsack.

---

## Key Concepts

### What is Dynamic Programming?
DP applies when a problem has two properties:

1. **Overlapping subproblems** — the same smaller problems are solved multiple times
2. **Optimal substructure** — the optimal solution is built from optimal solutions to subproblems

The idea: solve each subproblem **once**, store the result, and look it up instead of
recomputing. This transforms exponential algorithms into polynomial ones.

---

### Memoization (Top-Down)
Start with the naive recursive solution. Add a cache to store results.
`@functools.cache` does this automatically.

```python
from functools import cache

@cache
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

Naive fibonacci: O(2ⁿ) — exponential.
Memoized fibonacci: O(n) — each value computed once, then cached.

`@cache` (Python 3.9+) is equivalent to `@lru_cache(maxsize=None)`. It's unbounded.
Use `@lru_cache(maxsize=128)` if memory is a concern.

---

### Tabulation (Bottom-Up)
Instead of recursing top-down and caching, build the solution bottom-up with a table.
Start from the base cases and fill in larger subproblems iteratively.

```python
def fib_tabulation(n: int) -> int:
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]   # each value uses already-computed values
    return dp[n]
```

Space optimization: if you only need the last few values, you don't need the full table.

---

### Memoization vs Tabulation

| | Memoization (top-down) | Tabulation (bottom-up) |
|--|------------------------|----------------------|
| Code style | Recursive + cache | Iterative + table |
| Entry point | Problem statement directly | Build from base cases |
| Subproblems | Only computes needed ones | Computes all |
| Stack depth | Call stack grows with depth | No recursion |
| When to use | When not all subproblems are needed | When you need all of them; large n |

---

### Classic Problems Summary

| Problem | Recurrence | Complexity |
|---------|-----------|-----------|
| Fibonacci | `dp[n] = dp[n-1] + dp[n-2]` | O(n) time, O(n) space (O(1) optimized) |
| Climbing Stairs | `dp[n] = dp[n-1] + dp[n-2]` | O(n) time, O(1) space |
| Coin Change | `dp[amount] = min(dp[amount - coin] + 1)` | O(amount × coins) |
| LCS | `dp[i][j] = dp[i-1][j-1]+1` or `max(dp[i-1][j], dp[i][j-1])` | O(m×n) time and space |
| 0/1 Knapsack | `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])` | O(n×W) |

---

### How to Approach a DP Problem
1. **Define the subproblem**: what does `dp[i]` (or `dp[i][j]`) represent?
2. **Write the recurrence**: how does `dp[i]` depend on smaller subproblems?
3. **Identify base cases**: what are the trivially-known values?
4. **Determine computation order**: what do you need to compute before what?
5. **Extract the answer**: which cell in the table is the final answer?

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `@functools.cache` | Memoize a function — caches all calls |
| `@functools.lru_cache(maxsize=128)` | Memoize with a size limit |
| `fn.cache_clear()` | Clear the cache |
| `dp = [0] * (n+1)` | 1D DP table of zeros |
| `dp = [[0]*(m+1) for _ in range(n+1)]` | 2D DP table |
| `float('inf')` | Infinity — useful for min-DP initialization |

---

## Common Pitfalls

- **Not identifying the subproblem clearly** — the hardest part of DP. Before coding, write `dp[i] = "..."` in English.
- **Wrong base cases** — DP is sensitive to initialization. Off-by-one in base cases cascades through the table.
- **Using `@cache` on a method** — `@cache` doesn't work well on instance methods (the instance is part of the key). Use a module-level function or `functools.lru_cache`.
- **2D table initialization** — `[[0] * m] * n` creates n references to the SAME list. Use `[[0]*m for _ in range(n)]` instead.
- **Forgetting to handle the "don't take" case in knapsack** — the recurrence has two options; you need both.
- **Memoization + mutable arguments** — `@cache` requires arguments to be hashable. Lists aren't hashable; use tuples.

---

## When to Use DP

Ask yourself:
- Can I break this into smaller versions of the same problem?
- Do I solve the same subproblem multiple times?
- Does the optimal answer depend on optimal answers to subproblems?

If yes to all three → DP. Start with memoization (easier to think about), then convert
to tabulation if you need to avoid recursion depth or squeeze out space.
