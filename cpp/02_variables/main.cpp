// ─────────────────────────────────────────────────────────────
//  Lesson 02 — Variables & Assignments
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <cmath>
#include <format>
#include <iostream>
#include <string>

// constexpr: value known at compile time — preferred over const for literals
constexpr double PI{3.14159265358979};
constexpr int    MAX_STUDENTS{30};

int main() {
    // ── Core Types ────────────────────────────────────────────
    // {} initialization prevents narrowing: int x{3.9} is a compile error
    // whereas int x = 3.9 silently truncates to 3
    int         score{95};
    double      gpa{3.85};
    float       temp{98.6f};     // f suffix marks a float literal
    char        grade{'A'};
    bool        enrolled{true};
    std::string name{"Alice"};

    std::cout << std::format("Name: {}, Score: {}, GPA: {:.2f}\n",
                             name, score, gpa);

    // boolalpha: print "true"/"false" instead of 1/0
    std::cout << "Enrolled: " << std::boolalpha << enrolled << '\n';

    // ── auto ─────────────────────────────────────────────────
    // Compiler deduces the type — useful for long type names
    auto count{0};          // int
    auto ratio{0.75};       // double
    auto label{std::string{"exam"}};  // std::string
    std::cout << std::format("count: {}, ratio: {}, label: {}\n",
                             count, ratio, label);

    // ── Constants ─────────────────────────────────────────────
    std::cout << std::format("PI = {:.5f}, Max students = {}\n",
                             PI, MAX_STUDENTS);

    // ── Arithmetic ────────────────────────────────────────────
    int a{10}, b{3};
    std::cout << std::format("{} + {} = {}\n", a, b, a + b);
    std::cout << std::format("{} / {} = {} (integer division)\n", a, b, a / b);
    std::cout << std::format("{} % {} = {} (remainder)\n", a, b, a % b);

    // Cast to double for real division
    std::cout << std::format("{} / {} = {:.4f} (real division)\n",
                             a, b, static_cast<double>(a) / b);

    // ── Type Conversion ───────────────────────────────────────
    // static_cast<T> is explicit and safe — preferred over C-style (double)a
    double asDouble{static_cast<double>(score)};
    std::cout << std::format("static_cast: {} → {:.1f}\n", score, asDouble);

    // ── Compound Assignment ───────────────────────────────────
    int x{10};
    x += 5;   // 15
    x *= 2;   // 30
    ++x;      // 31 — prefix ++ preferred
    std::cout << std::format("x after +=5, *=2, ++: {}\n", x);

    // ── Math Functions ────────────────────────────────────────
    std::cout << std::format("pow(2, 8)   = {:.0f}\n", std::pow(2.0, 8.0));
    std::cout << std::format("sqrt(144)   = {:.0f}\n", std::sqrt(144.0));
    std::cout << std::format("ceil(4.1)   = {:.0f}\n", std::ceil(4.1));
    std::cout << std::format("floor(4.9)  = {:.0f}\n", std::floor(4.9));
    std::cout << std::format("abs(-7)     = {}\n",     std::abs(-7));

    return 0;
}
