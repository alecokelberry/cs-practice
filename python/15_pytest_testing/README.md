# Lesson 15 — Testing with pytest

## Overview

`pytest` is the standard Python testing framework. It finds tests automatically, gives readable failure messages, and has a rich plugin ecosystem. This lesson covers writing tests, using fixtures, parametrizing test cases, and organizing a test suite.

---

## Install

```bash
pip install pytest
```

---

## Running Tests

```bash
pytest                        # discover and run all tests in current directory
pytest test_example.py        # run a specific file
pytest test_example.py::test_add  # run one test
pytest -v                     # verbose — show each test name
pytest -x                     # stop at first failure
pytest -k "add or subtract"   # run tests matching the name pattern
pytest --tb=short             # shorter traceback on failures
```

---

## Writing Tests

Test functions start with `test_`. pytest discovers them automatically:

```python
# test_math.py

def add(a: int, b: int) -> int:
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5
```

pytest's `assert` gives detailed failure messages automatically — no need for `assertEqual` or other assert helpers.

---

## Testing Exceptions

```python
import pytest

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(1, 0)
```

---

## Fixtures — Reusable Setup

A fixture is a function decorated with `@pytest.fixture`. pytest injects it by name into test parameters:

```python
import pytest

@pytest.fixture
def sample_data() -> list[int]:
    """Provide a fresh list for each test that requests it."""
    return [3, 1, 4, 1, 5, 9, 2, 6]

def test_max(sample_data: list[int]) -> None:
    assert max(sample_data) == 9

def test_min(sample_data: list[int]) -> None:
    assert min(sample_data) == 1

def test_sorted(sample_data: list[int]) -> None:
    assert sorted(sample_data) == [1, 1, 2, 3, 4, 5, 6, 9]
```

### Fixture Scopes

| Scope | When the fixture runs |
|-------|-----------------------|
| `"function"` (default) | Once per test function |
| `"class"` | Once per test class |
| `"module"` | Once per test file |
| `"session"` | Once per entire test run |

```python
@pytest.fixture(scope="module")
def db_connection():
    conn = create_connection()
    yield conn       # use yield to provide teardown
    conn.close()     # teardown runs after all tests in the module
```

---

## Parametrize — Multiple Inputs in One Test

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected
```

This runs the test 4 times with different inputs. Each case shows up separately in the output.

---

## Built-in Fixtures

### `tmp_path` — Temporary Directory

```python
from pathlib import Path

def test_write_file(tmp_path: Path) -> None:
    f = tmp_path / "output.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"
```

`tmp_path` provides a fresh temporary directory per test — no cleanup needed.

### `capsys` — Capture stdout/stderr

```python
def test_print_output(capsys) -> None:
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

### `monkeypatch` — Patch Attributes, Env Vars, and More

```python
def test_env_var(monkeypatch) -> None:
    monkeypatch.setenv("API_KEY", "test-key")
    import os
    assert os.environ["API_KEY"] == "test-key"
```

---

## Test Organization

```
my-project/
├── src/
│   └── my_package/
│       └── utils.py
└── tests/
    ├── conftest.py         ← shared fixtures available to all tests
    ├── test_utils.py
    └── test_models.py
```

`conftest.py` — put fixtures here to share them across all test files without importing:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def client():
    ...  # shared test client setup
```

---

## Marks — Skip, xfail, and Custom

```python
import pytest

@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    ...

@pytest.mark.xfail(reason="known bug #42")
def test_known_broken():
    assert False   # expected to fail

@pytest.mark.slow            # custom mark — run with: pytest -m slow
def test_heavy_computation():
    ...
```

Register custom marks in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
markers = ["slow: marks tests as slow"]
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Test file not named `test_*.py` | pytest only discovers files matching `test_*.py` or `*_test.py` |
| Test function not named `test_*` | pytest only collects functions starting with `test_` |
| Sharing mutable state between tests | Use fixtures — each test gets a fresh copy |
| Asserting with `==` on floats | Use `pytest.approx`: `assert result == pytest.approx(0.1 + 0.2)` |
| `assert x == True` | Write `assert x` instead — more readable |
| Fixtures with scope="session" for mutable state | Higher-scope fixtures are shared — mutation in one test affects others |

---

## Quick Reference Card

```bash
# Run
pytest -v                          # verbose
pytest -x                          # stop at first failure
pytest -k "pattern"                # filter by name
pytest --tb=short                  # shorter tracebacks
```

```python
# Basic test
def test_something():
    assert result == expected

# Expect exception
with pytest.raises(SomeError, match="message"):
    risky_function()

# Fixture
@pytest.fixture
def resource():
    setup = create()
    yield setup      # teardown below yield
    cleanup(setup)

# Parametrize
@pytest.mark.parametrize("input, expected", [(1, 2), (2, 4)])
def test_double(input, expected):
    assert double(input) == expected

# Approx floats
assert result == pytest.approx(0.3, rel=1e-6)

# Built-in fixtures
def test_files(tmp_path): ...        # temp dir
def test_output(capsys): ...         # capture stdout
def test_env(monkeypatch): ...       # patch env/attrs
```
