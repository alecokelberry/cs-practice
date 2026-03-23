// ─────────────────────────────────────────────────────────────
//  Lesson 07 — Classes
//  Compile: g++ -std=c++20 main.cpp -o main && ./main
// ─────────────────────────────────────────────────────────────

#include <format>
#include <iostream>
#include <string>
#include <vector>

// ── Class Definition ──────────────────────────────────────────
class Student {
  public:
    // Member initializer list — initializes members directly, more efficient
    // than assigning inside the constructor body.
    // Required for const members and references.
    Student(std::string name, int id)
        : name_{std::move(name)}, id_{id}   // std::move avoids copying the string
    {}

    // Compiler-generated default constructor
    Student() = default;

    // Disallow copying — copy constructor and copy assignment are deleted.
    // Trying to copy a Student is a compile error instead of a silent performance hit.
    Student(const Student&)            = delete;
    Student& operator=(const Student&) = delete;

    // Allow moving
    Student(Student&&)            = default;
    Student& operator=(Student&&) = default;

    // const getter: won't modify the object — callable on const Student objects
    // [[nodiscard]]: warns if the caller ignores the return value
    [[nodiscard]] const std::string& name() const { return name_; }
    [[nodiscard]] int                id()   const { return id_;   }

    // Non-const setter — modifies the object
    void setName(std::string n) { name_ = std::move(n); }

    // const method: safe to call on const objects
    void print() const {
        std::cout << std::format("Student: {:15} | ID: {:5}\n", name_, id_);
    }

    [[nodiscard]] bool isHonors(double gpa) const { return gpa >= 3.5; }

  private:
    std::string name_;
    int         id_{0};  // in-class default — used if no constructor sets it
};

// ── struct ────────────────────────────────────────────────────
// struct = class with public by default; use for simple data bundles
struct CourseRecord {
    std::string code;
    std::string title;
    int         credits{3};  // in-class default
};

// ── Main ──────────────────────────────────────────────────────
int main() {
    // Construction
    Student s1{"Alice", 12345};
    s1.print();

    // Const object — can only call const member functions
    const Student s2{"Bob", 67890};
    s2.print();
    // s2.setName("Rob");  // compile error — setName is not const

    // Copy is deleted — this would be a compile error:
    // Student s3{s1};

    // Move is allowed — transfers ownership of s1's data to s3
    Student s3{std::move(s1)};
    s3.print();

    // Accessing via const getter
    std::cout << std::format("Name: {}, ID: {}\n", s2.name(), s2.id());

    // ── Vector of objects ─────────────────────────────────────
    std::vector<Student> roster;
    roster.reserve(3);
    roster.emplace_back("Carol", 1001);  // constructs directly in vector
    roster.emplace_back("Dave",  1002);
    roster.emplace_back("Eve",   1003);

    std::cout << "\nRoster:\n";
    for (const auto& s : roster) {
        s.print();
    }

    // ── struct usage ──────────────────────────────────────────
    CourseRecord c{"C867", "Scripting & Programming - C++"};
    std::cout << std::format("\n{} — {} ({} credits)\n",
                             c.code, c.title, c.credits);

    return 0;
}
