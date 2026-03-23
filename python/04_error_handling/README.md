# Lesson 04 — Error Handling

## What This Covers
Python's exception model: `try/except/else/finally`, catching multiple exceptions,
exception chaining, custom exception classes, `contextlib.suppress`, context managers
(`with`), writing your own context managers, and `logging` vs `print`.

---

## Key Concepts

### try / except / else / finally
```python
try:
    result = int(user_input)    # might raise ValueError
except ValueError:
    print("Not a valid number")
except (TypeError, OverflowError) as e:  # catch multiple at once
    print(f"Type problem: {e}")
else:
    # Runs ONLY if no exception was raised — use this for the "happy path"
    print(f"Got: {result}")
finally:
    # ALWAYS runs — cleanup code here (close files, release locks)
    print("Done, regardless of outcome")
```

The `else` clause is underused but powerful: it lets you separate "the operation" from
"what to do on success", making it clearer than stuffing everything in `try`.

---

### Specific Exception Types
Always catch the most specific exception you can. Bare `except:` and `except Exception:`
hide bugs.

| Exception | Raised when |
|-----------|------------|
| `ValueError` | Right type, wrong value (`int("abc")`) |
| `TypeError` | Wrong type (`1 + "a"`) |
| `KeyError` | Dict key doesn't exist |
| `IndexError` | List index out of range |
| `AttributeError` | Object doesn't have that attribute |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Division by zero |
| `StopIteration` | Iterator exhausted |
| `RuntimeError` | General runtime error |

---

### Exception Chaining — raise X from Y
When you catch one exception and raise another, use `raise NewError(...) from original_error`.
This preserves the original traceback and makes debugging much easier.

```python
try:
    with open("config.json") as f:
        data = json.load(f)
except FileNotFoundError as e:
    raise RuntimeError("Config file is missing — cannot start") from e
    # The traceback shows BOTH: why you're raising AND the original cause
```

Use `raise X from None` to deliberately suppress the chain (rare — only when the original
error is irrelevant to the caller).

---

### Custom Exception Classes
Define your own exception hierarchy for your application. It lets callers catch your errors
specifically without catching unrelated exceptions.

```python
class AppError(Exception):
    """Base exception for this application."""
    pass

class ValidationError(AppError):
    """Input failed validation."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation failed for {field!r}: {message}")

class DatabaseError(AppError):
    """Database operation failed."""
    pass
```

Callers can `except AppError` to catch all app errors, or `except ValidationError` to
catch only validation failures.

---

### contextlib.suppress
When you genuinely don't care if an operation fails (and that's intentional, not lazy),
`suppress` is cleaner than a try/except block.

```python
from contextlib import suppress

# Instead of:
try:
    os.remove("temp.txt")
except FileNotFoundError:
    pass   # didn't exist, that's fine

# Write:
with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

Only use this when "it's okay if this fails" is genuinely the right policy.

---

### The with Statement (Context Managers)
`with` guarantees cleanup even if an exception is raised. The context manager's
`__exit__` method is called whether the block succeeds or fails.

```python
# File handling — the canonical example
with open("data.txt", "r") as f:
    content = f.read()
# f.close() is called automatically here — even if read() raised

# Multiple context managers (Python 3.10+ parenthesized form)
with (
    open("input.txt") as infile,
    open("output.txt", "w") as outfile,
):
    outfile.write(infile.read())
```

---

### Writing Your Own Context Manager
Use `@contextlib.contextmanager` and `yield` to write a context manager as a simple
generator function. The code before `yield` is setup; after `yield` is teardown.

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield                        # caller's 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f}s")

with timer("my operation"):
    do_something()
```

---

### logging vs print
`print` is for the user. `logging` is for the developer and ops team.

```python
import logging

# Configure once at module/app startup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)  # use the module name as logger name

logger.debug("Detailed info for debugging")
logger.info("Normal operation info")
logger.warning("Something unexpected but not fatal")
logger.error("Something failed")
logger.exception("Error with full traceback — call inside except block")
```

Levels (lowest to highest): DEBUG → INFO → WARNING → ERROR → CRITICAL.
Set `level=logging.WARNING` in production to suppress debug output.

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `try: ... except E:` | Catch specific exception E |
| `except (E1, E2) as e:` | Catch either exception, bind to e |
| `else:` after except | Runs only if no exception raised |
| `finally:` | Always runs — cleanup |
| `raise` | Re-raise the current exception |
| `raise E from orig` | Raise E, chain orig as cause |
| `raise E from None` | Raise E, suppress chain |
| `with suppress(E):` | Silently ignore exception E |
| `with open(...) as f:` | Context manager |
| `@contextmanager` | Make a generator a context manager |
| `logger.exception(msg)` | Log error with full traceback |

---

## Common Pitfalls

- **Bare `except:`** catches `SystemExit`, `KeyboardInterrupt`, and everything else — almost always wrong. Use `except Exception:` at minimum, specific types ideally.
- **Catching `Exception` and ignoring it** — same problem as bare except. Log it at minimum.
- **`finally` always runs, even if `return` is in `try`** — don't use `return` or assignment in `finally` as it overrides the `try` return value.
- **Forgetting `from e` in exception chains** — you lose the root cause traceback, which makes debugging painful.
- **Using `print` for errors** — it goes to stdout, not stderr, and disappears in production. Use `logging`.
- **Creating custom exceptions without calling `super().__init__`** — the message won't appear in tracebacks.

---

## When to Use What

| Situation | Use |
|-----------|-----|
| Operation might fail, you handle the failure | `try/except` |
| Genuinely optional operation, failure is fine | `contextlib.suppress` |
| Any resource needing cleanup | `with` statement |
| Code that provides setup/teardown | `@contextmanager` |
| Re-raising with more context | `raise NewError(...) from original` |
| Debug/operational messages | `logging` |
| Output to the user | `print` |
