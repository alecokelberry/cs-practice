// ─────────────────────────────────────────────────────────────
//  Lesson 03 — Branches
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <string>

int main() {
    // ── if / else if / else ───────────────────────────────────
    int score{85};

    if (score >= 90) {
        std::cout << std::format("Score {} → Grade A\n", score);
    } else if (score >= 80) {
        std::cout << std::format("Score {} → Grade B\n", score);
    } else if (score >= 70) {
        std::cout << std::format("Score {} → Grade C\n", score);
    } else {
        std::cout << std::format("Score {} → Grade F\n", score);
    }

    // ── Logical Operators ─────────────────────────────────────
    bool enrolled{true};
    bool hasPayment{false};

    if (enrolled && !hasPayment) {
        std::cout << "Enrolled but payment is missing.\n";
    }

    // ── if with Initializer (C++17) ───────────────────────────
    // The variable 'bonus' only exists inside this if/else block
    if (int bonus{score - 80}; bonus > 0) {
        std::cout << std::format("Bonus points above 80: {}\n", bonus);
    }

    // ── Ternary Operator ──────────────────────────────────────
    auto result{(score >= 60) ? "Pass" : "Fail"};
    std::cout << std::format("Result: {}\n", result);

    // ── switch ────────────────────────────────────────────────
    char menuOption{'b'};
    switch (menuOption) {
        case 'a':
            std::cout << "Option A: View profile\n";
            break;
        case 'b':
            std::cout << "Option B: Edit settings\n";
            break;
        case 'c':
            std::cout << "Option C: Logout\n";
            break;
        default:
            std::cout << "Invalid option\n";
            break;
    }

    // ── [[fallthrough]] — Intentional Fallthrough ─────────────
    // Without [[fallthrough]], the compiler may warn about a missing break.
    // With it, you document that falling through is deliberate.
    int dayNum{6};  // Saturday
    switch (dayNum) {
        case 1: case 2: case 3: case 4: case 5:
            std::cout << "Weekday\n";
            break;
        case 6:
            std::cout << "Saturday — almost done!\n";
            [[fallthrough]];   // intentionally falls through to case 7
        case 7:
            std::cout << "Weekend!\n";
            break;
        default:
            std::cout << "Invalid day\n";
            break;
    }

    return 0;
}
