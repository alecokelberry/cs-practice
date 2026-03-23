# ─────────────────────────────────────────────────────────────
#  Lesson 16 — Type Hints
#  Run: python3 main.py
#  Type-check: mypy main.py  (pip install mypy)
# ─────────────────────────────────────────────────────────────

from __future__ import annotations   # enables newer syntax on Python 3.8+

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol, TypedDict, TypeVar, overload


# ── BASIC ANNOTATIONS ─────────────────────────────────────────
print("── Basic Annotations ────────────────────────────────")


def greet(name: str) -> str:
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    return a + b


def log(msg: str) -> None:
    print(f"  LOG: {msg}")


print(f"  greet('Alice'): {greet('Alice')}")
print(f"  add(3, 4): {add(3, 4)}")
log("this returns None")


# ── BUILT-IN GENERICS ─────────────────────────────────────────
print("\n── Built-in Generics ────────────────────────────────")


def first(items: list[int]) -> int:
    return items[0]


def merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {**a, **b}


def unique_sorted(items: list[str]) -> list[str]:
    return sorted(set(items))


print(f"  first([5,3,1]): {first([5, 3, 1])}")
print(f"  merge: {merge({'a': 1}, {'b': 2})}")
print(f"  unique_sorted: {unique_sorted(['b', 'a', 'b', 'c', 'a'])}")


# ── OPTIONAL AND UNION ────────────────────────────────────────
print("\n── Optional and Union ───────────────────────────────")

users = {"alice": 42, "bob": 7}


def find_user(name: str) -> str | None:
    uid = users.get(name)
    if uid is None:
        return None
    return f"user:{uid}"


def display(result: str | None) -> str:
    # Must guard against None before using as str
    return result if result is not None else "(not found)"


print(f"  find_user('alice'): {display(find_user('alice'))}")
print(f"  find_user('carol'): {display(find_user('carol'))}")


def stringify(value: int | float | str) -> str:
    return str(value)


print(f"  stringify(42): {stringify(42)!r}")
print(f"  stringify(3.14): {stringify(3.14)!r}")
print(f"  stringify('hi'): {stringify('hi')!r}")


# ── TypeVar — GENERIC FUNCTIONS ───────────────────────────────
print("\n── TypeVar (Generic Functions) ──────────────────────")

T = TypeVar("T")


def identity(x: T) -> T:
    """Return x unchanged. Return type matches input type."""
    return x


def first_item(items: list[T]) -> T:
    """Return first item, preserving element type."""
    return items[0]


print(f"  identity(10): {identity(10)}")
print(f"  identity('hi'): {identity('hi')}")
print(f"  first_item([1,2,3]): {first_item([1, 2, 3])}")
print(f"  first_item(['a','b']): {first_item(['a', 'b'])}")


# ── CALLABLE ──────────────────────────────────────────────────
print("\n── Callable ─────────────────────────────────────────")


def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    return fn(a, b)


print(f"  apply(add, 3, 7): {apply(add, 3, 7)}")
print(f"  apply(lambda x,y: x*y, 4, 5): {apply(lambda x, y: x * y, 4, 5)}")

# Callable used as a type alias
Transformer = Callable[[str], str]


def pipeline(text: str, *transforms: Transformer) -> str:
    result = text
    for t in transforms:
        result = t(result)
    return result


result = pipeline("  hello world  ", str.strip, str.upper)
print(f"  pipeline strip+upper: {result!r}")


# ── TypedDict ─────────────────────────────────────────────────
print("\n── TypedDict ────────────────────────────────────────")


class Movie(TypedDict):
    title: str
    year: int
    rating: float


def display_movie(movie: Movie) -> str:
    return f"{movie['title']} ({movie['year']}) — ★{movie['rating']}"


m: Movie = {"title": "Dune", "year": 2021, "rating": 8.0}
print(f"  {display_movie(m)}")


# ── PROTOCOL — STRUCTURAL TYPING ──────────────────────────────
print("\n── Protocol (Structural Typing) ─────────────────────")


class Drawable(Protocol):
    def draw(self) -> str: ...


class Circle:
    def draw(self) -> str:
        return "○ circle"


class Square:
    def draw(self) -> str:
        return "□ square"


class Triangle:
    def draw(self) -> str:
        return "△ triangle"


def render_all(shapes: list[Drawable]) -> None:
    for shape in shapes:
        print(f"  {shape.draw()}")


# No inheritance needed — any class with draw() satisfies Drawable
render_all([Circle(), Square(), Triangle()])


# ── DATACLASS WITH TYPE HINTS ─────────────────────────────────
print("\n── @dataclass with Type Hints ───────────────────────")


@dataclass
class Point:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass
class Student:
    name: str
    scores: list[int] = field(default_factory=list)

    def average(self) -> float | None:
        return sum(self.scores) / len(self.scores) if self.scores else None


p = Point(3.0, 4.0)
print(f"  Point(3,4): {p}, distance: {p.distance_from_origin()}")

s = Student("Alice", [90, 85, 92])
print(f"  Student: {s}, avg: {s.average():.1f}")


# ── OVERLOAD ──────────────────────────────────────────────────
print("\n── @overload ────────────────────────────────────────")


@overload
def double(val: int) -> int: ...
@overload
def double(val: str) -> str: ...


def double(val: int | str) -> int | str:
    if isinstance(val, int):
        return val * 2
    return val * 2   # str * 2 = repeated string


print(f"  double(5): {double(5)}")
print(f"  double('hi'): {double('hi')!r}")


# ── ANY — OPT OUT ─────────────────────────────────────────────
print("\n── Any ──────────────────────────────────────────────")


def log_anything(value: Any) -> None:
    """Accept literally any type — no type checking on value."""
    print(f"  log: {value!r} (type: {type(value).__name__})")


log_anything(42)
log_anything({"key": [1, 2, 3]})
log_anything(None)
