# Lesson 01 — Basics

## What This Covers
Python's primitive types, variables, type hints, f-strings, truthiness, type conversion,
`match/case` for dispatch, and the walrus operator `:=`. This is the foundation everything
else builds on — worth knowing cold.

---

## Key Concepts

### Variables and Type Hints
Python is dynamically typed — you don't *have* to annotate types. But annotating makes
your intent clear, catches bugs early (with tools like `mypy`), and makes code far more
readable.

```python
name: str = "Alec"
age: int = 25
gpa: float = 3.8
is_enrolled: bool = True
nothing: None = None
```

The annotation is just metadata — Python doesn't enforce it at runtime. A type checker
(like mypy or Pyright) does. Think of it as self-documentation that tools can verify.

---

### Primitive Types

| Type | Example | Notes |
|------|---------|-------|
| `int` | `42`, `-7`, `1_000_000` | Arbitrary precision — no overflow |
| `float` | `3.14`, `1.5e10` | IEEE 754 double — watch for `.1 + .2 != .3` |
| `str` | `"hello"`, `'world'` | Immutable, Unicode by default |
| `bool` | `True`, `False` | Subclass of int — `True == 1`, `False == 0` |
| `None` | `None` | Python's null — its own type (`NoneType`) |

---

### f-Strings (the only formatting you need)

```python
name = "Alec"
score = 95.678

# Basic
f"Hello, {name}"                    # → "Hello, Alec"

# Expression inside braces
f"2 + 2 = {2 + 2}"                 # → "2 + 2 = 4"

# Format spec: :.2f = 2 decimal places
f"Score: {score:.2f}"              # → "Score: 95.68"

# Format spec: :>10 = right-align in 10-char field
f"{'right':>10}"                   # → "     right"

# Format spec: :,  = thousands separator
f"{1_000_000:,}"                   # → "1,000,000"

# Debug format: = prints name + value
f"{score=}"                        # → "score=95.678"
```

The `=` format spec is extremely useful for debugging — print the variable name and
value at once without typing both.

---

### Truthiness
Every object in Python has a boolean value. You don't need `== True` or `== False`.

```python
# Falsy values (evaluate to False in a boolean context)
False, None, 0, 0.0, "", [], {}, set()

# Everything else is truthy
```

```python
# Don't write this:
if len(my_list) > 0:

# Write this — it reads like English and is more Pythonic:
if my_list:
```

---

### Type Conversion
```python
int("42")        # → 42   (string to int)
float("3.14")    # → 3.14
str(100)         # → "100"
bool(0)          # → False
bool("hello")    # → True
```

`int()` truncates — it doesn't round. `int(3.9)` → `3`.

---

### match/case (Python 3.10+)
`match/case` is structural pattern matching — more powerful than a switch statement.
It matches on *structure*, not just equality.

```python
command = "quit"

match command:
    case "quit" | "exit":
        print("Goodbye")
    case "help":
        print("Available commands: ...")
    case _:          # _ is the wildcard — matches anything
        print(f"Unknown command: {command}")
```

It also matches on type and structure:
```python
point = (1, 0)

match point:
    case (0, 0):
        print("origin")
    case (x, 0):     # captures x from the tuple
        print(f"on x-axis at {x}")
    case (0, y):
        print(f"on y-axis at {y}")
    case (x, y):
        print(f"at ({x}, {y})")
```

---

### Walrus Operator :=
The walrus operator assigns *and* returns a value in one expression. Useful when you
need a value for a condition and also want to use it in the body.

```python
# Without walrus — redundant call
data = input("Enter something: ")
if data:
    print(f"You said: {data}")

# With walrus — assign and test in one line
if data := input("Enter something: "):
    print(f"You said: {data}")
```

Most useful in `while` loops that read data:
```python
while chunk := file.read(8192):    # read chunk, stop when empty
    process(chunk)
```

Use it when it genuinely reduces repetition. Don't use it just to look clever.

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `x: int = 5` | Variable with type hint |
| `f"{val:.2f}"` | f-string, 2 decimal places |
| `f"{val=}"` | Debug: prints `val=<value>` |
| `int(x)`, `str(x)`, `float(x)` | Type conversion |
| `type(x)` | Returns the type object |
| `isinstance(x, int)` | Check type at runtime |
| `match val: case ...:` | Structural pattern matching |
| `x := expr` | Walrus: assign and return |
| `//` | Floor division (integer result) |
| `**` | Exponentiation |
| `%` | Modulo (remainder) |

---

## Common Pitfalls

- **Float equality**: `0.1 + 0.2 == 0.3` is `False` due to IEEE 754. Use `math.isclose()` for comparisons.
- **`bool` is a subclass of `int`**: `True + True == 2`. Don't use bools in arithmetic unless intentional.
- **`int()` truncates, doesn't round**: `int(2.9)` is `2`. Use `round()` to round.
- **`None` comparisons**: always use `is None` / `is not None`, never `== None`. `==` can be overridden by a class; `is` checks identity.
- **Mutable default arguments**: Never use `def f(x=[]):` — the list is shared across calls. Use `None` and create inside.
- **Walrus in comprehensions**: valid but can look confusing — use sparingly.

---

## When to Use What

- **Type hints**: always, on function signatures and non-obvious variables
- **f-strings**: always for string formatting — never `.format()` or `%`
- **`match/case`**: when you have 3+ cases based on value or structure — cleaner than if/elif chains
- **Walrus `:=`**: in `while` loops that consume data, or `if` conditions where you need the value in the body
- **`is None`**: always, for None checks — never `== None`
