// ─────────────────────────────────────────────────────────────
//  Lesson 09 — Smart Pointers
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <memory>
#include <string>

// A class that announces construction and destruction — useful for tracing
class Resource {
  public:
    explicit Resource(std::string name) : name_{std::move(name)} {
        std::cout << std::format("  [+] Resource '{}' created\n", name_);
    }
    ~Resource() {
        std::cout << std::format("  [-] Resource '{}' destroyed\n", name_);
    }

    void use() const { std::cout << std::format("  using '{}'\n", name_); }

    // Non-copyable, movable
    Resource(const Resource&)            = delete;
    Resource& operator=(const Resource&) = delete;
    Resource(Resource&&)                 = default;
    Resource& operator=(Resource&&)      = default;

  private:
    std::string name_;
};

int main() {
    // ── unique_ptr — Single Owner ─────────────────────────────
    std::cout << "=== unique_ptr ===\n";
    {
        auto ptr{std::make_unique<Resource>("file")};
        ptr->use();
        // ptr automatically deletes "file" when it leaves this scope
    }
    std::cout << "after scope — file is already deleted\n\n";

    // Transfer ownership with std::move — source becomes nullptr
    std::cout << "--- ownership transfer ---\n";
    auto owner1{std::make_unique<Resource>("texture")};
    auto owner2{std::move(owner1)};  // owner1 → nullptr; owner2 takes over
    std::cout << std::format("owner1 is null: {}\n", owner1 == nullptr);
    owner2->use();
    std::cout << '\n';

    // ── shared_ptr — Shared Ownership ────────────────────────
    std::cout << "=== shared_ptr ===\n";
    {
        auto s1{std::make_shared<Resource>("network")};
        std::cout << std::format("use_count: {}\n", s1.use_count());  // 1

        {
            auto s2{s1};  // copy is OK — both now own the resource
            std::cout << std::format("use_count: {}\n", s1.use_count());  // 2
            s2->use();
        }  // s2 gone — count drops to 1; resource is NOT deleted yet

        std::cout << std::format("use_count after s2 gone: {}\n", s1.use_count());  // 1
    }  // s1 gone — count → 0 → resource deleted
    std::cout << '\n';

    // ── weak_ptr — Non-Owning Observer ───────────────────────
    std::cout << "=== weak_ptr ===\n";
    auto shared{std::make_shared<Resource>("cache")};
    std::weak_ptr<Resource> weak{shared};

    std::cout << std::format("weak.expired(): {}\n", weak.expired());  // false

    // To use a weak_ptr, "lock" it — returns shared_ptr or nullptr if gone
    if (auto locked{weak.lock()}) {
        locked->use();  // safe
    }

    shared.reset();  // release the shared_ptr — count → 0 → resource deleted
    std::cout << std::format("weak.expired() after reset: {}\n", weak.expired());  // true

    if (auto locked{weak.lock()}) {
        locked->use();  // never reached
    } else {
        std::cout << "resource is gone — lock() returned nullptr\n";
    }
    std::cout << '\n';

    // ── Raw Pointer from .get() ───────────────────────────────
    std::cout << "=== non-owning raw pointer ===\n";
    auto uptr{std::make_unique<Resource>("owned")};
    Resource* raw{uptr.get()};  // raw observer — does NOT own the resource
    raw->use();                  // safe as long as uptr is alive
    // do NOT delete raw — uptr will clean up

    return 0;
}
