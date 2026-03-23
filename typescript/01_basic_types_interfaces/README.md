# 01 — Basic Types & Interfaces

TypeScript adds type annotations to JavaScript. You declare what type a variable holds, and the compiler checks that you never put the wrong thing in it. Most of the time types are **inferred** — you don't need to write them explicitly.

---

## Primitive Types

```ts
let name: string = "Alice";
let age: number = 30;
let active: boolean = true;
let nothing: null = null;
let missing: undefined = undefined;
let id: symbol = Symbol("id");
let big: bigint = 9007199254740993n;
```

### Type inference

You don't need to annotate when the value is obvious. TypeScript infers the type from the right side.

```ts
let name = "Alice";    // inferred as string — no annotation needed
let count = 0;         // inferred as number
```

Annotation is most useful for function parameters (TypeScript can't infer those) and when you want to be explicit.

---

## Arrays and Tuples

```ts
// Array — all elements the same type
let scores: number[] = [90, 85, 92];
let names: Array<string> = ["Alice", "Bob"];  // generic syntax, same thing

// Tuple — fixed-length array, each position has its own type
let pair: [string, number] = ["Alice", 30];
let rgb: [number, number, number] = [255, 128, 0];

// Optional tuple element
let optPair: [string, number?] = ["Alice"];
```

Tuples are useful for returning multiple values from a function when you don't want a full object:

```ts
function minMax(nums: number[]): [number, number] {
    return [Math.min(...nums), Math.max(...nums)];
}
const [min, max] = minMax([3, 1, 4, 1, 5]);
```

---

## any, unknown, never, void

```ts
// any — opts out of type checking (avoid)
let x: any = "hello";
x = 42;           // no error
x.foo.bar();      // no error — dangerous

// unknown — safer alternative to any; must narrow before use
let y: unknown = getValueFromSomewhere();
if (typeof y === "string") {
    console.log(y.toUpperCase());  // safe — we checked first
}

// never — a type that can never be produced
function fail(msg: string): never {
    throw new Error(msg);  // never returns
}

// void — function that returns nothing (undefined in practice)
function log(msg: string): void {
    console.log(msg);
}
```

**Rule:** Prefer `unknown` over `any`. `any` disables type checking entirely. `unknown` keeps it safe.

---

## Object Types Inline

```ts
// Object literal type annotation
function greet(user: { name: string; age: number }): string {
    return `Hello, ${user.name}`;
}

// Optional property
function greet2(user: { name: string; age?: number }): string {
    return `Hello, ${user.name}, age ${user.age ?? "unknown"}`;
}

// Readonly property
function process(point: { readonly x: number; readonly y: number }) {
    // point.x = 5;  // error — can't modify
}
```

---

## Interfaces

An interface is a named type for the shape of an object.

```ts
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;           // optional
    readonly createdAt: Date; // can't be changed after creation
}

const alice: User = {
    id: 1,
    name: "Alice",
    email: "alice@example.com",
    createdAt: new Date(),
};
```

### Extending interfaces

```ts
interface Animal {
    name: string;
}

interface Dog extends Animal {
    breed: string;
}

const dog: Dog = { name: "Rex", breed: "Lab" };
```

### Function signatures in interfaces

```ts
interface Formatter {
    format(value: string): string;
    (value: string): string;  // callable signature (less common)
}

interface Logger {
    log: (message: string) => void;  // property that is a function
}
```

---

## type Aliases

`type` creates an alias for any type expression — primitives, unions, tuples, objects, anything.

```ts
type UserID = number;
type Name = string;

type Point = {
    x: number;
    y: number;
};

// type can alias complex expressions
type Nullable<T> = T | null;
type Pair<T> = [T, T];
```

### interface vs type

Both can describe object shapes. The practical differences:

| | `interface` | `type` |
|--|-------------|--------|
| Extend | `extends` keyword | `&` intersection |
| Merge declarations | Yes — can redeclare to add fields | No |
| Non-object types | No | Yes (unions, primitives, tuples) |
| Error messages | Usually cleaner | Sometimes verbose |

**Rule of thumb:** Use `interface` for object shapes that might be extended (API contracts, component props). Use `type` for unions, tuples, aliases, or complex compositions.

---

## Enums

```ts
// Numeric enum (values 0, 1, 2, ...)
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

const move = Direction.Up;  // 0

// String enum (recommended — values are readable in runtime output)
enum Status {
    Active = "ACTIVE",
    Inactive = "INACTIVE",
    Pending = "PENDING",
}

const status = Status.Active;  // "ACTIVE"
```

**Modern alternative:** Many TypeScript developers prefer a union of string literals over enums. They're simpler and have no runtime overhead:

```ts
type Status = "ACTIVE" | "INACTIVE" | "PENDING";
```

---

## Type Assertions

Tells the compiler "trust me, I know the type." Use sparingly — it overrides type safety.

```ts
// as syntax (preferred)
const input = document.getElementById("username") as HTMLInputElement;
input.value = "Alice";

// angle-bracket syntax (not usable in JSX files)
const input2 = <HTMLInputElement>document.getElementById("username");
```

---

## Common Pitfalls

**Annotating everything manually**
TypeScript infers most types. Over-annotating makes code verbose without benefit. Annotate function parameters and return types; let inference handle the rest.

**Using `any` when you mean `unknown`**
`any` turns off type checking. `unknown` keeps it safe by requiring you to narrow the type before using it.

**Confusing `null` and `undefined`**
With `strictNullChecks` enabled (it is in strict mode), `null` and `undefined` are not assignable to other types. You must handle them explicitly — which is the correct behavior.

**`interface` vs `type` bikeshedding**
They're nearly identical for object shapes. Pick one and stay consistent. The project's conventions matter more than personal preference.

---

## Quick Reference

```
Primitives
  string, number, boolean, null, undefined, symbol, bigint

Arrays / Tuples
  number[]           -- array of numbers
  Array<string>      -- same, generic syntax
  [string, number]   -- tuple (fixed types per position)

Special types
  any     -- opt out of type checking (avoid)
  unknown -- safe any — must narrow before use
  never   -- can never be produced (throws, exhausted unions)
  void    -- function returns nothing

Interface
  interface Foo { prop: string; optional?: number; readonly id: number }
  interface Bar extends Foo { extra: boolean }

type alias
  type ID = number
  type Point = { x: number; y: number }
  type MaybeString = string | null

interface vs type
  interface — object shapes, extendable, declaration merging
  type      — anything (unions, tuples, aliases), no declaration merging

Type assertion
  value as SomeType       -- override inferred type
  <SomeType>value         -- same (not in JSX)

Enum
  enum Color { Red = "RED", Green = "GREEN" }
  → prefer union literals: type Color = "RED" | "GREEN"
```
