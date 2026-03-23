# Lesson 01 — Introduction to C++

## Overview

Every C++ program starts at `main()` and uses `#include` to pull in libraries. This lesson covers the skeleton of a program, console I/O, string formatting, and how to write comments.

---

## Program Structure

```cpp
#include <iostream>   // include the I/O library
#include <string>

int main() {
    // your code here
    return 0;  // 0 = success; the OS receives this
}
```

- `#include` brings in a standard library header
- `main()` is the entry point — every program has exactly one
- `return 0` signals successful completion

---

## Comments

```cpp
// Single-line comment

/* Multi-line
   comment */
```

Use comments to explain *why*, not *what* — the code itself shows what it does.

---

## Console Output — `std::cout`

```cpp
#include <iostream>

std::cout << "Hello, C++!\n";         // print text
std::cout << 42 << '\n';              // print a number
std::cout << "x = " << x << '\n';    // chain multiple values with <<
```

- `<<` is the insertion operator — sends data to the output stream
- Use `'\n'` for newlines, not `std::endl` — `endl` flushes the buffer on every call, which is slower
- Always qualify with `std::` — don't use `using namespace std;` (it imports every name from the standard library into global scope, causing potential collisions)

---

## Console Input — `std::cin`

```cpp
int age;
std::cin >> age;  // reads one whitespace-delimited token

std::string fullName;
std::getline(std::cin, fullName);  // reads the entire line including spaces
```

`cin >>` stops at whitespace. Use `std::getline` when input might contain spaces.

---

## `std::format` — Formatted Strings (C++20)

`std::format` builds formatted strings, similar to Python f-strings. Cleaner than chaining `<<`.

```cpp
#include <format>

std::string name{"Alice"};
int score{95};

// Build a formatted string
std::string msg{std::format("Name: {}, Score: {}", name, score)};
std::cout << msg << '\n';

// Inline (no intermediate variable needed)
std::cout << std::format("PI ≈ {:.4f}\n", 3.14159);
std::cout << std::format("Score: {:3d}%\n", score);  // right-aligned, width 3
```

---

## Standard Headers

| Header | What it gives you |
|--------|-------------------|
| `<iostream>` | `std::cout`, `std::cin` |
| `<string>` | `std::string`, `std::getline` |
| `<format>` | `std::format` (C++20) |
| `<cmath>` | `std::sqrt`, `std::pow`, etc. |

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `using namespace std;` | Always use the `std::` prefix |
| `std::endl` in loops | Use `'\n'` — `endl` flushes the buffer every call |
| `cin >>` for strings with spaces | Use `std::getline` instead |
| Missing `#include` for a type | Each header must be explicitly included |

---

## Quick Reference Card

```cpp
#include <format>
#include <iostream>
#include <string>

int main() {
    // Output
    std::cout << "Hello\n";
    std::cout << std::format("Name: {}, Score: {:.2f}\n", name, score);

    // Input
    int n;
    std::cin >> n;

    std::string line;
    std::getline(std::cin, line);

    return 0;
}
```
