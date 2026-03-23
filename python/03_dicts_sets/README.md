# Lesson 03 — Dicts and Sets

## What This Covers
Python's `dict` and `set` types, the essential `collections` helpers (`defaultdict`, `Counter`),
dict merging, set algebra, and `frozenset`. These data structures handle the vast majority of
real-world data-mapping and deduplication tasks.

---

## Key Concepts

### dict — the core mapping type
Dicts store key-value pairs. Keys must be *hashable* (immutable: strings, ints, tuples).
Values can be anything.

```python
person: dict[str, str | int] = {
    "name": "Alec",
    "age": 25,
    "city": "Denver",
}

# Access
person["name"]          # "Alec" — KeyError if missing
person.get("email")     # None   — safe, no exception
person.get("email", "no email")   # custom default
```

Always prefer `.get()` over direct access when a key might not exist.

---

### Dict Methods
```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()    # dict_keys(['a', 'b', 'c'])
d.values()  # dict_values([1, 2, 3])
d.items()   # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Most common pattern: iterate key-value pairs
for key, value in d.items():
    print(key, value)

d.pop("a")              # removes and returns value — KeyError if missing
d.pop("z", None)        # safe pop with default
d.setdefault("x", 0)    # insert key with default ONLY if key doesn't exist
d.update({"d": 4})      # merge another dict in (modifies in place)
```

---

### Dict Comprehensions
```python
# {key: value for item in iterable}
squares = {n: n ** 2 for n in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invert a dict (swap keys and values)
inverted = {v: k for k, v in squares.items()}

# Filter a dict
big_squares = {k: v for k, v in squares.items() if v > 9}
```

---

### Merging Dicts (Python 3.9+)
```python
defaults = {"theme": "dark", "lang": "en", "size": 12}
user_prefs = {"theme": "light", "size": 14}

# | creates a new merged dict — right side wins on conflicts
merged = defaults | user_prefs
# {"theme": "light", "lang": "en", "size": 14}

# |= updates in place
defaults |= user_prefs
```

---

### collections.defaultdict
A dict that auto-creates a default value for missing keys. No more checking "does this
key exist before appending to the list?"

```python
from collections import defaultdict

# Old way — verbose
groups = {}
for word in words:
    if word[0] not in groups:
        groups[word[0]] = []
    groups[word[0]].append(word)

# New way — defaultdict handles the missing-key case
groups = defaultdict(list)   # default factory is list()
for word in words:
    groups[word[0]].append(word)   # auto-creates [] if key missing
```

Common factories: `list`, `int` (default 0), `set`, `dict`.

---

### collections.Counter
Purpose-built for counting. Takes any iterable and counts occurrences.

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'cherry': 1})

c.most_common(2)   # [('apple', 3), ('banana', 2)]
c["apple"]         # 3
c["missing"]       # 0  — no KeyError (acts like defaultdict(int))

# Counters support arithmetic
c1 = Counter(a=3, b=2)
c2 = Counter(a=1, b=4)
c1 + c2   # Counter({'b': 6, 'a': 4})
c1 - c2   # Counter({'a': 2})  — only keeps positives
```

---

### set — unordered, deduplicated collection
Sets contain unique hashable elements. No duplicates, no guaranteed order.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b    # union: {1, 2, 3, 4, 5, 6}
a & b    # intersection: {3, 4}
a - b    # difference: {1, 2}  (in a, not in b)
a ^ b    # symmetric difference: {1, 2, 5, 6}  (in one but not both)

# Test membership — O(1) average (much faster than list)
3 in a      # True
7 not in a  # True
```

---

### frozenset — immutable set
A `frozenset` is a set you can't modify — and therefore it's hashable, meaning you can use
it as a dict key or store it inside another set.

```python
fs = frozenset([1, 2, 3])
# Same operations as set (union, intersection, etc.) but no add/remove
# Can be used as a dict key — regular set cannot
cache = {frozenset([1, 2]): "result"}
```

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `d[key]` | Access by key — KeyError if missing |
| `d.get(key)` | Access by key — returns None if missing |
| `d.get(key, default)` | Access with custom default |
| `d.setdefault(key, val)` | Insert default only if key absent |
| `key in d` | Membership test (checks keys) — O(1) |
| `d.items()` | Iterable of `(key, value)` tuples |
| `d.keys()` | Iterable of keys |
| `d.values()` | Iterable of values |
| `d.pop(key)` | Remove and return value |
| `d1 \| d2` | Merge dicts — right wins conflicts |
| `d1 \|= d2` | Merge in place |
| `{k: v for ...}` | Dict comprehension |
| `defaultdict(list)` | Dict with auto-created defaults |
| `Counter(iterable)` | Count occurrences |
| `c.most_common(n)` | Top n most frequent items |
| `{1, 2, 3}` | Set literal |
| `set()` | Empty set (not `{}` — that's a dict!) |
| `a \| b` | Set union |
| `a & b` | Set intersection |
| `a - b` | Set difference |
| `a ^ b` | Symmetric difference |
| `frozenset(iterable)` | Immutable set |

---

## Common Pitfalls

- **Empty set**: `{}` creates an empty *dict*, not a set. Use `set()` for an empty set.
- **Mutable values in dicts**: `d["key"].append(x)` works, but make sure the key exists first. Use `defaultdict` to avoid the check.
- **Dict ordering**: Python 3.7+ dicts maintain insertion order. Don't rely on it for sorted access — use `sorted(d.items())`.
- **Counter missing keys return 0**: unlike a regular dict, `Counter["missing"]` is 0, not a KeyError. This is intentional.
- **Sets are unordered**: `{3, 1, 2}` and `{1, 2, 3}` are equal. Don't depend on set order.
- **Iterating and modifying a dict**: causes RuntimeError. Copy first: `for k in list(d.keys()):`.

---

## When to Use What

| Need | Use |
|------|-----|
| Key → value mapping | `dict` |
| Default value for missing keys | `defaultdict` |
| Count occurrences | `Counter` |
| Unique membership, fast lookup | `set` |
| Set as a dict key | `frozenset` |
| Ordered dict (insertion order) | Regular `dict` (3.7+) |
| Sorted key iteration | `sorted(d.items())` |
