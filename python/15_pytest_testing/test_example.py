# ─────────────────────────────────────────────────────────────
#  Lesson 15 — Testing with pytest
#  Run: pytest test_example.py -v
#  Install: pip install pytest
# ─────────────────────────────────────────────────────────────

from pathlib import Path

import pytest


# ── CODE UNDER TEST ───────────────────────────────────────────
# In a real project these would live in a separate module.
# Inline here to keep the lesson self-contained.

def add(a: int, b: int) -> int:
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


def fizzbuzz(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


class Stack:
    def __init__(self) -> None:
        self._data: list = []

    def push(self, val) -> None:
        self._data.append(val)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if not self._data:
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


# ── BASIC TESTS ───────────────────────────────────────────────

def test_add_positive() -> None:
    assert add(2, 3) == 5


def test_add_negative() -> None:
    assert add(-4, -6) == -10


def test_add_zero() -> None:
    assert add(0, 100) == 100


def test_divide_normal() -> None:
    assert divide(10, 2) == 5.0


def test_divide_float() -> None:
    # Use pytest.approx for floating-point comparisons
    assert divide(1, 3) == pytest.approx(0.3333, rel=1e-3)


# ── TESTING EXCEPTIONS ────────────────────────────────────────

def test_divide_by_zero() -> None:
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(1, 0)


def test_stack_pop_empty() -> None:
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_stack_peek_empty() -> None:
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()


# ── FIXTURES ─────────────────────────────────────────────────

@pytest.fixture
def stack() -> Stack:
    """Fresh Stack for each test that requests it."""
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    return s


def test_stack_peek(stack: Stack) -> None:
    assert stack.peek() == 30


def test_stack_pop(stack: Stack) -> None:
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert len(stack) == 1


def test_stack_is_empty(stack: Stack) -> None:
    assert not stack.is_empty()
    stack.pop(); stack.pop(); stack.pop()
    assert stack.is_empty()


# ── PARAMETRIZE ───────────────────────────────────────────────

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (-10, -10, -20),
])
def test_add_parametrized(a: int, b: int, expected: int) -> None:
    assert add(a, b) == expected


@pytest.mark.parametrize("n, expected", [
    (1,  "1"),
    (3,  "Fizz"),
    (5,  "Buzz"),
    (15, "FizzBuzz"),
    (30, "FizzBuzz"),
    (7,  "7"),
    (9,  "Fizz"),
    (10, "Buzz"),
])
def test_fizzbuzz(n: int, expected: str) -> None:
    assert fizzbuzz(n) == expected


# ── BUILT-IN FIXTURES ─────────────────────────────────────────

def test_write_and_read_file(tmp_path: Path) -> None:
    """tmp_path provides a fresh temp directory per test."""
    f = tmp_path / "output.txt"
    f.write_text("hello pytest", encoding="utf-8")
    assert f.read_text(encoding="utf-8") == "hello pytest"


def test_multiple_files(tmp_path: Path) -> None:
    for i in range(3):
        (tmp_path / f"file_{i}.txt").write_text(str(i), encoding="utf-8")
    txt_files = list(tmp_path.glob("*.txt"))
    assert len(txt_files) == 3


def test_print_captured(capsys) -> None:
    """capsys captures stdout/stderr."""
    print("hello from test")
    captured = capsys.readouterr()
    assert "hello from test" in captured.out


def test_env_variable(monkeypatch) -> None:
    """monkeypatch sets env vars just for this test."""
    import os
    monkeypatch.setenv("MY_API_KEY", "test-secret")
    assert os.environ["MY_API_KEY"] == "test-secret"


# ── MARKS ─────────────────────────────────────────────────────

@pytest.mark.skip(reason="placeholder — not implemented yet")
def test_future_feature() -> None:
    assert False


@pytest.mark.xfail(reason="known issue: negative zero edge case", strict=False)
def test_known_edge_case() -> None:
    # This is expected to fail
    assert add(-0, 0) == 1   # wrong on purpose to demonstrate xfail
