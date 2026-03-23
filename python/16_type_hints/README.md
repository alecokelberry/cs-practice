# Lesson 16 — Type Hints

## Overview

Type hints let you annotate what types a function expects and returns. Python doesn't enforce them at runtime — but tools like `mypy` and your IDE use them to catch bugs before you run the code. Think of them as documentation that machines can check.

---

## Basic Annotations

```python
# Variables
name: str = "Alice"
age: int = 30
pi: float = 3.14
active: bool = True

# Function parameters and return type
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

# No return value
def log(msg: str) -> None:
    print(msg)
```

---

## Built-in Generic Types (Python 3.9+)

Use the built-in types directly as generics — no imports needed:

```python
def first(items: list[int]) -> int:
    return items[0]

def merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {**a, **b}

def coords() -> tuple[float, float]:
    return (1.0, 2.0)

def unique(items: list[str]) -> set[str]:
    return set(items)
```

Before Python 3.9, you needed `from typing import List, Dict, Tuple, Set` — avoid these in new code.

---

## Optional and Union (Python 3.10+)

```python
# A value that might be None
def find_user(user_id: int) -> str | None:
    ...

# Multiple possible types
def stringify(value: int | float | str) -> str:
    return str(value)

# Before Python 3.10: Optional[str] means str | None
from typing import Optional
def legacy(name: Optional[str]) -> str:  # same as str | None
    return name or "anonymous"
```

---

## `Any` — Opt Out of Type Checking

```python
from typing import Any

def log_anything(value: Any) -> None:
    print(value)   # no type errors possible — Any matches everything
```

Use sparingly. `Any` disables type checking for that variable/param.

---

## `Callable` — Type Hints for Functions

```python
from typing import Callable

def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    return fn(a, b)

# Callable[[arg_types...], return_type]
Transformer = Callable[[str], str]

def process(text: str, transform: Transformer) -> str:
    return transform(text)
```

---

## `TypeVar` — Generic Functions

Use `TypeVar` when you want a function to work with any type while preserving the relationship between input and output types:

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

# first([1, 2, 3]) → int
# first(["a", "b"]) → str
# The return type matches the list element type
```

---

## `TypedDict` — Dict with Known Keys

```python
from typing import TypedDict

class Movie(TypedDict):
    title: str
    year: int
    rating: float

def display(movie: Movie) -> str:
    return f"{movie['title']} ({movie['year']}) — {movie['rating']}"

m: Movie = {"title": "Dune", "year": 2021, "rating": 8.0}
```

Use `TypedDict` instead of bare `dict[str, Any]` when you know the exact keys.

---

## `Protocol` — Structural Typing (Duck Typing)

A `Protocol` defines what methods/attributes a type must have — without requiring inheritance:

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("drawing circle")

class Square:
    def draw(self) -> None:
        print("drawing square")

def render(shape: Drawable) -> None:
    shape.draw()   # works for anything with a .draw() method

render(Circle())   # ✓ — no explicit inheritance needed
render(Square())   # ✓
```

---

## `dataclass` with Type Hints

`@dataclass` uses type hints to generate `__init__`, `__repr__`, and `__eq__`:

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Student:
    name: str
    scores: list[int] = field(default_factory=list)
    gpa: float = 0.0
```

---

## `overload` — Multiple Signatures

```python
from typing import overload

@overload
def process(val: int) -> int: ...
@overload
def process(val: str) -> str: ...

def process(val: int | str) -> int | str:
    if isinstance(val, int):
        return val * 2
    return val.upper()
```

---

## Running `mypy`

```bash
pip install mypy
mypy main.py              # check one file
mypy .                    # check all files
mypy --strict main.py     # strictest checks
```

Common mypy errors:

| Error | Meaning |
|-------|---------|
| `Argument 1 to "foo" has incompatible type "str"; expected "int"` | Wrong type passed |
| `Item "None" of "X \| None" has no attribute "y"` | Need a None check |
| `Return type expected "int" but got "str"` | Return type mismatch |
| `Missing return statement` | Not all paths return a value |

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `list[int]` on Python 3.8 | Use `from __future__ import annotations` to enable it, or `typing.List[int]` |
| Mutable default: `def f(items: list = [])` | Use `None` and set inside the function; or `field(default_factory=list)` in dataclass |
| `Optional[str]` confusion | It's just `str \| None` — always check for `None` before using the value |
| Annotating but not checking | Run `mypy` — annotations do nothing at runtime on their own |
| `Any` everywhere | Defeats the purpose; use it only at true system boundaries |

---

## Quick Reference Card

```python
# Basics
name: str
items: list[int]
mapping: dict[str, float]
pair: tuple[int, str]
options: set[str]

# Optional / Union (3.10+)
value: str | None
result: int | float | str

# Callable
fn: Callable[[int, int], int]

# TypeVar — generic functions
T = TypeVar("T")
def identity(x: T) -> T: ...

# TypedDict
class Config(TypedDict):
    host: str
    port: int

# Protocol (structural duck typing)
class HasDraw(Protocol):
    def draw(self) -> None: ...

# dataclass
@dataclass
class Point:
    x: float
    y: float

# Run mypy
# mypy --strict main.py
```
