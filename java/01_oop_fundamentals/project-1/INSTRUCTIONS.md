## Exercise: Build a `Student` class

Create a file called `Student.java` anywhere you like (e.g. `java/01_oop_fundamentals/Student.java`).

### Requirements

**1. Fields (all `private`)**
- `name` (String)
- `studentId` (int)
- `gpa` (double)
- `studentCount` (static int) — tracks how many Student objects have been created

**2. Constructor**
- Takes `name`, `studentId`, and `gpa`
- Validates that `gpa` is between 0.0 and 4.0 — throw `IllegalArgumentException` if not
- Increments `studentCount` each time a new student is created

**3. Methods**
- Getters for all three instance fields
- A static `getStudentCount()` method
- Override `toString()` to return something like: `Student[id=1, name=Alice, gpa=3.8]`

**4. A `main` method** (in the same file or a separate `Main.java`) that:
- Creates 2-3 students
- Prints each one using `System.out.println(student)` — this calls `toString()` automatically
- Prints the total student count via `Student.getStudentCount()`
- Tries to create a student with a bad GPA (5.0) inside a `try/catch` and prints the error message

---

### How to compile and run

```bash
javac Student.java && java Student
```

If your `main` is in a separate file:
```bash
javac Student.java Main.java && java Main
```

---

### What you're practicing

| Concept | Where |
|---------|-------|
| `private` fields | All fields |
| Constructor + `this` | Setting fields |
| Validation | GPA check |
| `static` | `studentCount` |
| `toString()` override | Printing |
| `try/catch` | Bad GPA test |