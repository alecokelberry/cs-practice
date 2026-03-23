// ─────────────────────────────────────────────────────────────
//  Lesson 14 — const Correctness
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <string>
#include <vector>

// ── constexpr function — evaluated at compile time ────────────
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}
constexpr int FACT5{factorial(5)};  // 120, computed at compile time

// ── Class demonstrating const member functions ────────────────
class Temperature {
  public:
    explicit Temperature(double celsius) : celsius_{celsius} {}

    // const getters: won't modify the object; callable on const Temperature
    [[nodiscard]] double celsius()    const { return celsius_; }
    [[nodiscard]] double fahrenheit() const { return celsius_ * 9.0 / 5.0 + 32.0; }

    // non-const setter: modifies the object
    void setCelsius(double c) { celsius_ = c; }

    void print() const {
        std::cout << std::format("  {:.1f}°C = {:.1f}°F\n", celsius_, fahrenheit());
    }

  private:
    double celsius_;
};

// ── Class with mutable cache ───────────────────────────────────
class CachedFibonacci {
  public:
    // result() is logically const — it doesn't change observable state.
    // But we cache internally using mutable to avoid recomputing.
    [[nodiscard]] long long result(int n) const {
        if (n == last_n_) return cached_;       // return cached value
        last_n_ = n;
        cached_ = compute(n);
        return cached_;
    }

  private:
    mutable int       last_n_{-1};
    mutable long long cached_{0};

    static long long compute(int n) {
        if (n <= 1) return n;
        long long a{0}, b{1};
        for (int i{2}; i <= n; ++i) { auto t{a + b}; a = b; b = t; }
        return b;
    }
};

int main() {
    // ── const Variables ───────────────────────────────────────
    std::cout << "=== const variables ===\n";
    constexpr double PI{3.14159265358979};
    const int MAX{100};
    std::cout << std::format("PI = {:.5f}, MAX = {}, FACT5 = {}\n\n",
                             PI, MAX, FACT5);

    // ── const Reference Parameters ────────────────────────────
    std::cout << "=== const& parameter ===\n";
    auto print{[](const std::string& s) {
        std::cout << std::format("  length of '{}' = {}\n", s, s.size());
        // s += "!";  // compile error — s is const
    }};
    std::string greeting{"Hello"};
    print(greeting);
    std::cout << '\n';

    // ── const Member Functions ────────────────────────────────
    std::cout << "=== const member functions ===\n";
    Temperature t{100.0};
    t.print();         // 100.0°C = 212.0°F

    // const object — can only call const methods
    const Temperature freezing{0.0};
    freezing.print();
    // freezing.setCelsius(10.0);  // compile error — setCelsius is not const

    t.setCelsius(37.0);
    t.print();
    std::cout << '\n';

    // ── const Pointer Variations ──────────────────────────────
    std::cout << "=== const pointer variations ===\n";
    int x{10}, y{20};

    // Pointer to const — can't modify the pointed-to value
    const int* p1{&x};
    std::cout << std::format("  *p1 = {}\n", *p1);
    p1 = &y;           // OK — can point elsewhere
    // *p1 = 99;       // compile error — pointed-to value is const

    // Const pointer — can't reassign the pointer itself
    int* const p2{&x};
    *p2 = 99;          // OK — can change the value
    // p2 = &y;        // compile error — pointer is const
    std::cout << std::format("  x after *p2=99: {}\n", x);

    // Const pointer to const — neither can change
    const int* const p3{&y};
    std::cout << std::format("  *p3 = {}\n", *p3);
    // *p3 = 5;        // compile error
    // p3 = &x;        // compile error
    std::cout << '\n';

    // ── mutable Cache ─────────────────────────────────────────
    std::cout << "=== mutable cache ===\n";
    const CachedFibonacci fib;  // const object
    for (int n : {10, 10, 20, 20, 30}) {
        std::cout << std::format("  fib({}) = {}\n", n, fib.result(n));
    }

    return 0;
}
