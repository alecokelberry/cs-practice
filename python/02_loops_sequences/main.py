# ─────────────────────────────────────────────────────────────
#  Lesson 02 — Loops and Sequences
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

from itertools import islice, chain, product, combinations


# ── FOR LOOP ──────────────────────────────────────────────────
print("── for loop ─────────────────────────────────")

fruits: list[str] = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"  {fruit}")

# Strings are iterable — loop over characters
for char in "Python":
    print(f"  {char}", end=" ")
print()  # newline after the inline prints


# ── RANGE ─────────────────────────────────────────────────────
print("\n── range() ──────────────────────────────────")

# range(stop) — 0 to stop-1
print(f"  range(5):        {list(range(5))}")

# range(start, stop)
print(f"  range(2, 8):     {list(range(2, 8))}")

# range(start, stop, step)
print(f"  range(0, 10, 2): {list(range(0, 10, 2))}")

# Counting down
print(f"  range(5, 0, -1): {list(range(5, 0, -1))}")

# range() is lazy — it doesn't build a list in memory.
# That's why we wrap it in list() above — just to show the values.
# In real loops, never do list(range(...)); just use range directly.


# ── WHILE LOOP ────────────────────────────────────────────────
print("\n── while loop ───────────────────────────────")

count: int = 0
while count < 5:
    print(f"  count = {count}")
    count += 1

# while True with break — pattern for user-driven loops
attempts: int = 0
while True:
    attempts += 1
    if attempts >= 3:
        print(f"  Gave up after {attempts} attempts")
        break


# ── BREAK AND CONTINUE ────────────────────────────────────────
print("\n── break and continue ───────────────────────")

# continue — skip to next iteration
print("  Odd numbers only:")
for n in range(10):
    if n % 2 == 0:
        continue       # skip even numbers
    print(f"    {n}", end=" ")
print()

# break — exit the loop early
print("  Stop at first multiple of 7:")
for n in range(1, 50):
    if n % 7 == 0:
        print(f"    Found: {n}")
        break


# ── LOOP ELSE ─────────────────────────────────────────────────
print("\n── loop else ────────────────────────────────")

# The else clause runs only if the loop completed WITHOUT a break.
# This is the canonical Python pattern for "search and report not found."

def find_prime_factor(n: int) -> None:
    """Print the first prime factor of n, or report it's prime."""
    for divisor in range(2, n):
        if n % divisor == 0:
            print(f"  {n} is divisible by {divisor}")
            break           # found — don't run else
    else:
        # Only runs if we exhausted range(2, n) without breaking
        print(f"  {n} is prime")

for num in [7, 12, 17, 100]:
    find_prime_factor(num)


# ── ENUMERATE ─────────────────────────────────────────────────
print("\n── enumerate() ──────────────────────────────")

languages: list[str] = ["Python", "C++", "Rust", "Go"]

# Never do: for i in range(len(languages)): languages[i]
# Always do: enumerate

for i, lang in enumerate(languages):
    print(f"  [{i}] {lang}")

print()
# start= shifts the index — useful for 1-based numbering
for i, lang in enumerate(languages, start=1):
    print(f"  {i}. {lang}")


# ── ZIP ───────────────────────────────────────────────────────
print("\n── zip() ────────────────────────────────────")

names: list[str] = ["Alice", "Bob", "Carol", "Dave"]
scores: list[int] = [95, 87, 92, 78]
grades: list[str] = ["A", "B", "A", "C"]

# Walk two sequences in lockstep
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

print()
# zip works with more than two iterables
for name, score, grade in zip(names, scores, grades):
    print(f"  {name}: {score} ({grade})")

print()
# zip stops at the SHORTEST — if lengths differ, you lose data silently
# Use itertools.zip_longest to keep all elements
from itertools import zip_longest
short: list[int] = [1, 2]
long_: list[int] = [10, 20, 30, 40]
for a, b in zip_longest(short, long_, fillvalue=0):
    print(f"  {a} + {b} = {a + b}")


# ── LIST COMPREHENSIONS ───────────────────────────────────────
print("\n── list comprehensions ──────────────────────")

# Form: [expression for item in iterable if condition]
# Think of it as "build a list of <expression> for each <item>, but only if <condition>"

numbers: list[int] = list(range(1, 11))   # [1, 2, ..., 10]

# Transform: square every number
squares: list[int] = [n ** 2 for n in numbers]
print(f"  squares:    {squares}")

# Filter: keep only even numbers
evens: list[int] = [n for n in numbers if n % 2 == 0]
print(f"  evens:      {evens}")

# Transform AND filter: square even numbers only
even_squares: list[int] = [n ** 2 for n in numbers if n % 2 == 0]
print(f"  even_sq:    {even_squares}")

# Works on strings too
words: list[str] = ["hello", "world", "python", "rocks"]
upper_long: list[str] = [w.upper() for w in words if len(w) > 5]
print(f"  upper_long: {upper_long}")

# Nested comprehension — generates cartesian product
# [... for x in outer for y in inner] — same order as nested for loops
pairs: list[tuple[int, int]] = [
    (x, y)
    for x in range(1, 4)    # outer loop
    for y in range(1, 4)    # inner loop
    if x != y               # filter
]
print(f"  pairs:      {pairs}")


# ── GENERATOR EXPRESSIONS ─────────────────────────────────────
print("\n── generator expressions ────────────────────")

# Generators use () instead of [].
# They're lazy — they produce one value at a time, never the full list.
# Use when you only need to consume the result once.

# This would create a million-element list in memory — wasteful:
# total = sum([x ** 2 for x in range(1_000_000)])

# This computes each value on demand — memory stays constant:
total: int = sum(x ** 2 for x in range(1_000_000))   # no [] needed inside sum()
print(f"  sum of squares 0–999999: {total:,}")

# max/min/any/all all accept generators
has_negative: bool = any(n < 0 for n in [1, 2, -3, 4])
all_positive: bool = all(n > 0 for n in [1, 2, 3, 4])
print(f"  has_negative: {has_negative}")
print(f"  all_positive: {all_positive}")

# You can store a generator and consume it once
def squares_up_to(n: int):
    """Generator function — yields squares lazily."""
    for i in range(n):
        yield i ** 2  # 'yield' suspends and returns — resumes on next()

gen = squares_up_to(5)
print(f"  generator squares: {list(gen)}")   # consume the generator into a list


# ── SLICING ───────────────────────────────────────────────────
print("\n── slicing ──────────────────────────────────")

lst: list[int] = list(range(10))   # [0, 1, 2, ..., 9]
print(f"  full:        {lst}")
print(f"  [2:5]:       {lst[2:5]}")       # index 2, 3, 4 (stop is exclusive)
print(f"  [:3]:        {lst[:3]}")         # from start to 2
print(f"  [7:]:        {lst[7:]}")         # from 7 to end
print(f"  [-3:]:       {lst[-3:]}")        # last 3 (negative counts from end)
print(f"  [1:-1]:      {lst[1:-1]}")       # drop first and last
print(f"  [::2]:       {lst[::2]}")        # every 2nd element
print(f"  [1::2]:      {lst[1::2]}")       # odd-index elements
print(f"  [::-1]:      {lst[::-1]}")       # reversed (step of -1)

# Slicing creates a SHALLOW COPY — original is unchanged
original: list[int] = [1, 2, 3, 4, 5]
copy: list[int] = original[:]    # full slice = full copy
copy[0] = 99
print(f"\n  original after modifying copy: {original}")   # unchanged


# ── ITERTOOLS ─────────────────────────────────────────────────
print("\n── itertools ────────────────────────────────")

# islice: take first N items from any iterable (even infinite ones)
def count_up(start: int = 0):
    """Infinite generator — counts up forever."""
    n = start
    while True:
        yield n
        n += 1

first_five = list(islice(count_up(10), 5))   # take 5 from infinite generator
print(f"  islice(count_up(10), 5): {first_five}")

# chain: concatenate iterables lazily
a: list[int] = [1, 2, 3]
b: list[int] = [4, 5, 6]
c: list[int] = [7, 8, 9]
chained: list[int] = list(chain(a, b, c))
print(f"  chain: {chained}")

# product: cartesian product
print("  product('AB', repeat=2):", list(product("AB", repeat=2)))

# combinations: all r-length combinations (order doesn't matter)
combos = list(combinations([1, 2, 3, 4], 2))
print(f"  combinations([1,2,3,4], 2): {combos}")


# ── PRACTICAL EXAMPLE — word frequency ───────────────────────
print("\n── practical: word frequency ────────────────")

text: str = "the quick brown fox jumps over the lazy dog the fox"
words_list: list[str] = text.split()   # split on whitespace

# Count word occurrences with a comprehension + set
unique_words: set[str] = set(words_list)   # deduplicate
freq: dict[str, int] = {
    word: words_list.count(word)
    for word in unique_words
}

# Sort by frequency descending
sorted_freq = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
for word, count in sorted_freq:
    print(f"  {word:10} {count}")


if __name__ == "__main__":
    pass
