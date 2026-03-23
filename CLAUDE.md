# CLAUDE.md — cs-practice

This is a personal study repo for Alec, a WGU BSCS student. It's used to build self-paced reference material and practice code across languages.

---

## Who I Am

- WGU BSCS student — early in the program
- Only C++ course completed so far: **C867 (Scripting & Programming - C++)**
- Learning Python (via freeCodeCamp), and eventually Java and TypeScript
- Not a professional developer — treat explanations accordingly

---

## Repo Structure

```
cs-practice/
├── cpp/             ← C++ reference course (17 lessons, modern C++20)
├── python/          ← Python reference course (10 lessons, modern Python 3.12+)
├── javascript/      ← JavaScript reference course (9 lessons, modern ES2015+)
├── typescript/      ← Planned
├── java/            ← Planned
├── sql/             ← Planned
├── html/            ← HTML reference course (5 lessons)
├── css/             ← CSS reference course (7 lessons)
├── projects/        ← Full-stack apps (planned)
├── common-skills/   ← Language-agnostic developer skills (in progress)
└── CLAUDE.md
```

---

## C++ Lessons — How They're Structured

Every lesson lives in `cpp/0N_topic/` and contains:
- `README.md` — concept overview, syntax reference, common pitfalls, quick reference card
- `main.cpp` — working code with inline comments (lesson 17 is README-only)

One style only: modern C++20 best practices.

All files compile with:
```bash
g++ -std=c++20 main.cpp -o main && ./main
```

The 17 current lessons:
1. `01_introduction` — program structure, I/O, std::format
2. `02_variables` — types, uniform init, constexpr, auto
3. `03_branches` — if/else, switch, ternary, [[fallthrough]]
4. `04_loops` — while, for, do-while, range-for, ranges
5. `05_arrays_vectors` — std::array, std::vector, sorting, searching
6. `06_functions` — pass by value/const&/ref, [[nodiscard]], lambdas
7. `07_classes` — constructors, member init list, const methods, = default/delete
8. `08_pointers` — raw pointers, nullptr, ->, non-owning use
9. `09_smart_pointers` — unique_ptr, shared_ptr, weak_ptr
10. `10_raii_memory_management` — RAII, destructors, lock_guard, Rule of 0
11. `11_stl_containers` — map, unordered_map, set, unordered_set, deque
12. `12_stl_algorithms` — sort, find, transform, accumulate, erase_if, ranges
13. `13_oop_inheritance_polymorphism` — virtual, override, pure virtual, abstract classes
14. `14_const_correctness` — const correctness, constexpr, mutable
15. `15_move_semantics_rule_of_5` — lvalue/rvalue, std::move, move constructor, Rule of 5
16. `16_lambdas_templates_basics` — lambda captures, generic lambdas, function/class templates
17. `17_cmake_basics` — CMakeLists.txt, targets, FetchContent (README only)

---

## Python Lessons — How They're Structured

Every lesson lives in `python/0N_topic/` and contains:
- `README.md` — concept overview, syntax quick reference, common pitfalls, when-to-use guidance
- `main.py` — runnable code demonstrating all concepts with section headers and inline comments

```python
# ── SECTION NAME ─────────────────────────────────────────────
```

All files run with:
```bash
python3 main.py
```

Unlike C++, Python has **one style only** — modern best practices (Python 3.12+). No school vs modern split.

Some lessons deviate from the standard `main.py` convention:
- Lesson 11 — README only (venv/packaging can't be demonstrated in a script)
- Lesson 15 — `test_example.py` (run with `pytest test_example.py -v`)
- Lesson 17 — `app.py` (run with `uvicorn app:app --reload`)

The 18 current lessons:
1. `01_basics` — types, f-strings, match/case, walrus operator
2. `02_loops_sequences` — for/while, enumerate, zip, comprehensions, generators, itertools
3. `03_dicts_sets` — dict, defaultdict, Counter, set operations
4. `04_error_handling` — try/except, custom exceptions, context managers, logging
5. `05_classes_objects` — class, @property, @dataclass, staticmethod, classmethod
6. `06_oop` — inheritance, ABC, Protocol, mixins, dunder methods
7. `07_linear_data_structures` — stack, deque/queue, linked list
8. `08_algorithms` — search, sort, recursion, two-pointer, sliding window, Big-O
9. `09_graphs_trees` — BFS, DFS, tree traversals, heapq, Dijkstra
10. `10_dynamic_programming` — memoization, tabulation, Fibonacci, coin change, LCS, knapsack
11. `11_venv_packaging` — venv, pip, requirements.txt, pyproject.toml (README only)
12. `12_comprehensions_generators` — nested comprehensions, walrus, generator pipelines, advanced itertools
13. `13_stdlib_modules` — collections, pathlib, datetime, functools
14. `14_file_io_context_managers` — open(), JSON, CSV, custom context managers, contextlib
15. `15_pytest_testing` — pytest, fixtures, parametrize, tmp_path, capsys, monkeypatch
16. `16_type_hints` — annotations, generics, Optional/Union, TypeVar, Protocol, TypedDict
17. `17_fastapi_basics` — FastAPI routes, Pydantic models, path/query params, status codes
18. `18_sqlalchemy_sql_basics` — engine, session, ORM models, CRUD, relationships, raw SQL

---

## HTML Lessons — How They're Structured

Every lesson lives in `html/0N_topic/` and contains:
- `README.md` — concept overview, tag/attribute reference, common pitfalls, quick reference card

No runnable code files — read-and-reference guides only.

The 5 current lessons:
1. `01_basics_semantic_tags` — document structure, semantic elements, links, images, lists
2. `02_forms_inputs_validation` — form elements, input types, labels, built-in validation
3. `03_accessibility_aria` — ARIA roles/states, keyboard nav, focus, skip links
4. `04_meta_tags_seo` — charset, viewport, description, Open Graph, canonical, favicons
5. `05_structuring_a_page` — header/nav/main/aside/footer, landmark regions, heading hierarchy

---

## CSS Lessons — How They're Structured

Every lesson lives in `css/0N_topic/` and contains:
- `README.md` — concept overview, property reference, common pitfalls, quick reference card

No runnable code files — read-and-reference guides only.

The 7 current lessons:
1. `01_box_model_specificity` — box model, box-sizing, margin/padding, specificity, cascade
2. `02_flexbox` — flex container/item properties, alignment, common patterns
3. `03_css_grid` — grid tracks, areas, auto-fit/minmax, placement
4. `04_responsive_media_queries` — mobile-first, breakpoints, fluid units, clamp(), responsive images
5. `05_positioning` — static, relative, absolute, fixed, sticky, z-index
6. `06_variables_transitions_animations` — custom properties, transition, @keyframes, animation
7. `07_tailwind_basics` — utility classes, spacing scale, responsive prefixes, state variants

---

## JavaScript Lessons — How They're Structured

Every lesson lives in `javascript/0N_topic/` and contains:
- `README.md` — concept overview, syntax reference, common pitfalls, quick reference card

No runnable code files — read-and-reference guides only.

The 9 current lessons:
1. `01_modern_es6_basics` — let/const, arrow functions, destructuring, spread, optional chaining
2. `02_arrays_methods` — map, filter, reduce, find, some/every, flat, sort
3. `03_objects_prototypes_this` — object literals, Object methods, prototype chain, this binding, class syntax
4. `04_closures_scope` — var/let/const scope, hoisting, lexical scope, closure patterns, IIFE
5. `05_async_promises_fetch` — Promise states, .then/.catch, Promise.all/allSettled, fetch API
6. `06_async_await_event_loop` — async/await, try/catch, parallel vs sequential, event loop model
7. `07_dom_manipulation_events` — querySelector, textContent/innerHTML, classList, addEventListener, event delegation
8. `08_modules_import_export` — named/default exports, re-exports, barrel files, dynamic import(), ESM vs CJS
9. `09_error_handling_debugging` — try/catch/finally, custom Error classes, console methods, debugger

---

## Common Skills — How They're Structured

Every topic lives in `common-skills/0N_topic/` and contains:
- `README.md` — concept overview, command/syntax reference, common pitfalls, quick reference card

No runnable code files — these are read-and-reference guides only.

The 5 planned topics:
1. `01_git_workflow` — Git + GitHub: core workflow, branching, remotes, PRs ✅
2. `02_leetcode_easy_medium` — 50–80 curated problems with walkthroughs and patterns
3. `03_rest_api_basics` — HTTP, REST, JSON, curl, status codes
4. `04_debugging_sanitizers` — Debugging techniques, GDB, sanitizers
5. `05_clean_code_practices` — Naming, functions, comments, SOLID basics

---

## Guidelines for New Lessons or Changes

### C++ lessons
- **Match the existing format** — README.md + main.cpp per folder, numbered prefix
- **One style only** — modern C++20 best practices; no legacy/C867 split
- **All code must compile** — verify with `g++ -std=c++20` before finishing
- **Explain the why, not just the what** — comments and README entries should explain *why* a pattern is used
- **End each README with a quick reference card**

### Python lessons
- **One style only** — modern Python 3.12+ best practices
- **All code must run** — verify with `python3 main.py` before finishing
- **Use type hints everywhere** — built-in generics (`list[int]`, not `List[int]`)
- **f-strings for formatting**, `@dataclass` for data classes, `@functools.cache` for memoization
- **Keep it beginner-friendly** — Alec is learning Python via freeCodeCamp; explain non-obvious concepts

### JavaScript lessons
- **README only** — no code files; these are read-and-reference guides
- **Match the numbered folder format** — `0N_topic/README.md`
- **End each guide with a quick reference card**
- **Modern JS only** — ES2015+; no `var`, no callbacks without context, no jQuery
- **Beginner-friendly explanations** — mental model first, then reference, then pitfalls

### HTML & CSS lessons
- **README only** — no code files; these are read-and-reference guides
- **Match the numbered folder format** — `0N_topic/README.md`
- **End each guide with a quick reference card**
- **Beginner-friendly explanations** — mental model first, then reference, then pitfalls

### Common Skills
- **README only** — no code files; these are reference guides
- **Match the numbered folder format** — `0N_topic/README.md`
- **End each guide with a quick reference card** — a compact cheat sheet of the most-used commands/patterns

### Both
- **Don't over-engineer** — one focused concept per lesson, minimal boilerplate
- **Don't add features or refactor things that weren't asked about**

---

## Tone & Style

- Be direct and practical — skip filler
- Short explanations are better than long ones
- Code comments should explain the non-obvious parts
- When introducing a modern feature, compare it to something familiar so there's a mental anchor
- Don't add features or refactor things that weren't asked about
