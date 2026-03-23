// ─────────────────────────────────────────────────────────────
//  Lesson 12 — STL Algorithms
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <algorithm>
#include <format>
#include <iostream>
#include <numeric>
#include <ranges>
#include <string>
#include <vector>

void print(const std::string& label, const std::vector<int>& v) {
    std::cout << std::format("{}: ", label);
    for (int x : v) { std::cout << x << ' '; }
    std::cout << '\n';
}

int main() {
    std::vector<int> v{3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    print("original", v);

    // ── Sorting ───────────────────────────────────────────────
    std::vector<int> asc{v};
    std::ranges::sort(asc);                                   // ascending (C++20 ranges)
    print("sorted asc", asc);

    std::vector<int> desc{v};
    std::ranges::sort(desc, std::greater<int>{});             // descending
    print("sorted desc", desc);

    // ── Searching ─────────────────────────────────────────────
    std::cout << '\n';
    auto it{std::ranges::find(asc, 5)};
    if (it != asc.end()) {
        std::cout << std::format("find(5) at index {}\n",
                                 std::distance(asc.begin(), it));
    }

    bool found9{std::ranges::binary_search(asc, 9)};  // requires sorted
    std::cout << std::format("binary_search(9): {}\n", found9);

    auto big{std::ranges::find_if(v, [](int x){ return x > 7; })};
    if (big != v.end()) {
        std::cout << std::format("first element > 7: {}\n", *big);
    }

    // ── Testing ───────────────────────────────────────────────
    std::cout << '\n';
    std::cout << std::format("any > 8:    {}\n",
        std::ranges::any_of(v,  [](int x){ return x > 8; }));
    std::cout << std::format("all > 0:    {}\n",
        std::ranges::all_of(v,  [](int x){ return x > 0; }));
    std::cout << std::format("none < 0:   {}\n",
        std::ranges::none_of(v, [](int x){ return x < 0; }));

    int fives{static_cast<int>(std::ranges::count(v, 5))};
    int evens{static_cast<int>(std::ranges::count_if(v, [](int x){ return x % 2 == 0; }))};
    std::cout << std::format("count(5) = {}, count_if(even) = {}\n", fives, evens);

    // ── Transforming ──────────────────────────────────────────
    std::cout << '\n';
    std::vector<int> squares(v.size());
    std::transform(v.begin(), v.end(), squares.begin(),
                   [](int x){ return x * x; });
    print("squares", squares);

    std::vector<int> doubled{v};
    std::ranges::for_each(doubled, [](int& x){ x *= 2; });
    print("doubled (for_each)", doubled);

    // ── Accumulation ─────────────────────────────────────────
    std::cout << '\n';
    int sum{std::accumulate(v.begin(), v.end(), 0)};
    std::cout << std::format("sum = {}\n", sum);

    int product{std::accumulate(asc.begin(), asc.end(), 1,
                                std::multiplies<int>{})};
    std::cout << std::format("product = {}\n", product);

    // ── Removing ──────────────────────────────────────────────
    std::cout << '\n';
    std::vector<int> cleaned{v};

    // erase-remove idiom (classic)
    cleaned.erase(std::remove(cleaned.begin(), cleaned.end(), 1), cleaned.end());
    print("after erase(1)", cleaned);

    // C++20 shorthand
    std::erase(cleaned, 3);
    print("after std::erase(3)", cleaned);

    std::erase_if(cleaned, [](int x){ return x > 5; });
    print("after erase_if(>5)", cleaned);

    // ── Copying ───────────────────────────────────────────────
    std::cout << '\n';
    std::vector<int> evensOnly;
    std::copy_if(v.begin(), v.end(), std::back_inserter(evensOnly),
                 [](int x){ return x % 2 == 0; });
    print("copy_if(even)", evensOnly);

    // ── Ranges + Views Pipeline ───────────────────────────────
    std::cout << '\n';
    std::cout << "ranges pipeline (filter >3, then *2): ";
    for (int x : v
                 | std::views::filter([](int n){ return n > 3; })
                 | std::views::transform([](int n){ return n * 2; })) {
        std::cout << x << ' ';
    }
    std::cout << '\n';

    return 0;
}
