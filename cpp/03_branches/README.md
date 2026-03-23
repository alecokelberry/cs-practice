# Lesson 03 — Branches

## Overview

Branches let your program make decisions — execute one block of code or another based on a condition. C++ has two main branching tools: `if/else if/else` for flexible conditions and ranges, and `switch` for matching a single value against a fixed set of cases.

---

## Relational Operators

These compare two values and return `true` or `false`:

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `score == 100` |
| `!=` | Not equal to | `grade != 'F'` |
| `>` | Greater than | `age > 18` |
| `<` | Less than | `price < 50.0` |
| `>=` | Greater than or equal | `score >= 90` |
| `<=` | Less than or equal | `count <= 10` |

> `=` assigns. `==` compares. Mixing them up (`if (x = 5)`) is a common bug — it assigns 5 to x and always evaluates as true.

---

## Logical Operators

Combine multiple conditions:

| Operator | Meaning | Example |
|----------|---------|---------|
| `&&` | AND — both must be true | `age >= 18 && hasID` |
| `\|\|` | OR — at least one must be true | `isAdmin \|\| isOwner` |
| `!` | NOT — flips true/false | `!isLoggedIn` |

---

## if / else if / else

```cpp
int score{85};

if (score >= 90) {
    std::cout << "Grade: A\n";
} else if (score >= 80) {
    std::cout << "Grade: B\n";
} else if (score >= 70) {
    std::cout << "Grade: C\n";
} else {
    std::cout << "Grade: F\n";
}
```

- Only one branch executes — the first matching condition wins
- The `else` at the end is a catch-all

---

## `if` with Initializer (C++17)

Declare a variable scoped to the `if` block:

```cpp
// The variable 'bonus' only exists inside this if/else
if (int bonus{score - 80}; bonus > 0) {
    std::cout << std::format("Bonus points: {}\n", bonus);
} else {
    std::cout << "No bonus\n";
}
// bonus is not accessible here
```

Useful for keeping scope tight when you need a value only for the check.

---

## Ternary Operator

A one-liner for simple true/false choices:

```cpp
// condition ? value_if_true : value_if_false
std::string result{(score >= 60) ? "Pass" : "Fail"};
```

Avoid nesting ternary operators — it gets unreadable fast.

---

## switch

Best when you're checking one variable against a fixed set of exact values:

```cpp
char grade{'B'};

switch (grade) {
    case 'A':
        std::cout << "Excellent!\n";
        break;
    case 'B':
        std::cout << "Good job!\n";
        break;
    case 'C':
        std::cout << "Passing.\n";
        break;
    default:
        std::cout << "See your advisor.\n";
        break;
}
```

- `break` exits the switch; without it, execution falls through to the next case
- `default` is the catch-all (like `else`)
- Works with `int`, `char`, and `enum` — not with `std::string` or `double`

---

## `[[fallthrough]]` — Intentional Fallthrough

Without `[[fallthrough]]`, the compiler may warn about a missing `break`. The annotation silences the warning and documents that the fallthrough is deliberate:

```cpp
int dayNum{6};  // Saturday
switch (dayNum) {
    case 1: case 2: case 3: case 4: case 5:
        std::cout << "Weekday\n";
        break;
    case 6:
        std::cout << "Saturday — almost done!\n";
        [[fallthrough]];   // intentional — Saturday and Sunday share the next block
    case 7:
        std::cout << "Weekend!\n";
        break;
    default:
        std::cout << "Invalid day\n";
        break;
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `if (x = 5)` instead of `if (x == 5)` | Assignment in a condition is a bug — use `==` |
| Missing `break` in switch | All cases fall through without `break`; add it or use `[[fallthrough]]` |
| `switch` on a `std::string` | Not supported — use `if/else` or `std::unordered_map` |
| Nesting ternary operators | Unreadable — use `if/else` for anything non-trivial |

---

## Quick Reference Card

```cpp
// if / else
if (condition) { ... }
else if (other) { ... }
else { ... }

// if with initializer
if (int val{compute()}; val > 0) { ... }

// ternary
auto label{(x > 0) ? "positive" : "non-positive"};

// switch
switch (x) {
    case 1: ...; break;
    case 2: ...; [[fallthrough]];
    case 3: ...;  break;
    default: ...;  break;
}
```
