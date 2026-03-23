# ─────────────────────────────────────────────────────────────
#  Lesson 13 — Standard Library Modules
#  Run: python3 main.py
# ─────────────────────────────────────────────────────────────

from collections import Counter, defaultdict, deque, namedtuple, OrderedDict
from datetime import date, datetime, timedelta, timezone
from functools import cache, partial, reduce
from pathlib import Path


# ── COLLECTIONS: namedtuple ───────────────────────────────────
print("── collections.namedtuple ───────────────────────────")

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"  Point(3, 4): x={p.x}, y={p.y}")
print(f"  indexable:   p[0]={p[0]}")
x, y = p
print(f"  unpackable:  x={x}, y={y}")

# namedtuple._replace — create modified copy (immutable)
p2 = p._replace(y=10)
print(f"  _replace(y=10): {p2}")


# ── COLLECTIONS: Counter ──────────────────────────────────────
print("\n── collections.Counter ──────────────────────────────")

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(f"  Counter: {dict(c)}")
print(f"  most_common(2): {c.most_common(2)}")
print(f"  count of 'apple': {c['apple']}")
print(f"  count of 'mango': {c['mango']}")  # missing key → 0

# Counter arithmetic
a = Counter("aab")
b = Counter("abc")
print(f"  Counter('aab') + Counter('abc') = {dict(a + b)}")
print(f"  Counter('aab') - Counter('abc') = {dict(a - b)}")

# Count characters
char_counts = Counter("mississippi")
print(f"  'mississippi' chars: {char_counts.most_common()}")


# ── COLLECTIONS: defaultdict ──────────────────────────────────
print("\n── collections.defaultdict ──────────────────────────")

# Group words by first letter
by_letter: defaultdict[str, list[str]] = defaultdict(list)
for word in ["apple", "ant", "banana", "bear", "cherry"]:
    by_letter[word[0]].append(word)

for letter, group in sorted(by_letter.items()):
    print(f"  {letter!r}: {group}")

# Word frequency count without KeyError
freq: defaultdict[str, int] = defaultdict(int)
for char in "hello world":
    freq[char] += 1
print(f"  freq of 'l': {freq['l']}, 'z': {freq['z']}")


# ── COLLECTIONS: deque ────────────────────────────────────────
print("\n── collections.deque ────────────────────────────────")

dq: deque[int] = deque([1, 2, 3], maxlen=5)
dq.appendleft(0)   # O(1) — no shifting like list.insert(0, ...)
dq.append(4)
print(f"  after appendleft(0), append(4): {list(dq)}")

dq.popleft()        # O(1)
print(f"  after popleft(): {list(dq)}")

dq.rotate(1)        # rotate right
print(f"  after rotate(1): {list(dq)}")

# Sliding window: keep last N items
window: deque[int] = deque(maxlen=3)
for n in range(6):
    window.append(n)
    print(f"  window after append({n}): {list(window)}")


# ── PATHLIB ───────────────────────────────────────────────────
print("\n── pathlib ──────────────────────────────────────────")

# Build paths with / — no string concatenation needed
here = Path(__file__).parent      # directory containing this script
readme = here.parent / "README.md"

print(f"  this file:    {Path(__file__).name}")
print(f"  parent dir:   {here.name}")
print(f"  readme path:  {readme}")
print(f"  readme exists: {readme.exists()}")

# Path properties
p = Path("data/report.csv")
print(f"  name:    {p.name}")
print(f"  stem:    {p.stem}")
print(f"  suffix:  {p.suffix}")
print(f"  parent:  {p.parent}")

# Write and read a temp file
tmp = here / "_tmp_lesson13.txt"
tmp.write_text("hello from pathlib\n", encoding="utf-8")
content = tmp.read_text(encoding="utf-8")
print(f"  read back: {content.strip()!r}")
tmp.unlink()   # clean up
print(f"  deleted temp file: {not tmp.exists()}")

# Glob: list Python files in this lesson dir
py_files = list(here.glob("*.py"))
print(f"  .py files here: {[f.name for f in py_files]}")


# ── DATETIME ──────────────────────────────────────────────────
print("\n── datetime ─────────────────────────────────────────")

today = date.today()
print(f"  today:     {today}")
print(f"  formatted: {today.strftime('%B %d, %Y')}")

# datetime — date + time
now_utc = datetime.now(tz=timezone.utc)
print(f"  now (UTC): {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Arithmetic with timedelta
tomorrow   = today + timedelta(days=1)
next_week  = today + timedelta(weeks=1)
print(f"  tomorrow:  {tomorrow}")
print(f"  next week: {next_week}")

# Parse a string
parsed = datetime.strptime("2026-06-15", "%Y-%m-%d")
print(f"  parsed:    {parsed.date()}")

# Days between two dates
new_year = date(2027, 1, 1)
delta = new_year - today
print(f"  days until 2027: {delta.days}")


# ── FUNCTOOLS ─────────────────────────────────────────────────
print("\n── functools ────────────────────────────────────────")


@cache
def fib(n: int) -> int:
    """Memoized fibonacci — O(n) vs O(2^n) without cache."""
    return n if n <= 1 else fib(n - 1) + fib(n - 2)


print(f"  fib(10): {fib(10)}")
print(f"  fib(30): {fib(30)}")

# partial — fix some arguments
power_of_2 = partial(pow, 2)    # first arg fixed to 2
print(f"  power_of_2(8): {power_of_2(8)}")   # 2^8 = 256

# reduce — fold a sequence into a single value
product = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])
print(f"  reduce product [1..5]: {product}")

total = reduce(lambda a, b: a + b, range(1, 101))
print(f"  reduce sum 1..100: {total}")
