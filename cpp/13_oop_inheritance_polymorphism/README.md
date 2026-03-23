# Lesson 13 — OOP: Inheritance & Polymorphism

## Overview

**Inheritance** lets a class ("derived") reuse and extend another class ("base"). **Polymorphism** lets you call a method on a base-class pointer/reference and have the correct derived-class version run at runtime — without knowing the exact type at compile time.

---

## Inheritance Basics

```cpp
class Animal {
  public:
    Animal(std::string name) : name_{std::move(name)} {}

    void breathe() const { std::cout << name_ << " breathes.\n"; }

    [[nodiscard]] const std::string& name() const { return name_; }

  protected:
    std::string name_;  // accessible in derived classes, not public
};

class Dog : public Animal {   // Dog inherits all public and protected members
  public:
    Dog(std::string name) : Animal{std::move(name)} {}  // delegate to base constructor

    void bark() const { std::cout << name_ << " barks!\n"; }
};

Dog d{"Rex"};
d.breathe();   // inherited from Animal
d.bark();      // Dog's own method
```

Access specifiers in inheritance:
- `public` — public stays public, protected stays protected (most common)
- `protected` — public becomes protected
- `private` — everything from base becomes private in derived

---

## Virtual Functions — Runtime Polymorphism

A `virtual` function can be overridden in a derived class. When called through a base pointer or reference, the **derived version runs** — even though the static type is base.

```cpp
class Shape {
  public:
    virtual double area() const { return 0.0; }  // default implementation

    virtual void describe() const {
        std::cout << std::format("Shape with area {:.2f}\n", area());
    }

    virtual ~Shape() = default;  // ALWAYS make base class destructor virtual
};

class Circle : public Shape {
  public:
    explicit Circle(double r) : radius_{r} {}

    double area() const override { return 3.14159 * radius_ * radius_; }

  private:
    double radius_;
};

class Rectangle : public Shape {
  public:
    Rectangle(double w, double h) : width_{w}, height_{h} {}

    double area() const override { return width_ * height_; }

  private:
    double width_, height_;
};
```

### Polymorphic Usage

```cpp
// Base pointer to derived object — this is polymorphism
std::unique_ptr<Shape> s1{std::make_unique<Circle>(5.0)};
std::unique_ptr<Shape> s2{std::make_unique<Rectangle>(4.0, 6.0)};

s1->area();     // calls Circle::area() — not Shape::area()
s2->area();     // calls Rectangle::area()
s1->describe(); // calls Shape::describe(), which internally calls Circle::area()
```

---

## `override` and `final`

Always use `override` when overriding a virtual function — the compiler will catch typos or mismatches:

```cpp
class Circle : public Shape {
  public:
    double area() const override { ... }  // compiler verifies this overrides a virtual
    // double are() const override { ... }  // compile error — no 'are' in base
};
```

`final` prevents further overriding or further inheritance:

```cpp
class ConcreteShape final : public Shape { ... };  // no one can inherit from this
double area() const override final { ... }         // no derived class can override this
```

---

## Pure Virtual Functions — Abstract Classes

A pure virtual function (`= 0`) has no implementation in the base class. A class with any pure virtual function is **abstract** — it cannot be instantiated directly. Derived classes must provide an implementation.

```cpp
class Shape {
  public:
    virtual double area()      const = 0;  // pure virtual — derived MUST implement
    virtual double perimeter() const = 0;

    virtual ~Shape() = default;

    // Non-virtual method can use the virtual ones
    void print() const {
        std::cout << std::format("area: {:.2f}, perimeter: {:.2f}\n",
                                 area(), perimeter());
    }
};

// Shape s;  // compile error — abstract class cannot be instantiated

class Square : public Shape {
  public:
    explicit Square(double side) : side_{side} {}

    double area()      const override { return side_ * side_; }
    double perimeter() const override { return 4 * side_; }

  private:
    double side_;
};
```

---

## Virtual Destructor — Critical

When you `delete` an object through a base pointer, the **base destructor runs** unless it's virtual. This skips the derived destructor, causing resource leaks.

```cpp
class Base {
  public:
    virtual ~Base() = default;  // MUST be virtual if you ever delete via base pointer
};

class Derived : public Base {
    std::vector<int> data_;  // this would leak without virtual destructor
};

std::unique_ptr<Base> ptr{std::make_unique<Derived>()};
// When ptr goes out of scope, ~Derived() runs correctly because ~Base() is virtual
```

**Rule:** if a class has any virtual functions, give it a `virtual` destructor.

---

## Object Slicing

Slicing happens when you assign a derived object to a base object **by value** — the derived part is discarded:

```cpp
Circle c{5.0};
Shape s{c};     // SLICED — only the Shape part is copied; Circle::area() is lost
s.area();       // calls Shape::area(), not Circle::area()
```

Fix: use pointers or references to base, never base objects by value:

```cpp
Shape& ref{c};   // no slicing — ref.area() calls Circle::area()
Shape* ptr{&c};  // no slicing
```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Base destructor not virtual | Add `virtual ~Base() = default;` |
| Forgetting `override` | Always use it — catches typos and signature mismatches |
| Object slicing | Use pointers or references to base, never base by value |
| Calling virtual in constructor/destructor | Virtual dispatch doesn't work here — calls the current class's version |

---

## Quick Reference Card

```cpp
// Base class
class Base {
  public:
    virtual void fn() const { ... }  // virtual — can be overridden
    virtual void pure() const = 0;   // pure virtual — must be overridden
    virtual ~Base() = default;       // virtual destructor — required

  protected:
    int x_{0};
};

// Derived class
class Derived : public Base {
  public:
    Derived(int x) : Base{} { x_ = x; }

    void fn()   const override { ... }  // override — compiler verifies
    void pure() const override { ... }  // must implement pure virtual

    void ownMethod() const { ... }      // derived-only method
};

// Polymorphic usage
std::unique_ptr<Base> ptr{std::make_unique<Derived>(42)};
ptr->fn();    // calls Derived::fn()
ptr->pure();  // calls Derived::pure()
// ~Derived() runs when ptr goes out of scope (virtual destructor)
```
