# Lesson 14 — File I/O & Context Managers

## Overview

Reading and writing files is a daily task. Python makes it clean with `open()`, `pathlib`, and context managers. Context managers (`with` statements) ensure resources are always released — even when exceptions occur.

---

## Opening Files with `open()`

```python
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
f.close()   # must close manually — easy to forget
```

**Always use `with`** — it closes the file automatically:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
# file is closed here, even if an exception was raised
```

### File Modes

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default) — fails if file doesn't exist |
| `"w"` | Write — creates file, truncates if it exists |
| `"a"` | Append — creates file, adds to end if it exists |
| `"x"` | Exclusive create — fails if file already exists |
| `"r+"` | Read and write |
| `"rb"`, `"wb"` | Binary read/write (images, PDFs, etc.) |

Always specify `encoding="utf-8"` for text files. Omitting it uses the platform default, which differs between Windows and macOS/Linux.

---

## Reading Files

```python
# Read entire file as a string
with open("data.txt", encoding="utf-8") as f:
    text = f.read()

# Read all lines into a list
with open("data.txt", encoding="utf-8") as f:
    lines = f.readlines()          # includes \n at end of each line

# Iterate line by line — memory-efficient for large files
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        process(line.rstrip("\n"))
```

---

## Writing Files

```python
# Write a string — overwrites the file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, file!\n")
    f.write("Second line.\n")

# Write multiple lines at once
lines = ["line 1\n", "line 2\n", "line 3\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Append without overwriting
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

---

## `pathlib` for File I/O

`pathlib.Path` provides shorthand methods that handle `open()` internally:

```python
from pathlib import Path

p = Path("data.txt")
text = p.read_text(encoding="utf-8")    # read entire file
p.write_text("new content\n", encoding="utf-8")  # overwrite

data = p.read_bytes()   # binary read
p.write_bytes(b"\x00\xFF")
```

For simple reads/writes, `pathlib` is cleaner. Use `open()` when you need to stream or append.

---

## JSON and CSV

### JSON

```python
import json

# Write
data = {"name": "Alice", "scores": [95, 88, 72]}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Read
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)

# String ↔ dict (no file)
s = json.dumps(data)
obj = json.loads(s)
```

### CSV

```python
import csv

# Write
rows = [["Alice", 95], ["Bob", 88]]
with open("grades.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "score"])   # header
    writer.writerows(rows)

# Read as dicts (header row becomes keys)
with open("grades.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["score"])
```

---

## How Context Managers Work

The `with` statement calls two special methods:
- `__enter__` — runs on entry, returns the resource (bound to `as` target)
- `__exit__` — runs on exit, even if an exception occurred

```python
class ManagedResource:
    def __enter__(self):
        print("acquiring resource")
        return self       # value bound to `as`

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("releasing resource")
        return False      # False = don't suppress exceptions

with ManagedResource() as r:
    print("using resource")
# "releasing resource" always prints, even if an exception happened
```

---

## `contextlib.contextmanager` — Generator-Based Context Manager

Instead of writing a class, use a generator function:

```python
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield    # code inside `with` runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")

with timer("my task"):
    sum(range(1_000_000))
```

The `try/finally` ensures cleanup even if the `with` block raises.

### `contextlib.suppress` — Ignore Specific Exceptions

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    Path("missing.txt").unlink()   # no error if file doesn't exist
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `open()` without `with` | The file may never close if an exception occurs |
| Missing `encoding="utf-8"` | Platform default differs — always specify encoding |
| `"w"` mode on existing file | It silently truncates the file — use `"x"` if you want it to fail instead |
| `f.readlines()` on a huge file | Loads everything into memory — iterate `for line in f` instead |
| `csv.writer` without `newline=""` | Extra blank lines on Windows — always pass `newline=""` |
| `__exit__` returning `True` | Suppresses all exceptions — only do this intentionally |

---

## Quick Reference Card

```python
# Basic file I/O
with open("file.txt", "r", encoding="utf-8") as f:
    text = f.read()                  # whole file
    lines = f.readlines()            # list of lines
    for line in f: ...               # stream line by line

with open("file.txt", "w", encoding="utf-8") as f:
    f.write("content\n")

# pathlib shortcuts
from pathlib import Path
Path("f.txt").read_text(encoding="utf-8")
Path("f.txt").write_text("...", encoding="utf-8")

# JSON
import json
json.dump(obj, f, indent=2)
json.load(f)
json.dumps(obj) / json.loads(s)

# CSV
import csv
csv.writer(f).writerows(rows)
csv.DictReader(f)  # rows as dicts

# Custom context manager
from contextlib import contextmanager

@contextmanager
def managed():
    # setup
    try:
        yield resource
    finally:
        # teardown (always runs)
        ...

# Suppress specific exceptions
from contextlib import suppress
with suppress(FileNotFoundError): ...
```
