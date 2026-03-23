# Lesson 06 — OOP (Inheritance, Protocols, Dunders)

## What This Covers
Inheritance, `super()`, method overriding, `isinstance`/`issubclass`, abstract base
classes (`ABC` + `@abstractmethod`), polymorphism, mixins, `Protocol` for structural
subtyping (duck typing), and the key dunder methods that make Python objects feel native.

---

## Key Concepts

### Inheritance and super()
A subclass inherits all methods and attributes of its parent. `super()` delegates to
the parent class — always call it in `__init__` to ensure proper initialization.

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)   # run Animal.__init__ first
        self.breed = breed

    def speak(self) -> str:     # override the parent method
        return f"{self.name} says: Woof!"
```

---

### isinstance and issubclass
```python
d = Dog("Rex", "Shepherd")

isinstance(d, Dog)      # True  — is it a Dog?
isinstance(d, Animal)   # True  — is it an Animal? (yes — Dog inherits Animal)
isinstance(d, str)      # False

issubclass(Dog, Animal)  # True — is Dog a subclass of Animal?
```

`isinstance` respects the inheritance hierarchy. This is why you can write a function
that accepts `Animal` and pass any subclass to it.

---

### Abstract Base Classes (ABC)
`ABC` lets you define an interface — methods that subclasses *must* implement.
If a subclass doesn't implement every `@abstractmethod`, it can't be instantiated.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Subclasses must implement this."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:   # concrete method — shared by all subclasses
        return f"Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f}"

# Shape()  ← TypeError: can't instantiate abstract class
```

Use ABCs when you're designing a family of related classes that share a contract.

---

### Polymorphism
Polymorphism means different objects respond to the same method call differently.
Python's duck typing makes this natural — you don't need an inheritance relationship
to achieve it.

```python
shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
for shape in shapes:
    print(shape.describe())  # calls the right area/perimeter for each type
```

---

### Mixins
A mixin is a class that provides methods to be mixed into another class. It's not meant
to be instantiated on its own. Mixins are how Python achieves "multiple inheritance
done right" — each mixin has a single, narrow responsibility.

```python
class JsonMixin:
    """Adds JSON serialization to any class."""
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    """Adds logging to any class."""
    def log(self, msg: str) -> None:
        print(f"[{self.__class__.__name__}] {msg}")

class Player(JsonMixin, LogMixin):
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

p = Player("Alice", 100)
p.log("started game")
print(p.to_json())
```

Order matters in multiple inheritance — Python uses the MRO (Method Resolution Order,
C3 linearization). Put mixins before the base class.

---

### Protocol — structural subtyping (duck typing)
`Protocol` defines an interface by *structure*, not inheritance. If an object has the
right methods, it satisfies the Protocol — no `isinstance` check, no inheritance needed.

This is "duck typing" made formal and checkable by type checkers.

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Circle:
    def draw(self) -> str:
        return "○"

class Square:
    def draw(self) -> str:
        return "□"

def render(shape: Drawable) -> None:
    print(shape.draw())

# Circle and Square don't inherit Drawable — but they satisfy it structurally
render(Circle())   # works
render(Square())   # works
```

Use `Protocol` when you want type safety without forcing subclassing.

---

### Key Dunder Methods

| Method | Called when | Example |
|--------|-------------|---------|
| `__len__` | `len(obj)` | Container size |
| `__getitem__` | `obj[key]` | Indexing/subscript |
| `__setitem__` | `obj[key] = val` | Index assignment |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj:` | Iteration |
| `__next__` | `next(obj)` | Iterator protocol |
| `__add__` | `a + b` | Addition operator |
| `__eq__` | `a == b` | Equality |
| `__lt__` | `a < b` | Less than |
| `__hash__` | `hash(obj)`, dict/set key | Hash value |
| `__call__` | `obj()` | Call like a function |
| `__enter__` / `__exit__` | `with obj:` | Context manager |

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `class Sub(Base):` | Inherit from Base |
| `super().__init__(...)` | Call parent's __init__ |
| `super().method()` | Call parent's method |
| `isinstance(obj, Cls)` | Check type (respects inheritance) |
| `issubclass(Sub, Base)` | Check class hierarchy |
| `from abc import ABC, abstractmethod` | Import ABC tools |
| `class Foo(ABC):` | Make Foo abstract |
| `@abstractmethod` | Mark method as required in subclass |
| `from typing import Protocol` | Import Protocol |
| `class P(Protocol): def m(self): ...` | Define structural interface |
| `__len__`, `__getitem__`, etc. | Dunder (magic) methods |

---

## Common Pitfalls

- **Forgetting `super().__init__()`** — parent's `__init__` won't run, leaving the object partially initialized.
- **Overriding but not calling `super()`** — often you want the parent behavior *plus* your additions.
- **Multiple inheritance diamond problem** — Python's MRO handles it, but keep inheritance hierarchies shallow.
- **Making everything abstract** — only use ABC when the parent truly cannot provide a default implementation.
- **`isinstance` vs `type(x) ==`** — always use `isinstance`; `type(x) ==` breaks with subclasses.
- **Protocol at runtime** — `isinstance(obj, MyProtocol)` doesn't work unless you also inherit from `Protocol` and use `runtime_checkable`. Use it for type checking, not runtime checks.

---

## When to Use What

| Need | Use |
|------|-----|
| Shared implementation | Inheritance |
| Required interface, related classes | ABC + @abstractmethod |
| Type-safe duck typing | Protocol |
| Adding behavior to unrelated classes | Mixin |
| Make object work with `len()`, `[]` etc. | Dunder methods |
| Check if object is "a kind of" something | `isinstance()` |
