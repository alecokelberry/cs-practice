# Python Reference Course

A personal reference course covering modern Python best practices as of 2026 (Python 3.12/3.13).
Built for someone who knows programming basics and wants to write Python the *right* way — one style, the best style.

---

## How to Use This

Each lesson has:
- **README.md** — concept explanations, syntax tables, pitfalls
- **main.py** — runnable code demonstrating everything, heavily commented

Run any lesson with:
```bash
python3 main.py
```

All files require Python 3.12+. Exceptions:
- Lesson 11 — README only (venv/packaging can't be demonstrated in a single script)
- Lesson 15 — `test_example.py` instead of `main.py` (run with `pytest test_example.py -v`)
- Lesson 17 — `app.py` instead of `main.py` (run with `uvicorn app:app --reload`)

---

## Lessons

| # | Folder | Topic |
|---|--------|-------|
| 01 | `01_basics/` | Variables, types, f-strings, match/case, walrus operator |
| 02 | `02_loops_sequences/` | for/while, range, enumerate, zip, comprehensions, generators |
| 03 | `03_dicts_sets/` | dicts, defaultdict, Counter, sets, frozenset |
| 04 | `04_error_handling/` | try/except/else/finally, custom exceptions, context managers, logging |
| 05 | `05_classes_objects/` | class, __init__, properties, dataclasses |
| 06 | `06_oop/` | Inheritance, ABC, Protocol, mixins, dunder methods |
| 07 | `07_linear_data_structures/` | Stack, queue, deque, linked list |
| 08 | `08_algorithms/` | Search, sort, recursion, two-pointer, sliding window, Big-O |
| 09 | `09_graphs_trees/` | BFS, DFS, binary trees, heapq, Dijkstra |
| 10 | `10_dynamic_programming/` | Memoization, tabulation, classic DP problems |
| 11 | `11_venv_packaging/` | venv, pip, requirements.txt, pyproject.toml |
| 12 | `12_comprehensions_generators/` | Nested comprehensions, walrus, generator pipelines, advanced itertools |
| 13 | `13_stdlib_modules/` | collections, pathlib, datetime, functools |
| 14 | `14_file_io_context_managers/` | open(), JSON, CSV, custom context managers, contextlib |
| 15 | `15_pytest_testing/` | pytest, fixtures, parametrize, tmp_path, capsys, monkeypatch |
| 16 | `16_type_hints/` | Annotations, generics, Optional/Union, TypeVar, Protocol, TypedDict |
| 17 | `17_fastapi_basics/` | REST routes, Pydantic models, path/query params, status codes |
| 18 | `18_sqlalchemy_sql_basics/` | Engine, session, ORM models, CRUD, relationships, raw SQL |

---

## Modern Python Standards Used Throughout

- **Type hints** with built-in generics (`list[int]`, `dict[str, int]`, not `List`, `Dict`)
- **f-strings** for all string formatting
- **`@dataclass`** for data-holding classes
- **`match/case`** for structural pattern matching
- **Walrus operator** `:=` where it genuinely helps
- **`collections.deque`**, **`Counter`**, **`defaultdict`** — stdlib first
- **`functools.cache`** for memoization
- **`abc.ABC`** and **`Protocol`** for abstractions
- **Docstrings** on all functions and classes
- **`if __name__ == "__main__":` guard** in every main.py
- No bare `except:` — always catch specific exceptions

---

## Prerequisites

You should know: variables, functions, basic loops, conditionals. That's it.
