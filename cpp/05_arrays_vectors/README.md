# Lesson 05 — Arrays & Vectors

## Overview

Arrays and vectors both store multiple values of the same type in sequence. The key difference: arrays have a **fixed size** set at compile time; vectors can **grow and shrink** at runtime. In modern C++, `std::array` replaces raw C-arrays and `std::vector` is the go-to dynamic container.

---

## C-Style Arrays (Legacy)

```cpp
int scores[5]{85, 92, 78, 95, 88};

scores[0];   // 85 — zero-based indexing
scores[4];   // 88 — last element (index = size - 1)
```

C-arrays don't know their own size, have no bounds checking, and don't work cleanly with STL algorithms. They appear in legacy code and C APIs — understand them, but prefer `std::array` for new code.

---

## `std::array` — Fixed-Size, Modern

Same performance as a C-array. Knows its own size. Works with STL algorithms. Bounds-checked access via `.at()`.

```cpp
#include <array>

std::array<int, 5> scores{85, 92, 78, 95, 88};

scores.size();      // 5 — it knows its size
scores.front();     // 85
scores.back();      // 88
scores.at(2);       // 78 — throws std::out_of_range if index is bad
scores[2];          // 78 — fast, no bounds check
```

---

## `std::vector` — Dynamic (Preferred)

Resizes automatically. The most commonly used container in C++.

```cpp
#include <vector>

std::vector<int> grades;
grades.reserve(5);           // pre-allocate to avoid repeated re-allocations

grades.emplace_back(85);     // construct in-place — preferred over push_back
grades.emplace_back(92);
grades.emplace_back(78);

grades.size();               // number of elements
grades.capacity();           // allocated space (≥ size)
grades.pop_back();           // remove last element
grades.at(1);                // bounds-checked access
grades[1];                   // fast access, no bounds check
grades.front();              // first element
grades.back();               // last element
grades.empty();              // true if no elements
grades.clear();              // remove all elements
```

### `emplace_back` vs `push_back`

```cpp
// push_back: creates a value, then copies/moves it into the vector
grades.push_back(95);

// emplace_back: constructs the value directly inside the vector — no copy
grades.emplace_back(95);
```

For simple types like `int`, the difference is negligible. For complex objects (structs, classes), `emplace_back` is more efficient because it constructs in-place.

---

## Looping Over Collections

```cpp
// Range-based for — preferred for both std::array and std::vector
for (const auto& score : scores) {
    std::cout << score << ' ';
}

// Mutable range-based for
for (auto& score : scores) {
    score += 5;  // modifies in place
}
```

---

## Sorting and Searching

```cpp
#include <algorithm>

std::vector<int> nums{5, 2, 8, 1, 9};

std::sort(nums.begin(), nums.end());         // sort ascending
std::sort(nums.begin(), nums.end(),
          [](int a, int b){ return a > b; }); // sort descending

// Find a value — returns an iterator, or end() if not found
auto it{std::find(nums.begin(), nums.end(), 8)};
if (it != nums.end()) {
    std::cout << "Found at index " << std::distance(nums.begin(), it) << '\n';
}
```

---

## 2D Vectors

```cpp
std::vector<std::vector<int>> grid{
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

std::cout << grid[1][2];  // 6 (row 1, column 2)
```

---

## When to Use What

| Container | Use when |
|-----------|----------|
| `std::array<T, N>` | Fixed size known at compile time; want stack allocation |
| `std::vector<T>` | Size is dynamic or unknown; this is the default choice |
| C-array `T arr[N]` | Interfacing with C APIs; otherwise avoid |

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Accessing out of bounds with `[]` | Use `.at()` during development; validate indices |
| `v.size()` returns `size_t` (unsigned) — comparison warning | Cast: `static_cast<int>(v.size())`, or use range-based `for` |
| `push_back` for objects with complex constructors | Use `emplace_back` |
| Sorting part of a range with wrong iterators | Double-check `begin()`/`end()` bounds |

---

## Quick Reference Card

```cpp
#include <algorithm>
#include <array>
#include <vector>

// std::array (fixed)
std::array<int, 5> arr{1, 2, 3, 4, 5};
arr.size();   arr.front();   arr.back();   arr.at(i);

// std::vector (dynamic)
std::vector<int> v;
v.reserve(n);
v.emplace_back(x);
v.pop_back();
v.size();   v.empty();   v.clear();

// Range-based for
for (const auto& x : v) { ... }
for (auto& x : v) { x = modified; }

// Sort
std::sort(v.begin(), v.end());
std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });

// Find
auto it{std::find(v.begin(), v.end(), target)};
if (it != v.end()) { /* found */ }
```
