# 03 — Type Narrowing & Guards

Narrowing is when TypeScript figures out a more specific type within a branch of code. After a `typeof` check or `if` statement, TypeScript knows more about what a value is and allows type-specific operations.

---

## The Mental Model

When you have a union type, TypeScript won't let you use methods that only exist on one member — because it doesn't know which one it is yet. Narrowing is how you tell it.

```ts
function process(value: string | number) {
    // value.toUpperCase()  // error — toUpperCase doesn't exist on number
    // value.toFixed(2)     // error — toFixed doesn't exist on string

    if (typeof value === "string") {
        value.toUpperCase();  // fine — TypeScript knows it's string here
    } else {
        value.toFixed(2);     // fine — TypeScript knows it's number here
    }
}
```

---

## typeof Narrowing

Works for JavaScript primitive types: `"string"`, `"number"`, `"boolean"`, `"bigint"`, `"symbol"`, `"undefined"`, `"function"`, `"object"`.

```ts
function format(value: string | number | boolean): string {
    if (typeof value === "string") return value.toUpperCase();
    if (typeof value === "number") return value.toFixed(2);
    return String(value);
}
```

**Limitation:** `typeof null === "object"` — a JavaScript quirk. Check for `null` explicitly.

```ts
function getName(value: string | null): string {
    if (value === null) return "unknown";
    return value.toUpperCase();  // value is string here
}
```

---

## Truthiness Narrowing

Checking for `null`, `undefined`, `""`, `0`, or `false` narrows the type:

```ts
function greet(name: string | null | undefined): string {
    if (name) {
        return `Hello, ${name}`;  // name is string here
    }
    return "Hello, stranger";
}
```

**Caution:** Truthiness doesn't distinguish `null` from `undefined` from `""` or `0`. Be specific if the distinction matters.

---

## Equality Narrowing

Comparing with `===` narrows both sides:

```ts
function compare(a: string | number, b: string | boolean) {
    if (a === b) {
        // Both must be string (only type in common) — TypeScript knows
        a.toUpperCase();
        b.toUpperCase();
    }
}

function check(x: string | null) {
    if (x === null) {
        // x is null here
    } else {
        x.toUpperCase();  // x is string here
    }
}
```

---

## instanceof Narrowing

Works for class instances.

```ts
class Dog {
    bark() { console.log("Woof"); }
}

class Cat {
    meow() { console.log("Meow"); }
}

function makeNoise(animal: Dog | Cat) {
    if (animal instanceof Dog) {
        animal.bark();   // animal is Dog here
    } else {
        animal.meow();   // animal is Cat here
    }
}
```

---

## in Narrowing

Checks whether a property exists on an object. Useful for discriminating between object types that don't have a shared literal field.

```ts
type Admin = { role: "admin"; permissions: string[] };
type Guest = { role: "guest"; sessionId: string };
type User = Admin | Guest;

function getAccess(user: User) {
    if ("permissions" in user) {
        console.log(user.permissions);  // user is Admin
    } else {
        console.log(user.sessionId);    // user is Guest
    }
}
```

---

## Discriminated Union Narrowing (Recommended)

The cleanest pattern. Add a `kind` or `type` field with a literal value to each member of the union (see lesson 02). TypeScript uses it automatically.

```ts
type ApiResult =
    | { status: "success"; data: string[] }
    | { status: "error"; message: string }
    | { status: "loading" };

function handleResult(result: ApiResult) {
    switch (result.status) {
        case "success":
            console.log(result.data);    // data is string[]
            break;
        case "error":
            console.log(result.message); // message is string
            break;
        case "loading":
            console.log("Loading...");
            break;
    }
}
```

---

## Custom Type Predicates

When built-in narrowing isn't enough, write a function that returns `arg is SomeType`. TypeScript trusts this assertion and narrows accordingly.

```ts
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function process(value: unknown) {
    if (isString(value)) {
        value.toUpperCase();  // TypeScript knows it's string
    }
}
```

A more realistic example — validating that an object has a specific shape:

```ts
interface User {
    id: number;
    name: string;
}

function isUser(obj: unknown): obj is User {
    return (
        typeof obj === "object" &&
        obj !== null &&
        "id" in obj &&
        "name" in obj &&
        typeof (obj as User).id === "number" &&
        typeof (obj as User).name === "string"
    );
}

const data: unknown = JSON.parse(response);
if (isUser(data)) {
    console.log(data.name);  // TypeScript knows it's User
}
```

---

## Assertion Functions

An assertion function throws if a condition is not met. TypeScript narrows past the call site.

```ts
function assert(condition: boolean, msg: string): asserts condition {
    if (!condition) throw new Error(msg);
}

function assertIsString(val: unknown): asserts val is string {
    if (typeof val !== "string") throw new Error(`Expected string, got ${typeof val}`);
}

let x: unknown = getInput();
assertIsString(x);
x.toUpperCase();  // TypeScript knows it's string after the assertion
```

---

## The `never` Type and Exhaustiveness

After narrowing all cases in a union, the remaining type is `never`. You can use this to make the compiler error if you add a new union member without updating your switch statement:

```ts
type Shape = { kind: "circle"; r: number } | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle": return Math.PI * s.r ** 2;
        case "rect":   return s.w * s.h;
        default:
            const _: never = s;  // if a case is missing, s won't be never → error
            return 0;
    }
}
```

---

## Common Pitfalls

**Relying on truthiness when 0 or "" are valid values**
```ts
function setCount(n: number | undefined) {
    if (n) { /* n is 0? — falls through! */ }
    if (n !== undefined) { /* correct */ }
}
```

**`typeof null === "object"`**
Always check for `null` explicitly when narrowing objects:
```ts
if (typeof x === "object" && x !== null) { ... }
```

**Type predicates can lie**
If your `is` function has a bug, TypeScript will believe it and you'll get a runtime error that TypeScript thought was impossible. Keep predicates simple and accurate.

---

## Quick Reference

```
typeof
  if (typeof x === "string") { ... }
  if (typeof x === "number") { ... }
  typeof null === "object"  ← quirk — check null explicitly

Truthiness
  if (x) { ... }   — narrows out null/undefined/0/""/false

Equality
  if (x === null) { ... }     — narrow to null
  if (x !== undefined) { ... } — narrow out undefined

instanceof
  if (x instanceof SomeClass) { ... }

in (property check)
  if ("propName" in obj) { ... }

Discriminated union
  switch (x.kind) { case "foo": ... }  — best pattern

Type predicate (custom guard)
  function isFoo(val: unknown): val is Foo {
      return typeof val === "object" && val !== null && "foo" in val;
  }

Assertion function
  function assertIsString(val: unknown): asserts val is string {
      if (typeof val !== "string") throw new Error("...");
  }

Exhaustiveness
  default: const _: never = x;  — error if union case is unhandled
```
