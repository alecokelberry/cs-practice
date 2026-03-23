// ─────────────────────────────────────────────────────────────
//  Lesson 01 — Introduction to C++
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <string>

int main() {
    // ── Comments ──────────────────────────────────────────────
    // Single-line comment

    /* Multi-line
       comment */

    // ── Output ────────────────────────────────────────────────
    // Use std:: explicitly — don't write "using namespace std"
    // Use '\n' over std::endl — endl flushes the buffer every call, which is slower
    std::cout << "Hello, C++!\n";

    // Chain multiple values with <<
    std::string course{"C++ Fundamentals"};
    int         year{2026};
    std::cout << "Course: " << course << ", Year: " << year << '\n';

    // ── std::format (C++20) ───────────────────────────────────
    // Like Python f-strings — cleaner than chaining << for formatted output
    std::string msg{std::format("Course: {}, Year: {}", course, year)};
    std::cout << msg << '\n';

    // Format specifiers work too
    double pi{3.14159265};
    std::cout << std::format("PI ≈ {:.4f}\n", pi);
    std::cout << std::format("Score: {:3d}%\n", 95);  // right-aligned, width 3

    // ── Input ─────────────────────────────────────────────────
    // Uncomment to try interactive input:
    // std::string name;
    // std::cout << "Enter your name: ";
    // std::getline(std::cin, name);   // reads the full line, including spaces
    //                                 // cin >> misses spaces
    // std::cout << std::format("Hello, {}!\n", name);

    return 0;
}
