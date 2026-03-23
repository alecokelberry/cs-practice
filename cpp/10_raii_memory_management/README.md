# Lesson 10 — RAII & Memory Management

## Overview

**RAII** (Resource Acquisition Is Initialization) is the central idiom of C++ resource management. The idea: tie a resource's lifetime to the lifetime of an object.

- **Acquire** the resource in the constructor
- **Release** it in the destructor

When the object goes out of scope — whether normally or because an exception was thrown — the destructor runs and the resource is freed. No `try/finally`, no manual cleanup.

---

## Why It Matters

Without RAII:

```cpp
void riskyFn() {
    FILE* f{fopen("data.txt", "r")};
    process(f);   // what if this throws?
    fclose(f);    // might never run — memory/resource leak
}
```

With RAII (using `std::fstream`):

```cpp
void riskyFn() {
    std::ifstream f{"data.txt"};  // opens in constructor
    process(f);                    // exception safe — destructor closes file
}                                  // file is closed here, guaranteed
```

---

## The Destructor as the Release Mechanism

```cpp
class Timer {
  public:
    Timer() { start_ = std::chrono::steady_clock::now(); }

    ~Timer() {
        auto end{std::chrono::steady_clock::now()};
        auto ms{std::chrono::duration_cast<std::chrono::milliseconds>(end - start_).count()};
        std::cout << std::format("Elapsed: {} ms\n", ms);
    }

  private:
    std::chrono::steady_clock::time_point start_;
};

void doWork() {
    Timer t;       // starts timing
    expensiveOp(); // even if this throws, ~Timer() runs
}                  // ~Timer() prints elapsed time
```

---

## Standard Library RAII Wrappers

The C++ standard library uses RAII everywhere:

| Type | Resource | Acquired | Released |
|------|----------|----------|---------|
| `std::ifstream` / `std::ofstream` | File handle | Constructor | Destructor |
| `std::unique_ptr<T>` | Heap memory | Constructor | Destructor |
| `std::shared_ptr<T>` | Heap memory (ref-counted) | Constructor | Last destructor |
| `std::lock_guard<M>` | Mutex lock | Constructor | Destructor |
| `std::scoped_lock<M...>` | Multiple mutex locks | Constructor | Destructor |

---

## Writing Your Own RAII Class

```cpp
class FileHandle {
  public:
    explicit FileHandle(const std::string& path) {
        file_.open(path);
        if (!file_.is_open()) {
            throw std::runtime_error{"Cannot open: " + path};
        }
    }

    ~FileHandle() {
        if (file_.is_open()) file_.close();
    }

    // RAII wrappers are usually non-copyable, move-only
    FileHandle(const FileHandle&)            = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&&)                 = default;
    FileHandle& operator=(FileHandle&&)      = default;

    std::ofstream& stream() { return file_; }

  private:
    std::ofstream file_;
};
```

---

## Mutex RAII — `std::lock_guard`

```cpp
#include <mutex>

std::mutex mtx;

void safeIncrement(int& counter) {
    std::lock_guard<std::mutex> lock{mtx};  // locks in constructor
    ++counter;
}  // unlocks in destructor — even if an exception was thrown
```

`std::scoped_lock` (C++17) handles multiple mutexes at once and avoids deadlocks:

```cpp
std::scoped_lock lock{mtx1, mtx2};  // locks both safely
```

---

## The Rule of Zero

If your class manages no resources directly — using STL containers and smart pointers instead — you don't need to write *any* of the special functions:

```cpp
class Config {
  public:
    Config(std::string name, std::vector<std::string> keys)
        : name_{std::move(name)}, keys_{std::move(keys)} {}

    void print() const { /* ... */ }

  private:
    std::string              name_;
    std::vector<std::string> keys_;
    // No destructor, no copy/move — the STL members handle everything
};
```

This is the **Rule of Zero**: prefer composition over manual resource management. When you can, let the types you use handle their own cleanup.

---

## The Rule of 5

If you *do* manage a resource directly (e.g., a raw pointer, a file descriptor), you likely need to define all five:

| Function | Reason |
|----------|--------|
| Destructor | Release the resource |
| Copy constructor | Deep-copy the resource |
| Copy assignment | Deep-copy; release old resource |
| Move constructor | Transfer resource ownership |
| Move assignment | Transfer; release old resource |

If you need to manage raw resources, prefer writing a dedicated RAII class for just that resource and then using Rule of Zero everywhere else.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Manual `fclose`/`delete` in destructors of non-RAII code | Wrap in RAII or use STL types |
| Forgetting that exceptions skip code below a throw | RAII guarantees cleanup regardless |
| Copying a RAII wrapper that owns a unique resource | `= delete` the copy constructor |
| Nested locks with `lock_guard` | Use `std::scoped_lock` to avoid deadlocks |

---

## Quick Reference Card

```cpp
// std::fstream (file RAII)
{
    std::ofstream out{"data.txt"};  // opens
    out << "hello\n";
}  // closes automatically

// lock_guard (mutex RAII)
{
    std::lock_guard<std::mutex> lock{mtx};
    // critical section
}  // unlocks automatically

// Custom RAII class pattern
class MyResource {
  public:
    MyResource()  { acquire(); }
    ~MyResource() { release(); }
    MyResource(const MyResource&)            = delete;
    MyResource& operator=(const MyResource&) = delete;
    MyResource(MyResource&&)                 = default;
    MyResource& operator=(MyResource&&)      = default;
};

// Rule of Zero — use this when possible
class Foo {
    std::unique_ptr<Bar> bar_;
    std::vector<int>     data_;
    // no destructor or copy/move needed
};
```
