# Lesson 08 — Algorithms

## What This Covers
Linear search, binary search (iterative + recursive), bubble sort (for understanding),
Python's built-in `sorted()` (Timsort), merge sort, recursion and the call stack,
the two-pointer technique, the sliding window technique, and Big-O notation explained
in plain terms.

---

## Key Concepts

### Big-O Notation — what it means
Big-O describes how an algorithm's runtime scales with input size n.
It ignores constants and lower-order terms — it's about the *shape* of the growth curve.

| Notation | Name | Example | n=1000 |
|----------|------|---------|--------|
| O(1) | Constant | Dict lookup, list append | Same always |
| O(log n) | Logarithmic | Binary search | ~10 steps |
| O(n) | Linear | Linear search, for loop | 1,000 steps |
| O(n log n) | Log-linear | Merge sort, Timsort | ~10,000 steps |
| O(n²) | Quadratic | Bubble sort, nested loops | 1,000,000 steps |
| O(2ⁿ) | Exponential | Naive fibonacci | 2^1000 ≈ ∞ |

The practical rule: if n can be 10,000+, you need O(n log n) or better.

---

### Linear Search — O(n)
Check every element until found. Works on any sequence, unsorted or sorted.

```python
def linear_search(lst: list[int], target: int) -> int:
    for i, val in enumerate(lst):
        if val == target:
            return i
    return -1
```

Use when: the list is small, or unsorted and you can't sort it first.

---

### Binary Search — O(log n)
Works only on **sorted** sequences. Repeatedly halves the search space.

```python
def binary_search(lst: list[int], target: int) -> int:
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2       # avoid overflow — Python ints don't overflow but habit
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            lo = mid + 1           # target is in the right half
        else:
            hi = mid - 1           # target is in the left half
    return -1
```

With n=1,000,000: binary search takes ~20 comparisons. Linear search takes up to 1,000,000.

Python's stdlib has `bisect` — use that in production instead of implementing your own.

---

### Bubble Sort — O(n²)
Repeatedly compare adjacent elements and swap if out of order. Easy to understand,
terrible in practice. Teach it to understand the concept of "comparison sorts."

```python
def bubble_sort(lst: list[int]) -> list[int]:
    arr = lst[:]   # sort a copy — don't modify input
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):   # already sorted part shrinks each pass
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]   # Pythonic swap
    return arr
```

---

### Python's sorted() — O(n log n) Timsort
Don't implement sorting in production — `sorted()` uses Timsort, which is faster than
nearly anything you'd write, and handles edge cases correctly.

```python
sorted([3, 1, 4, 1, 5], reverse=True)       # [5, 4, 3, 1, 1]
sorted(words, key=str.lower)                 # case-insensitive
sorted(people, key=lambda p: p.age)          # sort by attribute
sorted(people, key=lambda p: (-p.score, p.name))  # multi-key sort
```

The `key` parameter is extremely powerful — learn it well.

---

### Merge Sort — O(n log n)
Divide and conquer: split the list in half, sort each half recursively, then merge.
Good for understanding recursion and the O(n log n) lower bound for comparison sorts.

```
[5, 3, 1, 4, 2]
→ [5, 3] [1, 4, 2]
→ [5] [3] [1] [4, 2]
→ [5] [3] [1] [4] [2]
← [3, 5] [1] [2, 4]
← [1, 3, 5] [2, 4]
← [1, 2, 3, 4, 5]
```

---

### Two-Pointer Technique
Use two indices that move toward each other (or in the same direction) to solve problems
in O(n) that would naively be O(n²).

Classic problem: find two numbers in a sorted array that sum to a target.
```python
def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return lo, hi
        elif s < target:
            lo += 1   # sum too small — move left pointer right
        else:
            hi -= 1   # sum too large — move right pointer left
    return None
```

---

### Sliding Window Technique
Maintain a "window" of elements as you scan the array. Expand/contract the window instead
of recomputing from scratch each time.

Classic: maximum sum of any k consecutive elements.
```python
def max_subarray_sum(arr: list[int], k: int) -> int:
    window_sum = sum(arr[:k])   # compute first window
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]   # slide: add new, remove old
        max_sum = max(max_sum, window_sum)
    return max_sum
```

---

## Syntax Quick Reference

| Pattern | What it does |
|---------|-------------|
| `import bisect; bisect.bisect_left(lst, x)` | Binary search (stdlib) |
| `sorted(lst, key=fn)` | Sort with a key function |
| `sorted(lst, reverse=True)` | Sort descending |
| `lst.sort()` | Sort in place (returns None) |
| `lo, hi = 0, len(lst)-1` | Two-pointer setup |
| `mid = (lo + hi) // 2` | Binary search midpoint |
| `a, b = b, a` | Pythonic swap — no temp variable |

---

## Common Pitfalls

- **Using linear search on a sorted list** — if it's sorted, binary search is orders of magnitude faster.
- **Binary search on an unsorted list** — wrong answers, silently. Sort first.
- **`list.sort()` vs `sorted()`** — `sort()` mutates in place and returns `None`. `sorted()` returns a new list. Assigning the result of `.sort()` to a variable is a common bug.
- **Implementing sorting yourself** — use `sorted()`. Timsort is faster and well-tested.
- **Off-by-one in binary search** — use `lo <= hi` (not `<`) and `mid = (lo + hi) // 2`.
- **Recursion without a base case** — infinite recursion → `RecursionError`. Always define the base case first.
- **Python's recursion limit** — default 1000. Deep recursion (like naive recursive fibonacci) hits this quickly. Use memoization or iteration.

---

## When to Use What

| Situation | Algorithm |
|-----------|-----------|
| Unsorted list, find one item | Linear search O(n) |
| Sorted list, find one item | Binary search O(log n) |
| Sort any data | `sorted()` / `.sort()` O(n log n) |
| Understanding sort internals | Merge sort |
| Two elements summing to target (sorted) | Two-pointer |
| Max/min subarray of size k | Sliding window |
| Tree/graph traversal | Recursion (with memoization or iterative) |
