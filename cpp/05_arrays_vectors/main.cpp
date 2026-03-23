// ─────────────────────────────────────────────────────────────
//  Lesson 05 — Arrays & Vectors
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <algorithm>  // std::sort, std::find
#include <array>
#include <format>
#include <iostream>
#include <numeric>    // std::accumulate
#include <vector>

int main() {
    // ── C-Style Array (legacy) ────────────────────────────────
    // Shown for context — you'll see these in legacy code and C APIs.
    // No size awareness, no bounds checking, doesn't work cleanly with STL.
    int raw[5]{85, 92, 78, 95, 88};
    std::cout << "raw[0]=" << raw[0] << ", raw[4]=" << raw[4] << '\n';

    // ── std::array — Fixed-Size, Modern ──────────────────────
    // Same performance as C-array; knows its own size; works with STL
    std::array<int, 5> scores{85, 92, 78, 95, 88};

    std::cout << std::format("size: {}, front: {}, back: {}\n",
                             scores.size(), scores.front(), scores.back());

    scores.at(2) = 99;  // bounds-checked; throws std::out_of_range if bad index
    // scores[2]     — fast, no bounds check; use when index is known safe

    std::cout << "std::array: ";
    for (const auto& s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // Sort a std::array in place
    std::sort(scores.begin(), scores.end());
    std::cout << "sorted: ";
    for (const auto& s : scores) { std::cout << s << ' '; }
    std::cout << '\n';

    // ── std::vector — Dynamic, Preferred ─────────────────────
    std::vector<int> grades;
    grades.reserve(5);   // pre-allocate to avoid re-allocations during growth

    grades.emplace_back(70);  // construct in-place — preferred over push_back
    grades.emplace_back(80);
    grades.emplace_back(90);
    grades.emplace_back(95);

    std::cout << std::format("size: {}, capacity: {}\n",
                             grades.size(), grades.capacity());

    grades.pop_back();   // remove last element (95)

    std::cout << "grades: ";
    for (const auto& g : grades) { std::cout << g << ' '; }
    std::cout << '\n';

    // std::accumulate for sum without a manual loop
    int sum{std::accumulate(grades.begin(), grades.end(), 0)};
    double avg{static_cast<double>(sum) / static_cast<int>(grades.size())};
    std::cout << std::format("sum: {}, average: {:.2f}\n", sum, avg);

    // ── Sort and Find ─────────────────────────────────────────
    std::vector<int> nums{5, 2, 8, 1, 9, 3};
    std::sort(nums.begin(), nums.end());  // sort ascending

    auto it{std::find(nums.begin(), nums.end(), 8)};
    if (it != nums.end()) {
        std::cout << std::format("found 8 at index {}\n",
                                 std::distance(nums.begin(), it));
    }

    // Sort descending using a lambda comparator
    std::sort(nums.begin(), nums.end(), [](int a, int b){ return a > b; });
    std::cout << "descending: ";
    for (const auto& n : nums) { std::cout << n << ' '; }
    std::cout << '\n';

    // ── Vector of Strings ─────────────────────────────────────
    std::vector<std::string> courses;
    courses.emplace_back("C++ Fundamentals");
    courses.emplace_back("Data Structures");
    courses.emplace_back("Algorithms");

    for (const auto& c : courses) {
        std::cout << std::format("  - {}\n", c);
    }

    // ── 2D Vector ─────────────────────────────────────────────
    std::vector<std::vector<int>> grid{
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    std::cout << std::format("grid[1][2] = {}\n", grid[1][2]);  // 6

    return 0;
}
