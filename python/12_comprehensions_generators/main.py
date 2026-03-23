# ─────────────────────────────────────────────────────────────
#  Lesson 12 — Comprehensions & Generators (Deep Dive)
#  Run: python3 main.py
# ─────────────────────────────────────────────────────────────

import itertools


# ── LIST COMPREHENSIONS ───────────────────────────────────────
print("── List Comprehensions ──────────────────────────────")

words = ["hello", "world", "python", "rocks", "hi"]
squares = [x ** 2 for x in range(8)]
upper_long = [w.upper() for w in words if len(w) > 3]
print(f"  squares:          {squares}")
print(f"  upper (len > 3):  {upper_long}")

# Nested: flatten 2D list — outer loop first
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in matrix for n in row]
print(f"  flat matrix:      {flat}")

# Pairs where a != b
pairs = [(a, b) for a in [1, 2, 3] for b in [1, 2, 3] if a != b]
print(f"  unequal pairs:    {pairs}")


# ── WALRUS OPERATOR IN COMPREHENSIONS ────────────────────────
print("\n── Walrus Operator (:=) in Comprehensions ───────────")

# Compute len() once; use in both filter and expression
data = ["cat", "elephant", "ox", "rhinoceros", "bee"]
long_words = [(w, n) for w in data if (n := len(w)) > 3]
print(f"  (word, length) where len > 3: {long_words}")


# ── DICT AND SET COMPREHENSIONS ───────────────────────────────
print("\n── Dict & Set Comprehensions ────────────────────────")

word_lengths = {w: len(w) for w in words}
print(f"  word lengths:     {word_lengths}")

original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(f"  inverted dict:    {inverted}")

grades = {"Alice": 92, "Bob": 55, "Carol": 78, "Dave": 40}
passing = {name: score for name, score in grades.items() if score >= 60}
print(f"  passing grades:   {passing}")

unique_mods = {x % 5 for x in range(20)}
print(f"  unique x%%5 vals:  {sorted(unique_mods)}")


# ── GENERATOR EXPRESSIONS ─────────────────────────────────────
print("\n── Generator Expressions ────────────────────────────")

# Memory-efficient: no intermediate list
total = sum(x ** 2 for x in range(1_000))
print(f"  sum of squares 0..999: {total}")

exists = any(score < 60 for score in grades.values())
print(f"  any failing grades?    {exists}")

# next() to get first match without consuming the whole iterable
numbers = [4, -1, 7, -3, 8]
first_positive = next(x for x in numbers if x > 0)
print(f"  first positive:        {first_positive}")

# Generator object is single-pass
gen = (x ** 2 for x in range(5))
print(f"  first pass:  {list(gen)}")
print(f"  second pass: {list(gen)}")   # exhausted — empty


# ── GENERATOR FUNCTIONS ───────────────────────────────────────
print("\n── Generator Functions ──────────────────────────────")


def integers_from(start: int):
    """Infinite generator — yields integers starting at start."""
    n = start
    while True:
        yield n
        n += 1


def take(n: int, it) -> list:
    """Take first n values from any iterable."""
    return [val for _, val in zip(range(n), it)]


print(f"  integers_from(10), first 5: {take(5, integers_from(10))}")


def flatten(nested: list[list]) -> object:
    """Flatten one level with yield from."""
    for sub in nested:
        yield from sub


print(f"  flatten:  {list(flatten([[1, 2], [3, 4], [5]]))}")


# ── GENERATOR PIPELINE ────────────────────────────────────────
print("\n── Generator Pipeline ───────────────────────────────")

# Each stage processes one item at a time — no intermediate lists


def doubled(it):
    for x in it:
        yield x * 2


def only_even(it):
    for x in it:
        if x % 2 == 0:
            yield x


pipeline = only_even(doubled(integers_from(1)))
result = take(6, pipeline)
print(f"  doubled then filtered even, first 6: {result}")


# ── ADVANCED ITERTOOLS ────────────────────────────────────────
print("\n── Advanced itertools ───────────────────────────────")

# accumulate — running total
running = list(itertools.accumulate([1, 2, 3, 4, 5]))
print(f"  accumulate (sum):         {running}")

running_product = list(itertools.accumulate([1, 2, 3, 4, 5], lambda a, b: a * b))
print(f"  accumulate (product):     {running_product}")

# groupby — groups CONSECUTIVE equal keys (sort first for full grouping)
scores = [("A", 95), ("A", 88), ("B", 72), ("B", 65), ("C", 91)]
for grade, group in itertools.groupby(scores, key=lambda t: t[0]):
    names = [score for _, score in group]
    print(f"  groupby grade={grade!r}: {names}")

# starmap — unpack each item as args
powers = [(2, 3), (4, 2), (1, 10)]
print(f"  starmap(pow, pairs):      {list(itertools.starmap(pow, powers))}")

# takewhile / dropwhile
nums = [1, 2, 3, 5, 4, 6]
print(f"  takewhile(< 5):           {list(itertools.takewhile(lambda x: x < 5, nums))}")
print(f"  dropwhile(< 5):           {list(itertools.dropwhile(lambda x: x < 5, nums))}")

# pairwise (3.10+) — overlapping consecutive pairs
print(f"  pairwise([1..5]):         {list(itertools.pairwise([1, 2, 3, 4, 5]))}")

# batched (3.12+) — non-overlapping chunks of size n
print(f"  batched([1..7], 3):       {list(itertools.batched(range(1, 8), 3))}")

# cycle
toggle = itertools.cycle(["on", "off"])
print(f"  cycle 6 steps:            {[next(toggle) for _ in range(6)]}")
