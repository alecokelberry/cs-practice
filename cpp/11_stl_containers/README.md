# Lesson 11 — STL Containers

## Overview

The C++ Standard Template Library provides a set of container types for different access patterns and performance requirements. Choosing the right container for your use case is a core skill.

The containers in this lesson (beyond `vector` and `array` from lesson 05):

| Container | Ordered? | Key type | Duplicates | Typical use |
|-----------|----------|----------|------------|-------------|
| `std::map` | yes (sorted by key) | any type with `<` | no | ordered key-value lookup |
| `std::unordered_map` | no | any hashable type | no | fast key-value lookup |
| `std::set` | yes (sorted) | any type with `<` | no | sorted unique values |
| `std::unordered_set` | no | any hashable type | no | fast membership test |
| `std::deque` | sequence | index | yes | fast push/pop at both ends |

---

## `std::map` — Ordered Key-Value

Keys are sorted. All operations are **O(log n)** (implemented as a red-black tree).

```cpp
#include <map>

std::map<std::string, int> scores;

// Insert
scores["Alice"] = 95;
scores["Bob"]   = 82;
scores.emplace("Carol", 91);    // preferred — constructs in-place

// Access
scores["Alice"];                // 95 — creates entry if key doesn't exist!
scores.at("Alice");             // 95 — throws std::out_of_range if missing

// Check existence before accessing
if (scores.contains("Alice")) { /* safe */ }     // C++20
if (scores.count("Alice") > 0) { /* safe */ }    // pre-C++20

// Iterate — always in sorted key order
for (const auto& [key, val] : scores) {          // structured bindings (C++17)
    std::cout << std::format("{}: {}\n", key, val);
}

// Find
auto it{scores.find("Bob")};
if (it != scores.end()) {
    std::cout << it->second;  // 82
}

// Erase
scores.erase("Bob");
```

---

## `std::unordered_map` — Hash Map

No ordering. Average **O(1)** insert, lookup, erase. Use when you don't need sorted keys.

```cpp
#include <unordered_map>

std::unordered_map<std::string, int> freq;

// Count word frequencies
std::string word;
for (const auto& w : words) {
    ++freq[w];   // creates entry with 0 if not present, then increments
}

// Same interface as std::map for most operations
freq.contains("hello");
freq.at("hello");
freq.erase("hello");

for (const auto& [word, count] : freq) {
    // order is not guaranteed
}
```

---

## `std::set` — Ordered Unique Values

Like `map` but stores only keys (no values). Sorted. **O(log n)** operations.

```cpp
#include <set>

std::set<int> seen;

seen.insert(3);
seen.insert(1);
seen.insert(3);  // duplicate — ignored

// Iterates in sorted order: 1, 3
for (int n : seen) { std::cout << n << ' '; }

seen.contains(3);   // true
seen.erase(3);
```

---

## `std::unordered_set` — Hash Set

No ordering. Average **O(1)** insert, lookup, erase. Best for fast membership tests.

```cpp
#include <unordered_set>

std::unordered_set<std::string> visited;
visited.insert("page1");
visited.insert("page2");

if (!visited.contains("page3")) {
    visited.insert("page3");
}
```

---

## `std::deque` — Double-Ended Queue

Fast push/pop at **both** ends. Random access is O(1) like `vector`, but slower in practice due to layout. Use when you frequently add/remove from the front.

```cpp
#include <deque>

std::deque<int> dq;

dq.push_back(10);    // add to back
dq.push_front(5);    // add to front — O(1), unlike vector
dq.pop_back();       // remove from back
dq.pop_front();      // remove from front

dq[0];               // random access
dq.size();
```

---

## Choosing a Container

| You need | Use |
|----------|-----|
| Fast random access by index | `vector` or `array` |
| Key-value lookup, any order | `unordered_map` |
| Key-value lookup, sorted order | `map` |
| Unique values, sorted | `set` |
| Unique values, fast membership test | `unordered_set` |
| Fast push/pop at both ends | `deque` |
| Default choice for most sequences | `vector` |

**`vector` is the default container.** Only reach for something else when profiling or requirements make it necessary.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `map["key"]` when key might not exist | Creates an empty entry — use `.at()` or `.contains()` first |
| Assuming `unordered_map` order | It's undefined; iterate with that in mind |
| Using `map` when you just need fast lookup | Use `unordered_map` for O(1) average |
| Iterating while erasing | Use `it = container.erase(it)` pattern |

---

## Quick Reference Card

```cpp
// map
std::map<K, V> m;
m.emplace(key, val);
m.at(key);
m.contains(key);
m.erase(key);
for (const auto& [k, v] : m) { ... }

// unordered_map
std::unordered_map<K, V> um;
++um[key];               // increment count (inserts 0 first if absent)
um.contains(key);

// set / unordered_set
std::set<T> s;
s.insert(val);
s.contains(val);
s.erase(val);

// deque
std::deque<T> dq;
dq.push_front(val);
dq.push_back(val);
dq.pop_front();
dq.pop_back();
```
