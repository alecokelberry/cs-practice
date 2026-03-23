# Lesson 15 — Move Semantics & Rule of 5

## Overview

Move semantics allow C++ to **transfer** resources from one object to another instead of copying them. This makes moving large objects (vectors, strings) nearly free: instead of allocating new memory and copying data, you just redirect a pointer.

---

## lvalues and rvalues

An **lvalue** has a name and a persistent address — you can take its address with `&`.
An **rvalue** is temporary — a value that doesn't have a name, or is explicitly marked as movable.

```cpp
int x{5};         // x is an lvalue
int y{x + 3};     // x + 3 is an rvalue (temporary result)

std::string s{"hello"};           // s is an lvalue
std::string t{std::move(s)};      // std::move casts s to an rvalue — enables move
// s is now in a valid but unspecified state (don't use it)
```

---

## Move Constructor and Move Assignment

A **move constructor** transfers the resource instead of copying it:

```cpp
class Buffer {
  public:
    explicit Buffer(std::size_t size)
        : data_{new int[size]}, size_{size} {
        std::cout << "constructed\n";
    }

    ~Buffer() {
        delete[] data_;
        std::cout << "destroyed\n";
    }

    // Move constructor — transfer data from 'other' to 'this'
    Buffer(Buffer&& other) noexcept
        : data_{other.data_}, size_{other.size_} {
        other.data_ = nullptr;  // leave 'other' in a valid empty state
        other.size_ = 0;
        std::cout << "moved\n";
    }

    // Move assignment operator
    Buffer& operator=(Buffer&& other) noexcept {
        if (this == &other) return *this;  // self-assignment check
        delete[] data_;           // free current resource
        data_       = other.data_;
        size_       = other.size_;
        other.data_ = nullptr;
        other.size_ = 0;
        std::cout << "move-assigned\n";
        return *this;
    }

    // Delete copy to make it move-only
    Buffer(const Buffer&)            = delete;
    Buffer& operator=(const Buffer&) = delete;

  private:
    int*        data_{nullptr};
    std::size_t size_{0};
};
```

---

## `std::move`

`std::move` doesn't move anything itself — it's just a cast to an rvalue reference (`T&&`), which enables the move constructor/assignment to be called.

```cpp
std::vector<int> a{1, 2, 3, 4, 5};
std::vector<int> b{std::move(a)};  // b takes a's internal buffer; a becomes empty

std::cout << a.size();  // 0 — a's data was moved to b
std::cout << b.size();  // 5
```

After a move, the source object is in a **valid but unspecified state** — safe to destroy or reassign, but not safe to use its value.

---

## The Rule of 5

If your class directly manages a resource (raw memory, file handle, socket), you likely need to define all five special member functions:

| Function | Purpose |
|----------|---------|
| Destructor | Release the resource |
| Copy constructor | Deep-copy the resource |
| Copy assignment operator | Release current resource, deep-copy |
| **Move constructor** | Transfer resource from temporary |
| **Move assignment operator** | Release current, transfer from other |

```cpp
class MyClass {
  public:
    MyClass();                                  // default constructor

    ~MyClass();                                 // destructor
    MyClass(const MyClass& other);              // copy constructor
    MyClass& operator=(const MyClass& other);   // copy assignment
    MyClass(MyClass&& other) noexcept;          // move constructor
    MyClass& operator=(MyClass&& other) noexcept; // move assignment
};
```

If you define any one of these, you should explicitly define or delete all five.

---

## The Rule of 0

The better alternative: compose your class from types that already handle their own cleanup (smart pointers, `std::vector`, `std::string`). Then you need to define **none** of the special functions:

```cpp
class Config {
  public:
    Config(std::string name, std::vector<int> data)
        : name_{std::move(name)}, data_{std::move(data)} {}

    // No destructor, no copy/move defined — the members handle themselves
    // Move semantics work automatically via std::string and std::vector

  private:
    std::string  name_;
    std::vector<int> data_;
};
```

**Prefer Rule of 0.** Only write Rule of 5 when you truly need to manage a raw resource.

---

## `noexcept` on Move Operations

Move constructors and move assignment operators should be marked `noexcept` when they don't throw. This allows containers like `std::vector` to use move when resizing — without `noexcept`, `vector` falls back to copying for safety.

```cpp
Buffer(Buffer&& other) noexcept { ... }
Buffer& operator=(Buffer&& other) noexcept { ... }
```

---

## `std::move` in Practice

Use `std::move` when:
- Passing an object you no longer need to a function
- Returning a local object (though the compiler often does this automatically via NRVO)
- Building a class member from a constructor argument

```cpp
class Widget {
  public:
    Widget(std::string name) : name_{std::move(name)} {}  // move argument into member
  private:
    std::string name_;
};

void process(std::vector<int> v) { /* takes ownership */ }
std::vector<int> data{1, 2, 3};
process(std::move(data));  // avoids copying — data is now moved-from
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using a moved-from object | After `std::move`, treat the source as invalid — reassign before using |
| Move constructor without `noexcept` | `std::vector` won't use move on resize — add `noexcept` |
| Forgetting to null out the source pointer | Source destructor will double-delete — set pointer to `nullptr` in move |
| Writing Rule of 5 when Rule of 0 would work | Prefer composing with STL types |

---

## Quick Reference Card

```cpp
// std::move — cast to rvalue to enable move
std::vector<int> a{1, 2, 3};
auto b{std::move(a)};   // a is now empty

// Move constructor
MyClass(MyClass&& other) noexcept
    : ptr_{other.ptr_}, size_{other.size_}
{
    other.ptr_  = nullptr;
    other.size_ = 0;
}

// Move assignment
MyClass& operator=(MyClass&& other) noexcept {
    if (this == &other) return *this;
    delete[] ptr_;
    ptr_        = other.ptr_;
    size_       = other.size_;
    other.ptr_  = nullptr;
    other.size_ = 0;
    return *this;
}

// Rule of 0 — prefer this
class Safe {
    std::unique_ptr<T> ptr_;
    std::vector<int>   data_;
    // all special functions compiler-generated and correct
};
```
