# 04 — Exceptions, Enums, Records

Three distinct features that each clean up a different kind of mess: exceptions for error handling, enums for fixed sets of constants with behavior, and records for data-only classes without boilerplate.

---

## Exceptions

Exceptions are objects that represent an error condition. When something goes wrong, code **throws** an exception. Calling code can **catch** it and decide what to do.

### The Exception Hierarchy

```
Throwable
├── Error              — JVM failures (OutOfMemoryError) — never catch these
└── Exception
    ├── RuntimeException  — unchecked — no compile-time enforcement
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   ├── IndexOutOfBoundsException
    │   └── ... (most common in practice)
    └── IOException, SQLException, ...  — checked — compiler forces you to handle them
```

**Checked exceptions:** The compiler requires you to either catch them or declare them in `throws`. They represent conditions the caller can reasonably handle (file not found, network error).

**Unchecked exceptions (RuntimeException):** No compile-time enforcement. They usually represent bugs — null pointer, bad index, invalid argument. Don't catch them unless you have a clear recovery strategy.

---

### try / catch / finally

```java
try {
    int result = 10 / 0; // ArithmeticException
    System.out.println(result);
} catch (ArithmeticException e) {
    System.out.println("Math error: " + e.getMessage());
} catch (Exception e) {
    System.out.println("Unexpected: " + e.getMessage());
} finally {
    System.out.println("Always runs — even if exception or return");
}
```

Catch blocks are checked top to bottom — put specific exceptions before general ones. Catching `Exception` before `ArithmeticException` would make the specific one unreachable.

**Multi-catch** (Java 7+):
```java
try {
    // ...
} catch (IOException | SQLException e) {
    // handle both the same way
}
```

---

### try-with-resources

Automatically closes resources that implement `AutoCloseable`. No need for a `finally` block to call `.close()`.

```java
// Old way
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    String line = reader.readLine();
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (reader != null) reader.close(); // must remember this
}

// Modern — resource is closed automatically when the try block exits
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
} catch (IOException e) {
    System.err.println("Could not read file: " + e.getMessage());
}
```

Multiple resources, closed in reverse declaration order:
```java
try (
    var conn = DriverManager.getConnection(url);
    var stmt = conn.prepareStatement(sql)
) {
    // ...
}
```

---

### Custom Exceptions

Extend `RuntimeException` for unchecked, `Exception` for checked.

```java
// Unchecked — caller doesn't have to handle it
public class InsufficientFundsException extends RuntimeException {
    private final double amount;

    public InsufficientFundsException(double amount) {
        super("Insufficient funds: tried to withdraw " + amount);
        this.amount = amount;
    }

    public double getAmount() {
        return amount;
    }
}

// Usage
public void withdraw(double amount) {
    if (amount > balance) {
        throw new InsufficientFundsException(amount);
    }
    balance -= amount;
}
```

**Exception chaining** — preserve the original cause:
```java
try {
    Files.readString(Path.of("config.json"));
} catch (IOException e) {
    throw new ConfigLoadException("Failed to load config", e); // e is the cause
}
```

---

## Enums

Enums define a fixed set of named constants. Unlike plain constants (`static final int`), enum values are typed — the compiler prevents you from passing an invalid value.

### Basic Enum

```java
public enum Direction {
    NORTH, SOUTH, EAST, WEST
}

Direction d = Direction.NORTH;
d.name();    // "NORTH" — the constant's name as a string
d.ordinal(); // 0 — position in declaration order (fragile, avoid using)

// Switch expression (Java 14+)
String label = switch (d) {
    case NORTH -> "Up";
    case SOUTH -> "Down";
    case EAST  -> "Right";
    case WEST  -> "Left";
};
```

### Enums with Fields and Methods

Enums can have constructors, fields, and methods. The constructor is always `private`.

```java
public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS  (4.869e+24, 6.0518e6),
    EARTH  (5.976e+24, 6.37814e6);

    private final double mass;   // kg
    private final double radius; // m

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    static final double G = 6.67300E-11;

    public double surfaceGravity() {
        return G * mass / (radius * radius);
    }

    public double surfaceWeight(double otherMass) {
        return otherMass * surfaceGravity();
    }
}

double earthWeight = 75.0;
double mass = earthWeight / Planet.EARTH.surfaceGravity();

for (Planet p : Planet.values()) {
    System.out.printf("Weight on %s is %6.2f%n", p, p.surfaceWeight(mass));
}
```

### Enum Utilities

```java
// values() — all constants as an array
Direction[] all = Direction.values();

// valueOf() — get by name (throws IllegalArgumentException if not found)
Direction north = Direction.valueOf("NORTH");

// EnumSet and EnumMap — efficient, specialized collections for enums
EnumSet<Direction> horizontal = EnumSet.of(Direction.EAST, Direction.WEST);
EnumMap<Direction, String> labels = new EnumMap<>(Direction.class);
labels.put(Direction.NORTH, "Up");
```

---

## Records

Records (Java 16+) are immutable data carriers. They generate a constructor, getters, `equals()`, `hashCode()`, and `toString()` automatically.

```java
// Before records — 40 lines of boilerplate
public final class Point {
    private final int x;
    private final int y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int x() { return x; }
    public int y() { return y; }
    @Override public boolean equals(Object o) { ... }
    @Override public int hashCode() { ... }
    @Override public String toString() { ... }
}

// With records — one line
public record Point(int x, int y) {}

// Usage
Point p = new Point(3, 4);
p.x();        // 3 — getter is x(), not getX()
p.y();        // 4
p.toString(); // "Point[x=3, y=4]"
p.equals(new Point(3, 4)); // true
```

### Compact Constructor

Validates or normalizes data. You don't re-assign fields — they're set from the parameters automatically.

```java
public record Range(int min, int max) {
    // Compact constructor — no parameter list, no this.field = field
    Range {
        if (min > max) throw new IllegalArgumentException("min must be <= max");
    }
}

new Range(1, 10); // ok
new Range(10, 1); // IllegalArgumentException
```

### Adding Methods to Records

```java
public record Point(double x, double y) {
    // Instance method
    public double distanceTo(Point other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // Static factory method
    public static Point origin() {
        return new Point(0, 0);
    }
}
```

**Records cannot:** extend a class (they implicitly extend `Record`), have non-final fields, or be subclassed.

---

## Common Pitfalls

**Catching too broadly**
```java
try {
    riskyOperation();
} catch (Exception e) {
    // Swallowed — hides bugs, makes debugging impossible
}
```
Catch the most specific exception you can handle.

**Using `ordinal()` for persistence**
```java
// Fragile — if you reorder enum constants, ordinal changes
int stored = Direction.NORTH.ordinal(); // 0 today, maybe 2 tomorrow
```
Use `name()` for strings or store the enum by name, not ordinal.

**Mutable fields in records**
Records are meant to be immutable, but if a component is a mutable object, it can still be mutated:
```java
public record UserData(List<String> roles) {}

UserData u = new UserData(new ArrayList<>(List.of("admin")));
u.roles().add("superuser"); // compiles — the list itself is mutable
```
Use `List.copyOf()` in the compact constructor to protect against this.

---

## Quick Reference

```
Exception handling
  try { } catch (SpecificException e) { } finally { }
  try (Resource r = ...) { }    // auto-close
  throw new SomeException("msg");
  throw new SomeException("msg", cause); // chain with cause

Custom exception
  class Foo extends RuntimeException { Foo(String msg) { super(msg); } }
  class Foo extends Exception { ... }   // checked

Enum
  enum Color { RED, GREEN, BLUE }
  enum Planet { EARTH(mass, radius); Planet(double m, double r) { ... } }
  Color.values()         // all constants
  Color.valueOf("RED")   // by name
  c.name()               // "RED"
  switch (c) { case RED -> ...; }

Record
  record Point(int x, int y) {}
  Point p = new Point(3, 4);
  p.x()  p.y()           // generated getters (no "get" prefix)
  p.toString()           // "Point[x=3, y=4]"
  p.equals(other)        // structural equality

Compact constructor
  record Range(int min, int max) {
      Range { if (min > max) throw ...; }
  }
```
