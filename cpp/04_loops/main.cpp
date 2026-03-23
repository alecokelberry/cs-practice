// ─────────────────────────────────────────────────────────────
//  Lesson 04 — Loops
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <numeric>   // std::accumulate
#include <ranges>    // std::views — C++20
#include <vector>

int main() {
    // ── while ─────────────────────────────────────────────────
    // Use when the iteration count is unknown
    std::cout << "while (0-4): ";
    int count{0};
    while (count < 5) {
        std::cout << count << ' ';
        ++count;  // prefix ++ is preferred
    }
    std::cout << '\n';

    // ── for ───────────────────────────────────────────────────
    // Use when the iteration count is known
    std::cout << "for (0-4): ";
    for (int i{0}; i < 5; ++i) {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    // ── do-while ──────────────────────────────────────────────
    // Guarantees at least one execution — body runs before condition is checked
    int x{100};
    do {
        std::cout << "do-while: ran even though x=" << x << " is not < 5\n";
    } while (x < 5);

    // ── break and continue ────────────────────────────────────
    std::cout << "skip 3, stop at 7: ";
    for (int i{0}; i < 10; ++i) {
        if (i == 3) continue;  // skip this iteration
        if (i == 7) break;     // exit the loop
        std::cout << i << ' ';
    }
    std::cout << '\n';  // output: 0 1 2 4 5 6

    // ── Range-based for ───────────────────────────────────────
    // The modern default for iterating over any collection
    std::vector<int> scores{85, 92, 78, 95, 88};

    std::cout << "scores: ";
    for (const auto& s : scores) {  // const auto& avoids copying each element
        std::cout << s << ' ';
    }
    std::cout << '\n';

    // Mutable range-based for — modifies elements in place
    for (auto& s : scores) {
        s += 5;
    }
    std::cout << "scores + 5: ";
    for (const auto& s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // ── std::accumulate ──────────────────────────────────────
    // Replaces a manual sum loop
    int    total{std::accumulate(scores.begin(), scores.end(), 0)};
    double avg{static_cast<double>(total) / static_cast<int>(scores.size())};
    std::cout << std::format("total: {}, average: {:.2f}\n", total, avg);

    // ── Ranges (C++20) ────────────────────────────────────────
    // Lazy, composable operations — no intermediate containers created
    std::cout << "scores > 90: ";
    for (int s : scores | std::views::filter([](int x){ return x > 90; })) {
        std::cout << s << ' ';
    }
    std::cout << '\n';

    // Chain: filter > 90, then scale by 1.1
    std::cout << "above 90, scaled: ";
    for (int s : scores
                 | std::views::filter([](int x){ return x > 90; })
                 | std::views::transform([](int x){ return static_cast<int>(x * 1.1); })) {
        std::cout << s << ' ';
    }
    std::cout << '\n';

    // ── Nested Loops ──────────────────────────────────────────
    std::cout << "3x3 multiplication:\n";
    for (int row{1}; row <= 3; ++row) {
        for (int col{1}; col <= 3; ++col) {
            std::cout << std::format("{:3}", row * col);
        }
        std::cout << '\n';
    }

    return 0;
}
