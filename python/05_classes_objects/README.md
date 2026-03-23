# Lesson 05 — Classes and Objects

## What This Covers
Python's class system: `__init__`, instance variables, methods, `self`, `__str__` and
`__repr__`, `@property` and `.setter`, `@staticmethod`, `@classmethod`, and the `@dataclass`
decorator — the modern way to write simple data-holding classes.

---

## Key Concepts

### class and __init__
```python
class Dog:
    def __init__(self, name: str, breed: str, age: int) -> None:
        # Instance variables — belong to each individual object
        self.name = name
        self.breed = breed
        self.age = age

rex = Dog("Rex", "German Shepherd", 4)
```

`self` is the instance. Python passes it automatically — you just need to accept it
as the first parameter in every instance method.

---

### __str__ and __repr__
Both control how objects are displayed, but they serve different audiences.

| Method | When it's called | Audience |
|--------|-----------------|---------|
| `__repr__` | In the REPL, debugging, `repr()` | Developers — should be unambiguous |
| `__str__` | `print()`, `str()`, f-strings | Users — should be readable |

```python
def __repr__(self) -> str:
    return f"Dog(name={self.name!r}, breed={self.breed!r}, age={self.age})"

def __str__(self) -> str:
    return f"{self.name} ({self.breed}, {self.age} years old)"
```

If you only implement one, implement `__repr__`. Python falls back to `__repr__` when
`__str__` is missing.

---

### @property and .setter
`@property` lets you expose a method as if it were an attribute — no parentheses needed
from the caller's side. Use it to add validation or computation without changing the
public API.

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius   # _ prefix = "private by convention"

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2   # computed on access, not stored

c = Circle(5)
c.radius = 10    # calls the setter
print(c.area)    # calls the property getter — looks like an attribute
```

---

### @staticmethod and @classmethod

| Decorator | Receives | Use it when |
|-----------|----------|-------------|
| `@staticmethod` | Nothing extra | Logic related to the class but needing neither `self` nor `cls` |
| `@classmethod` | `cls` (the class) | Alternative constructors, factory methods |

```python
class Temperature:
    @staticmethod
    def celsius_to_fahrenheit(c: float) -> float:
        return c * 9/5 + 32

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        return cls((f - 32) * 5/9)   # cls lets this work in subclasses too
```

---

### @dataclass — the modern way to write data classes
For classes that mainly hold data (POD — plain old data), `@dataclass` auto-generates
`__init__`, `__repr__`, and `__eq__` for you.

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(p)          # Point(x=1.0, y=2.0)  — __repr__ generated
print(p == Point(1.0, 2.0))  # True — __eq__ generated
```

`field()` gives you more control over individual fields:
```python
@dataclass
class Player:
    name: str
    score: int = 0                           # default value
    tags: list[str] = field(default_factory=list)  # mutable default — MUST use field()
    _id: int = field(default=0, repr=False)  # hidden from repr
```

`frozen=True` makes instances immutable (and hashable):
```python
@dataclass(frozen=True)
class Coord:
    lat: float
    lon: float

c = Coord(40.7, -74.0)
# c.lat = 0.0  ← FrozenInstanceError
```

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `class Foo:` | Define a class |
| `def __init__(self, ...):` | Constructor — called on instantiation |
| `self.x = val` | Instance variable |
| `def method(self):` | Instance method |
| `__str__` | Human-readable string — `print()` |
| `__repr__` | Developer-readable string — REPL, debug |
| `@property` | Expose method as attribute (getter) |
| `@prop.setter` | Setter for a property |
| `@staticmethod` | Method with no self/cls |
| `@classmethod` | Method receives class as first arg |
| `@dataclass` | Auto-generate __init__, __repr__, __eq__ |
| `field(default_factory=list)` | Mutable default in dataclass |
| `@dataclass(frozen=True)` | Immutable dataclass |
| `@dataclass(order=True)` | Auto-generate comparison operators |

---

## Common Pitfalls

- **Mutable default arguments in `__init__`**: `def __init__(self, items=[])` shares the list across all instances. Use `None` then `self.items = items or []`, or use `@dataclass` with `field(default_factory=list)`.
- **Forgetting `self`**: every instance method needs `self` as the first parameter. Without it, Python treats it as a positional argument when calling.
- **`__str__` vs `__repr__`**: if you only write one, write `__repr__`. Python uses `__repr__` as the fallback.
- **`@property` vs method**: use `@property` for attributes that are computed but conceptually "a thing the object has" (like `area`). Use a method if there are parameters or side effects.
- **Dataclass mutable defaults**: `tags: list = []` in a dataclass raises a `ValueError`. Always use `field(default_factory=list)`.

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Class that primarily stores data | `@dataclass` |
| Need immutable, hashable instances | `@dataclass(frozen=True)` |
| Computed attribute (no params, no side effects) | `@property` |
| Validation on assignment | `@property` + `.setter` |
| Utility function tied to a class | `@staticmethod` |
| Alternative constructor | `@classmethod` |
| Complex behavior with state | Regular class |
