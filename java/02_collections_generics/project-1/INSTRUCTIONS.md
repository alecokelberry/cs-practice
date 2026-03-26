## Exercise: Build a `Gradebook`

Create two files in this folder: `Gradebook.java` and `Main.java`.

### Requirements

**1. `Gradebook` class**

- Stores a `Map<String, List<Integer>>` where the key is a student's name and the value is their list of scores
- All fields `private`

**2. Methods**

- `addScore(String name, int score)` — adds a score to the student's list; creates the list if the student doesn't exist yet (use `computeIfAbsent`)
- `getAverage(String name)` — returns the student's average score as a `double`; return `0.0` if the student isn't found
- `getTopStudents(double minAverage)` — returns a `List<String>` of names whose average is at or above `minAverage`; the list should be sorted A→Z
- `getAllNames()` — returns a `Set<String>` of all student names

**3. A generic utility method (static, on `Gradebook`)**

```java
public static <T extends Comparable<T>> T findMax(List<T> list)
```

- Returns the largest element in any `List` whose type supports comparison
- Throw `IllegalArgumentException` if the list is empty

**4. `Main.java`**

- Add scores for at least 3 students (give each 3–4 scores)
- Print each student's average: `"Alice: 91.5"`
- Print the names of students with an average ≥ 85
- Use `findMax` to find and print the highest score in a plain `List<Integer>` of your choice
- Demonstrate `getAllNames()` by printing all names

---

### How to compile and run

```bash
javac Gradebook.java Main.java && java Main
```

---

### What you're practicing

| Concept | Where |
|---------|-------|
| `HashMap` | Storing student → scores |
| `ArrayList` | Score lists per student |
| `computeIfAbsent` | Creating lists on first insert |
| `HashSet` / `Set<String>` | `getAllNames()` return type |
| Iterating `entrySet()` | Computing averages over all students |
| `Collections.sort` | Sorting names in `getTopStudents` |
| Generic method + bounded type | `findMax` |
| `IllegalArgumentException` | Empty-list guard |
