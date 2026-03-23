# 01 — OOP Fundamentals

Java is object-oriented from the ground up. Every piece of code lives inside a class. This lesson covers the building blocks: classes, objects, constructors, access modifiers, and the core OOP concepts Java is built around.

---

## Classes and Objects

A **class** is a blueprint. An **object** is an instance of that blueprint.

```java
public class Dog {
    // Fields (instance variables)
    private String name;
    private int age;

    // Constructor
    public Dog(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Method
    public void bark() {
        System.out.println(name + " says: Woof!");
    }
}

// Creating an object
Dog rex = new Dog("Rex", 3);
rex.bark(); // Rex says: Woof!
```

`this` refers to the current instance. It disambiguates when a parameter name matches a field name.

---

## Access Modifiers

| Modifier | Same Class | Same Package | Subclass | Anywhere |
|----------|-----------|--------------|----------|---------|
| `private` | ✅ | ❌ | ❌ | ❌ |
| (none) | ✅ | ✅ | ❌ | ❌ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| `public` | ✅ | ✅ | ✅ | ✅ |

**Rule of thumb:** Fields are `private`. Methods that form the public API are `public`. Everything else defaults to package-private until you have a reason to change it.

---

## Encapsulation — Getters and Setters

Make fields `private` and expose them through methods. This lets you validate or change the internal representation later without breaking callers.

```java
public class BankAccount {
    private double balance;

    public BankAccount(double initialBalance) {
        if (initialBalance < 0) throw new IllegalArgumentException("Balance can't be negative");
        this.balance = initialBalance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Deposit must be positive");
        balance += amount;
    }
}
```

Without encapsulation, any code could set `balance = -99999`. With it, the validation lives in one place.

---

## Static vs Instance

`static` means the member belongs to the **class**, not to any specific instance.

```java
public class Counter {
    private static int count = 0;  // shared across all instances
    private int id;                // unique per instance

    public Counter() {
        count++;
        this.id = count;
    }

    public static int getCount() { return count; }
    public int getId() { return id; }
}

Counter a = new Counter(); // count = 1, id = 1
Counter b = new Counter(); // count = 2, id = 2
Counter.getCount();        // 2 — called on the class, not an instance
```

Static methods can't access instance fields. Instance methods can access both.

---

## Constructors

A class can have multiple constructors (overloading). They differ by parameter list.

```java
public class Point {
    private final double x;
    private final double y;

    // Two-argument constructor
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // No-arg constructor — defaults to origin
    public Point() {
        this(0.0, 0.0);  // delegates to the two-arg constructor
    }
}
```

`this(...)` calls another constructor in the same class. It must be the first statement.

---

## `toString()` and `equals()`

`Object` is the root of every Java class. It provides default `toString()` and `equals()` — but the defaults are nearly useless.

```java
public class Point {
    private final double x;
    private final double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "Point(" + x + ", " + y + ")";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Point p)) return false;
        return Double.compare(x, p.x) == 0 && Double.compare(y, p.y) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}
```

**Always override `hashCode` when you override `equals`.** Objects used as HashMap keys or HashSet members depend on a consistent `hashCode`. The contract: if `a.equals(b)`, then `a.hashCode() == b.hashCode()`.

`instanceof Point p` is a **pattern match** (Java 16+) — it casts and names the variable in one step.

---

## `final`

| Context | Meaning |
|---------|---------|
| `final` field | Assigned once, never changed |
| `final` method | Can't be overridden in a subclass |
| `final` class | Can't be subclassed (e.g., `String`) |
| `final` variable | Can't be reassigned |

Prefer `final` fields for immutable data — it's a signal that the value won't change.

---

## Common Pitfalls

**Comparing strings with `==`**
```java
String a = new String("hello");
String b = new String("hello");
a == b;       // false — different objects
a.equals(b);  // true — same content
```
`==` compares references (memory addresses). `.equals()` compares content. Always use `.equals()` for strings.

**Forgetting `this` in constructors**
```java
// Bug: the parameter shadows the field, field is never set
public Dog(String name) {
    name = name;  // assigns parameter to itself
}

// Correct
public Dog(String name) {
    this.name = name;
}
```

**Mutable public fields**
```java
public class Config {
    public String apiKey; // anyone can set this to null or garbage
}
```
Make fields `private`. Expose them only through controlled methods.

---

## Quick Reference

```
Class declaration        public class Foo { ... }
Constructor              public Foo(Type param) { this.field = param; }
Field                    private Type name;
Static field             private static int count = 0;
Getter                   public Type getName() { return name; }
Setter                   public void setName(Type name) { this.name = name; }
Override toString        @Override public String toString() { return "..."; }
Override equals          @Override public boolean equals(Object o) { ... }
Delegate constructor     this(arg1, arg2);     // first line only
Call static method       ClassName.method();
Call instance method     object.method();
String comparison        a.equals(b)           // NOT a == b
Pattern match instanceof if (o instanceof Foo f) { f.method(); }
```
