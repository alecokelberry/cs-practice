# Lesson 08 — Raw Pointers

## Overview

A pointer stores a **memory address** — the location of another variable in memory. Understanding raw pointers is essential for reading legacy code, working with C APIs, and understanding what smart pointers (lesson 09) are doing under the hood. In modern C++, raw `new`/`delete` is rare — but raw pointers as non-owning observers are still common.

---

## Memory Basics

Every variable has:
1. A **value** — the data it holds
2. An **address** — where in memory it lives

```
int x{42};

Memory:  [ address: 0x7ffc5d ][ value: 42 ]
```

---

## Pointer Syntax

```cpp
int  x{10};
int* ptr{&x};   // ptr holds the ADDRESS of x
                //   & = "address-of" operator

std::cout << x;        // 10 (the value)
std::cout << &x;       // 0x7ffc... (the address)
std::cout << ptr;      // 0x7ffc... (same address — ptr stores it)
std::cout << *ptr;     // 10 — * dereferences: gives the value at that address
```

- `&` (address-of) — gives the address of a variable
- `*` in a declaration (`int* ptr`) — declares a pointer variable
- `*` in an expression (`*ptr`) — dereferences: "give me what's at this address"

---

## Modifying Through a Pointer

```cpp
int x{10};
int* ptr{&x};

*ptr = 99;    // changes x through the pointer
std::cout << x;  // 99
```

---

## `nullptr`

Always initialize pointers. An uninitialized pointer points to a random memory location — dereferencing it is undefined behavior (crash, memory corruption).

```cpp
int* ptr{nullptr};  // safe "empty" state

if (ptr != nullptr) {
    std::cout << *ptr;  // only dereference after checking
}
```

---

## The Arrow Operator (`->`)

When you have a pointer to an object, use `->` to access members:

```cpp
struct Node {
    int value{0};
};

Node  n{42};
Node* ptr{&n};

ptr->value;        // same as (*ptr).value
ptr->value = 99;   // same as (*ptr).value = 99
```

`->` = dereference + member access, combined.

---

## Dynamic Memory Allocation

`new` allocates memory on the **heap** — it persists until you explicitly `delete` it. The caller is responsible for freeing it.

```cpp
int* dynInt{new int{42}};   // allocate on heap
std::cout << *dynInt;
delete dynInt;              // REQUIRED — forgetting this is a memory leak
dynInt = nullptr;           // prevent dangling pointer (use after free)

// Dynamic array
int* arr{new int[3]{10, 20, 30}};
std::cout << arr[1];
delete[] arr;    // use delete[] for arrays — NOT just delete
arr = nullptr;
```

> In modern C++, prefer smart pointers (lesson 09) over raw `new`/`delete`. Smart pointers handle deallocation automatically.

---

## When Raw Pointers Are Still Used

Raw pointers aren't gone — they're just no longer used for *ownership*. They're still appropriate as **non-owning observers**:

```cpp
// The manager owns the resource; worker just observes it
auto manager{std::make_unique<Resource>()};
Resource* observer{manager.get()};  // raw pointer, no ownership

// observer can read/call methods — it does NOT delete anything
observer->doWork();
```

Common raw pointer use cases:
- Non-owning references to memory owned by a smart pointer
- Interfacing with C APIs (which expect raw pointers)
- Output parameters in legacy APIs
- Intrusive data structures (linked lists, trees) where ownership is explicit

---

## Common Pitfalls

| Mistake | What Happens | Fix |
|---------|-------------|-----|
| Forgetting `delete` | Memory leak | Use smart pointers (lesson 09) |
| Using pointer after `delete` | Undefined behavior / crash | Set to `nullptr` after delete |
| `delete` on an array | Undefined behavior | Use `delete[]` for arrays |
| Uninitialized pointer | Crash or silent corruption | Always initialize to `nullptr` |
| Double `delete` | Crash | Use smart pointers; set to `nullptr` after delete |

---

## Quick Reference Card

```cpp
// Pointer basics
int  x{42};
int* ptr{&x};   // address-of
*ptr;           // dereference
ptr->member;    // arrow (dereference + member access)

// nullptr
int* p{nullptr};
if (p != nullptr) { ... }

// Dynamic memory (prefer smart pointers — see lesson 09)
int* heap{new int{10}};
delete heap;
heap = nullptr;

int* arr{new int[5]};
delete[] arr;
arr = nullptr;

// Non-owning observer
auto owner{std::make_unique<Foo>()};
Foo* observer{owner.get()};  // raw, no ownership
```
