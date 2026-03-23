# 04 — Generics Basics

Generics let you write code that works with multiple types while still being type-safe. Instead of hardcoding a specific type like `string` or `number`, you use a **type parameter** — a placeholder that gets filled in when the function or class is called.

---

## The Mental Model

Without generics, you'd have to write a separate function for each type, or use `any` (which loses type safety):

```ts
function firstOfStrings(arr: string[]): string { return arr[0]; }
function firstOfNumbers(arr: number[]): number { return arr[0]; }
// ... one for every type

// Or with any — loses type safety
function first(arr: any[]): any { return arr[0]; }
const x = first(["a", "b"]);  // x is any, not string
```

With generics, you write it once and the type flows through:

```ts
function first<T>(arr: T[]): T {
    return arr[0];
}

const x = first(["a", "b"]);  // x is string — inferred
const y = first([1, 2, 3]);   // y is number — inferred
```

`T` is the type parameter. It's a placeholder that TypeScript fills in at the call site.

---

## Generic Functions

```ts
// Identity function — returns what it receives
function identity<T>(value: T): T {
    return value;
}

// TypeScript infers T from the argument
const s = identity("hello");  // T is string
const n = identity(42);       // T is number

// You can also specify T explicitly
const s2 = identity<string>("hello");
```

### Multiple type parameters

```ts
function pair<A, B>(first: A, second: B): [A, B] {
    return [first, second];
}

const p = pair("Alice", 30);  // [string, number]
```

### Swapping two values

```ts
function swap<T, U>(a: T, b: U): [U, T] {
    return [b, a];
}

const [x, y] = swap("hello", 42);  // x: number, y: string
```

---

## Generic Interfaces

```ts
interface Box<T> {
    value: T;
    label: string;
}

const stringBox: Box<string> = { value: "hello", label: "greeting" };
const numberBox: Box<number> = { value: 42, label: "answer" };

// Generic interface for API responses
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

type UserResponse = ApiResponse<User>;
type ListResponse = ApiResponse<User[]>;
```

---

## Generic Type Aliases

```ts
type Maybe<T> = T | null | undefined;
type List<T> = T[];
type Pair<T> = [T, T];
type Callback<T> = (value: T) => void;

// Usage
const name: Maybe<string> = null;
const nums: List<number> = [1, 2, 3];
const coords: Pair<number> = [10, 20];
```

---

## Constraints

Sometimes you need `T` to have certain properties. Use `extends` to constrain the type parameter.

```ts
// T must have a .length property
function logLength<T extends { length: number }>(value: T): void {
    console.log(value.length);
}

logLength("hello");       // fine — strings have .length
logLength([1, 2, 3]);     // fine — arrays have .length
// logLength(42);         // error — numbers don't have .length
```

### Constraining to a key of an object

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name");  // string
const age  = getProperty(user, "age");   // number
// getProperty(user, "email")            // error — "email" not in user
```

`keyof T` produces a union of the string keys of `T`. `K extends keyof T` means `K` must be one of those keys.

---

## Default Type Parameters

You can give a type parameter a default, like a function parameter default:

```ts
interface Wrapper<T = string> {
    value: T;
}

const w1: Wrapper = { value: "hello" };         // T defaults to string
const w2: Wrapper<number> = { value: 42 };      // T is number
```

---

## Generic Functions as Callbacks

```ts
// Map over an array — transforms each element
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
    return arr.map(fn);
}

const lengths = map(["hello", "world"], s => s.length);  // number[]
const doubled = map([1, 2, 3], n => n * 2);              // number[]
```

---

## Generic Classes

```ts
class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }
}

const stack = new Stack<number>();
stack.push(1);
stack.push(2);
const top = stack.pop();  // top is number | undefined
```

---

## Real-World Patterns

### Generic fetch wrapper

```ts
async function fetchJson<T>(url: string): Promise<T> {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json() as Promise<T>;
}

const users = await fetchJson<User[]>("/api/users");   // User[]
const post  = await fetchJson<Post>("/api/posts/1");   // Post
```

### Generic useState-like hook

```ts
function createState<T>(initial: T) {
    let value = initial;
    return {
        get: () => value,
        set: (next: T) => { value = next; },
    };
}

const count = createState(0);
count.set(5);
const n = count.get();  // number
```

---

## Common Pitfalls

**Using `any` instead of generics**
`any` loses the type relationship between input and output. Generics preserve it.

```ts
function identity(x: any): any { return x; }
const n = identity(42);  // n is any — lost the type!

function identity<T>(x: T): T { return x; }
const n = identity(42);  // n is number — preserved
```

**Over-constraining type parameters**
Only constrain when you actually need the constraint. A constraint that's too specific defeats the reusability of generics.

**Confusing `extends` for constraint vs inheritance**
In generics, `T extends SomeType` means "T must be assignable to SomeType." It's a constraint, not inheritance.

---

## Quick Reference

```
Generic function
  function fn<T>(arg: T): T { return arg; }

Multiple type params
  function fn<T, U>(a: T, b: U): [T, U] { ... }

Generic interface
  interface Box<T> { value: T }

Generic type alias
  type Maybe<T> = T | null

Generic class
  class Stack<T> { push(item: T): void { ... } }

Constraints
  function fn<T extends { length: number }>(x: T): number { return x.length; }

keyof constraint
  function get<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }

Default type param
  interface Wrapper<T = string> { value: T }

T is inferred at the call site — no need to specify explicitly unless inference fails:
  fn("hello")          → T is string (inferred)
  fn<string>("hello")  → T is string (explicit)
```
