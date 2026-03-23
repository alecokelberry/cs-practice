# ─────────────────────────────────────────────────────────────
#  Lesson 05 — Classes and Objects
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import math
from dataclasses import dataclass, field


# ── BASIC CLASS ───────────────────────────────────────────────
print("── basic class ──────────────────────────────")

class Dog:
    """A simple dog class demonstrating the basics."""

    # Class variable — shared by ALL instances (not per-object)
    species: str = "Canis lupus familiaris"

    def __init__(self, name: str, breed: str, age: int) -> None:
        # Instance variables — each Dog object has its own copy of these
        self.name = name
        self.breed = breed
        self.age = age

    def bark(self) -> str:
        """Instance method — has access to self (the object)."""
        return f"{self.name} says: Woof!"

    def birthday(self) -> None:
        """Modify instance state."""
        self.age += 1
        print(f"  {self.name} is now {self.age} years old.")

rex = Dog("Rex", "German Shepherd", 4)
buddy = Dog("Buddy", "Labrador", 2)

print(f"  rex:   {rex.name}, {rex.breed}, {rex.age}")
print(f"  buddy: {buddy.name}, {buddy.breed}, {buddy.age}")
print(f"  Class variable: {rex.species}")
print(f"  {rex.bark()}")
rex.birthday()


# ── __repr__ AND __str__ ──────────────────────────────────────
print("\n── __repr__ and __str__ ─────────────────────")

class Book:
    """Demonstrate __repr__ vs __str__."""

    def __init__(self, title: str, author: str, pages: int) -> None:
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self) -> str:
        # Should be unambiguous — ideally look like a constructor call.
        # Used in the REPL, in collections, and as the fallback for __str__.
        return f"Book(title={self.title!r}, author={self.author!r}, pages={self.pages})"

    def __str__(self) -> str:
        # Should be readable for end users.
        # Called by print(), str(), and f-strings.
        return f'"{self.title}" by {self.author} ({self.pages} pages)'

book = Book("Clean Code", "Robert Martin", 431)
print(f"  str(book):  {str(book)}")
print(f"  repr(book): {repr(book)}")
print(f"  f-string:   {book}")      # uses __str__

# In a list, Python uses __repr__ for the items
library = [book, Book("The Pragmatic Programmer", "Hunt & Thomas", 352)]
print(f"  In list: {library}")      # each item uses __repr__


# ── @property AND SETTER ──────────────────────────────────────
print("\n── @property and setter ─────────────────────")

class Circle:
    """Demonstrate @property for validation and computed attributes."""

    def __init__(self, radius: float) -> None:
        # Single underscore = "private by convention".
        # Not enforced by Python, but signals "don't access directly".
        self._radius: float = 0.0
        self.radius = radius    # use the setter — triggers validation

    @property
    def radius(self) -> float:
        """Getter — called when you access obj.radius."""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Setter — called when you assign obj.radius = value."""
        if value < 0:
            raise ValueError(f"Radius cannot be negative, got {value}")
        self._radius = value

    @property
    def area(self) -> float:
        """Computed property — no setter, so it's read-only.
        Callers see this as an attribute, not a method.
        """
        return math.pi * self._radius ** 2

    @property
    def circumference(self) -> float:
        """Another computed property."""
        return 2 * math.pi * self._radius

c = Circle(5.0)
print(f"  radius:        {c.radius}")
print(f"  area:          {c.area:.4f}")
print(f"  circumference: {c.circumference:.4f}")

c.radius = 10.0   # calls the setter
print(f"  after r=10: area = {c.area:.4f}")

try:
    c.radius = -1   # triggers validation in setter
except ValueError as e:
    print(f"  ValueError: {e}")


# ── @staticmethod AND @classmethod ────────────────────────────
print("\n── @staticmethod and @classmethod ──────────")

class Temperature:
    """Demonstrate the difference between static and class methods."""

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    def __repr__(self) -> str:
        return f"Temperature({self.celsius}°C)"

    @staticmethod
    def celsius_to_fahrenheit(c: float) -> float:
        """Static method — doesn't need self or cls.
        It's a utility function that belongs conceptually with this class.
        Could be a module-level function, but lives here for organization.
        """
        return c * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(f: float) -> float:
        """Another static utility."""
        return (f - 32) * 5 / 9

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """Class method — alternative constructor (factory method).
        cls is the class itself, not an instance.
        Using cls (instead of hardcoding Temperature) means subclasses work correctly.
        """
        return cls(cls.fahrenheit_to_celsius(fahrenheit))

    @classmethod
    def freezing(cls) -> "Temperature":
        """Another alternative constructor — a named constant."""
        return cls(0.0)

    @classmethod
    def boiling(cls) -> "Temperature":
        return cls(100.0)

# Static methods — called on the class (or instance, but class is clearer)
print(f"  100°C in °F: {Temperature.celsius_to_fahrenheit(100)}")
print(f"  212°F in °C: {Temperature.fahrenheit_to_celsius(212)}")

# Class methods — alternative constructors
body_temp = Temperature.from_fahrenheit(98.6)
print(f"  98.6°F → {body_temp}")
print(f"  Freezing: {Temperature.freezing()}")
print(f"  Boiling:  {Temperature.boiling()}")


# ── @dataclass ────────────────────────────────────────────────
print("\n── @dataclass ───────────────────────────────")

# @dataclass auto-generates __init__, __repr__, and __eq__ from your field annotations.
# Use it for any class that's primarily a data container.

@dataclass
class Point:
    """2D point — __init__, __repr__, __eq__ all generated automatically."""
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Custom method alongside generated ones."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

p1 = Point(1.0, 2.0)
p2 = Point(4.0, 6.0)
print(f"  p1: {p1}")               # auto __repr__
print(f"  p2: {p2}")
print(f"  p1 == Point(1,2): {p1 == Point(1.0, 2.0)}")  # auto __eq__
print(f"  distance: {p1.distance_to(p2):.4f}")


# ── DATACLASS WITH DEFAULTS AND FIELD() ───────────────────────
print("\n── dataclass with defaults and field() ──────")

@dataclass
class Player:
    """Demonstrate field() for mutable defaults and metadata."""
    name: str
    score: int = 0                               # simple default — fine for immutables

    # Mutable defaults (list, dict, set) MUST use field(default_factory=...)
    # Why: if you wrote `tags: list[str] = []`, all instances would SHARE that one list.
    # field(default_factory=list) creates a new [] for EACH instance.
    tags: list[str] = field(default_factory=list)

    # repr=False hides this field from __repr__ output
    _internal_id: int = field(default=0, repr=False)

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

p1 = Player("Alice", 1500)
p2 = Player("Bob")          # score defaults to 0

p1.add_tag("veteran")
p1.add_tag("top-10")
p2.add_tag("newcomer")

print(f"  p1: {p1}")
print(f"  p2: {p2}")
print(f"  p1.tags: {p1.tags}")
print(f"  p2.tags: {p2.tags}")  # different list — field(default_factory) works


# ── FROZEN DATACLASS ──────────────────────────────────────────
print("\n── frozen dataclass ─────────────────────────")

# frozen=True makes instances immutable — assigning to fields raises FrozenInstanceError.
# Also makes the class HASHABLE, so you can use it as a dict key or in a set.

@dataclass(frozen=True)
class Coordinate:
    """Immutable GPS coordinate."""
    latitude: float
    longitude: float

    def __str__(self) -> str:
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude):.4f}°{lat_dir}, {abs(self.longitude):.4f}°{lon_dir}"

denver = Coordinate(39.7392, -104.9903)
nyc    = Coordinate(40.7128, -74.0060)

print(f"  Denver: {denver}")
print(f"  NYC:    {nyc}")
print(f"  Same?   {denver == nyc}")

# Frozen dataclass is hashable — can be dict key or set element
visited: set[Coordinate] = {denver, nyc}
cache: dict[Coordinate, str] = {denver: "Denver", nyc: "New York City"}
print(f"  In set: {denver in visited}")
print(f"  Cache lookup: {cache[nyc]}")

try:
    denver.latitude = 0.0   # type: ignore[misc]
except Exception as e:
    print(f"  Can't modify frozen: {type(e).__name__}")


# ── DATACLASS WITH ORDER ──────────────────────────────────────
print("\n── dataclass with order=True ────────────────")

# order=True generates __lt__, __le__, __gt__, __ge__ based on field order.
# Fields are compared in the order they're defined (like a tuple comparison).

@dataclass(order=True)
class Version:
    """Semantic version number — comparable."""
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"

versions = [
    Version(2, 0, 0),
    Version(1, 5, 3),
    Version(1, 10, 0),
    Version(1, 5, 10),
]
print(f"  Before sort: {[str(v) for v in versions]}")
print(f"  After sort:  {[str(v) for v in sorted(versions)]}")
print(f"  Latest: {max(versions)}")


if __name__ == "__main__":
    pass
