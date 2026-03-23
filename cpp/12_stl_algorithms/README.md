# Lesson 12 — STL Algorithms

## Overview

`<algorithm>` provides a library of composable, efficient operations on ranges. Instead of writing raw loops, you express *what* you want done — the algorithm handles *how*.

All algorithms work with iterators (`v.begin()`, `v.end()`) and can operate on any container that provides them. C++20 ranges (`std::ranges::`) provide cleaner syntax that takes the container directly.

---

## Searching

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v{3, 1, 4, 1, 5, 9};

// find — returns iterator to first match, or end() if not found
auto it{std::find(v.begin(), v.end(), 4)};
if (it != v.end()) {
    std::cout << "found at index " << std::distance(v.begin(), it) << '\n';
}

// find_if — first element where predicate returns true
auto big{std::find_if(v.begin(), v.end(), [](int x){ return x > 7; })};

// binary_search — O(log n), requires sorted range; returns bool
std::sort(v.begin(), v.end());
bool found{std::binary_search(v.begin(), v.end(), 5)};

// lower_bound — first position where element could be inserted (sorted range)
auto pos{std::lower_bound(v.begin(), v.end(), 4)};
```

---

## Counting and Testing

```cpp
// count — exact matches
int threes{static_cast<int>(std::count(v.begin(), v.end(), 3))};

// count_if — matches a predicate
int evens{static_cast<int>(std::count_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; }))};

// any_of, all_of, none_of — short-circuit as soon as result is known
bool anyNeg{std::any_of(v.begin(), v.end(), [](int x){ return x < 0; })};
bool allPos{std::all_of(v.begin(), v.end(), [](int x){ return x > 0; })};
bool noneZero{std::none_of(v.begin(), v.end(), [](int x){ return x == 0; })};
```

---

## Sorting

```cpp
// sort — ascending by default; O(n log n)
std::sort(v.begin(), v.end());

// sort with custom comparator
std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });  // descending

// stable_sort — preserves relative order of equal elements
std::stable_sort(v.begin(), v.end());

// partial_sort — only sort the first N elements
std::partial_sort(v.begin(), v.begin() + 3, v.end());  // smallest 3 in front

// nth_element — element at position n is in its sorted position
// elements before n are ≤ it; elements after are ≥ it (not fully sorted)
std::nth_element(v.begin(), v.begin() + 2, v.end());
```

---

## Transforming

```cpp
#include <algorithm>

std::vector<int> src{1, 2, 3, 4, 5};
std::vector<int> dst(src.size());

// transform — apply a function to each element, write to output
std::transform(src.begin(), src.end(), dst.begin(),
               [](int x){ return x * x; });
// dst: {1, 4, 9, 16, 25}

// for_each — call a function on each element (no output)
std::for_each(src.begin(), src.end(), [](int& x){ x *= 2; });
// src: {2, 4, 6, 8, 10}
```

---

## Accumulation and Reduction

```cpp
#include <numeric>

std::vector<int> v{1, 2, 3, 4, 5};

// accumulate — sum with an initial value
int sum{std::accumulate(v.begin(), v.end(), 0)};          // 15

// with a custom operation — product
int product{std::accumulate(v.begin(), v.end(), 1, std::multiplies<int>{})};  // 120

// reduce (C++17) — parallel-friendly accumulate
int total{std::reduce(v.begin(), v.end())};  // 15, initial value defaults to T{}
```

---

## Removing Elements

Erase-remove idiom — the standard way to remove elements by value or predicate:

```cpp
std::vector<int> v{1, 2, 3, 2, 4, 2, 5};

// std::remove moves matching elements to the end and returns an iterator to the new end
// std::vector::erase then trims the vector to the new size
v.erase(std::remove(v.begin(), v.end(), 2), v.end());
// v: {1, 3, 4, 5}

// C++20: std::erase (shorthand for the above)
std::erase(v, 3);          // remove all 3s
std::erase_if(v, [](int x){ return x > 3; });  // remove all elements > 3
```

---

## Copying and Moving

```cpp
std::vector<int> src{1, 2, 3, 4, 5};
std::vector<int> dst;
dst.resize(src.size());

std::copy(src.begin(), src.end(), dst.begin());

// copy_if — copy only elements matching predicate
std::vector<int> evens;
std::copy_if(src.begin(), src.end(), std::back_inserter(evens),
             [](int x){ return x % 2 == 0; });
// evens: {2, 4}
```

---

## C++20 Ranges — Cleaner Syntax

```cpp
#include <algorithm>
#include <ranges>

std::vector<int> v{3, 1, 4, 1, 5, 9};

// ranges:: versions take the container directly — no begin()/end()
std::ranges::sort(v);
auto it{std::ranges::find(v, 4)};
std::ranges::for_each(v, [](int x){ std::cout << x << ' '; });

// Views compose lazily — no intermediate containers
for (int x : v | std::views::filter([](int n){ return n > 3; })
               | std::views::transform([](int n){ return n * 2; })) {
    std::cout << x << ' ';
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `std::remove` alone doesn't shrink the vector | Always follow with `.erase()` or use `std::erase` (C++20) |
| Calling `std::binary_search` on unsorted data | Sort first, or use `std::find` |
| `std::sort` on a `std::list` | `list` has its own `.sort()` member; `std::sort` needs random-access iterators |
| Capturing `[&]` in a lambda stored longer than its scope | Captured references become dangling |

---

## Quick Reference Card

```cpp
#include <algorithm>
#include <numeric>

// Searching
std::find(begin, end, val);
std::find_if(begin, end, pred);
std::binary_search(begin, end, val);  // requires sorted

// Testing
std::any_of(begin, end, pred);
std::all_of(begin, end, pred);
std::none_of(begin, end, pred);
std::count(begin, end, val);
std::count_if(begin, end, pred);

// Sorting
std::sort(begin, end);
std::sort(begin, end, [](T a, T b){ return a > b; });
std::stable_sort(begin, end);

// Transforming
std::transform(src_begin, src_end, dst_begin, fn);
std::for_each(begin, end, fn);

// Accumulation
std::accumulate(begin, end, init);

// Removing (erase-remove idiom)
v.erase(std::remove(begin, end, val), end);
std::erase(v, val);          // C++20
std::erase_if(v, pred);      // C++20

// Copying
std::copy(src_begin, src_end, dst_begin);
std::copy_if(src_begin, src_end, back_inserter(dst), pred);
```
