# Lesson 04 — Loops

## Overview

Loops repeat a block of code. C++ has three types: `while`, `for`, and `do-while`. The range-based `for` loop is the modern default for iterating over collections. C++20 also introduced ranges for composable, expressive iteration.

---

## while Loop

Runs **as long as** the condition is true. The condition is checked **before** each iteration.

```cpp
int count{0};
while (count < 5) {
    std::cout << count << ' ';
    ++count;  // prefix ++ preferred in loops
}
// Output: 0 1 2 3 4
```

Use `while` when you don't know in advance how many iterations you need — for example, reading input until the user types "quit".

---

## for Loop

Best when you **know exactly** how many iterations you need.

```cpp
// for (initialization; condition; update)
for (int i{0}; i < 5; ++i) {
    std::cout << i << ' ';
}
// Output: 0 1 2 3 4
```

All three parts are optional — `for (;;)` is an infinite loop.

---

## do-while Loop

Runs the body **first**, then checks the condition. Guarantees **at least one execution**.

```cpp
int x{100};
do {
    std::cout << "This always runs once.\n";
} while (x < 5);
```

Useful for menus where you want to show options at least once before checking if the user wants to continue.

---

## break and continue

```cpp
for (int i{0}; i < 10; ++i) {
    if (i == 3) continue;   // skip the rest of this iteration
    if (i == 7) break;      // exit the loop entirely
    std::cout << i << ' ';
}
// Output: 0 1 2 4 5 6
```

---

## Range-based for Loop

Cleaner way to iterate over a collection without managing an index:

```cpp
std::vector<int> scores{85, 92, 78, 95, 88};

// const auto& avoids copying; use for any element type you don't need to modify
for (const auto& score : scores) {
    std::cout << score << ' ';
}

// Mutable: use auto& to modify elements in place
for (auto& score : scores) {
    score += 5;
}
```

The range-based `for` is the default for iterating collections — it's cleaner, less error-prone, and works with any type that has `begin()` / `end()`.

---

## Ranges (C++20)

`std::views` gives you lazy, composable operations over collections without writing explicit loops:

```cpp
#include <ranges>

std::vector<int> scores{85, 92, 78, 95, 88};

// Filter: only scores above 80
for (int s : scores | std::views::filter([](int x){ return x > 80; })) {
    std::cout << s << ' ';
}

// Chain: filter scores above 80, then scale each by 1.1
auto adjusted = scores
    | std::views::filter([](int x){ return x > 80; })
    | std::views::transform([](int x){ return static_cast<int>(x * 1.1); });

for (int s : adjusted) { std::cout << s << ' '; }
```

Ranges are lazy — no intermediate collections are created.

---

## `std::accumulate` — Sum Without a Manual Loop

```cpp
#include <numeric>

std::vector<int> scores{85, 92, 78, 95, 88};
int total{std::accumulate(scores.begin(), scores.end(), 0)};
double avg{static_cast<double>(total) / static_cast<int>(scores.size())};
```

---

## Nested Loops

```cpp
for (int row{1}; row <= 3; ++row) {
    for (int col{1}; col <= 3; ++col) {
        std::cout << row * col << '\t';
    }
    std::cout << '\n';
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Off-by-one: `i <= n` vs `i < n` | Think carefully about the range; prefer range-based `for` to avoid it |
| Infinite loop: forgot to update loop variable | Add `++count` or equivalent |
| Index loop over vector: signed/unsigned warning | Use range-based `for`, or cast: `static_cast<int>(v.size())` |
| Modifying a collection while iterating with index | Erase elements after iteration, or use `std::erase_if` |

---

## Quick Reference Card

```cpp
// while
while (condition) { ... }

// for
for (int i{0}; i < n; ++i) { ... }

// do-while
do { ... } while (condition);

// range-based for (preferred for collections)
for (const auto& item : container) { ... }
for (auto& item : container) { item.modify(); }  // mutable

// ranges (C++20)
#include <ranges>
for (auto x : v | std::views::filter(pred) | std::views::transform(fn)) { ... }

// accumulate
#include <numeric>
int total{std::accumulate(v.begin(), v.end(), 0)};
```
