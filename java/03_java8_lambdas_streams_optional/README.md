# 03 — Java 8: Lambdas, Streams, Optional

Java 8 added functional programming tools that transformed how Java code is written. Lambdas replace anonymous classes, the Stream API replaces manual loops for data processing, and `Optional` is a typed container for values that might be absent.

---

## Functional Interfaces

A **functional interface** has exactly one abstract method. Lambdas implement functional interfaces.

```java
// The @FunctionalInterface annotation is optional but documents intent
@FunctionalInterface
public interface Transformer {
    String transform(String input);
}

// Old way — anonymous class
Transformer upper = new Transformer() {
    @Override
    public String transform(String input) {
        return input.toUpperCase();
    }
};

// Lambda — same thing, less noise
Transformer upper = input -> input.toUpperCase();
```

Java ships several built-in functional interfaces in `java.util.function`:

| Interface | Method | Description |
|-----------|--------|-------------|
| `Predicate<T>` | `boolean test(T t)` | Test a condition |
| `Function<T,R>` | `R apply(T t)` | Transform T to R |
| `Consumer<T>` | `void accept(T t)` | Use T, return nothing |
| `Supplier<T>` | `T get()` | Produce a T, take nothing |
| `BiFunction<T,U,R>` | `R apply(T t, U u)` | Transform two inputs |
| `UnaryOperator<T>` | `T apply(T t)` | Function where T in = T out |

```java
Predicate<String> isLong = s -> s.length() > 5;
isLong.test("hi");      // false
isLong.test("hello!");  // true

Function<String, Integer> length = String::length;
length.apply("hello");  // 5

Consumer<String> print = System.out::println;
print.accept("hello");  // prints "hello"

Supplier<List<String>> newList = ArrayList::new;
List<String> list = newList.get(); // new empty ArrayList
```

---

## Lambda Syntax

```java
// No parameters
Runnable r = () -> System.out.println("hello");

// One parameter (parens optional)
Predicate<String> isEmpty = s -> s.isEmpty();
Predicate<String> isEmpty = (s) -> s.isEmpty(); // same

// Multiple parameters
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

// Block body (multiple statements, explicit return)
Function<String, String> format = name -> {
    String trimmed = name.trim();
    return trimmed.isEmpty() ? "Unknown" : trimmed;
};
```

---

## Method References

Shorthand for lambdas that just call an existing method. Four forms:

```java
// 1. Static method: ClassName::staticMethod
Function<String, Integer> parse = Integer::parseInt;
// same as: s -> Integer.parseInt(s)

// 2. Instance method of a specific object: instance::method
String prefix = "Hello, ";
Function<String, String> greet = prefix::concat;
// same as: s -> prefix.concat(s)

// 3. Instance method of an arbitrary instance: ClassName::instanceMethod
Function<String, String> upper = String::toUpperCase;
// same as: s -> s.toUpperCase()

// 4. Constructor: ClassName::new
Supplier<ArrayList<String>> newList = ArrayList::new;
// same as: () -> new ArrayList<>()
```

---

## Stream API

Streams are a pipeline for processing sequences of elements. A stream has three parts: a **source**, zero or more **intermediate operations**, and a **terminal operation**.

```
source → [filter] → [map] → [sorted] → terminal (collect / forEach / reduce)
```

Streams are **lazy** — intermediate operations don't run until a terminal operation is called.

### Creating Streams

```java
List<String> names = List.of("Alice", "Bob", "Carol");

Stream<String> fromList    = names.stream();
Stream<String> fromArray   = Arrays.stream(new String[]{"a", "b"});
Stream<String> fromValues  = Stream.of("x", "y", "z");
IntStream range            = IntStream.range(0, 5);    // 0, 1, 2, 3, 4
IntStream rangeClosed      = IntStream.rangeClosed(1, 5); // 1, 2, 3, 4, 5
```

### Intermediate Operations (lazy, return a Stream)

```java
List<String> names = List.of("Alice", "Bob", "Carol", "Dave", "Eve");

names.stream()
    .filter(n -> n.length() > 3)     // keep Alice, Carol, Dave
    .map(String::toUpperCase)         // ALICE, CAROL, DAVE
    .sorted()                         // ALICE, CAROL, DAVE (alphabetical)
    .distinct()                       // remove duplicates
    .limit(2)                         // take first 2: ALICE, CAROL
    .skip(1)                          // skip first 1: CAROL
    .peek(n -> System.out.println(n)) // debug without consuming
    ...
```

### Terminal Operations (eager, trigger execution)

```java
List<String> names = List.of("Alice", "Bob", "Carol");

// collect — gather into a collection
List<String> filtered = names.stream()
    .filter(n -> n.startsWith("A"))
    .collect(Collectors.toList()); // or .toList() in Java 16+

// forEach — consume each element
names.stream().forEach(System.out::println);

// count
long count = names.stream().filter(n -> n.length() > 3).count(); // 2

// findFirst / findAny
Optional<String> first = names.stream().filter(n -> n.startsWith("C")).findFirst();

// anyMatch / allMatch / noneMatch
boolean hasShort = names.stream().anyMatch(n -> n.length() <= 3); // true (Bob, Eve)
boolean allLong  = names.stream().allMatch(n -> n.length() > 3);  // false

// reduce — fold elements into a single value
int total = IntStream.rangeClosed(1, 5).reduce(0, Integer::sum); // 15

// min / max
Optional<String> shortest = names.stream().min(Comparator.comparingInt(String::length));
```

### Collectors

```java
List<String> names = List.of("Alice", "Bob", "Carol", "Dave");

// toList
List<String> list = names.stream().collect(Collectors.toList());

// joining — concatenate strings
String joined = names.stream().collect(Collectors.joining(", ")); // "Alice, Bob, Carol, Dave"
String csv    = names.stream().collect(Collectors.joining(", ", "[", "]")); // "[Alice, Bob, ...]"

// groupingBy — like SQL GROUP BY
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));
// {5=[Alice, Carol], 3=[Bob], 4=[Dave]}

// counting — count per group
Map<Integer, Long> countByLength = names.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));

// toMap
Map<String, Integer> nameLengths = names.stream()
    .collect(Collectors.toMap(n -> n, String::length));
```

---

## Optional

`Optional<T>` is a container that either holds a value or is empty. It forces you to handle the "no value" case explicitly rather than checking for `null` everywhere.

```java
// Creating
Optional<String> present = Optional.of("hello");      // must be non-null
Optional<String> empty   = Optional.empty();
Optional<String> maybe   = Optional.ofNullable(null); // null becomes empty

// Checking and extracting
present.isPresent();  // true
empty.isPresent();    // false
present.isEmpty();    // false (Java 11+)

present.get();        // "hello" — throws NoSuchElementException if empty
present.orElse("default");               // "hello" (or "default" if empty)
present.orElseGet(() -> computeDefault()); // lazy — supplier only called if empty
present.orElseThrow(() -> new RuntimeException("missing")); // throw if empty

// Transforming
Optional<Integer> length = present.map(String::length); // Optional[5]
Optional<String> upper   = present.map(String::toUpperCase); // Optional["HELLO"]

// flatMap — when the mapping function also returns Optional
Optional<String> trimmed = present.flatMap(s -> s.isBlank() ? Optional.empty() : Optional.of(s.trim()));

// ifPresent — run code only if value exists
present.ifPresent(System.out::println); // prints "hello"
```

**When to use Optional:** Return types of methods that might not find a result. Do NOT use it as a field type or method parameter — it's for return values only.

```java
// Good use
public Optional<User> findById(int id) {
    return users.stream().filter(u -> u.getId() == id).findFirst();
}

// Caller handles the absence explicitly
findById(42)
    .map(User::getName)
    .orElse("Unknown");
```

---

## Common Pitfalls

**Reusing a stream**
```java
Stream<String> s = list.stream().filter(n -> n.length() > 3);
s.forEach(System.out::println); // fine
s.forEach(System.out::println); // IllegalStateException — stream already consumed
```

**Calling `Optional.get()` without checking**
```java
Optional<String> name = findName();
name.get(); // throws NoSuchElementException if empty — defeats the purpose
// Use orElse, orElseGet, or orElseThrow instead
```

**Modifying source data inside a stream**
```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
list.stream().forEach(s -> list.remove(s)); // ConcurrentModificationException
// Collect results to a new list instead
```

---

## Quick Reference

```
Lambda syntax
  () -> expr                   no params
  x -> expr                    one param
  (x, y) -> expr               two params
  (x, y) -> { ...; return v; } block body

Method references
  ClassName::staticMethod       static
  instance::method              bound instance
  ClassName::instanceMethod     unbound (instance chosen per element)
  ClassName::new                constructor

Stream pipeline
  .filter(predicate)           keep matching elements
  .map(function)               transform each element
  .flatMap(function)           transform + flatten
  .sorted() / .sorted(comp)   sort
  .distinct()                  deduplicate
  .limit(n) / .skip(n)        truncate / offset
  .collect(Collectors.toList()) gather to list
  .collect(Collectors.joining(", ")) concatenate strings
  .collect(Collectors.groupingBy(fn)) group into map
  .forEach(consumer)           consume (terminal)
  .count()                     count (terminal)
  .findFirst()                 first element → Optional (terminal)
  .anyMatch / allMatch / noneMatch  → boolean (terminal)
  .reduce(identity, accumulator)    fold (terminal)

Optional
  Optional.of(v)               non-null value
  Optional.ofNullable(v)       nullable value
  .isPresent() / .isEmpty()    check
  .orElse(default)             get or default
  .orElseGet(supplier)         get or compute
  .map(fn)                     transform if present
  .flatMap(fn)                 transform (fn returns Optional)
  .ifPresent(consumer)         act if present
```
