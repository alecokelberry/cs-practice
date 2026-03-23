# ─────────────────────────────────────────────────────────────
#  Lesson 06 — OOP (Inheritance, Protocols, Dunders)
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import math
import json
from abc import ABC, abstractmethod
from typing import Protocol


# ── INHERITANCE AND SUPER() ───────────────────────────────────
print("── inheritance and super() ──────────────────")

class Animal:
    """Base class for all animals."""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def speak(self) -> str:
        """Subclasses should override this."""
        return f"{self.name} makes a sound."

    def describe(self) -> str:
        """Concrete method — shared by all subclasses."""
        return f"{self.name} is a {type(self).__name__}, age {self.age}"

class Dog(Animal):
    """Dog inherits everything from Animal and adds/overrides."""

    def __init__(self, name: str, age: int, breed: str) -> None:
        # super().__init__() runs Animal's __init__ — without this,
        # self.name and self.age would never be set.
        super().__init__(name, age)
        self.breed = breed    # Dog-specific attribute

    def speak(self) -> str:
        """Override Animal.speak."""
        return f"{self.name} says: Woof!"

    def fetch(self, item: str) -> str:
        """Dog-specific method — not in Animal."""
        return f"{self.name} fetches the {item}!"

class Cat(Animal):
    def __init__(self, name: str, age: int, indoor: bool = True) -> None:
        super().__init__(name, age)
        self.indoor = indoor

    def speak(self) -> str:
        return f"{self.name} says: Meow!"

rex = Dog("Rex", 4, "German Shepherd")
whiskers = Cat("Whiskers", 3)

print(f"  {rex.describe()}")
print(f"  {rex.speak()}")
print(f"  {rex.fetch('ball')}")
print(f"  {whiskers.describe()}")
print(f"  {whiskers.speak()}")


# ── ISINSTANCE AND ISSUBCLASS ─────────────────────────────────
print("\n── isinstance and issubclass ────────────────")

# isinstance respects the inheritance chain
print(f"  isinstance(rex, Dog):    {isinstance(rex, Dog)}")
print(f"  isinstance(rex, Animal): {isinstance(rex, Animal)}")   # True — Dog IS-A Animal
print(f"  isinstance(rex, Cat):    {isinstance(rex, Cat)}")      # False

# Check multiple types at once with a tuple
print(f"  isinstance(rex, (Dog, Cat)): {isinstance(rex, (Dog, Cat))}")

print(f"  issubclass(Dog, Animal): {issubclass(Dog, Animal)}")
print(f"  issubclass(Cat, Dog):    {issubclass(Cat, Dog)}")


# ── ABSTRACT BASE CLASSES ─────────────────────────────────────
print("\n── abstract base classes ────────────────────")

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly.
    Any concrete subclass MUST implement area() and perimeter().
    """

    @abstractmethod
    def area(self) -> float:
        """Return the area of this shape."""
        ...   # The ... (Ellipsis) signals intentional non-implementation

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of this shape."""
        ...

    def describe(self) -> str:
        """Concrete method available to all subclasses.
        Calls the abstract methods — polymorphism in action.
        """
        return (
            f"{type(self).__name__}: "
            f"area={self.area():.2f}, "
            f"perimeter={self.perimeter():.2f}"
        )

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = self.perimeter() / 2   # semi-perimeter (Heron's formula)
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c

# Can't instantiate the abstract class directly
try:
    s = Shape()   # type: ignore[abstract]
except TypeError as e:
    print(f"  Shape() raises TypeError: {e}")

# Polymorphism — same .describe() call, different implementations
shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
for shape in shapes:
    print(f"  {shape.describe()}")

# isinstance still works with ABC
print(f"  isinstance(Circle(1), Shape): {isinstance(Circle(1), Shape)}")


# ── MIXINS ────────────────────────────────────────────────────
print("\n── mixins ───────────────────────────────────")

# Mixins add reusable behavior to unrelated classes.
# Key rule: mixins should be narrow in scope and not call super().__init__()
# because they're not meant to be instantiated alone.

class JsonMixin:
    """Adds JSON serialization to any class that has a __dict__."""

    def to_json(self) -> str:
        """Serialize the object's public attributes to JSON."""
        # vars(self) is equivalent to self.__dict__ — returns the instance dict
        public = {k: v for k, v in vars(self).items() if not k.startswith("_")}
        return json.dumps(public, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "JsonMixin":
        """Create an instance from a dict. Subclasses may override."""
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

class LogMixin:
    """Adds simple logging to any class."""

    def log(self, message: str) -> None:
        """Log a message prefixed with the class name."""
        print(f"  [{type(self).__name__}] {message}")

class Serializable:
    """Base class for domain objects — provides core functionality."""
    pass

# Multiple inheritance: mixins listed first, then the real base class.
# Python resolves methods left-to-right (MRO).
class GamePlayer(JsonMixin, LogMixin, Serializable):
    """A game player with JSON serialization and logging."""

    def __init__(self, username: str, level: int, score: int) -> None:
        self.username = username
        self.level = level
        self.score = score

    def level_up(self) -> None:
        self.level += 1
        self.score += 100
        self.log(f"leveled up to {self.level}!")   # from LogMixin

player = GamePlayer("Alice", 5, 1500)
player.level_up()
print(player.to_json())   # from JsonMixin


# ── PROTOCOL — STRUCTURAL SUBTYPING ──────────────────────────
print("\n── Protocol (duck typing) ───────────────────")

# Protocol defines an interface by STRUCTURE — if an object has the right methods,
# it satisfies the Protocol. No inheritance needed.
# Type checkers (mypy, Pyright) enforce this; no runtime overhead.

class Drawable(Protocol):
    """Any object that can draw itself."""
    def draw(self) -> str:
        ...

class Resizable(Protocol):
    """Any object that can be resized."""
    def resize(self, factor: float) -> None:
        ...

# These classes don't inherit from Drawable — but they satisfy its structure
class Emoji:
    """Not related to Shape — but satisfies Drawable."""
    def __init__(self, char: str) -> None:
        self.char = char

    def draw(self) -> str:
        return self.char

class TerminalRect:
    """ASCII rectangle."""
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h

    def draw(self) -> str:
        row = "█" * self.w
        return "\n".join(["  " + row] * self.h)

    def resize(self, factor: float) -> None:
        self.w = int(self.w * factor)
        self.h = int(self.h * factor)

def render_all(items: list[Drawable]) -> None:
    """Accepts any list of Drawable objects — no inheritance required."""
    for item in items:
        print(f"  {item.draw()}")

# Emoji and TerminalRect both satisfy Drawable — even though they're unrelated
render_all([Emoji("🐍"), Emoji("⭐"), TerminalRect(4, 1)])

# Protocol with Resizable
rect = TerminalRect(6, 2)
print(rect.draw())
rect.resize(0.5)
print(rect.draw())


# ── DUNDER METHODS ────────────────────────────────────────────
print("\n── dunder methods ───────────────────────────")

class NumberList:
    """A custom list-like container demonstrating key dunder methods.

    By implementing these, our class integrates with Python's built-in
    operations: len(), [], 'in', for loops, +, and print.
    """

    def __init__(self, items: list[int] | None = None) -> None:
        # Store internally as a list
        self._data: list[int] = items[:] if items else []

    def __repr__(self) -> str:
        return f"NumberList({self._data!r})"

    def __str__(self) -> str:
        return f"[{', '.join(str(x) for x in self._data)}]"

    def __len__(self) -> int:
        """Called by len(obj)."""
        return len(self._data)

    def __getitem__(self, index: int | slice) -> int | list[int]:
        """Called by obj[index] and obj[start:stop]."""
        return self._data[index]   # type: ignore[return-value]

    def __setitem__(self, index: int, value: int) -> None:
        """Called by obj[index] = value."""
        self._data[index] = value

    def __contains__(self, item: object) -> bool:
        """Called by 'x in obj'. Without this, Python falls back to __iter__."""
        return item in self._data

    def __iter__(self):
        """Called by 'for x in obj:'. Delegates to list's iterator."""
        return iter(self._data)

    def __add__(self, other: "NumberList") -> "NumberList":
        """Called by obj + other. Returns a new NumberList — don't mutate self."""
        return NumberList(self._data + other._data)

    def __eq__(self, other: object) -> bool:
        """Called by obj == other."""
        if not isinstance(other, NumberList):
            return NotImplemented   # let Python try the other side
        return self._data == other._data

    def total(self) -> int:
        return sum(self._data)

# Demonstrate each dunder in action
nl1 = NumberList([1, 2, 3, 4, 5])
nl2 = NumberList([6, 7, 8])

print(f"  repr:           {repr(nl1)}")
print(f"  str:            {nl1}")
print(f"  len:            {len(nl1)}")           # __len__
print(f"  nl1[2]:         {nl1[2]}")             # __getitem__
print(f"  nl1[1:3]:       {nl1[1:3]}")           # __getitem__ with slice
print(f"  3 in nl1:       {3 in nl1}")            # __contains__
print(f"  99 in nl1:      {99 in nl1}")
nl1[0] = 99                                      # __setitem__
print(f"  after nl1[0]=99:{nl1}")
nl1[0] = 1                                       # reset
combined = nl1 + nl2                              # __add__
print(f"  nl1 + nl2:      {combined}")
print(f"  nl1 == nl1:     {nl1 == NumberList([1, 2, 3, 4, 5])}")  # __eq__
print(f"  iteration:      ", end="")
for n in nl1:                                    # __iter__
    print(n, end=" ")
print()


if __name__ == "__main__":
    pass
