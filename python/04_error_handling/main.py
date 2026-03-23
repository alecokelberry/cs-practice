# ─────────────────────────────────────────────────────────────
#  Lesson 04 — Error Handling
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import logging
import time
from contextlib import contextmanager, suppress
from typing import Generator


# Set up logging once at the top — in a real app this goes in your entry point.
# %(name)s is the logger name — using __name__ means it shows which module logged it.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ── BASIC TRY / EXCEPT ────────────────────────────────────────
print("── try / except ─────────────────────────────")

def safe_divide(a: float, b: float) -> float | None:
    """Divide a by b, returning None if division is impossible."""
    try:
        result = a / b
    except ZeroDivisionError:
        # Catch the specific exception — not bare except, not Exception
        logger.warning("Division by zero attempted: %s / %s", a, b)
        return None
    return result

print(f"  10 / 2  = {safe_divide(10, 2)}")
print(f"  10 / 0  = {safe_divide(10, 0)}")


# ── TRY / EXCEPT / ELSE / FINALLY ────────────────────────────
print("\n── try / except / else / finally ────────────")

def parse_integer(text: str) -> int | None:
    """
    Convert a string to int.

    The else clause runs only on success — it separates 'the risky operation'
    from 'what to do when it worked', which is cleaner than putting everything in try.
    """
    try:
        value = int(text)           # might raise ValueError
    except ValueError as e:
        logger.debug("Could not parse %r as int: %s", text, e)
        return None
    else:
        # Only runs if NO exception was raised in try
        logger.debug("Successfully parsed %r → %d", text, value)
        return value
    finally:
        # ALWAYS runs — even if try had a return, even if except re-raised
        # Use for cleanup: close files, release locks, etc.
        logger.debug("parse_integer called with %r (done)", text)

print(f"  parse('42'):   {parse_integer('42')}")
print(f"  parse('abc'):  {parse_integer('abc')}")
print(f"  parse('3.14'): {parse_integer('3.14')}")  # float string → ValueError


# ── CATCHING MULTIPLE EXCEPTIONS ─────────────────────────────
print("\n── multiple exceptions ──────────────────────")

def safe_lookup(data: dict, key: str, index: int) -> str:
    """Safely look up data[key][index]."""
    try:
        return str(data[key][index])
    except KeyError:
        return f"<no key {key!r}>"
    except IndexError:
        return f"<index {index} out of range>"
    except TypeError as e:
        # TypeError if data[key] isn't subscriptable
        return f"<type error: {e}>"

sample: dict[str, list[int]] = {"scores": [90, 85, 92]}
print(f"  scores[1]:    {safe_lookup(sample, 'scores', 1)}")
print(f"  scores[99]:   {safe_lookup(sample, 'scores', 99)}")
print(f"  missing[0]:   {safe_lookup(sample, 'missing', 0)}")

# Catch two exception types in a single except clause
def risky(x: object) -> int:
    """Demonstrate catching multiple types at once."""
    try:
        return int(x) // int(x)    # type: ignore[arg-type]
    except (ValueError, ZeroDivisionError) as e:
        # Both errors handled the same way — tuple syntax
        print(f"  caught {type(e).__name__}: {e}")
        return -1

risky(0)        # ZeroDivisionError
risky("abc")    # ValueError


# ── EXCEPTION CHAINING ────────────────────────────────────────
print("\n── exception chaining ───────────────────────")

# When you catch one exception and raise another, use 'raise New from Original'.
# This preserves the full traceback chain — crucial for debugging.

class ConfigError(Exception):
    """Application configuration problem."""
    pass

def load_config(path: str) -> dict[str, str]:
    """Load config from a file path."""
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError as e:
        # Wrap the low-level OS error in a domain-specific error.
        # 'from e' means "this error was CAUSED by e" — both show in traceback.
        raise ConfigError(f"Config file not found: {path!r}") from e
    except Exception as e:
        raise ConfigError(f"Could not load config from {path!r}") from e

try:
    load_config("/nonexistent/config.json")
except ConfigError as e:
    print(f"  ConfigError: {e}")
    print(f"  Caused by:   {e.__cause__}")  # the original FileNotFoundError


# ── CUSTOM EXCEPTION CLASSES ──────────────────────────────────
print("\n── custom exceptions ────────────────────────")

# Build an exception hierarchy for your application.
# Callers can catch AppError to get all app errors,
# or ValidationError to be specific.

class AppError(Exception):
    """Base exception for this application."""
    pass

class ValidationError(AppError):
    """Input data failed validation."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        # Always call super().__init__ — it populates args, which shows in tracebacks
        super().__init__(f"Validation failed for {field!r}: {message}")

class NotFoundError(AppError):
    """Requested resource does not exist."""
    def __init__(self, resource: str, identifier: object) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier!r}")

def validate_age(age: int) -> None:
    """Raise ValidationError if age is invalid."""
    if age < 0:
        raise ValidationError("age", "must be non-negative")
    if age > 150:
        raise ValidationError("age", "must be ≤ 150")

def find_user(user_id: int) -> dict[str, str | int]:
    """Simulate user lookup — raises NotFoundError if missing."""
    users = {1: {"name": "Alice", "age": 30}, 2: {"name": "Bob", "age": 25}}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

# Test the hierarchy
for test in [(-5, 1), (25, 1), (25, 99)]:
    age, uid = test
    try:
        validate_age(age)
        user = find_user(uid)
        print(f"  age={age}, uid={uid} → OK: {user}")
    except ValidationError as e:
        print(f"  ValidationError ({e.field}): {e.message}")
    except NotFoundError as e:
        print(f"  NotFoundError: {e.resource} {e.identifier!r}")
    except AppError as e:
        print(f"  AppError: {e}")   # catches any other app error


# ── CONTEXTLIB.SUPPRESS ───────────────────────────────────────
print("\n── contextlib.suppress ──────────────────────")

import os

# suppress() is cleaner than try/except/pass for "I don't care if this fails"
# Only use it when failure is genuinely acceptable — not as a lazy shortcut

# Cleanup a temp file — it's fine if it wasn't there
temp_path = "/tmp/cs_practice_test_delete_me.txt"
with open(temp_path, "w") as f:
    f.write("temp")

with suppress(FileNotFoundError):
    os.remove(temp_path)
    print("  Removed temp file")

with suppress(FileNotFoundError):
    os.remove(temp_path)  # already gone — suppressed, no crash
    print("  This won't print")

print("  (second remove silently suppressed)")


# ── WITH STATEMENT AND CONTEXT MANAGERS ───────────────────────
print("\n── with statement ───────────────────────────")

# 'with' guarantees __exit__ is called — even if an exception occurs inside.
# File objects implement __enter__/__exit__, so open() works with with.

# Writing to a file
test_file = "/tmp/cs_practice_context_test.txt"
with open(test_file, "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")
# f is automatically closed here — no need for f.close()

# Reading it back
with open(test_file) as f:
    lines = f.readlines()

print(f"  Read {len(lines)} lines from file:")
for line in lines:
    print(f"    {line!r}")

# Clean up
with suppress(FileNotFoundError):
    os.remove(test_file)


# ── CUSTOM CONTEXT MANAGER ────────────────────────────────────
print("\n── custom context manager ───────────────────")

# @contextmanager turns a generator function into a context manager.
# Code BEFORE yield = __enter__ (setup)
# Code AFTER yield  = __exit__ (teardown) — always runs due to try/finally

@contextmanager
def timer(label: str) -> Generator[None, None, None]:
    """Context manager that measures and prints elapsed time."""
    logger.debug("Starting: %s", label)
    start = time.perf_counter()
    try:
        yield               # the caller's 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        # finally guarantees cleanup even if the with block raised an exception
        print(f"  {label}: {elapsed * 1000:.2f}ms")

with timer("list comprehension"):
    result = [x ** 2 for x in range(100_000)]

with timer("generator + sum"):
    total = sum(x ** 2 for x in range(100_000))

print(f"  (results match: {result[-1] == (99_999 ** 2)})")


@contextmanager
def managed_resource(name: str) -> Generator[dict, None, None]:
    """Simulate acquiring and releasing a resource."""
    resource: dict[str, str] = {}
    print(f"  Acquiring {name}...")
    try:
        resource["name"] = name
        resource["status"] = "active"
        yield resource          # caller gets access to 'resource'
    except Exception as e:
        print(f"  Error while using {name}: {e}")
        raise                   # re-raise so the caller knows something failed
    finally:
        resource["status"] = "released"
        print(f"  Released {name} (status={resource['status']!r})")

with managed_resource("database connection") as conn:
    print(f"  Using: {conn}")


# ── LOGGING ───────────────────────────────────────────────────
print("\n── logging ──────────────────────────────────")

# logging vs print:
#   print  → goes to stdout, disappears in production, no timestamps
#   logging → goes to stderr by default, has levels, configurable, persistent

def process_batch(items: list[int]) -> list[int]:
    """Process a batch of items, logging progress at each level."""
    logger.info("Starting batch of %d items", len(items))

    results: list[int] = []
    for item in items:
        logger.debug("Processing item: %d", item)   # usually suppressed in prod
        if item < 0:
            logger.warning("Negative item encountered: %d — skipping", item)
            continue
        try:
            # Simulate a risky operation
            if item == 0:
                raise ValueError("Cannot process zero")
            results.append(item * 10)
        except ValueError as e:
            # logger.exception() logs ERROR + the full traceback automatically
            logger.exception("Failed to process item %d", item)
            # Continue processing other items

    logger.info("Batch complete: %d/%d succeeded", len(results), len(items))
    return results

batch = [1, -2, 3, 0, 5, -1, 7]
output = process_batch(batch)
print(f"\n  Input:  {batch}")
print(f"  Output: {output}")

# Log levels (lowest → highest): DEBUG → INFO → WARNING → ERROR → CRITICAL
# Setting level=WARNING in production suppresses DEBUG and INFO automatically


if __name__ == "__main__":
    pass
