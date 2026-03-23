# ─────────────────────────────────────────────────────────────
#  Lesson 10 — Dynamic Programming
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import sys
import time
from functools import cache, lru_cache


# ── WHAT MAKES A PROBLEM "DP" ─────────────────────────────────
print("── what makes a problem dynamic programming ─")
print("""
  Two requirements:
  1. OVERLAPPING SUBPROBLEMS — the same smaller problem appears many times
  2. OPTIMAL SUBSTRUCTURE   — the optimal solution contains optimal subproblems

  The insight: solve each subproblem ONCE, store the result, reuse it.
  This transforms exponential → polynomial runtime.

  Two approaches:
  - Memoization (top-down): start with recursion, add a cache
  - Tabulation  (bottom-up): build a table from small cases to large
""")


# ── FIBONACCI — THE CANONICAL DP EXAMPLE ─────────────────────
print("── Fibonacci ────────────────────────────────")

# First: the naive recursive version — to see WHY DP helps
def fib_naive(n: int) -> int:
    """
    Naive recursion — O(2^n) time.
    fib(5) calls fib(4) and fib(3).
    fib(4) calls fib(3) and fib(2).
    fib(3) is computed TWICE — and it gets exponentially worse.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# Memoization: @cache stores every (n,) → result pair
# The first call computes the value; every subsequent call returns it instantly.
@cache
def fib_memo(n: int) -> int:
    """
    Memoized fibonacci — O(n) time, O(n) space (call stack + cache).
    @cache automatically handles the caching. No manual dict needed.
    """
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

# Tabulation: bottom-up with a table
def fib_tabulation(n: int) -> int:
    """
    Bottom-up tabulation — O(n) time, O(n) space.
    Build from base cases upward. No recursion.
    """
    if n <= 1:
        return n
    dp: list[int] = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]   # each value builds on two previous values
    return dp[n]

# Space-optimized: we only need the last two values — not the full table
def fib_optimized(n: int) -> int:
    """
    O(n) time, O(1) space — only track prev and curr.
    """
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(n - 1):
        prev, curr = curr, prev + curr   # slide the window forward
    return curr

# Show all versions agree
print("  n  | naive | memo | tabulation | optimized")
print("  " + "-" * 45)
for n in range(10):
    print(f"  {n:2} |  {fib_naive(n):4} | {fib_memo(n):4} | {fib_tabulation(n):10} | {fib_optimized(n):9}")

# Performance comparison
start = time.perf_counter()
result_naive = fib_naive(30)
naive_time = time.perf_counter() - start

start = time.perf_counter()
fib_memo.cache_clear()   # clear cache so this is a fair cold-start test
result_memo = fib_memo(30)
memo_time = time.perf_counter() - start

print(f"\n  fib(30) = {result_naive}")
print(f"  naive:  {naive_time*1000:.2f}ms")
print(f"  memo:   {memo_time*1000:.4f}ms  ({naive_time/memo_time:.0f}x faster)")


# ── CLIMBING STAIRS ───────────────────────────────────────────
print("\n── climbing stairs ──────────────────────────")

# Problem: n stairs, can climb 1 or 2 steps at a time.
# How many distinct ways to reach the top?
#
# Subproblem: ways(n) = ways(n-1) + ways(n-2)
# Why: last step was either 1 step from stair n-1, or 2 steps from stair n-2.
# This recurrence is IDENTICAL to Fibonacci — same pattern, different story.

@cache
def climb(n: int) -> int:
    """
    Distinct ways to climb n stairs (1 or 2 steps at a time).
    Subproblem: climb(n) = climb(n-1) + climb(n-2)
    Base cases: 1 stair → 1 way, 2 stairs → 2 ways (1+1 or 2)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1   # only way: take 1 step
    if n == 2:
        return 2   # two ways: (1,1) or (2)
    return climb(n-1) + climb(n-2)

for n in range(1, 9):
    print(f"  climb({n}) = {climb(n)} ways")


# ── COIN CHANGE ───────────────────────────────────────────────
print("\n── coin change ──────────────────────────────")

# Problem: given coin denominations and a target amount,
# find the MINIMUM number of coins needed to make the amount.
# If impossible, return -1.
#
# Subproblem: dp[amount] = minimum coins needed to make 'amount'
# Recurrence: dp[a] = 1 + min(dp[a - coin] for each coin if a - coin >= 0)
#
# Build bottom-up: start from dp[0] = 0, fill up to target.

def coin_change(coins: list[int], amount: int) -> int:
    """
    Minimum coins to make 'amount'.
    Time:  O(amount × number_of_coins)
    Space: O(amount)

    dp[a] = minimum coins needed to make exactly a.
    Initialize to infinity (impossible) except dp[0] = 0.
    """
    # Use amount + 1 as a sentinel for "impossible" — we can't need more than
    # amount coins (worst case: all 1-cent coins)
    dp: list[int] = [float("inf")] * (amount + 1)
    dp[0] = 0   # base case: 0 coins needed to make amount 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                # Option: use this coin, then solve for (a - coin)
                dp[a] = min(dp[a], 1 + dp[a - coin])   # 1 coin + best for remainder

    return dp[amount] if dp[amount] != float("inf") else -1

test_cases = [
    ([1, 5, 10, 25], 41),
    ([1, 5, 10, 25], 11),
    ([2], 3),          # impossible
    ([1, 2, 5], 11),
]
for coins, amount in test_cases:
    result = coin_change(coins, amount)
    print(f"  coins={coins}, amount={amount} → {result} coins")


# ── LONGEST COMMON SUBSEQUENCE (LCS) ─────────────────────────
print("\n── longest common subsequence (LCS) ─────────")

# Problem: given two strings, find the length of their longest common subsequence.
# A subsequence preserves order but doesn't need to be contiguous.
# Example: LCS("ABCDE", "ACE") = 3 ("ACE")
#
# Subproblem: dp[i][j] = LCS length for s1[0..i] and s2[0..j]
# Recurrence:
#   if s1[i] == s2[j]: dp[i][j] = dp[i-1][j-1] + 1  (extend LCS by 1)
#   else:              dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (best without current char)

def lcs_length(s1: str, s2: str) -> int:
    """
    Length of the longest common subsequence.
    Time:  O(m × n)
    Space: O(m × n) for the 2D table
    """
    m, n = len(s1), len(s2)

    # dp[i][j] = LCS of s1[:i] and s2[:j]
    # Row/column 0 = empty string → LCS = 0 (base cases handled by initialization)
    # IMPORTANT: [[0]*cols] * rows shares the same list — use a list comprehension!
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:            # characters match — extend LCS
                dp[i][j] = dp[i-1][j-1] + 1
            else:                              # no match — take best of ignoring either char
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

def lcs_string(s1: str, s2: str) -> str:
    """Reconstruct the actual LCS string (not just its length)."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack through the table to reconstruct the sequence
    result: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1])   # this character is in the LCS
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1                    # came from above — skip s1[i]
        else:
            j -= 1                    # came from left — skip s2[j]

    return "".join(reversed(result))   # we built it backwards

lcs_tests = [
    ("ABCDE", "ACE"),
    ("AGGTAB", "GXTXAYB"),
    ("intention", "execution"),
    ("ABCBDAB", "BDCABA"),
]
for a, b in lcs_tests:
    length = lcs_length(a, b)
    seq = lcs_string(a, b)
    print(f"  LCS({a!r}, {b!r}) = {length} → {seq!r}")


# ── 0/1 KNAPSACK ──────────────────────────────────────────────
print("\n── 0/1 knapsack ─────────────────────────────")

# Problem: n items, each with a weight and value. Knapsack has capacity W.
# Maximize total value without exceeding weight limit.
# Each item can be taken at most once (0/1 — either take it or don't).
#
# Subproblem: dp[i][w] = max value using first i items with weight limit w
# Recurrence:
#   Don't take item i: dp[i][w] = dp[i-1][w]
#   Take item i (if it fits): dp[i][w] = values[i] + dp[i-1][w - weights[i]]
#   dp[i][w] = max of the two options

def knapsack_01(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> tuple[int, list[int]]:
    """
    0/1 knapsack — maximize value within weight capacity.
    Time:  O(n × W)
    Space: O(n × W) for the table

    Returns: (max_value, list of item indices taken)
    """
    n = len(weights)

    # dp[i][w] = best value using items 0..i-1 with capacity w
    dp: list[list[int]] = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i-1]
        val = values[i-1]
        for w in range(capacity + 1):
            # Option 1: don't take item i → same as without it
            dp[i][w] = dp[i-1][w]

            # Option 2: take item i (only if it fits)
            if wt <= w:
                with_item = val + dp[i-1][w - wt]
                dp[i][w] = max(dp[i][w], with_item)

    # Backtrack to find which items were taken
    taken: list[int] = []
    w = capacity
    for i in range(n, 0, -1):
        # If dp[i][w] != dp[i-1][w], item i was included
        if dp[i][w] != dp[i-1][w]:
            taken.append(i - 1)      # store 0-based index
            w -= weights[i - 1]      # reduce remaining capacity

    return dp[n][capacity], list(reversed(taken))

# Example items
item_names = ["laptop", "phone", "tablet", "watch", "headphones", "camera"]
item_weights = [3, 1, 2, 1, 1, 2]   # kg
item_values  = [4, 3, 3, 1, 2, 4]   # value units
bag_capacity = 5

max_val, taken_indices = knapsack_01(item_weights, item_values, bag_capacity)

print(f"  Items: {list(zip(item_names, item_weights, item_values))}")
print(f"  (name, weight, value)")
print(f"  Capacity: {bag_capacity}kg")
print(f"\n  Max value: {max_val}")
print(f"  Items taken:")
total_weight = 0
for idx in taken_indices:
    print(f"    {item_names[idx]:12} weight={item_weights[idx]} value={item_values[idx]}")
    total_weight += item_weights[idx]
print(f"  Total weight: {total_weight}/{bag_capacity}kg")


# ── SPACE-OPTIMIZED KNAPSACK ──────────────────────────────────
print("\n── space-optimized knapsack — O(W) space ────")

def knapsack_space_optimized(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    Same as above but uses O(W) space instead of O(n×W).
    We only need the previous row to compute the current row, so
    we maintain a single 1D array and update it in reverse order.

    Reverse order is critical: ensures we don't use the same item twice
    (that would make it the unbounded knapsack problem).
    """
    dp: list[int] = [0] * (capacity + 1)

    for i in range(len(weights)):
        wt, val = weights[i], values[i]
        # Iterate capacity in REVERSE — if we went forward, we'd reuse item i
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], val + dp[w - wt])

    return dp[capacity]

result = knapsack_space_optimized(item_weights, item_values, bag_capacity)
print(f"  Space-optimized max value: {result}  (matches: {result == max_val})")


# ── DP PATTERN SUMMARY ────────────────────────────────────────
print("\n── DP pattern summary ───────────────────────")
print("""
  Template for ANY DP problem:

  1. Define dp[i] (or dp[i][j]):
     → "dp[i] = ..." in plain English

  2. Write the recurrence (how to compute dp[i] from smaller values)

  3. Set base cases (the trivially-known values)

  4. Decide computation order (usually smallest to largest)

  5. Return dp[n] (or dp[m][n] for 2D)

  Memoization first (easier to think about):
    @cache
    def solve(n):
        if base_case: return ...
        return recurrence(solve(n-1), ...)

  Tabulation when needed (no recursion, better for large n):
    dp = [base_values...]
    for i in range(...):
        dp[i] = recurrence(dp[i-1], ...)
    return dp[n]
""")


if __name__ == "__main__":
    pass
