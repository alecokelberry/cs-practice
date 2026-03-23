// ─────────────────────────────────────────────────────────────
//  Lesson 13 — OOP: Inheritance & Polymorphism
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <cmath>
#include <format>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// ── Abstract Base Class ───────────────────────────────────────
// Pure virtual functions make this abstract — cannot be instantiated directly.
// Virtual destructor is required when deleting via base pointer.
class Shape {
  public:
    virtual double area()      const = 0;  // pure virtual — derived MUST implement
    virtual double perimeter() const = 0;
    virtual std::string typeName() const = 0;

    virtual ~Shape() = default;  // MUST be virtual — see lesson for why

    // Non-virtual: uses virtual functions internally (polymorphism in action)
    void print() const {
        std::cout << std::format("  {} — area: {:.2f}, perimeter: {:.2f}\n",
                                 typeName(), area(), perimeter());
    }
};

// ── Concrete Derived Classes ──────────────────────────────────
class Circle : public Shape {
  public:
    explicit Circle(double r) : radius_{r} {}

    double      area()      const override { return M_PI * radius_ * radius_; }
    double      perimeter() const override { return 2 * M_PI * radius_; }
    std::string typeName()  const override { return "Circle"; }

  private:
    double radius_;
};

class Rectangle : public Shape {
  public:
    Rectangle(double w, double h) : width_{w}, height_{h} {}

    double      area()      const override { return width_ * height_; }
    double      perimeter() const override { return 2 * (width_ + height_); }
    std::string typeName()  const override { return "Rectangle"; }

  private:
    double width_, height_;
};

// Square is a Rectangle — inherits from a concrete class
class Square : public Rectangle {
  public:
    explicit Square(double side) : Rectangle{side, side} {}

    std::string typeName() const override { return "Square"; }
};

// ── Inheritance Without Polymorphism ──────────────────────────
// Showing basic inheritance (no virtual functions)
class Animal {
  public:
    explicit Animal(std::string name) : name_{std::move(name)} {}
    void breathe() const { std::cout << std::format("  {} breathes.\n", name_); }
    [[nodiscard]] const std::string& name() const { return name_; }
  protected:
    std::string name_;
};

class Dog : public Animal {
  public:
    explicit Dog(std::string name) : Animal{std::move(name)} {}
    void bark() const { std::cout << std::format("  {} barks!\n", name_); }
};

int main() {
    // ── Polymorphism via Base Pointer ─────────────────────────
    std::cout << "=== Polymorphism ===\n";

    // Build a vector of Shape pointers — each holds a different concrete type
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));
    shapes.push_back(std::make_unique<Square>(3.0));

    // Calling print() on a Shape* calls the correct overridden methods
    for (const auto& s : shapes) {
        s->print();
    }

    // Calculate total area without knowing the concrete types
    double total{0.0};
    for (const auto& s : shapes) {
        total += s->area();  // each s->area() calls the right derived version
    }
    std::cout << std::format("Total area: {:.2f}\n\n", total);

    // ── Virtual Destructor Demo ───────────────────────────────
    // Because Shape::~Shape() is virtual, the correct derived destructor runs
    // when a unique_ptr<Shape> goes out of scope.
    // Without virtual ~Shape(), only ~Shape() would run — resource leaks.
    std::cout << "=== virtual destructor works correctly ===\n";
    {
        std::unique_ptr<Shape> s{std::make_unique<Circle>(1.0)};
        s->print();
    }  // ~Circle() runs here because ~Shape() is virtual
    std::cout << '\n';

    // ── Basic Inheritance ─────────────────────────────────────
    std::cout << "=== Basic Inheritance ===\n";
    Dog d{"Rex"};
    d.breathe();   // inherited from Animal
    d.bark();      // Dog's own method
    std::cout << std::format("  dog's name: {}\n\n", d.name());

    // ── Object Slicing ────────────────────────────────────────
    // Assigning a derived to a base by VALUE slices off the derived part
    std::cout << "=== Object Slicing (demonstration) ===\n";
    Circle c{5.0};
    // If Shape weren't abstract, this would slice: Shape s{c}; // loses Circle part
    // Instead, use reference or pointer to avoid slicing:
    const Shape& ref{c};
    std::cout << std::format("  via reference — area: {:.2f} (Circle::area called)\n",
                             ref.area());

    return 0;
}
