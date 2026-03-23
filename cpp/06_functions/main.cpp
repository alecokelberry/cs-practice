// ─────────────────────────────────────────────────────────────
//  Lesson 06 — Functions
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <algorithm>
#include <format>
#include <iostream>
#include <string>
#include <vector>

// ── Forward Declarations ──────────────────────────────────────
// Define the signature here so main() can call these before their definitions
[[nodiscard]] int    add(int a, int b);
[[nodiscard]] double add(double a, double b);  // overload — same name, different types
void printName(const std::string& name);
void increment(int& value);
void greet(const std::string& name, const std::string& greeting = "Hello");
[[nodiscard]] double computeGPA(int totalPoints, int courseCount);

// ── Definitions ───────────────────────────────────────────────

// Pass by value: a copy is made, original unchanged — fine for small types
int    add(int a, int b)       { return a + b; }
double add(double a, double b) { return a + b; }

// Pass by const&: no copy, read-only — use for strings, vectors, any large object
void printName(const std::string& name) {
    std::cout << std::format("Name: {}\n", name);
}

// Pass by reference: gives direct access to the original — use when you need to modify it
void increment(int& value) { ++value; }

// Default parameter — "Hello" is used if no greeting is provided
void greet(const std::string& name, const std::string& greeting) {
    std::cout << std::format("{}, {}!\n", greeting, name);
}

// [[nodiscard]]: compiler warns if the caller discards the return value
[[nodiscard]] double computeGPA(int totalPoints, int courseCount) {
    return static_cast<double>(totalPoints) / courseCount;
}

// ── Main ──────────────────────────────────────────────────────
int main() {
    // Function calls
    std::cout << std::format("add(3, 5)     = {}\n", add(3, 5));
    std::cout << std::format("add(1.5, 2.5) = {}\n", add(1.5, 2.5));

    // Pass by reference — modifies the original
    int score{90};
    increment(score);
    std::cout << std::format("score after increment: {}\n", score);  // 91

    // Pass by const reference — no copy, read-only
    std::string course{"C++ Fundamentals"};
    printName(course);

    // Default parameter
    greet("Alice");              // Hello, Alice!
    greet("Bob", "Welcome");    // Welcome, Bob!

    // [[nodiscard]] — ignoring this would be a compiler warning
    double gpa{computeGPA(340, 4)};
    std::cout << std::format("GPA: {:.2f}\n", gpa);

    // ── Lambdas ───────────────────────────────────────────────
    // Anonymous functions — define right where you need them

    // Basic lambda
    auto square{[](int x) { return x * x; }};
    std::cout << std::format("square(5) = {}\n", square(5));

    // Capture by value — copies 'bonus' at lambda creation time
    int bonus{10};
    auto withBonus{[bonus](int base) { return base + bonus; }};
    std::cout << std::format("withBonus(85) = {}\n", withBonus(85));

    // Capture by reference — reads 'multiplier' when the lambda is called
    int multiplier{3};
    auto scale{[&multiplier](int x) { return x * multiplier; }};
    multiplier = 5;  // changing it affects the lambda
    std::cout << std::format("scale(4) = {}\n", scale(4));  // 20, not 12

    // Lambdas with STL algorithms
    std::vector<int> scores{72, 88, 55, 95, 63};

    // Sort descending
    std::sort(scores.begin(), scores.end(), [](int a, int b){ return a > b; });
    std::cout << "descending: ";
    for (const auto& s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // Count values above 80
    int high{static_cast<int>(
        std::count_if(scores.begin(), scores.end(), [](int s){ return s > 80; })
    )};
    std::cout << std::format("scores above 80: {}\n", high);

    return 0;
}
