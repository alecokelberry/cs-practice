# Lesson 09 — Smart Pointers

## Overview

Smart pointers are wrapper objects that **automatically delete** the memory they own when they go out of scope. No `delete` needed — no memory leaks. They express *ownership* explicitly in the type system, which makes code easier to reason about.

The three smart pointers in `<memory>`:
- `std::unique_ptr` — one owner
- `std::shared_ptr` — many owners (reference-counted)
- `std::weak_ptr` — non-owning reference to a `shared_ptr` resource

---

## `std::unique_ptr` — Single Owner

One `unique_ptr` owns the resource. When it goes out of scope (or is reset), the resource is deleted automatically.

```cpp
#include <memory>

auto ptr{std::make_unique<int>(42)};   // allocate + initialize
std::cout << *ptr;                     // dereference like a raw pointer
ptr->memberFn();                       // arrow operator works too

// ptr is deleted automatically when it goes out of scope — no delete needed
```

### Ownership Transfer

`unique_ptr` cannot be copied — only moved. After `std::move`, the source is `nullptr`.

```cpp
auto a{std::make_unique<Resource>()};
auto b{std::move(a)};   // b now owns the resource; a is nullptr

if (!a) std::cout << "a is now null\n";  // true
b->use();
```

### Releasing Ownership

```cpp
auto ptr{std::make_unique<Resource>()};

Resource* raw{ptr.release()};  // gives up ownership — YOU must delete raw now
delete raw;

// OR: reset destroys the current resource and optionally takes a new one
ptr.reset();                        // destroy and set to nullptr
ptr.reset(new Resource{});          // destroy old, take ownership of new
```

---

## `std::shared_ptr` — Shared Ownership

Multiple `shared_ptr`s can point to the same resource. The resource is destroyed when the **last** `shared_ptr` is gone (reference count drops to 0).

```cpp
auto s1{std::make_shared<Resource>()};
std::cout << s1.use_count();   // 1

{
    auto s2{s1};               // copy is OK — both own the resource
    std::cout << s1.use_count(); // 2
}  // s2 gone
std::cout << s1.use_count();   // 1 — resource still lives

s1.reset();                    // release s1's ownership; count → 0 → resource deleted
```

---

## `std::weak_ptr` — Non-Owning Observer

A `weak_ptr` observes a `shared_ptr` resource **without contributing to the reference count**. The resource can be deleted even while a `weak_ptr` exists.

Use it to break **circular references** (two `shared_ptr`s that own each other — count never reaches 0, causing a memory leak):

```cpp
auto shared{std::make_shared<Resource>()};
std::weak_ptr<Resource> weak{shared};

std::cout << weak.expired();  // false — resource still alive

// Must "lock" to use: returns a shared_ptr or nullptr if the resource is gone
if (auto locked{weak.lock()}) {
    locked->use();  // safe to use
}

shared.reset();  // release shared_ptr
std::cout << weak.expired();  // true — resource was deleted
```

### Breaking Circular References

```cpp
struct Node {
    std::shared_ptr<Node> next;   // owns next
    std::weak_ptr<Node>   prev;   // observes previous — no ownership cycle
};
```

If both `next` and `prev` were `shared_ptr`, two adjacent nodes would own each other and never be freed.

---

## When to Use What

| Situation | Use |
|-----------|-----|
| One clear owner | `unique_ptr` |
| Multiple owners sharing a resource | `shared_ptr` |
| Observe a `shared_ptr` resource without owning it | `weak_ptr` |
| Non-owning reference to any resource | raw pointer (`.get()`) |
| Avoid ownership entirely (read-only caller) | `const&` parameter |

**Default to `unique_ptr`.** Only upgrade to `shared_ptr` when multiple ownership is genuinely needed — it has higher overhead (atomic reference count).

---

## Getting the Raw Pointer

Sometimes you need a raw pointer (e.g., for a C API):

```cpp
auto ptr{std::make_unique<Resource>()};
Resource* raw{ptr.get()};   // raw pointer — does NOT transfer ownership
callCApi(raw);               // safe as long as ptr outlives this call
```

Never `delete` a raw pointer obtained via `.get()` — the smart pointer still owns it.

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `new` without a smart pointer | Wrap immediately: `std::make_unique<T>(...)` |
| Copying a `unique_ptr` | `unique_ptr` is move-only — use `std::move` |
| `shared_ptr` cycle | Break with `weak_ptr` on one side |
| Calling `.get()` and storing the raw pointer | Ensure the smart pointer outlives all raw pointer uses |
| Using `shared_ptr` everywhere | Prefer `unique_ptr` — less overhead, clearer ownership |

---

## Quick Reference Card

```cpp
#include <memory>

// unique_ptr — single owner
auto u{std::make_unique<T>(args...)};
u->member;        // arrow operator
*u;               // dereference
u.get();          // raw pointer (no ownership transfer)
u.reset();        // destroy and nullptr
auto v{std::move(u)};  // transfer ownership

// shared_ptr — shared ownership
auto s1{std::make_shared<T>(args...)};
auto s2{s1};          // copy OK — ref count ++
s1.use_count();       // current owner count
s1.reset();           // release this owner's share

// weak_ptr — non-owning observer
std::weak_ptr<T> w{s1};
w.expired();              // true if resource is gone
if (auto locked{w.lock()}) { locked->use(); }  // safe access
```
