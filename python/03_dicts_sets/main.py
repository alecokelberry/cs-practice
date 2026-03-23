# ─────────────────────────────────────────────────────────────
#  Lesson 03 — Dicts and Sets
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

from collections import defaultdict, Counter


# ── DICT BASICS ───────────────────────────────────────────────
print("── dict basics ──────────────────────────────")

person: dict[str, str | int] = {
    "name": "Alec",
    "age": 25,
    "city": "Denver",
}
print(f"  dict: {person}")
print(f"  name: {person['name']}")

# .get() — safe access, returns None (or your default) if key is absent
# Prefer this over direct [] access when the key might not exist
print(f"  email (missing): {person.get('email')}")
print(f"  email (default): {person.get('email', 'no email set')}")

# Add / update
person["email"] = "alec@example.com"
person["age"] = 26     # overwrites existing value
print(f"  after update: {person}")

# Delete
removed = person.pop("city")   # removes and returns the value
print(f"  removed 'city': {removed!r}")
print(f"  after pop: {person}")

# Safe pop — won't raise KeyError if key is missing
person.pop("phone", None)   # returns None if 'phone' doesn't exist


# ── DICT ITERATION ────────────────────────────────────────────
print("\n── dict iteration ───────────────────────────")

grades: dict[str, int] = {"Alice": 95, "Bob": 87, "Carol": 92, "Dave": 78}

# .items() — most common pattern, gives (key, value) pairs
print("  Grades:")
for student, score in grades.items():
    print(f"    {student}: {score}")

# .keys() and .values()
print(f"  Students: {list(grades.keys())}")
print(f"  Scores:   {list(grades.values())}")
print(f"  Average:  {sum(grades.values()) / len(grades):.1f}")

# Membership test checks KEYS — O(1) average
print(f"  'Alice' in grades: {'Alice' in grades}")
print(f"  95 in grades:      {95 in grades}")           # False — keys, not values
print(f"  95 in grades.values(): {95 in grades.values()}")  # True — now values


# ── SETDEFAULT ────────────────────────────────────────────────
print("\n── setdefault ───────────────────────────────")

# setdefault(key, default) — insert default ONLY if key doesn't exist
# Returns the existing value if key is present, or the default if newly inserted

inventory: dict[str, int] = {"apples": 5, "bananas": 3}
inventory.setdefault("apples", 100)     # key exists — does nothing, returns 5
inventory.setdefault("oranges", 10)     # key missing — inserts 10
print(f"  inventory: {inventory}")


# ── DICT COMPREHENSIONS ───────────────────────────────────────
print("\n── dict comprehensions ──────────────────────")

# Build a dict from a range
squares: dict[int, int] = {n: n ** 2 for n in range(1, 8)}
print(f"  squares: {squares}")

# Filter a dict — keep only entries where value > 9
big_squares: dict[int, int] = {k: v for k, v in squares.items() if v > 9}
print(f"  big_squares: {big_squares}")

# Invert a dict (swap keys and values)
inverted: dict[int, int] = {v: k for k, v in squares.items()}
print(f"  inverted: {inverted}")

# Build a dict from two parallel lists using zip
names: list[str] = ["Alice", "Bob", "Carol"]
scores: list[int] = [95, 87, 92]
name_scores: dict[str, int] = {name: score for name, score in zip(names, scores)}
print(f"  name_scores: {name_scores}")


# ── MERGING DICTS (Python 3.9+) ───────────────────────────────
print("\n── merging dicts ────────────────────────────")

defaults: dict[str, str | int] = {
    "theme": "dark",
    "language": "en",
    "font_size": 12,
    "show_line_numbers": True,
}
user_prefs: dict[str, str | int] = {
    "theme": "light",    # overrides default
    "font_size": 14,     # overrides default
}

# | creates a new merged dict — right side wins on key conflicts
merged: dict[str, str | int] = defaults | user_prefs
print(f"  merged: {merged}")

# |= updates in place (modifies defaults directly)
config = defaults.copy()
config |= user_prefs
print(f"  config (|=): {config}")

# Old way (still valid, less readable):
# merged = {**defaults, **user_prefs}


# ── DEFAULTDICT ───────────────────────────────────────────────
print("\n── collections.defaultdict ──────────────────")

# defaultdict(factory) auto-creates a default value when a key is missing.
# The factory is called with no arguments: list → [], int → 0, set → set()

words: list[str] = ["apple", "ant", "bat", "banana", "cherry", "avocado", "blueberry"]

# Group words by their first letter — defaultdict avoids the "key exists?" check
by_letter: defaultdict[str, list[str]] = defaultdict(list)
for word in words:
    # Without defaultdict we'd need: if word[0] not in by_letter: by_letter[word[0]] = []
    by_letter[word[0]].append(word)

print("  Words grouped by first letter:")
for letter in sorted(by_letter):
    print(f"    {letter}: {by_letter[letter]}")

# defaultdict(int) — perfect for counting
sentence: str = "the quick brown fox jumps over the lazy dog"
char_count: defaultdict[str, int] = defaultdict(int)
for char in sentence.replace(" ", ""):
    char_count[char] += 1   # auto-initializes to 0 before +=

top_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)[:5]
print(f"\n  Top 5 chars: {top_chars}")


# ── COUNTER ───────────────────────────────────────────────────
print("\n── collections.Counter ──────────────────────")

# Counter is a specialized dict for counting hashable objects.
# It's the idiomatic way to count anything in Python.

text: str = "abracadabra"
letter_counts = Counter(text)
print(f"  Counter({text!r}): {letter_counts}")

# most_common(n) — sorted by frequency, descending
print(f"  most_common(3): {letter_counts.most_common(3)}")

# Missing keys return 0 (unlike regular dict)
print(f"  count of 'z': {letter_counts['z']}")   # 0, not KeyError

# Count words in a sentence
sentence_words: list[str] = "to be or not to be that is the question".split()
word_freq = Counter(sentence_words)
print(f"\n  Word frequencies: {dict(word_freq)}")
print(f"  most_common(3): {word_freq.most_common(3)}")

# Counter arithmetic
c1 = Counter({"a": 4, "b": 2, "c": 1})
c2 = Counter({"a": 1, "b": 3, "d": 5})
print(f"\n  c1:       {dict(c1)}")
print(f"  c2:       {dict(c2)}")
print(f"  c1 + c2:  {dict(c1 + c2)}")   # add counts
print(f"  c1 - c2:  {dict(c1 - c2)}")   # subtract, keep positives
print(f"  c1 & c2:  {dict(c1 & c2)}")   # min of each count
print(f"  c1 | c2:  {dict(c1 | c2)}")   # max of each count


# ── SETS ──────────────────────────────────────────────────────
print("\n── sets ─────────────────────────────────────")

# Sets: unordered collections of unique, hashable elements.
# Main uses: deduplication and fast membership testing.

nums: set[int] = {1, 2, 3, 4, 5}
more: set[int] = {3, 4, 5, 6, 7}

# Set operations — mirrors mathematical set algebra
print(f"  a: {nums}")
print(f"  b: {more}")
print(f"  a | b (union):         {nums | more}")          # all elements
print(f"  a & b (intersection):  {nums & more}")          # shared elements
print(f"  a - b (difference):    {nums - more}")          # in a, not in b
print(f"  b - a (difference):    {more - nums}")          # in b, not in a
print(f"  a ^ b (sym. diff):     {nums ^ more}")          # in one but not both

# Subset / superset tests
small: set[int] = {3, 4}
print(f"\n  {small} is subset of {nums}:   {small <= nums}")    # ≤ is subset
print(f"  {nums} is superset of {small}: {nums >= small}")   # ≥ is superset
print(f"  {nums} == {more}:              {nums == more}")

# Mutation
nums.add(10)         # add one element
nums.discard(99)     # remove — no error if absent (use this over .remove())
nums.remove(1)       # remove — raises KeyError if absent
print(f"\n  after add/discard/remove: {nums}")

# Membership test: O(1) average — much faster than list for large sets
print(f"  3 in nums: {3 in nums}")

# Deduplication — cast list to set and back
dupes: list[int] = [1, 2, 2, 3, 3, 3, 4]
unique: list[int] = list(set(dupes))
print(f"\n  deduplicated: {sorted(unique)}")   # sort because sets are unordered


# ── FROZENSET ─────────────────────────────────────────────────
print("\n── frozenset ────────────────────────────────")

# frozenset is an immutable set — same operations as set, but no add/remove.
# Since it's immutable, it's HASHABLE — you can use it as a dict key or set element.

fs1: frozenset[int] = frozenset([1, 2, 3])
fs2: frozenset[int] = frozenset([3, 4, 5])

print(f"  frozenset:         {fs1}")
print(f"  union:             {fs1 | fs2}")
print(f"  intersection:      {fs1 & fs2}")

# Use as dict key — impossible with a regular mutable set
graph_edges: dict[frozenset[str], int] = {
    frozenset({"A", "B"}): 5,    # edge A-B with weight 5
    frozenset({"B", "C"}): 3,    # edge B-C with weight 3
    frozenset({"A", "C"}): 8,    # edge A-C with weight 8
}
print(f"\n  edge A-B weight: {graph_edges[frozenset({'A', 'B'})]}")


# ── PRACTICAL EXAMPLE — inventory analysis ────────────────────
print("\n── practical: inventory analysis ────────────")

# Simulated store inventory and wishlist
in_stock: set[str] = {"apple", "banana", "milk", "eggs", "bread", "butter"}
wishlist: set[str] = {"milk", "eggs", "coffee", "yogurt", "apple"}

available: set[str] = in_stock & wishlist        # items you can actually get
need_elsewhere: set[str] = wishlist - in_stock   # on wishlist, not in stock
extras: set[str] = in_stock - wishlist           # in stock but not on wishlist

print(f"  In stock:      {sorted(in_stock)}")
print(f"  Wishlist:      {sorted(wishlist)}")
print(f"  Can get:       {sorted(available)}")
print(f"  Need elsewhere:{sorted(need_elsewhere)}")
print(f"  Not needed:    {sorted(extras)}")


if __name__ == "__main__":
    pass
