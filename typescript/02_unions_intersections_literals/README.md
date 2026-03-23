# 02 — Unions, Intersections & Literals

Union and intersection types let you compose types from existing ones. Literal types let you constrain a value to a specific set of values rather than just a broad type like `string`.

---

## Union Types ( | )

A union says: this value can be **one of these types**.

```ts
let id: string | number;
id = "abc-123";  // fine
id = 42;         // fine
// id = true;    // error — not string or number

function printId(id: string | number): void {
    console.log(id);
}
```

### Working with unions

When a value has a union type, you can only use operations that exist on **all** members:

```ts
function double(x: string | number) {
    // x.toFixed(2)     // error — toFixed doesn't exist on string
    // x.toUpperCase()  // error — toUpperCase doesn't exist on number

    console.log(x);   // fine — console.log accepts anything
}
```

To use type-specific operations, you narrow the type first (see lesson 03).

---

## Intersection Types ( & )

An intersection says: this value must have **all the properties of all these types**.

```ts
interface HasName {
    name: string;
}

interface HasAge {
    age: number;
}

type Person = HasName & HasAge;

const alice: Person = { name: "Alice", age: 30 };  // must have both
```

Intersections are mostly used to combine object shapes. Think of them as "merge these two types into one."

### Merging interfaces vs intersections

```ts
// Using & (type alias intersection)
type AdminUser = User & { role: "admin" };

// Using extends (interface inheritance) — same result for objects
interface AdminUser extends User {
    role: "admin";
}
```

Both work for objects. Use `&` when working with `type` aliases; use `extends` when working with interfaces.

---

## Literal Types

Instead of `string`, you can type a variable as a specific string value. That value is the only one allowed.

```ts
type Direction = "north" | "south" | "east" | "west";

let dir: Direction = "north";  // fine
// dir = "up";  // error — not in the union

type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
let roll: DiceRoll = 3;  // fine
// roll = 7;  // error

type Result = "success" | "failure" | "pending";
```

### Why literal types beat plain `string`

```ts
// Without literal types
function setStatus(status: string) { ... }
setStatus("activ");    // typo — no error at compile time

// With literal types
type Status = "active" | "inactive";
function setStatus(status: Status) { ... }
// setStatus("activ");  // error — caught at compile time
```

---

## Discriminated Unions

The most important pattern in TypeScript. Each member of the union has a **common literal property** (the discriminant) that TypeScript can use to tell them apart.

```ts
type Circle = {
    kind: "circle";
    radius: number;
};

type Rectangle = {
    kind: "rectangle";
    width: number;
    height: number;
};

type Triangle = {
    kind: "triangle";
    base: number;
    height: number;
};

type Shape = Circle | Rectangle | Triangle;

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;  // shape is Circle here
        case "rectangle":
            return shape.width * shape.height;   // shape is Rectangle here
        case "triangle":
            return 0.5 * shape.base * shape.height; // shape is Triangle here
    }
}
```

The `kind` field is the discriminant. Inside each `case`, TypeScript knows the exact type.

### Exhaustiveness checking

Add a `default` branch that assigns to `never` to get a compile error if you forget to handle a new shape:

```ts
function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle": return Math.PI * shape.radius ** 2;
        case "rectangle": return shape.width * shape.height;
        case "triangle": return 0.5 * shape.base * shape.height;
        default: {
            const _exhaustive: never = shape;  // error if a case is missing
            return _exhaustive;
        }
    }
}
```

If you add `Square` to `Shape` without adding a case, the `default` branch fails to compile.

---

## Optional Chaining and Null Unions

A very common union is `T | null` or `T | undefined`:

```ts
type MaybeUser = User | null;

function greet(user: User | null): string {
    if (user === null) return "Hello, stranger";
    return `Hello, ${user.name}`;  // TypeScript knows user is User here
}

// Optional chaining works with null unions
const name = user?.name ?? "unknown";
```

---

## Template Literal Types

String literal types that use template syntax:

```ts
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// → "onClick" | "onFocus" | "onBlur"

type CssProperty = "margin" | "padding";
type Side = "Top" | "Right" | "Bottom" | "Left";
type SpacingProp = `${CssProperty}${Side}`;
// → "marginTop" | "marginRight" | ... | "paddingBottom" | "paddingLeft"
```

Useful for building event-handler maps, CSS-in-TS, and strongly-typed string patterns.

---

## Common Pitfalls

**Forgetting to narrow a union before using type-specific methods**
You can't call `.toFixed()` on `string | number` until you narrow to `number`. See lesson 03 for narrowing patterns.

**Intersection of incompatible types produces `never`**
```ts
type A = { x: string };
type B = { x: number };
type C = A & B;  // x must be string AND number — impossible → x: never
```

If an intersection produces `never` for a property, the whole object type becomes `never` (can't be created).

**Wide literal widening**
```ts
let dir = "north";        // inferred as string — widened
const dir2 = "north";     // inferred as "north" — literal (const can't change)

function go(d: Direction) { ... }
go(dir);   // error — string is not assignable to Direction
go(dir2);  // fine — "north" is assignable to Direction
```

Use `const` or `as const` when you need the literal type preserved.

---

## Quick Reference

```
Union
  type A = string | number
  type B = "a" | "b" | "c"   -- literal union

Intersection
  type C = TypeA & TypeB      -- must have all properties of both

Literal types
  type Dir = "north" | "south" | "east" | "west"
  type Digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

Discriminated union pattern
  type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number }
  → switch on shape.kind to narrow to exact type

Exhaustiveness check
  default: const _: never = val  -- compile error if case is missing

Template literal types
  type Handler = `on${Capitalize<string>}`  -- "onClick" etc.

Widening pitfall
  let x = "north"   → string (widened)
  const x = "north" → "north" (literal)
  const x = "north" as const → "north" (explicit)
```
