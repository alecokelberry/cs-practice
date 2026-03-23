// ─────────────────────────────────────────────────────────────
//  Lesson 16 — Lambdas & Templates Basics
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <algorithm>
#include <concepts>
#include <format>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

// ── Function Templates ────────────────────────────────────────
// One implementation — works for any type that supports the operation
template <typename T>
[[nodiscard]] T square(T x) { return x * x; }

template <typename T>
[[nodiscard]] T maxOf(T a, T b) { return (a > b) ? a : b; }

// Concept constraint (C++20) — T must be an integral type
template <std::integral T>
[[nodiscard]] T gcd(T a, T b) {
    while (b) { auto t{b}; b = a % b; a = t; }
    return a;
}

// ── Class Template ────────────────────────────────────────────
template <typename T>
class Stack {
  public:
    void push(T val) { data_.push_back(std::move(val)); }

    void pop() {
        if (!data_.empty()) data_.pop_back();
    }

    [[nodiscard]] T&          top()   { return data_.back(); }
    [[nodiscard]] bool        empty() const { return data_.empty(); }
    [[nodiscard]] std::size_t size()  const { return data_.size(); }

  private:
    std::vector<T> data_;
};

// ── Function accepting any callable via template ──────────────
template <typename Fn>
void applyToEach(std::vector<int>& v, Fn fn) {
    for (auto& x : v) { x = fn(x); }
}

int main() {
    // ── Lambdas ───────────────────────────────────────────────
    std::cout << "=== Lambdas ===\n";

    // Basic lambda
    auto add{[](int a, int b) { return a + b; }};
    std::cout << std::format("  add(3, 5) = {}\n", add(3, 5));

    // Capture by value — snapshot of x at creation time
    int x{10};
    auto byVal{[x]() { return x * 2; }};
    x = 99;
    std::cout << std::format("  byVal() = {} (captured old x=10)\n", byVal());

    // Capture by reference — reads current x
    auto byRef{[&x]() { return x * 2; }};
    std::cout << std::format("  byRef() = {} (reads current x=99)\n", byRef());

    // mutable lambda — can modify the local captured copy
    int count{0};
    auto counter{[count]() mutable { return ++count; }};
    std::cout << std::format("  counter(): {}, {}, {}\n",
                             counter(), counter(), counter());
    std::cout << std::format("  original count unchanged: {}\n\n", count);

    // ── Generic Lambda ────────────────────────────────────────
    std::cout << "=== Generic Lambda ===\n";
    auto printAny{[](const auto& val) {
        std::cout << std::format("  {}\n", val);
    }};
    printAny(42);
    printAny(3.14);
    printAny(std::string{"hello"});

    // Generic lambda with two auto params
    auto genericAdd{[](auto a, auto b) { return a + b; }};
    std::cout << std::format("  genericAdd(1, 2)   = {}\n", genericAdd(1, 2));
    std::cout << std::format("  genericAdd(1.5, 2.5) = {}\n\n", genericAdd(1.5, 2.5));

    // ── Lambdas with STL ──────────────────────────────────────
    std::cout << "=== Lambdas with STL ===\n";
    std::vector<int> scores{55, 82, 91, 67, 78, 95};

    std::sort(scores.begin(), scores.end(), [](int a, int b){ return a > b; });
    std::cout << "  sorted desc: ";
    for (int s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // applyToEach with a template callable parameter — zero overhead vs std::function
    applyToEach(scores, [](int x){ return x + 5; });
    std::cout << "  after +5: ";
    for (int s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // std::function — type-erased callable storage
    std::function<int(int)> transform;
    bool boost{true};
    transform = boost
        ? std::function<int(int)>{[](int x){ return x + 10; }}
        : std::function<int(int)>{[](int x){ return x; }};
    std::cout << std::format("  transform(50) = {}\n\n", transform(50));

    // ── Function Templates ────────────────────────────────────
    std::cout << "=== Function Templates ===\n";
    std::cout << std::format("  square(5)    = {}\n", square(5));
    std::cout << std::format("  square(3.0)  = {}\n", square(3.0));
    std::cout << std::format("  maxOf(3, 7)  = {}\n", maxOf(3, 7));
    std::cout << std::format("  gcd(12, 8)   = {}\n", gcd(12, 8));
    // gcd(1.5, 2.5);  // compile error — double doesn't satisfy std::integral
    std::cout << '\n';

    // ── Class Template ────────────────────────────────────────
    std::cout << "=== Class Template (Stack<T>) ===\n";
    Stack<int> intStack;
    intStack.push(10);
    intStack.push(20);
    intStack.push(30);
    std::cout << std::format("  top: {}, size: {}\n", intStack.top(), intStack.size());
    intStack.pop();
    std::cout << std::format("  after pop, top: {}\n", intStack.top());

    Stack<std::string> strStack;
    strStack.push("first");
    strStack.push("second");
    std::cout << std::format("  string top: {}\n", strStack.top());

    return 0;
}
