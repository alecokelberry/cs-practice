# ─────────────────────────────────────────────────────────────
#  Lesson 01 — Basics
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import math


# ── VARIABLES AND TYPE HINTS ──────────────────────────────────
# Type hints don't change runtime behavior — Python doesn't enforce them.
# They exist for YOU and for tools like mypy/Pyright that catch bugs before runtime.

name: str = "Alec"
age: int = 25
gpa: float = 3.85
is_enrolled: bool = True
graduation: None = None   # None is its own type (NoneType)

print("── Variables ────────────────────────────────")
print(f"name={name!r}  type={type(name).__name__}")  # !r adds quotes around strings
print(f"age={age}  type={type(age).__name__}")
print(f"gpa={gpa}  type={type(gpa).__name__}")
print(f"is_enrolled={is_enrolled}  type={type(is_enrolled).__name__}")
print(f"graduation={graduation}  type={type(graduation).__name__}")


# ── INTEGERS ──────────────────────────────────────────────────
print("\n── Integers ─────────────────────────────────")

# Underscores in numeric literals — purely visual, ignored by Python
population: int = 8_100_000_000
print(f"World population: {population:,}")  # :, adds thousands separators

# Python ints have arbitrary precision — no overflow like C++
huge: int = 2 ** 100
print(f"2^100 = {huge}")

# Integer division operators
a, b = 17, 5
print(f"{a} / {b}  = {a / b}")    # true division → always float
print(f"{a} // {b} = {a // b}")   # floor division → int (rounds toward -inf)
print(f"{a} % {b}  = {a % b}")    # modulo (remainder)
print(f"{a} ** {b} = {a ** b}")   # exponentiation


# ── FLOATS ────────────────────────────────────────────────────
print("\n── Floats ───────────────────────────────────")

x: float = 0.1 + 0.2
print(f"0.1 + 0.2 = {x}")              # → 0.30000000000000004 (IEEE 754 issue)
print(f"== 0.3? {x == 0.3}")           # → False — never compare floats with ==

# Use math.isclose() for float equality
print(f"isclose? {math.isclose(x, 0.3)}")  # → True — correct way to compare floats

# Special float values
print(f"inf:  {float('inf')}")
print(f"-inf: {float('-inf')}")
print(f"nan:  {float('nan')}")


# ── STRINGS ───────────────────────────────────────────────────
print("\n── Strings ──────────────────────────────────")

greeting: str = "Hello, World!"
print(f"Length: {len(greeting)}")
print(f"Upper: {greeting.upper()}")
print(f"Slice [0:5]: {greeting[0:5]}")   # "Hello" — strings are sequences
print(f"Reversed: {greeting[::-1]}")     # step of -1 reverses

# Strings are immutable — you can't do greeting[0] = "h"
# You create a new string instead
fixed: str = "h" + greeting[1:]
print(f"Lowercased first char: {fixed}")

# Multiline strings
haiku: str = """
Old pond—
a frog jumps in,
sound of water.
"""
print(haiku.strip())  # .strip() removes leading/trailing whitespace


# ── F-STRINGS ─────────────────────────────────────────────────
print("\n── f-strings ────────────────────────────────")

score: float = 95.6789
player: str = "Alec"
rank: int = 1

# Basic interpolation
print(f"Player: {player}")

# Format specs after the colon
print(f"Score: {score:.2f}")         # 2 decimal places
print(f"Score: {score:.0f}")         # 0 decimal places (rounds)
print(f"Rank: {rank:03d}")           # pad with zeros to width 3
print(f"Score: {score:>10.2f}")      # right-align in 10-char field
print(f"Score: {score:<10.2f}|")     # left-align in 10-char field
print(f"Big: {1_000_000:,}")         # thousands separator
print(f"Hex: {255:#x}")              # hex with 0x prefix
print(f"Pct: {0.856:.1%}")          # percentage format

# Debug format — prints the variable name AND its value
# Invaluable when debugging
print(f"{score=}")        # → score=95.6789
print(f"{player=}")       # → player='Alec'

# Expressions inside f-strings
print(f"{'hello'.upper()}")          # → HELLO
print(f"{2 ** 10 = }")               # → 2 ** 10 = 1024


# ── BOOLEANS AND TRUTHINESS ───────────────────────────────────
print("\n── Booleans and Truthiness ──────────────────")

# bool is a subclass of int — True == 1, False == 0
print(f"True + True = {True + True}")       # → 2
print(f"True * 10 = {True * 10}")           # → 10 (legal but avoid in practice)

# Falsy values: False, None, 0, 0.0, "", [], {}, set()
# Everything else is truthy

falsy_examples: list = [False, None, 0, 0.0, "", [], {}, set()]
for val in falsy_examples:
    # bool() converts any value to True/False
    print(f"  bool({val!r:10}) = {bool(val)}")

print()
# Pythonic: rely on truthiness, don't compare to True/False
my_list: list[int] = [1, 2, 3]
empty_list: list[int] = []

# Bad (redundant):
# if len(my_list) > 0:

# Good (idiomatic):
if my_list:
    print("my_list has items")
if not empty_list:
    print("empty_list is empty")


# ── TYPE CONVERSION ───────────────────────────────────────────
print("\n── Type Conversion ──────────────────────────")

# String → int/float
num_str: str = "42"
print(f'int("42")   = {int(num_str)}')
print(f'float("42") = {float(num_str)}')

# int() truncates — does NOT round
print(f"int(3.9)  = {int(3.9)}")    # → 3
print(f"int(-3.9) = {int(-3.9)}")   # → -3  (truncates toward zero)
print(f"round(3.9) = {round(3.9)}") # → 4   (rounds to nearest)
print(f"round(3.5) = {round(3.5)}") # → 4   (banker's rounding — rounds to even)

# Number → string
print(f'str(100) = {str(100)!r}')

# Check isinstance (preferred over type() ==)
val: int = 42
print(f"isinstance(42, int)       = {isinstance(val, int)}")
print(f"isinstance(True, int)     = {isinstance(True, int)}")   # True! bool is a subclass
print(f"isinstance(42, (int, float)) = {isinstance(val, (int, float))}")  # check multiple


# ── NONE AND IDENTITY ─────────────────────────────────────────
print("\n── None and Identity ────────────────────────")

result: str | None = None   # Union type — can be str or None

# Always use 'is None' — never '== None'
# == can be overridden by a class's __eq__; 'is' checks object identity
if result is None:
    print("result is None")

result = "done"
if result is not None:
    print(f"result has a value: {result!r}")


# ── MATCH / CASE ──────────────────────────────────────────────
print("\n── match/case ───────────────────────────────")

# match/case is structural pattern matching — cleaner than if/elif chains
# for 3+ branches based on value or structure

def describe_status(code: int) -> str:
    """Return a human-readable HTTP status description."""
    match code:
        case 200:
            return "OK"
        case 301 | 302:        # | means "or" — matches either
            return "Redirect"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:                # _ is the wildcard — catch-all
            return f"Unknown status: {code}"

for code in [200, 301, 404, 418, 500]:
    print(f"  {code} → {describe_status(code)}")

print()

# match on structure — tuples and sequences
def describe_point(point: tuple[int, int]) -> str:
    """Describe where a 2D point is."""
    match point:
        case (0, 0):
            return "origin"
        case (x, 0):           # captures 'x' from the tuple
            return f"on x-axis at {x}"
        case (0, y):           # captures 'y'
            return f"on y-axis at {y}"
        case (x, y) if x == y: # guard clause — extra condition
            return f"on diagonal at ({x}, {y})"
        case (x, y):
            return f"at ({x}, {y})"

points = [(0, 0), (3, 0), (0, -2), (4, 4), (1, 7)]
for pt in points:
    print(f"  {pt} → {describe_point(pt)}")


# ── WALRUS OPERATOR := ────────────────────────────────────────
print("\n── Walrus Operator := ───────────────────────")

# The walrus operator assigns a value AND returns it in one expression.
# Removes the need to call a function twice (once for the condition, once for use).

# Classic pattern: while loop that reads data until empty/None
import random

def get_next_value() -> int | None:
    """Simulate reading data — returns None when done."""
    val = random.randint(0, 5)
    return val if val != 0 else None  # None signals end-of-data

print("Reading values until None:")
random.seed(42)   # fix seed so output is reproducible
while (n := get_next_value()) is not None:  # assign n AND test it
    print(f"  got: {n}")
print("  (done)")

# Also useful in comprehensions (though use sparingly — readability first)
numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Filter and transform in one pass, keeping the computed value
results: list[int] = [
    doubled
    for n in numbers
    if (doubled := n * 2) > 10   # assign doubled, test it, use it
]
print(f"\nDoubled values > 10: {results}")


# ── ARITHMETIC SUMMARY ────────────────────────────────────────
print("\n── Arithmetic Summary ───────────────────────")

print(f"  10 + 3  = {10 + 3}")   # addition
print(f"  10 - 3  = {10 - 3}")   # subtraction
print(f"  10 * 3  = {10 * 3}")   # multiplication
print(f"  10 / 3  = {10 / 3}")   # true division → float
print(f"  10 // 3 = {10 // 3}")  # floor division → int
print(f"  10 % 3  = {10 % 3}")   # modulo
print(f"  10 ** 3 = {10 ** 3}")  # exponentiation

# Augmented assignment operators
x = 10
x += 5;  print(f"  after += 5: {x}")
x -= 3;  print(f"  after -= 3: {x}")
x *= 2;  print(f"  after *= 2: {x}")
x //= 4; print(f"  after //= 4: {x}")


if __name__ == "__main__":
    pass  # All output runs at module level — guard is here for import safety
