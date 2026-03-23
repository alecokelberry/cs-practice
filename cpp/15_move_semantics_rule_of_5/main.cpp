// ─────────────────────────────────────────────────────────────
//  Lesson 15 — Move Semantics & Rule of 5
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

// ── Rule of 5 Example — manages a raw heap buffer ─────────────
// This is a teaching example. In real code, use std::vector (Rule of 0).
class Buffer {
  public:
    explicit Buffer(std::size_t size, int fillValue = 0)
        : data_{new int[size]}, size_{size}
    {
        std::fill(data_, data_ + size_, fillValue);
        std::cout << std::format("  Buffer({}) constructed\n", size_);
    }

    // 1. Destructor
    ~Buffer() {
        delete[] data_;
        std::cout << std::format("  Buffer({}) destroyed\n", size_);
    }

    // 2. Copy constructor — deep copy
    Buffer(const Buffer& other)
        : data_{new int[other.size_]}, size_{other.size_}
    {
        std::copy(other.data_, other.data_ + size_, data_);
        std::cout << std::format("  Buffer({}) copied\n", size_);
    }

    // 3. Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this == &other) return *this;
        delete[] data_;
        size_ = other.size_;
        data_ = new int[size_];
        std::copy(other.data_, other.data_ + size_, data_);
        std::cout << std::format("  Buffer({}) copy-assigned\n", size_);
        return *this;
    }

    // 4. Move constructor — steal the resource, leave source empty
    Buffer(Buffer&& other) noexcept
        : data_{other.data_}, size_{other.size_}
    {
        other.data_ = nullptr;  // leave source in valid empty state
        other.size_ = 0;
        std::cout << std::format("  Buffer moved (noexcept)\n");
    }

    // 5. Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this == &other) return *this;
        delete[] data_;           // free current resource
        data_       = other.data_;
        size_       = other.size_;
        other.data_ = nullptr;
        other.size_ = 0;
        std::cout << "  Buffer move-assigned\n";
        return *this;
    }

    [[nodiscard]] std::size_t size()  const { return size_; }
    [[nodiscard]] int         at(std::size_t i) const { return data_[i]; }

  private:
    int*        data_{nullptr};
    std::size_t size_{0};
};

// ── Rule of 0 Example — composes with STL types ───────────────
class Config {
  public:
    Config(std::string name, std::vector<int> values)
        : name_{std::move(name)}, values_{std::move(values)} {}

    void print() const {
        std::cout << std::format("  Config '{}': {} values\n", name_, values_.size());
    }

    // No destructor, copy, or move defined — STL members handle everything
    // Move semantics work automatically and correctly
};

int main() {
    // ── std::move on STL types ────────────────────────────────
    std::cout << "=== std::move on std::vector ===\n";
    std::vector<int> a{1, 2, 3, 4, 5};
    std::cout << std::format("  a.size() before move: {}\n", a.size());

    std::vector<int> b{std::move(a)};  // transfer a's buffer to b; a becomes empty
    std::cout << std::format("  a.size() after move:  {}\n", a.size());  // 0
    std::cout << std::format("  b.size() after move:  {}\n\n", b.size());  // 5

    // ── Buffer Rule of 5 Demo ─────────────────────────────────
    std::cout << "=== Buffer (Rule of 5) ===\n";
    {
        Buffer buf1{5, 42};
        std::cout << std::format("  buf1[0] = {}\n", buf1.at(0));

        // Copy — deep copy, both have independent data
        Buffer buf2{buf1};
        std::cout << std::format("  buf2[0] = {} (copy)\n", buf2.at(0));

        // Move — buf1's data transferred to buf3; buf1 becomes empty
        Buffer buf3{std::move(buf1)};
        std::cout << std::format("  buf3[0] = {} (moved from buf1)\n", buf3.at(0));
        std::cout << std::format("  buf1.size() = {} (now empty)\n", buf1.size());
    }
    std::cout << "  (destructors ran above)\n\n";

    // ── Rule of 0 Demo ────────────────────────────────────────
    std::cout << "=== Config (Rule of 0) ===\n";
    Config c1{"server", {80, 443, 8080}};
    c1.print();

    // Move works automatically — STL members move themselves
    Config c2{std::move(c1)};
    c2.print();

    // ── std::move in constructor ───────────────────────────────
    std::cout << "\n=== std::move in constructor argument ===\n";
    std::string name{"Alice"};
    std::cout << std::format("  name before move: '{}'\n", name);
    Config c3{std::move(name), {1, 2, 3}};  // name is moved into Config
    std::cout << std::format("  name after move: '{}'\n", name);  // empty (moved-from)
    c3.print();

    return 0;
}
