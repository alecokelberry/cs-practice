# Lesson 07 — Classes

## Overview

A **class** is a blueprint for creating objects. It bundles data (member variables) and behavior (member functions) together. This lesson covers class structure, constructors, access control, `const` correctness on methods, and explicit compiler control with `= default` and `= delete`.

---

## Class Structure

```cpp
class ClassName {
  public:
    // Constructor
    ClassName(int id, std::string name);

    // Member functions
    void printInfo() const;   // const = won't modify the object
    int  getId() const;

  private:
    // Data members — hidden from outside code
    int         id_;
    std::string name_;
};
```

Default access for `class` is `private`. Default for `struct` is `public`.

---

## Access Modifiers

| Modifier | Who can access |
|----------|---------------|
| `private` | Only code inside the class |
| `public` | Anyone |
| `protected` | Class and its subclasses (inheritance) |

**Standard pattern:** make data `private`, expose it through `public` methods.

---

## Member Initializer List

Initialize members in the constructor directly — more efficient than assigning inside the constructor body. **Required** for `const` members and references.

```cpp
class Student {
  public:
    Student(std::string name, int id)
        : name_{std::move(name)}, id_{id}
    {}                              // body is empty — all initialization happens above

  private:
    std::string name_;
    int         id_{0};  // in-class default — used if not set by a constructor
};
```

`std::move(name)` avoids copying the string argument — it transfers ownership into `name_`.

---

## `const` Member Functions

Mark a method `const` if it doesn't modify the object. `const` objects can only call `const` methods.

```cpp
class Student {
  public:
    [[nodiscard]] const std::string& name() const { return name_; }  // const getter
    [[nodiscard]] int                id()   const { return id_;   }

    void setName(std::string n) { name_ = std::move(n); }  // non-const setter

  private:
    std::string name_;
    int         id_;
};

const Student cs{"Bob", 2};
cs.name();          // OK — name() is const
// cs.setName("X"); // compile error — setName is not const
```

---

## `= default` and `= delete`

Explicit control over which compiler-generated operations are available:

```cpp
class Resource {
  public:
    Resource() = default;                          // compiler generates default constructor
    ~Resource() = default;                         // compiler generates destructor

    // Disallow copying — prevents accidental expensive copies
    Resource(const Resource&)            = delete;
    Resource& operator=(const Resource&) = delete;

    // Allow moving
    Resource(Resource&&)            = default;
    Resource& operator=(Resource&&) = default;
};
```

`= delete` makes copy/assignment a **compile error** rather than silently allowing an expensive or incorrect operation.

---

## Getters and Setters

The standard way to give controlled access to private data:

```cpp
class Student {
  public:
    [[nodiscard]] const std::string& name() const { return name_; }
    void setName(std::string n) { name_ = std::move(n); }

  private:
    std::string name_;
};
```

---

## `struct` vs `class`

`struct` is identical to `class` but with `public` as the default access. Use it for simple data bundles where everything should be visible:

```cpp
struct Point {
    double x{0.0};
    double y{0.0};
};

Point p{3.0, 4.0};
std::cout << std::format("({}, {})\n", p.x, p.y);
```

---

## Separating Declaration from Definition

In real projects, classes are split across files:
- **`Student.h`** — the class declaration
- **`Student.cpp`** — the method definitions

For lessons, everything is in `main.cpp` for simplicity.

```cpp
// In the .cpp file — use ClassName:: to link the method to its class
void Student::printInfo() const {
    std::cout << std::format("{}: {}\n", id_, name_);
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Assigning in constructor body instead of initializer list | Use `: member{value}` syntax — more efficient, required for `const`/reference members |
| Non-const getter | Mark getters `const` so they work on `const` objects |
| Forgetting `[[nodiscard]]` on getters | Add it — silences bugs from ignored return values |
| Implicit copying of expensive objects | `= delete` the copy constructor/assignment if copying shouldn't be allowed |

---

## Quick Reference Card

```cpp
class Student {
  public:
    // Constructor with member initializer list
    Student(std::string name, int id)
        : name_{std::move(name)}, id_{id} {}

    Student()             = default;
    Student(const Student&)            = delete;   // no copy
    Student& operator=(const Student&) = delete;
    Student(Student&&)            = default;        // move OK
    Student& operator=(Student&&) = default;

    // const getter
    [[nodiscard]] const std::string& name() const { return name_; }
    [[nodiscard]] int                id()   const { return id_;   }

    // non-const setter
    void setName(std::string n) { name_ = std::move(n); }

    void print() const {
        std::cout << std::format("{}: {}\n", id_, name_);
    }

  private:
    std::string name_;
    int         id_{0};
};
```
