# ─────────────────────────────────────────────────────────────
#  Lesson 14 — File I/O & Context Managers
#  Run: python3 main.py
# ─────────────────────────────────────────────────────────────

import csv
import json
import time
from contextlib import contextmanager, suppress
from pathlib import Path

# Working directory for temp files
HERE = Path(__file__).parent


# ── TEXT FILES ────────────────────────────────────────────────
print("── Text File I/O ────────────────────────────────────")

# Write a text file
txt_path = HERE / "_demo.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("line one\n")
    f.write("line two\n")
    f.write("line three\n")
print(f"  wrote {txt_path.name}")

# Read entire file
with open(txt_path, encoding="utf-8") as f:
    content = f.read()
print(f"  read entire file:\n{content}", end="")

# Read line by line — efficient for large files
print("  iterate line by line:")
with open(txt_path, encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"    {i}: {line.rstrip()}")

# Append
with open(txt_path, "a", encoding="utf-8") as f:
    f.write("line four (appended)\n")
print("  appended line four")

# pathlib shorthand — simpler for full reads/writes
content2 = txt_path.read_text(encoding="utf-8")
print(f"  pathlib read_text lines: {content2.count(chr(10))}")


# ── JSON ──────────────────────────────────────────────────────
print("\n── JSON ─────────────────────────────────────────────")

json_path = HERE / "_demo.json"

# Write JSON
data = {
    "name": "Alice",
    "scores": [95, 88, 72],
    "active": True,
    "address": None,
}
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(f"  wrote {json_path.name}")

# Read JSON
with open(json_path, encoding="utf-8") as f:
    loaded = json.load(f)
print(f"  loaded name: {loaded['name']}, scores: {loaded['scores']}")

# String round-trip (no file)
serialized = json.dumps(data, indent=2)
parsed = json.loads(serialized)
print(f"  round-trip active: {parsed['active']}, address: {parsed['address']}")


# ── CSV ───────────────────────────────────────────────────────
print("\n── CSV ──────────────────────────────────────────────")

csv_path = HERE / "_demo.csv"

# Write rows
students = [
    {"name": "Alice", "grade": "A", "score": 95},
    {"name": "Bob",   "grade": "B", "score": 82},
    {"name": "Carol", "grade": "A", "score": 91},
]
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "grade", "score"])
    writer.writeheader()
    writer.writerows(students)
print(f"  wrote {csv_path.name}")

# Read as dicts
with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']}: {row['grade']} ({row['score']})")


# ── CUSTOM CONTEXT MANAGER (class-based) ──────────────────────
print("\n── Custom Context Manager (class) ───────────────────")


class LoggedSection:
    """Context manager that prints when entering and exiting a section."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> "LoggedSection":
        print(f"  [{self.name}] entering")
        return self   # value of `as` target

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type:
            print(f"  [{self.name}] exiting with error: {exc_val}")
        else:
            print(f"  [{self.name}] exiting cleanly")
        return False  # do not suppress exceptions


with LoggedSection("demo") as section:
    print(f"  inside section, got: {section.name!r}")

# Show that __exit__ runs even when an exception occurs
try:
    with LoggedSection("error case"):
        raise ValueError("something went wrong")
except ValueError:
    print("  caught the ValueError after __exit__ ran")


# ── CONTEXTLIB: @contextmanager ───────────────────────────────
print("\n── @contextmanager ──────────────────────────────────")


@contextmanager
def timer(label: str):
    """Measure and print elapsed time for a block of code."""
    start = time.perf_counter()
    try:
        yield   # code inside `with` runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed * 1000:.2f}ms")


with timer("sum 1M"):
    total = sum(range(1_000_000))
    print(f"  sum result: {total}")


# ── CONTEXTLIB: suppress ──────────────────────────────────────
print("\n── contextlib.suppress ──────────────────────────────")

missing = HERE / "_does_not_exist.txt"

# Without suppress — need explicit try/except
try:
    missing.unlink()
except FileNotFoundError:
    print("  FileNotFoundError caught manually")

# With suppress — cleaner for expected/ignorable errors
with suppress(FileNotFoundError):
    missing.unlink()
print("  suppress(FileNotFoundError): no crash on missing file")


# ── CLEANUP ───────────────────────────────────────────────────
for tmp in [txt_path, json_path, csv_path]:
    with suppress(FileNotFoundError):
        tmp.unlink()
print("\n  cleaned up temp files")
