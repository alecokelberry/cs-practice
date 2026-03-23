# C++ Personal Reference Course

A self-paced C++ reference built for clarity and correctness. Each lesson focuses on one topic: the concept, the syntax, and how to use it well in modern C++.

---

## Lessons

| # | Folder | Topic |
|---|--------|-------|
| 01 | [01_introduction](01_introduction/) | Program structure, I/O, std::format |
| 02 | [02_variables](02_variables/) | Types, uniform init, constexpr, auto |
| 03 | [03_branches](03_branches/) | if/else, switch, ternary, [[fallthrough]] |
| 04 | [04_loops](04_loops/) | while, for, do-while, range-for, ranges |
| 05 | [05_arrays_vectors](05_arrays_vectors/) | std::array, std::vector, sorting, searching |
| 06 | [06_functions](06_functions/) | Pass by value/const&/ref, overloading, [[nodiscard]], lambdas |
| 07 | [07_classes](07_classes/) | Constructors, member init list, const methods, = default/delete |
| 08 | [08_pointers](08_pointers/) | Raw pointers, nullptr, ->, dynamic memory, non-owning use |
| 09 | [09_smart_pointers](09_smart_pointers/) | unique_ptr, shared_ptr, weak_ptr |
| 10 | [10_raii_memory_management](10_raii_memory_management/) | RAII, destructors, lock_guard, Rule of 0 |
| 11 | [11_stl_containers](11_stl_containers/) | map, unordered_map, set, unordered_set, deque |
| 12 | [12_stl_algorithms](12_stl_algorithms/) | sort, find, transform, accumulate, erase_if, ranges |
| 13 | [13_oop_inheritance_polymorphism](13_oop_inheritance_polymorphism/) | virtual, override, pure virtual, abstract classes |
| 14 | [14_const_correctness](14_const_correctness/) | const variables, const&, const methods, constexpr, mutable |
| 15 | [15_move_semantics_rule_of_5](15_move_semantics_rule_of_5/) | lvalue/rvalue, std::move, move constructor, Rule of 5 |
| 16 | [16_lambdas_templates_basics](16_lambdas_templates_basics/) | Lambda captures, generic lambdas, function/class templates |
| 17 | [17_cmake_basics](17_cmake_basics/) | CMakeLists.txt, targets, FetchContent, build types |

---

## How to Compile & Run

```bash
# Works for any lesson (01–16)
cd 01_introduction
g++ -std=c++20 main.cpp -o main && ./main
```

Lesson 17 (CMake) has no `main.cpp` — it's a reference guide only.

---

## Style

All lessons use modern C++ (C++20):

- `std::` prefix always — no `using namespace std;`
- `{}` initialization to prevent narrowing
- `constexpr` over `const` for compile-time constants
- `const&` for large objects passed to functions
- Smart pointers for owned heap memory
- Range-based `for` and `std::ranges` over index loops
- `[[nodiscard]]` on functions where ignoring the return value is a bug
