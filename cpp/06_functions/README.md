# Lesson 06 — Functions

## Overview

Functions let you write a block of code once and call it many times. They're how you break a large program into smaller, manageable pieces. This lesson covers how to define functions, how data flows in and out of them, lambdas, and attributes like `[[nodiscard]]`.

---

## Function Anatomy

```cpp
returnType functionName(paramType paramName, ...) {
    // body
    return value;  // omit if returnType is void
}
```

A function must be **declared before it's used**. Use a forward declaration (prototype) if you define it after `main`:

```cpp
// Forward declaration — tells the compiler what the function looks like
int add(int a, int b);

int main() {
    std::cout << add(3, 5);  // compiles even though add is defined below
}

int add(int a, int b) { return a + b; }
```

---

## Return Types

| Return type | Meaning |
|-------------|---------|
| `void` | Returns nothing |
| `int`, `double`, `bool` | Returns that type |
| `auto` | Compiler deduces from the `return` statement |

---

## Pass by Value vs. Pass by Reference

### Pass by Value (default)

A **copy** of the argument is made. The original is unchanged.

```cpp
void addTen(int num) {
    num += 10;  // changes only the local copy
}

int x{5};
addTen(x);
// x is still 5
```

### Pass by Reference (`&`)

The function gets **direct access** to the original. Changes affect the caller.

```cpp
void addTen(int& num) {
    num += 10;  // changes the original
}

int x{5};
addTen(x);
// x is now 15
```

### Pass by `const` Reference

Read-only access to the original — no copy, no modification. This is the most efficient way to pass objects you don't need to modify.

```cpp
void printName(const std::string& name) {
    std::cout << name;  // can read, cannot modify
}
```

**Rule of thumb:** pass fundamental types (`int`, `double`) by value; pass objects (`std::string`, `std::vector`, classes) by `const&`.

---

## Default Parameters

```cpp
void greet(const std::string& name, const std::string& greeting = "Hello") {
    std::cout << std::format("{}, {}!\n", greeting, name);
}

greet("Alice");              // Hello, Alice!
greet("Bob", "Welcome");    // Welcome, Bob!
```

Default parameters must be at the **end** of the parameter list.

---

## Function Overloading

Multiple functions with the same name but different parameter types or counts:

```cpp
int    add(int a, int b)       { return a + b; }
double add(double a, double b) { return a + b; }
```

The compiler picks the right one based on the argument types.

---

## `[[nodiscard]]`

Tells the compiler to warn if the caller ignores the return value:

```cpp
[[nodiscard]] int computeScore() { return 42; }

computeScore();           // warning: ignoring return value
int s{computeScore()};    // fine
```

Use `[[nodiscard]]` on functions where ignoring the return value is almost certainly a bug (e.g., error codes, computed results).

---

## Lambdas — Anonymous Functions

A lambda is a function you define inline. Great for short, one-off operations, especially when passing behavior to STL algorithms.

```cpp
// Basic lambda
auto doubleIt{[](int x) { return x * 2; }};
std::cout << doubleIt(5);  // 10

// Capture by value — copies the variable at the time of lambda creation
int bonus{10};
auto withBonus{[bonus](int base) { return base + bonus; }};

// Capture by reference — reads the current value when the lambda is called
int multiplier{3};
auto scale{[&multiplier](int x) { return x * multiplier; }};
multiplier = 5;
std::cout << scale(4);  // 20, not 12

// Capture everything by value
auto fn{[=](int x) { return x + bonus + multiplier; }};

// Capture everything by reference
auto fn2{[&](int x) { bonus = x; }};
```

### Lambdas with STL Algorithms

```cpp
std::vector<int> scores{72, 88, 55, 95, 63};

// Sort descending
std::sort(scores.begin(), scores.end(), [](int a, int b){ return a > b; });

// Count scores above 80
int high{static_cast<int>(
    std::count_if(scores.begin(), scores.end(), [](int s){ return s > 80; })
)};
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Passing large objects by value | Use `const&` — avoids an expensive copy |
| Modifying a `const&` param | It won't compile; intentional — use a non-const `&` if you need to modify |
| Dangling reference from lambda `[&]` | Make sure captured variables outlive the lambda |
| Default parameter not at the end | Compiler error — defaults must come last |

---

## Quick Reference Card

```cpp
// Function declaration + definition
[[nodiscard]] int add(int a, int b);
void printName(const std::string& name);
void increment(int& value);
void greet(const std::string& name, const std::string& greet = "Hello");

// Overloads
int    add(int a, int b)       { return a + b; }
double add(double a, double b) { return a + b; }

// Lambda
auto square{[](int x) { return x * x; }};
auto withBonus{[bonus](int x) { return x + bonus; }};  // capture by value
auto scale{[&factor](int x) { return x * factor; }};   // capture by reference

// With STL
std::sort(v.begin(), v.end(), [](int a, int b){ return a > b; });
std::count_if(v.begin(), v.end(), [](int x){ return x > 80; });
```
