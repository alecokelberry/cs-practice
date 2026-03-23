# Lesson 02 — Loops and Sequences

## What This Covers
Python's loop constructs (`for`, `while`), `range()`, loop control (`break`/`continue`/`else`),
the essential builtins `enumerate()` and `zip()`, list comprehensions (the most idiomatic
Python pattern), generator expressions, and `itertools`. Sequences (lists, tuples, strings)
are covered through slicing and iteration patterns.

---

## Key Concepts

### for Loop
Python's `for` iterates over any *iterable* — lists, strings, ranges, dicts, files, generators.
There's no index arithmetic like C++ `for (int i = 0; i < n; i++)`.

```python
for item in ["a", "b", "c"]:
    print(item)

for char in "hello":    # strings are iterable
    print(char)
```

---

### range()
Three forms:

| Call | Produces |
|------|---------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(2, 8)` | 2, 3, 4, 5, 6, 7 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(10, 0, -1)` | 10, 9, 8, ..., 1 |

`range` is lazy — it doesn't build a list, it generates values on demand.

---

### enumerate() — when you need the index
If you need both the index and the value, use `enumerate()`. Never do `for i in range(len(lst))`.

```python
items = ["apple", "banana", "cherry"]

# Bad:
for i in range(len(items)):
    print(i, items[i])

# Good:
for i, item in enumerate(items):
    print(i, item)

# With custom start index:
for i, item in enumerate(items, start=1):
    print(i, item)   # 1, 2, 3 instead of 0, 1, 2
```

---

### zip() — iterating two sequences in parallel
```python
names = ["Alice", "Bob", "Carol"]
scores = [95, 87, 92]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip stops at the shorter sequence
# Use itertools.zip_longest() if you need to keep going
```

---

### break, continue, else on loops
The `else` clause on a loop runs if the loop *completed without a `break`*. This is
useful for search patterns.

```python
# Search for a target — else means "not found"
target = 7
for n in [1, 3, 5, 9]:
    if n == target:
        print("found!")
        break
else:
    print("not found")   # runs because we never broke
```

---

### List Comprehensions
The most distinctively Pythonic construct. A comprehension builds a new list by expressing
the *transformation* and optional *filter* in one readable line.

```python
# Form: [expression for item in iterable if condition]

squares = [x ** 2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
upper   = [s.upper() for s in ["hello", "world"]]

# Nested (generates pairs — think nested for loops)
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
```

**Rule of thumb**: if the comprehension fits on one line and reads naturally, use it.
If it needs multi-level nesting with complex conditions, use a regular loop.

---

### Generator Expressions
Like a list comprehension, but lazy — it yields values one at a time instead of building
the whole list in memory. Use when you don't need the full list at once.

```python
# List comprehension — builds the whole list immediately
squares_list = [x ** 2 for x in range(1_000_000)]

# Generator expression — computes each value only when needed
squares_gen = (x ** 2 for x in range(1_000_000))   # parentheses, not brackets

# sum(), max(), min(), any(), all() accept generators directly
total = sum(x ** 2 for x in range(1_000_000))   # no intermediate list
```

---

### Slicing
```python
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

lst[2:5]      # [2, 3, 4]          — index 2 up to (not including) 5
lst[:3]       # [0, 1, 2]          — from start to 3
lst[7:]       # [7, 8, 9]          — from 7 to end
lst[-3:]      # [7, 8, 9]          — last 3 elements
lst[::2]      # [0, 2, 4, 6, 8]   — every 2nd element
lst[::-1]     # [9, 8, ..., 0]    — reversed
```

Slicing creates a **new list** (a shallow copy). It doesn't modify the original.

---

### itertools highlights
`itertools` is stdlib — no install needed.

```python
from itertools import islice, chain, product, combinations, permutations

islice(gen, 5)          # take first 5 items from any iterable
chain([1,2], [3,4])     # concatenate iterables lazily
product("AB", repeat=2) # cartesian product: AA, AB, BA, BB
combinations([1,2,3], 2)# (1,2), (1,3), (2,3) — order doesn't matter
permutations([1,2,3], 2)# (1,2), (1,3), (2,1), ... — order matters
```

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `for x in iterable:` | Iterate over any iterable |
| `range(n)` | 0 to n-1 |
| `range(a, b, step)` | a to b-1, by step |
| `enumerate(lst)` | Yields `(index, value)` pairs |
| `enumerate(lst, start=1)` | Same but starts index at 1 |
| `zip(a, b)` | Pairs elements from two iterables |
| `break` | Exit the loop immediately |
| `continue` | Skip to next iteration |
| `for ...: ... else:` | else runs if no break occurred |
| `[expr for x in lst]` | List comprehension |
| `[expr for x in lst if cond]` | Filtered comprehension |
| `(expr for x in lst)` | Generator expression (lazy) |
| `lst[a:b:step]` | Slice |
| `lst[::-1]` | Reverse a sequence |

---

## Common Pitfalls

- **Modifying a list while iterating it** — iterate over a copy (`for x in lst[:]`) or collect changes and apply after.
- **`range(len(lst))`** — almost always wrong. Use `enumerate()` instead.
- **Forgetting `break` resets the `else`** — the `else` only runs if the loop *exhausted* without breaking.
- **List comprehension vs generator** — if you just pass the result to `sum()` or `max()`, use a generator (`()`) not a list (`[]`). No reason to build the full list.
- **Nested comprehensions read left-to-right in the same order as nested for-loops** — `[... for x in a for y in b]` means x is the outer loop, y is the inner.
- **`zip()` silently truncates** — if sequences have different lengths, it stops at the shortest. Use `itertools.zip_longest` if you need all elements.

---

## When to Use What

- **`for x in collection`** — always, for iterating
- **`range(n)`** — when you need a count-based loop or numeric sequence
- **`enumerate()`** — whenever you need both index and value
- **`zip()`** — whenever you need to walk two sequences in lockstep
- **List comprehension** — transforming or filtering a sequence into a new list
- **Generator expression** — when you only need to consume the results once (pass to `sum`, `any`, etc.)
- **`itertools`** — lazy combinations, cartesian products, chunking — reach for it before writing your own loop
