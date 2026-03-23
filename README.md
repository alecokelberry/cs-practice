# cs-practice — Alec's CS Study Repo

A self-paced reference and practice repo built alongside my WGU BSCS program. Each folder is a structured mini-course — readable, runnable, and organized for quick review.

---

## Roadmap

| Folder | Language / Topic | Status |
|---|---|---|
| `cpp/` | C++ (modern C++20) | ✅ 17 lessons |
| `python/` | Python 3.12+ modern best practices | ✅ 18 lessons |
| `javascript/` | JavaScript | ✅ 9 lessons |
| `typescript/` | TypeScript | 🔜 Planned |
| `java/` | Java | 🔜 Planned |
| `sql/` | SQL | 🔜 Planned |
| `html/` | HTML | ✅ 5 lessons |
| `css/` | CSS | ✅ 7 lessons |
| `projects/` | Full-stack apps (React + FastAPI, etc.) | 🔜 Planned |
| `common-skills/` | Git, LeetCode patterns, REST, debugging, clean code | 🟡 In progress |

---

## C++ — `cpp/`

17 lessons covering modern C++20. Every lesson has a `README.md` and a `main.cpp` (lesson 17 is README-only).

**Run any lesson:**
```bash
g++ -std=c++20 main.cpp -o main && ./main
```

| # | Topic |
|---|---|
| 01 | Program structure, I/O, std::format |
| 02 | Types, uniform init, constexpr, auto |
| 03 | if/else, switch, ternary, [[fallthrough]] |
| 04 | while, for, do-while, range-for, ranges |
| 05 | std::array, std::vector, sorting, searching |
| 06 | Functions, pass by value/const&/ref, [[nodiscard]], lambdas |
| 07 | Classes, constructors, const methods, = default/delete |
| 08 | Raw pointers, nullptr, ->, non-owning use |
| 09 | unique\_ptr, shared\_ptr, weak\_ptr |
| 10 | RAII, destructors, lock\_guard, Rule of 0 |
| 11 | map, unordered\_map, set, unordered\_set, deque |
| 12 | sort, find, transform, accumulate, erase\_if, ranges |
| 13 | virtual, override, pure virtual, abstract classes |
| 14 | const correctness, constexpr, mutable |
| 15 | lvalue/rvalue, std::move, move constructor, Rule of 5 |
| 16 | Lambda captures, generic lambdas, function/class templates |
| 17 | CMake basics — README only |

---

## Python — `python/`

18 lessons covering modern Python 3.12+ only. One style: best practices. No school-vs-modern split.

**Run any lesson:**
```bash
python3 main.py
```

| # | Topic |
|---|---|
| 01 | Types, f-strings, match/case, walrus operator |
| 02 | for/while, enumerate, zip, comprehensions, generators, itertools |
| 03 | dict, defaultdict, Counter, set operations |
| 04 | try/except, custom exceptions, context managers, logging |
| 05 | class, @property, @dataclass, @staticmethod, @classmethod |
| 06 | Inheritance, ABC, Protocol, mixins, dunder methods |
| 07 | Stack, deque/queue, linked list, circular buffer |
| 08 | Search, sort, recursion, two-pointer, sliding window, Big-O |
| 09 | BFS, DFS, tree traversals, heapq, Dijkstra |
| 10 | Memoization, tabulation, Fibonacci, coin change, LCS, knapsack |
| 11 | venv, pip, requirements.txt, pyproject.toml — README only |
| 12 | Nested comprehensions, walrus, generator pipelines, advanced itertools |
| 13 | collections, pathlib, datetime, functools |
| 14 | File I/O, JSON, CSV, custom context managers, contextlib |
| 15 | pytest — fixtures, parametrize, tmp\_path, monkeypatch |
| 16 | Type hints — generics, Optional, TypeVar, Protocol, TypedDict |
| 17 | FastAPI — routes, Pydantic, path/query params, status codes |
| 18 | SQLAlchemy — ORM models, CRUD, relationships, raw SQL |

---

## JavaScript — `javascript/`

9 lessons covering modern JavaScript (ES2015+). Read-and-reference guides — no code files.

| # | Topic |
|---|---|
| 01 | Modern ES6+ basics — let/const, arrow functions, destructuring, spread |
| 02 | Array methods — map, filter, reduce, find, flat, sort |
| 03 | Objects, prototypes, and `this` — binding rules, class syntax |
| 04 | Closures and scope — lexical scope, hoisting, closure patterns |
| 05 | Async: Promises and fetch — Promise API, fetch, error handling |
| 06 | Async: async/await and the event loop — await, try/catch, microtasks |
| 07 | DOM manipulation and events — selecting, mutating, event delegation |
| 08 | Modules — import/export, dynamic import, ESM vs CommonJS |
| 09 | Error handling and debugging — try/catch, custom errors, console, debugger |

---

## HTML — `html/`

5 lessons covering HTML5 structure, forms, accessibility, SEO, and page layout. Read-and-reference guides — no code files.

| # | Topic |
|---|---|
| 01 | Document structure, semantic tags, links, images, lists |
| 02 | Forms, input types, labels, built-in validation |
| 03 | Accessibility, ARIA, keyboard navigation, focus |
| 04 | Meta tags, SEO, Open Graph, favicons |
| 05 | Page structure — header/nav/main/aside/footer, landmark regions |

---

## CSS — `css/`

7 lessons covering the layout systems, visual properties, and Tailwind used in modern web development. Read-and-reference guides.

| # | Topic |
|---|---|
| 01 | Box model, margin/padding, specificity, cascade |
| 02 | Flexbox — container and item properties, common patterns |
| 03 | CSS Grid — tracks, areas, auto-fit, minmax |
| 04 | Responsive design, media queries, mobile-first, fluid units |
| 05 | Positioning — static, relative, absolute, fixed, sticky |
| 06 | Variables, transitions, @keyframes animations |
| 07 | Tailwind — utility classes, responsive prefixes, dark mode |

---

## Common Skills — `common-skills/`

Language-agnostic skills every developer needs. See each folder for a detailed guide.

| Folder | Topic |
|---|---|
| `01_git_workflow/` | Git + GitHub — core workflow, branching, remotes, PRs |
| `02_leetcode_easy_medium/` | 50–80 curated problems with walkthroughs and patterns |
| `03_rest_api_basics/` | HTTP, REST, JSON, curl, status codes |
| `04_debugging_sanitizers/` | Debugging techniques, GDB, sanitizers |
| `05_clean_code_practices/` | Naming, functions, comments, SOLID basics |

---

## How This Repo Is Organized

Each language folder follows the same pattern:
- Numbered lesson folders (`01_topic/`)
- `README.md` — concept overview, syntax reference, pitfalls
- Runnable code file (`main.cpp`, `main.py`, etc.)

`common-skills/` uses the same structure but without code files — just READMEs you can read and reference.
