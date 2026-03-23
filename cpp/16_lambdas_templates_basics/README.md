# Lesson 16 — Lambdas & Templates Basics

## Overview

**Lambdas** are anonymous functions you define inline — you saw them with STL algorithms in lessons 06 and 12. This lesson covers them fully: captures, `mutable`, generic lambdas, and storing them.

**Templates** let you write one function or class that works for any type. They're how `std::vector<T>`, `std::sort`, and smart pointers work.

---

## Lambda Syntax

```cpp
[captures](parameters) -> return_type { body }
```

The return type is usually deduced — you rarely need to write it explicitly.

```cpp
auto add{[](int a, int b) { return a + b; }};
std::cout << add(3, 5);  // 8

// With explicit return type
auto divide{[](double a, double b) -> double { return a / b; }};
```

---

## Captures

The capture list (`[]`) determines which variables from the surrounding scope the lambda can see.

```cpp
int x{10}, y{20};

// Capture nothing
auto fn{[]() { return 42; }};

// Capture x by value — lambda gets a copy of x at creation time
auto byVal{[x]() { return x * 2; }};
x = 99;
std::cout << byVal();  // 20 — captured the old value of x

// Capture x by reference — reads x's current value when called
auto byRef{[&x]() { return x * 2; }};
std::cout << byRef();  // 198 — reads the current x

// Capture all by value
auto allByVal{[=]() { return x + y; }};

// Capture all by reference
auto allByRef{[&]() { x += y; }};  // modifies x and y in the outer scope
```

---

## `mutable` Lambdas

By default, captured-by-value variables are `const` inside the lambda. Use `mutable` to allow modifying the local copy:

```cpp
int count{0};

// Without mutable — cannot modify the captured copy
// auto fn{[count]() { ++count; }};  // compile error

// With mutable — can modify the LOCAL copy (doesn't affect the original)
auto fn{[count]() mutable { ++count; return count; }};
std::cout << fn();  // 1
std::cout << fn();  // 2
std::cout << count; // 0 — original unchanged
```

---

## Generic Lambdas (C++14)

Use `auto` parameters to make a lambda that works with any type:

```cpp
auto print{[](const auto& val) { std::cout << val << '\n'; }};
print(42);       // int
print(3.14);     // double
print("hello");  // string literal

// Generic lambda with multiple auto parameters
auto add{[](auto a, auto b) { return a + b; }};
std::cout << add(1, 2);          // 3 (int)
std::cout << add(1.5, 2.5);      // 4.0 (double)
std::cout << add(std::string{"hi"}, std::string{"!"});  // "hi!"
```

---

## Storing Lambdas — `std::function`

`auto` works for storing a lambda in one place. Use `std::function<R(Args...)>` when you need to store different callables (lambdas, free functions, functors) in a container or pass them as function parameters:

```cpp
#include <functional>

// Accepts any callable that takes int and returns int
void apply(const std::function<int(int)>& fn, int x) {
    std::cout << fn(x) << '\n';
}

apply([](int x){ return x * 2; }, 5);   // 10
apply([](int x){ return x + 10; }, 5);  // 15
```

Note: `std::function` has overhead — prefer `auto` or templates when performance matters.

---

## Function Templates

Write one function, use it with any type:

```cpp
template <typename T>
T square(T x) { return x * x; }

std::cout << square(5);      // 25 (int)
std::cout << square(3.0);    // 9.0 (double)
std::cout << square(2.0f);   // 4.0f (float)
```

### Template with Multiple Parameters

```cpp
template <typename T, typename U>
auto add(T a, U b) { return a + b; }

std::cout << add(1, 2.5);  // 3.5 (int + double → double)
```

### Requiring a Concept (C++20)

Constrain which types are accepted:

```cpp
#include <concepts>

template <std::integral T>      // T must be an integral type (int, long, etc.)
T gcd(T a, T b) {
    while (b) { auto t{b}; b = a % b; a = t; }
    return a;
}

gcd(12, 8);   // 4 — OK
// gcd(1.5, 2.5);  // compile error — double doesn't satisfy std::integral
```

---

## Class Templates

A class that works for any type:

```cpp
template <typename T>
class Stack {
  public:
    void push(T val)  { data_.push_back(std::move(val)); }
    void pop()        { data_.pop_back(); }
    [[nodiscard]] T& top() { return data_.back(); }
    [[nodiscard]] bool empty() const { return data_.empty(); }
    [[nodiscard]] std::size_t size() const { return data_.size(); }

  private:
    std::vector<T> data_;
};

Stack<int>         intStack;
Stack<std::string> strStack;

intStack.push(1);
intStack.push(2);
std::cout << intStack.top();  // 2

strStack.push("hello");
std::cout << strStack.top();  // "hello"
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Dangling reference capture `[&]` in a lambda stored longer than its scope | Use `[=]` (copy) for long-lived lambdas |
| Modifying captured-by-value variable — compile error | Add `mutable` to the lambda |
| `std::function` overhead in hot loops | Use `auto` or a template parameter for the callable |
| Template defined in .cpp file, used in another .cpp | Template definitions must be in the header (they're instantiated at compile time) |

---

## Quick Reference Card

```cpp
// Basic lambda
auto fn{[](int x) { return x * 2; }};

// Captures
auto bv{[x]() { return x; }};       // by value (copy at creation)
auto br{[&x]() { return x; }};      // by reference
auto all_v{[=]() { return x + y; }}; // all by value
auto all_r{[&]() { x = 0; }};        // all by reference

// Mutable lambda
auto counter{[n = 0]() mutable { return ++n; }};

// Generic lambda
auto pr{[](const auto& v) { std::cout << v << '\n'; }};

// std::function (type-erased callable)
std::function<int(int)> f{[](int x){ return x * x; }};

// Function template
template <typename T>
T max(T a, T b) { return (a > b) ? a : b; }

// Class template
template <typename T>
class Box {
    T value_;
  public:
    explicit Box(T v) : value_{std::move(v)} {}
    [[nodiscard]] const T& get() const { return value_; }
};
```
