// ─────────────────────────────────────────────────────────────
//  Lesson 08 — Raw Pointers
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <memory>    // for non-owning observer demo at the end
#include <string>

struct Node {
    int         value{0};
    std::string label;

    Node(int v, std::string l) : value{v}, label{std::move(l)} {}
    void print() const {
        std::cout << std::format("Node[{}] = {}\n", label, value);
    }
};

int main() {
    // ── Pointer Basics ────────────────────────────────────────
    int x{42};
    int* ptr{&x};  // & = address-of; ptr stores the address of x

    std::cout << std::format("x      = {}\n", x);
    std::cout << std::format("*ptr   = {}\n", *ptr);   // dereference: value at address
    // ptr itself holds a memory address (printed as hex)
    std::cout << std::format("ptr    = {}\n", static_cast<void*>(ptr));

    // Modify x through the pointer
    *ptr = 99;
    std::cout << std::format("x after *ptr=99: {}\n", x);

    // ── nullptr ───────────────────────────────────────────────
    // Always initialize pointers — uninitialized pointers point to garbage memory.
    // Dereferencing garbage is undefined behavior (crash, corruption, or worse).
    int* p{nullptr};
    if (p != nullptr) {
        std::cout << *p;  // never reached
    } else {
        std::cout << "pointer is null — safe\n";
    }

    // ── Arrow Operator ────────────────────────────────────────
    // ptr->member is shorthand for (*ptr).member
    Node  n{10, "A"};
    Node* np{&n};
    std::cout << std::format("via ->: Node[{}] = {}\n", np->label, np->value);
    // same as: (*np).label and (*np).value

    // ── Dynamic Memory (new / delete) ─────────────────────────
    // Shown to build understanding — prefer smart pointers (lesson 09) in real code.
    // Caller is responsible for calling delete — forgetting it is a memory leak.
    int* dynInt{new int{55}};
    std::cout << std::format("heap int: {}\n", *dynInt);
    delete dynInt;    // free the memory
    dynInt = nullptr; // null out to prevent use-after-free

    // Dynamic array — must use delete[], NOT delete
    int* arr{new int[3]{10, 20, 30}};
    std::cout << std::format("arr[1] = {}\n", arr[1]);
    delete[] arr;     // delete[] for arrays
    arr = nullptr;

    // ── Arrow Operator with Dynamic Allocation ────────────────
    Node* dn{new Node{42, "B"}};
    dn->print();      // -> is shorthand for (*dn).print()
    delete dn;
    dn = nullptr;

    // ── Non-Owning Raw Pointer ────────────────────────────────
    // In modern C++, raw pointers are used as non-owning observers.
    // The smart pointer owns the resource; the raw pointer just looks at it.
    auto owner{std::make_unique<Node>(999, "Owner")};
    Node* observer{owner.get()};   // .get() returns the raw pointer — no ownership
    std::cout << std::format("observer sees: Node[{}] = {}\n",
                             observer->label, observer->value);
    // observer doesn't delete anything; owner handles cleanup automatically

    return 0;
}
