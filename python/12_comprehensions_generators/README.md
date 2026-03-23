# Lesson 12 — Comprehensions & Generators (Deep Dive)

## Overview

Comprehensions and generators are Python's core idioms for building and processing sequences. This lesson goes beyond the basics: nested comprehensions, walrus operator in comprehensions, generator pipelines, advanced `itertools`, and when to choose each tool.

---

## List Comprehensions

```python
# Basic form: [expression for item in iterable if condition]
squares     = [x ** 2 for x in range(10)]
evens       = [x for x in range(20) if x % 2 == 0]
upper_long  = [w.upper() for w in words if len(w) > 4]
```

### Nested Comprehensions

Outer loop first — same order as the equivalent `for` loops written out:

```python
# Flatten a 2D list
flat = [n for row in matrix for n in row]

# All pairs where a != b
pairs = [(a, b) for a in [1, 2, 3] for b in [1, 2, 3] if a != b]
```

### Walrus Operator in Comprehensions

Compute a value once and use it in both the filter and the expression:

```python
# Without walrus — compute expensive(x) twice
results = [expensive(x) for x in data if expensive(x) > 0]

# With walrus — compute once, reuse the result
results = [v for x in data if (v := expensive(x)) > 0]
```

---

## Dict and Set Comprehensions

```python
# Dict comprehension
word_lengths = {word: len(word) for word in words}

# Invert a dict (assumes unique values)
inverted = {v: k for k, v in original.items()}

# Conditional dict comprehension
passing = {name: score for name, score in grades.items() if score >= 60}

# Set comprehension — unique values only
unique_mods = {x % 5 for x in range(100)}
```

---

## Generator Expressions

Like a list comprehension but **lazy** — produces values one at a time without allocating a list:

```python
# Efficient: no intermediate list in memory
total  = sum(x ** 2 for x in range(1_000_000))
exists = any(x > 100 for x in data)
first  = next(x for x in data if x > 0)  # get first match
```

| | List comp | Generator expr |
|--|-----------|----------------|
| Syntax | `[x for x in ...]` | `(x for x in ...)` |
| Returns | `list` | generator object |
| Memory | All values at once | One at a time |
| Reusable | Yes | No — single-pass |
| Use when | You need random access or multiple passes | Streaming, large data, sum/any/all/next |

---

## Generator Functions

A function with `yield` pauses at each yield and resumes on the next `next()` call:

```python
def integers_from(start: int):
    """Infinite generator — yields integers forever."""
    n = start
    while True:
        yield n
        n += 1

def take(n: int, it):
    """Take first n items from any iterable."""
    for _, val in zip(range(n), it):
        yield val

list(take(5, integers_from(10)))   # [10, 11, 12, 13, 14]
```

### `yield from` — Delegating to Sub-iterables

```python
def flatten(nested):
    for sub in nested:
        yield from sub   # equivalent to: for item in sub: yield item

def chain_files(paths):
    for path in paths:
        yield from open(path)   # yield lines from each file
```

### Generator Pipelines

Chain generators for memory-efficient data processing:

```python
def read_lines(path):
    with open(path) as f:
        yield from f

def strip_lines(lines):
    for line in lines:
        yield line.strip()

def non_empty(lines):
    for line in lines:
        if line:
            yield line

# Pipeline: each stage processes one line at a time
pipeline = non_empty(strip_lines(read_lines("data.txt")))
for line in pipeline:
    process(line)
```

---

## Advanced `itertools`

```python
import itertools

# accumulate — running total (or any binary op)
list(itertools.accumulate([1, 2, 3, 4]))         # [1, 3, 6, 10]
list(itertools.accumulate([1,2,3,4], lambda a,b: a*b))  # [1,2,6,24]

# groupby — consecutive groups with the same key
data = [("a", 1), ("a", 2), ("b", 3), ("c", 4), ("c", 5)]
for key, group in itertools.groupby(data, key=lambda t: t[0]):
    print(key, list(group))
# Note: groupby only groups CONSECUTIVE equal keys — sort first if needed

# starmap — like map but unpacks each item as args
pairs = [(2, 3), (4, 2), (1, 5)]
list(itertools.starmap(pow, pairs))              # [8, 16, 1]

# takewhile / dropwhile
list(itertools.takewhile(lambda x: x < 5, [1,2,3,5,4]))  # [1,2,3]
list(itertools.dropwhile(lambda x: x < 5, [1,2,3,5,4]))  # [5,4]

# pairwise (Python 3.10+) — overlapping pairs
list(itertools.pairwise([1, 2, 3, 4]))           # [(1,2),(2,3),(3,4)]

# batched (Python 3.12+) — non-overlapping chunks
list(itertools.batched([1,2,3,4,5], 2))          # [(1,2),(3,4),(5,)]

# cycle — repeat an iterable forever
counter = itertools.cycle(["on", "off"])
[next(counter) for _ in range(5)]               # ['on','off','on','off','on']

# repeat — repeat a value N times (or forever)
list(itertools.repeat(0, 4))                     # [0, 0, 0, 0]
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Reusing an exhausted generator | Generators are single-pass — create a new one or convert to `list` |
| Nested comprehension order confusion | Write the equivalent `for` loops first, then collapse: outer loop comes first |
| Over-complex comprehension | If it needs a nested `if` + nested loop + transform, use a regular loop |
| `groupby` on unsorted data | Groups only consecutive equal keys — `sort()` by key before `groupby()` |
| `[x for x in gen]` on huge data | Defeats the purpose — use `sum()`, `any()`, or stream directly |
| Walrus in comprehensions (scope) | The walrus-created variable leaks into the enclosing scope — name it clearly |

---

## Quick Reference Card

```python
# Comprehensions
[expr for x in it if cond]                 # list
{k: v for k, v in pairs}                   # dict
{expr for x in it}                         # set
(expr for x in it)                         # generator

# Walrus in comprehension
[v for x in data if (v := f(x)) > 0]

# Generator function
def gen():
    yield value

# yield from
def flat(nested):
    for sub in nested:
        yield from sub

# Key itertools
itertools.accumulate(it, func)
itertools.groupby(it, key=fn)      # sort first!
itertools.starmap(fn, pairs)
itertools.takewhile(pred, it)
itertools.dropwhile(pred, it)
itertools.pairwise(it)             # 3.10+
itertools.batched(it, n)           # 3.12+
itertools.cycle(it)
itertools.repeat(val, n)
```
