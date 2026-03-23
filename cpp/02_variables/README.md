# Lesson 02 — Variables & Assignments

## Overview

Variables store data. In C++, every variable has a **type** fixed at compile time. This lesson covers the core types, initialization, constants, arithmetic, type conversion, and math functions.

---

## Core Data Types

| Type | What it stores | Example |
|------|---------------|---------|
| `int` | Whole numbers | `int age{21};` |
| `double` | Decimal numbers (high precision) | `double gpa{3.85};` |
| `float` | Decimal numbers (less precision) | `float temp{98.6f};` |
| `char` | A single character | `char grade{'A'};` |
| `string` | A sequence of characters | `std::string name{"Alice"};` |
| `bool` | True or false | `bool enrolled{true};` |

> Prefer `double` over `float` — `double` is more precise and is the default type for floating-point literals.

---

## Uniform Initialization (`{}`)

The `{}` syntax is preferred for initialization. It prevents **narrowing conversions** — the compiler errors if you try to store a value that doesn't fit.

```cpp
int score{95};       // preferred
double pi{3.14159};
bool active{true};

// int x{3.9};  // compile error — 3.9 doesn't fit in an int without losing data
// int x = 3.9; // silently truncates to 3 — no error
```

---

## `auto` — Type Deduction

The compiler figures out the type from the assigned value. Useful when the type is long or obvious from context.

```cpp
auto count{0};           // int
auto ratio{0.75};        // double
auto name{std::string{"Alice"}};  // std::string
```

Be explicit when the type matters for clarity — `auto` is a tool, not a default.

---

## Constants

```cpp
// constexpr: value is known at compile time — zero runtime cost
constexpr double PI{3.14159265358979};
constexpr int    MAX_STUDENTS{30};

// const: value cannot change at runtime, but isn't necessarily compile-time
const std::string CONFIG_PATH{"/etc/app/config"};
```

Prefer `constexpr` over `const` for numeric literals. The compiler can do more optimization with it.

---

## Arithmetic Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `+` | Addition | `5 + 3 → 8` |
| `-` | Subtraction | `10 - 4 → 6` |
| `*` | Multiplication | `3 * 4 → 12` |
| `/` | Division | `10 / 3 → 3` (integer division!) |
| `%` | Modulo (remainder) | `10 % 3 → 1` |

> Integer division drops the decimal. `10 / 3` gives `3`, not `3.333`. Cast at least one operand to `double` for a decimal result.

### Compound Assignment

```cpp
x += 5;   // same as x = x + 5
x -= 2;
x *= 3;
x /= 2;
++x;      // prefix increment (preferred over x++ in loops)
x++;      // postfix increment
```

---

## Type Conversion

```cpp
int a{5};
double b{static_cast<double>(a)};  // explicit, safe cast — preferred

// C-style cast — avoid; the compiler can't warn about wrong casts
double c{(double)a};
```

Always use `static_cast<T>()`. It's more readable and the compiler can catch type mismatches that C-style casts silently allow.

---

## Math Functions — `<cmath>`

```cpp
#include <cmath>

std::pow(2.0, 8.0)   // 2^8 = 256
std::sqrt(144.0)     // 12
std::abs(-5)         // 5 (integer)
std::fabs(-3.7)      // 3.7 (floating-point)
std::ceil(4.1)       // 5.0 (round up)
std::floor(4.9)      // 4.0 (round down)
std::round(4.5)      // 5.0
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Integer division surprise: `10 / 3 = 3` | Cast one operand: `static_cast<double>(10) / 3` |
| Using `(double)x` | Use `static_cast<double>(x)` |
| Narrowing with `=`: `int x = 3.9;` silently truncates | Use `{}` initialization — it makes narrowing an error |
| `float` precision issues | Use `double` unless you specifically need `float` |

---

## Quick Reference Card

```cpp
#include <cmath>
#include <format>
#include <iostream>
#include <string>

constexpr double PI{3.14159265358979};

int main() {
    // Initialization
    int    score{95};
    double gpa{3.85};
    bool   active{true};
    auto   name{std::string{"Alice"}};

    // Arithmetic
    int a{10}, b{3};
    std::cout << std::format("{} / {} = {} (int division)\n", a, b, a / b);
    std::cout << std::format("{} / {} = {:.4f} (real)\n", a, b,
                             static_cast<double>(a) / b);

    // Math
    std::cout << std::format("sqrt(144) = {}\n", std::sqrt(144.0));

    return 0;
}
```
