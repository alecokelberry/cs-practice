// ─────────────────────────────────────────────────────────────
//  Lesson 11 — STL Containers
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <deque>
#include <format>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

int main() {
    // ── std::map — Ordered Key-Value ──────────────────────────
    std::cout << "=== std::map (sorted by key) ===\n";
    std::map<std::string, int> scores;

    scores.emplace("Alice", 95);  // preferred over operator[]
    scores.emplace("Bob",   82);
    scores.emplace("Carol", 91);
    scores["Dave"] = 78;          // operator[] — creates entry if missing

    // Iterate — always in sorted key order (A, B, C, D...)
    for (const auto& [name, score] : scores) {  // structured bindings (C++17)
        std::cout << std::format("  {}: {}\n", name, score);
    }

    // Safe access
    std::cout << std::format("Alice: {}\n", scores.at("Alice"));  // throws if missing

    // Check before accessing
    if (scores.contains("Bob")) {
        std::cout << std::format("Bob's score: {}\n", scores["Bob"]);
    }

    // Find returns an iterator
    auto it{scores.find("Carol")};
    if (it != scores.end()) {
        std::cout << std::format("Found Carol: {}\n", it->second);
    }

    scores.erase("Dave");
    std::cout << std::format("size after erase: {}\n\n", scores.size());

    // ── std::unordered_map — Hash Map ─────────────────────────
    std::cout << "=== std::unordered_map (O(1) average) ===\n";
    std::vector<std::string> words{"apple", "banana", "apple", "cherry", "banana", "apple"};
    std::unordered_map<std::string, int> freq;

    for (const auto& w : words) {
        ++freq[w];  // operator[] inserts 0 if absent, then we increment
    }

    for (const auto& [word, count] : freq) {
        std::cout << std::format("  {}: {}\n", word, count);
    }
    // Note: order is not guaranteed with unordered_map

    std::cout << std::format("contains 'apple': {}\n\n", freq.contains("apple"));

    // ── std::set — Ordered Unique Values ─────────────────────
    std::cout << "=== std::set (sorted, unique) ===\n";
    std::vector<int> nums{3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
    std::set<int> unique{nums.begin(), nums.end()};  // deduplicate on construction

    std::cout << "unique sorted: ";
    for (int n : unique) { std::cout << n << ' '; }  // 1 2 3 4 5 6 9
    std::cout << '\n';

    unique.insert(7);
    unique.erase(1);
    std::cout << std::format("contains 5: {}\n\n", unique.contains(5));

    // ── std::unordered_set — Fast Membership Test ─────────────
    std::cout << "=== std::unordered_set ===\n";
    std::unordered_set<std::string> visited;
    std::vector<std::string> pages{"home", "about", "home", "contact", "about"};

    for (const auto& page : pages) {
        if (visited.contains(page)) {
            std::cout << std::format("  already visited: {}\n", page);
        } else {
            visited.insert(page);
            std::cout << std::format("  visiting: {}\n", page);
        }
    }
    std::cout << '\n';

    // ── std::deque — Double-Ended Queue ──────────────────────
    std::cout << "=== std::deque ===\n";
    std::deque<int> dq;
    dq.push_back(10);   // add to back
    dq.push_back(20);
    dq.push_front(5);   // add to front — O(1), unlike vector
    dq.push_front(1);

    std::cout << "deque: ";
    for (int n : dq) { std::cout << n << ' '; }  // 1 5 10 20
    std::cout << '\n';

    dq.pop_front();  // remove 1
    dq.pop_back();   // remove 20
    std::cout << std::format("after pop front+back: front={}, back={}\n",
                             dq.front(), dq.back());  // 5, 10

    return 0;
}
