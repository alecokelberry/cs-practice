# Lesson 13 — Standard Library Modules

## Overview

Python's standard library is enormous. This lesson covers four modules you'll use constantly: `collections` (specialized data structures), `itertools` (covered more in lesson 12 — here: the essentials), `pathlib` (filesystem paths as objects), and `datetime` (dates and times).

---

## `collections` — Specialized Containers

### `namedtuple` — Lightweight Immutable Record

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0])        # 3 — also indexable
x, y = p           # also unpackable
```

For mutable named records, prefer `@dataclass` (see lesson 05). Use `namedtuple` when immutability and tuple-like behavior matter.

### `Counter` — Count Hashable Items

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)                       # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(c["apple"])              # 3
print(c.most_common(2))        # [('apple', 3), ('banana', 2)]

# Counter arithmetic
a = Counter("aab")
b = Counter("abc")
print(a + b)                   # Counter({'a': 3, 'b': 2, 'c': 1})
print(a - b)                   # Counter({'a': 1}) — drops zero/negative
```

### `defaultdict` — Dict with a Default Factory

```python
from collections import defaultdict

# Group words by first letter
by_letter: defaultdict[str, list[str]] = defaultdict(list)
for word in ["apple", "ant", "banana", "bear"]:
    by_letter[word[0]].append(word)
# {'a': ['apple', 'ant'], 'b': ['banana', 'bear']}

# Count without KeyError
counts: defaultdict[str, int] = defaultdict(int)
for char in "mississippi":
    counts[char] += 1
```

### `OrderedDict` — Dict with Insertion-Order Guarantees

Regular `dict` preserves insertion order since Python 3.7. Use `OrderedDict` when you need `move_to_end()` or comparison that considers order:

```python
from collections import OrderedDict

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od.move_to_end("a")           # move "a" to the end
od.move_to_end("b", last=False)  # move "b" to the front
```

### `deque` — Double-Ended Queue

```python
from collections import deque

dq = deque([1, 2, 3], maxlen=5)   # optional max size
dq.appendleft(0)                   # O(1) — unlike list.insert(0, ...)
dq.append(4)
dq.popleft()                       # O(1) — unlike list.pop(0)
dq.rotate(2)                       # rotate right by 2
```

Use `deque` for queues, sliding windows, and anything that needs efficient front-insertion/removal.

---

## `pathlib` — Filesystem Paths as Objects

`pathlib.Path` replaces `os.path` with a clean, object-oriented API.

```python
from pathlib import Path

# Create path objects (no file system access yet)
p = Path(".")
home = Path.home()
config = Path("/etc/hosts")

# Build paths with /
src = Path("project") / "src" / "main.py"
```

### Common Operations

```python
p = Path("data/report.csv")

p.name           # "report.csv"
p.stem           # "report"
p.suffix         # ".csv"
p.parent         # Path("data")
p.resolve()      # absolute path

p.exists()       # True/False
p.is_file()      # True if it's a file
p.is_dir()       # True if it's a directory

# Read/write text files
text = p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")

# Read/write bytes
data = p.read_bytes()
p.write_bytes(b"\x00\x01")

# Create directories
Path("new/dir").mkdir(parents=True, exist_ok=True)

# List directory contents
for child in Path(".").iterdir():
    print(child)

# Glob — find files by pattern
for py_file in Path(".").glob("**/*.py"):
    print(py_file)
```

---

## `datetime` — Dates and Times

```python
from datetime import date, datetime, timedelta, timezone
```

### `date` — Calendar Date

```python
today = date.today()
specific = date(2026, 3, 15)
print(specific.year, specific.month, specific.day)
print(specific.strftime("%B %d, %Y"))   # "March 15, 2026"
```

### `datetime` — Date + Time

```python
now = datetime.now()                     # local time
now_utc = datetime.now(tz=timezone.utc) # UTC (timezone-aware)

dt = datetime(2026, 3, 15, 14, 30, 0)
print(dt.strftime("%Y-%m-%d %H:%M:%S")) # "2026-03-15 14:30:00"

# Parse a string back to datetime
parsed = datetime.strptime("2026-03-15", "%Y-%m-%d")
```

### `timedelta` — Duration Arithmetic

```python
tomorrow   = date.today() + timedelta(days=1)
next_week  = datetime.now() + timedelta(weeks=1)
two_hours  = timedelta(hours=2)

# Difference between two datetimes → timedelta
delta = datetime(2026, 12, 31) - datetime.now()
print(f"{delta.days} days until year end")
```

### Common `strftime` Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2026 |
| `%m` | Zero-padded month | 03 |
| `%d` | Zero-padded day | 15 |
| `%H` | 24-hour hour | 14 |
| `%M` | Minute | 30 |
| `%S` | Second | 00 |
| `%B` | Full month name | March |
| `%A` | Full weekday name | Sunday |
| `%Z` | Timezone name | UTC |

---

## `functools` — Higher-Order Function Utilities

```python
from functools import cache, lru_cache, partial, reduce

# cache — unlimited memoization
@cache
def fib(n: int) -> int:
    return n if n <= 1 else fib(n-1) + fib(n-2)

# partial — fix some arguments of a function
from functools import partial
double = partial(pow, exp=2)   # fixes exp=2

# reduce — fold a sequence into a single value
from functools import reduce
product = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])  # 120
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `os.path.join(a, b)` for paths | Use `Path(a) / b` instead |
| `datetime.now()` for UTC | Use `datetime.now(tz=timezone.utc)` — naive datetimes have no timezone info |
| Comparing naive and aware datetimes | Python raises `TypeError` — be consistent: always use aware or always naive |
| `Counter("abc") - Counter("abc")` | Result is empty — subtraction drops zero/negative counts |
| Using `list` where `deque` fits | `list.insert(0, x)` is O(n); `deque.appendleft(x)` is O(1) |

---

## Quick Reference Card

```python
from collections import namedtuple, Counter, defaultdict, OrderedDict, deque
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from functools import cache, partial, reduce

# namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2); p.x; p.y

# Counter
c = Counter(iterable); c.most_common(n)

# defaultdict
d = defaultdict(list); d["key"].append(val)

# deque
dq = deque(maxlen=10); dq.appendleft(x); dq.popleft()

# pathlib
p = Path("dir") / "file.txt"
p.read_text(); p.write_text("..."); p.exists(); p.glob("*.py")

# datetime
datetime.now(tz=timezone.utc)
dt.strftime("%Y-%m-%d"); datetime.strptime(s, fmt)
timedelta(days=7)

# functools
@cache
def fn(n): ...
partial(fn, fixed_arg=val)
reduce(lambda a, b: a + b, seq)
```
