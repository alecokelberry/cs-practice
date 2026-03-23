# 02 — Collections & Generics

Java's Collections Framework is a set of interfaces and implementations for working with groups of objects. Generics let you write type-safe code that works with any type — the compiler catches type mismatches before the code runs.

---

## The Core Interfaces

```
Iterable
└── Collection
    ├── List     — ordered, allows duplicates (ArrayList, LinkedList)
    ├── Set      — no duplicates (HashSet, TreeSet, LinkedHashSet)
    └── Queue    — FIFO/priority ordering (LinkedList, PriorityQueue)

Map              — key-value pairs, not a Collection (HashMap, TreeMap)
```

Always program to the **interface**, not the implementation:

```java
// Preferred — you can swap ArrayList for LinkedList without changing callers
List<String> names = new ArrayList<>();

// Avoid — locks you into ArrayList everywhere
ArrayList<String> names = new ArrayList<>();
```

---

## ArrayList

Resizable array. Fast random access by index. Slow insert/remove in the middle.

```java
List<String> fruits = new ArrayList<>();
fruits.add("apple");
fruits.add("banana");
fruits.add("cherry");

fruits.get(1);           // "banana"
fruits.size();           // 3
fruits.contains("apple"); // true
fruits.remove("banana"); // removes by value
fruits.remove(0);        // removes by index

// Iterate
for (String fruit : fruits) {
    System.out.println(fruit);
}

// Sort
Collections.sort(fruits);

// Initialize with values (fixed-size — can't add/remove)
List<String> fixed = List.of("a", "b", "c");
```

---

## HashMap

Key-value store. Keys are unique. Order is not guaranteed. O(1) average for get/put.

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
scores.put("Alice", 100); // overwrites — keys are unique

scores.get("Alice");           // 100
scores.getOrDefault("Eve", 0); // 0 — safer than get() which returns null
scores.containsKey("Bob");     // true
scores.remove("Bob");

// Iterate entries
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}

// putIfAbsent — only sets if key doesn't exist
scores.putIfAbsent("Carol", 88);

// computeIfAbsent — useful for building nested structures
Map<String, List<String>> groups = new HashMap<>();
groups.computeIfAbsent("admins", k -> new ArrayList<>()).add("Alice");
```

---

## HashSet

Unordered collection of unique elements. O(1) average for add/contains/remove.

```java
Set<String> tags = new HashSet<>();
tags.add("java");
tags.add("backend");
tags.add("java"); // duplicate — silently ignored

tags.contains("java"); // true
tags.size();           // 2
tags.remove("backend");

// Set operations
Set<String> a = new HashSet<>(Set.of("x", "y", "z"));
Set<String> b = new HashSet<>(Set.of("y", "z", "w"));

a.retainAll(b); // intersection — a is now {y, z}
a.addAll(b);    // union
a.removeAll(b); // difference
```

**When order matters:** Use `LinkedHashSet` (insertion order) or `TreeSet` (sorted order).

---

## Generics

Generics let a class or method work with any type while preserving type safety. The type is specified at compile time — no casting, no `ClassCastException` at runtime.

```java
// Without generics — error-prone
List list = new ArrayList();
list.add("hello");
String s = (String) list.get(0); // requires cast, could throw at runtime

// With generics — compiler enforces the type
List<String> list = new ArrayList<>();
list.add("hello");
String s = list.get(0); // no cast needed
```

### Generic Classes

```java
public class Box<T> {
    private T value;

    public Box(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}

Box<String> strBox = new Box<>("hello");
Box<Integer> intBox = new Box<>(42);

strBox.get(); // "hello" — String, no cast
intBox.get(); // 42 — Integer, no cast
```

### Generic Methods

```java
public static <T> void swap(T[] arr, int i, int j) {
    T temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

Integer[] nums = {1, 2, 3};
swap(nums, 0, 2); // {3, 2, 1}
```

### Bounded Type Parameters

```java
// T must extend Number (accepts Integer, Double, Long, etc.)
public static <T extends Number> double sum(List<T> list) {
    double total = 0;
    for (T item : list) {
        total += item.doubleValue();
    }
    return total;
}

sum(List.of(1, 2, 3));       // works — Integer extends Number
sum(List.of(1.5, 2.5));      // works — Double extends Number
sum(List.of("a", "b"));      // compile error — String doesn't extend Number
```

### Wildcards

The wildcard `?` means "some unknown type". Used when you need flexibility without making a method generic.

```java
// ? extends Number — read-only, accepts List<Integer>, List<Double>, etc.
public static double sumWild(List<? extends Number> list) {
    double total = 0;
    for (Number n : list) total += n.doubleValue();
    return total;
}

// ? super Integer — write-only, accepts List<Integer>, List<Number>, List<Object>
public static void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}
```

**Rule:** Use `? extends T` to read from a collection. Use `? super T` to write into one. (Producer Extends, Consumer Super — PECS)

---

## Collections Utility Class

```java
List<Integer> nums = new ArrayList<>(List.of(3, 1, 4, 1, 5));

Collections.sort(nums);              // [1, 1, 3, 4, 5]
Collections.reverse(nums);           // [5, 4, 3, 1, 1]
Collections.shuffle(nums);           // random order
Collections.min(nums);               // smallest element
Collections.max(nums);               // largest element
Collections.frequency(nums, 1);      // count of 1 → 2
Collections.unmodifiableList(nums);  // read-only view
```

---

## Choosing the Right Collection

| Need | Use |
|------|-----|
| Ordered list, fast index access | `ArrayList` |
| Fast insert/remove at ends | `LinkedList` (as `Deque`) |
| Unique elements, fast lookup | `HashSet` |
| Unique elements, sorted | `TreeSet` |
| Unique elements, insertion order | `LinkedHashSet` |
| Key-value pairs, fast lookup | `HashMap` |
| Key-value pairs, sorted by key | `TreeMap` |
| Key-value pairs, insertion order | `LinkedHashMap` |
| Priority-based removal | `PriorityQueue` |

---

## Common Pitfalls

**Modifying a list while iterating**
```java
// Throws ConcurrentModificationException
for (String s : list) {
    if (s.isEmpty()) list.remove(s); // bug
}

// Correct — use iterator
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().isEmpty()) it.remove(); // safe
}

// Or: list.removeIf(String::isEmpty);
```

**`null` keys/values**
- `HashMap` allows one `null` key and multiple `null` values
- `TreeMap` does not allow `null` keys (it needs to compare them)
- `HashSet` allows one `null` element

---

## Quick Reference

```
ArrayList<T>          new ArrayList<>()
  add(e)              append
  get(i)              by index
  remove(i/e)         by index or value
  size()              count
  contains(e)         boolean lookup

HashMap<K,V>          new HashMap<>()
  put(k, v)           set key
  get(k)              retrieve (null if missing)
  getOrDefault(k, d)  retrieve with fallback
  containsKey(k)      boolean check
  entrySet()          iterate key-value pairs

HashSet<T>            new HashSet<>()
  add(e)              insert (ignored if duplicate)
  contains(e)         O(1) lookup
  remove(e)           delete

Generics
  class Box<T>        generic class
  <T> void m(T t)     generic method
  <T extends Foo>     bounded — T must be Foo or subtype
  List<? extends T>   read from (covariant)
  List<? super T>     write to (contravariant)
```
