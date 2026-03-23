// ─────────────────────────────────────────────────────────────
//  Lesson 10 — RAII & Memory Management
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <chrono>
#include <format>
#include <fstream>
#include <iostream>
#include <memory>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>

// ── Custom RAII Wrapper ───────────────────────────────────────
// Acquires a file on construction; releases it on destruction.
// Destructor runs even if an exception is thrown — that's the key guarantee.
class FileHandle {
  public:
    explicit FileHandle(const std::string& path) {
        file_.open(path);
        if (!file_.is_open()) {
            throw std::runtime_error{"Cannot open: " + path};
        }
        std::cout << std::format("  FileHandle: opened '{}'\n", path);
    }

    ~FileHandle() {
        if (file_.is_open()) {
            file_.close();
            std::cout << "  FileHandle: closed (destructor ran)\n";
        }
    }

    FileHandle(const FileHandle&)            = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&&)                 = default;
    FileHandle& operator=(FileHandle&&)      = default;

    std::ofstream& stream() { return file_; }

  private:
    std::ofstream file_;
};

// ── Scope Timer — RAII for Timing ────────────────────────────
class ScopeTimer {
  public:
    explicit ScopeTimer(std::string label) : label_{std::move(label)} {
        start_ = std::chrono::steady_clock::now();
    }
    ~ScopeTimer() {
        auto end{std::chrono::steady_clock::now()};
        auto us{std::chrono::duration_cast<std::chrono::microseconds>(end - start_).count()};
        std::cout << std::format("  Timer '{}': {} µs\n", label_, us);
    }
  private:
    std::string                            label_;
    std::chrono::steady_clock::time_point  start_;
};

// ── Rule of Zero — STL members manage themselves ─────────────
class Config {
  public:
    Config(std::string name, std::vector<std::string> keys)
        : name_{std::move(name)}, keys_{std::move(keys)} {}

    void print() const {
        std::cout << std::format("  Config '{}': {} keys\n", name_, keys_.size());
    }

    // No destructor, no copy/move defined — STL members handle everything.
    // This is the Rule of Zero: compose with types that already do RAII.

  private:
    std::string              name_;
    std::vector<std::string> keys_;
};

int main() {
    // ── std::fstream — File RAII ──────────────────────────────
    std::cout << "=== std::fstream (standard RAII) ===\n";
    {
        std::ofstream out{"raii_test.txt"};  // opens in constructor
        out << "Hello from RAII\n";
    }  // file closed here — destructor runs even if an exception occurs
    std::cout << "  file closed automatically after scope\n\n";

    // ── Custom FileHandle ─────────────────────────────────────
    std::cout << "=== Custom FileHandle ===\n";
    try {
        FileHandle fh{"raii_test2.txt"};
        fh.stream() << "Custom RAII-managed file\n";
    }  // fh goes out of scope — destructor closes the file
    catch (const std::exception& e) {
        std::cout << std::format("Error: {}\n", e.what());
    }
    std::cout << '\n';

    // ── Scope Timer ───────────────────────────────────────────
    std::cout << "=== ScopeTimer ===\n";
    {
        ScopeTimer t{"loop"};
        int sum{0};
        for (int i{0}; i < 1'000'000; ++i) { sum += i; }
        std::cout << std::format("  sum = {}\n", sum);
    }  // timer prints elapsed time in destructor
    std::cout << '\n';

    // ── std::lock_guard — Mutex RAII ─────────────────────────
    std::cout << "=== std::lock_guard ===\n";
    std::mutex mtx;
    {
        std::lock_guard<std::mutex> lock{mtx};  // locks in constructor
        std::cout << "  mutex is locked\n";
    }  // unlocked in destructor — even if an exception was thrown
    std::cout << "  mutex released\n\n";

    // ── Rule of Zero ─────────────────────────────────────────
    std::cout << "=== Rule of Zero ===\n";
    Config cfg{"server", {"host", "port", "timeout", "max-connections"}};
    cfg.print();
    // No manual cleanup needed — std::string and std::vector handle themselves

    return 0;
}
