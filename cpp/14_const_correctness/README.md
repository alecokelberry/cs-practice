# Lesson 14 — `const` Correctness

## Overview

`const` correctness means annotating everything that shouldn't change with `const`. This lets the compiler catch accidental mutations, enables optimization, and makes code easier to reason about. It's a design discipline, not just a keyword.

---

## `const` Variables

```cpp
const int MAX{100};        // cannot be changed after initialization
constexpr int SIZE{50};    // also computed at compile time — prefer for literals

MAX = 200;  // compile error
```

---

## `const` References

Pass by `const&` when you want read-only access to an object without copying it:

```cpp
void print(const std::string& s) {
    std::cout << s;       // read — OK
    // s += "!";          // compile error — s is const
}
```

Binding a temporary to a `const&` is valid (the lifetime is extended):

```cpp
const std::string& greeting{std::string{"Hello"}};  // OK — lifetime extended
```

---

## `const` Member Functions

A method marked `const` promises it won't modify the object's data. Only `const` methods can be called on `const` objects.

```cpp
class Counter {
  public:
    void increment() { ++count_; }       // non-const — modifies
    int  value() const { return count_; } // const — read-only; callable on const Counter

  private:
    int count_{0};
};

const Counter c;
c.value();       // OK — value() is const
// c.increment(); // compile error — increment() is not const
```

Always mark getters and any function that only reads data as `const`.

---

## `const` Pointers — Three Variations

The position of `const` relative to `*` matters:

```cpp
int x{10}, y{20};

// 1. Pointer to const int — can't change the value; can point elsewhere
const int* ptr1{&x};
// *ptr1 = 99;    // compile error — pointed-to value is const
ptr1 = &y;       // OK — pointer itself can change

// 2. Const pointer to int — can change the value; can't point elsewhere
int* const ptr2{&x};
*ptr2 = 99;      // OK — can change the value
// ptr2 = &y;    // compile error — pointer cannot change

// 3. Const pointer to const int — neither can change
const int* const ptr3{&x};
// *ptr3 = 99;   // compile error
// ptr3 = &y;    // compile error
```

Memory trick: read right-to-left from the variable name.
- `const int* ptr` → ptr is a (pointer to (const int))
- `int* const ptr` → ptr is a (const pointer to (int))

---

## `constexpr`

`constexpr` means the value or result is known at compile time. The compiler can use it for optimization and it's required in some template/array contexts.

```cpp
constexpr int SQUARES[]{1, 4, 9, 16, 25};  // array size must be constexpr

constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

constexpr int fact5{factorial(5)};  // computed at compile time = 120
```

---

## `mutable` — Exception to `const`

`mutable` marks a member variable that may be modified even inside a `const` method. Used for caching or lazy evaluation:

```cpp
class ExpensiveQuery {
  public:
    int result() const {
        if (!cached_) {
            result_  = expensiveCompute();  // mutates — allowed because mutable
            cached_  = true;
        }
        return result_;
    }

  private:
    mutable int  result_{0};
    mutable bool cached_{false};

    int expensiveCompute() const { return 42; }  // simulated
};
```

Use `mutable` sparingly — it breaks the `const` guarantee from the caller's perspective, so it should only be used for implementation details that don't change logical state.

---

## `const` Return Types

Returning `const` references avoids copies and prevents modification:

```cpp
class Config {
  public:
    [[nodiscard]] const std::string& name() const { return name_; }
    // caller can't modify name through this reference
  private:
    std::string name_;
};
```

Returning `const` values (not references) has little benefit and can prevent move optimization — avoid it for value returns.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Non-const getter: `std::string getName() const` returns a copy anyway, but `const std::string& getName() const` avoids the copy | Use `const T&` for getters of large members |
| Non-const method called on a const object | Mark the method `const` if it doesn't modify anything |
| Confusing `const T*` and `T* const` | Read right-to-left from the variable name |
| `const` on returned value (not reference): `const int fn()` | Useless on primitives — the copy is already immutable to the caller |
| Modifying data through `mutable` in ways visible to the caller | `mutable` is for transparent caching, not for sneaking mutations past the interface |

---

## Quick Reference Card

```cpp
// const variable
const int MAX{100};
constexpr double PI{3.14159};

// const reference parameter — no copy, read-only
void fn(const std::string& s);

// const member function — callable on const objects
class Foo {
  public:
    int  value() const { return x_; }    // const getter
    void set(int x)    { x_ = x; }       // non-const setter
  private:
    int          x_{0};
    mutable bool cached_{false};  // can be modified inside const methods
};

// const pointer variations
const int* p1{&x};      // can't change *p1 (pointed-to value)
int* const p2{&x};      // can't change p2 (the pointer itself)
const int* const p3{&x}; // can't change either

// constexpr function — evaluated at compile time
constexpr int sq(int n) { return n * n; }
constexpr int result{sq(7)};  // 49, computed at compile time
```
