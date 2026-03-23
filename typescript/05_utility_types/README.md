# 05 — Utility Types

TypeScript ships with a set of built-in generic types that transform existing types into new ones. Instead of writing new type definitions from scratch, you build on types you already have.

---

## The Mental Model

Utility types are like functions for types. You pass in a type, and get a modified version back.

```ts
interface User {
    id: number;
    name: string;
    email: string;
    age: number;
}

// Make all fields optional
type UserDraft = Partial<User>;
// → { id?: number; name?: string; email?: string; age?: number }

// Keep only certain fields
type UserPreview = Pick<User, "id" | "name">;
// → { id: number; name: string }
```

---

## Partial\<T>

Makes all properties of `T` optional.

```ts
interface Config {
    host: string;
    port: number;
    timeout: number;
}

// Used for update operations — only pass what you want to change
function updateConfig(current: Config, updates: Partial<Config>): Config {
    return { ...current, ...updates };
}

updateConfig(config, { port: 8080 });           // fine — only updating port
updateConfig(config, { host: "localhost" });     // fine
updateConfig(config, {});                        // fine — nothing changes
```

---

## Required\<T>

The opposite of `Partial` — makes all optional properties required.

```ts
interface Options {
    color?: string;
    size?: number;
    label?: string;
}

type FullOptions = Required<Options>;
// → { color: string; size: number; label: string }

// Useful when you've validated all fields are present
function render(opts: Required<Options>) {
    console.log(opts.color);  // no need to check for undefined
}
```

---

## Readonly\<T>

Makes all properties of `T` read-only — they can be set once but never reassigned.

```ts
interface Point {
    x: number;
    y: number;
}

const p: Readonly<Point> = { x: 1, y: 2 };
// p.x = 5;  // error — cannot assign to 'x' because it is a read-only property

// Useful for config objects and immutable data
const CONFIG: Readonly<Config> = {
    host: "api.example.com",
    port: 443,
    timeout: 5000,
};
```

Note: `Readonly` is shallow — nested objects can still be mutated.

---

## Pick\<T, K>

Creates a new type by picking only the specified keys from `T`.

```ts
interface User {
    id: number;
    name: string;
    email: string;
    password: string;
    createdAt: Date;
}

// What to show in a user list — don't include password
type UserSummary = Pick<User, "id" | "name">;

// What to send as a session token payload
type UserPayload = Pick<User, "id" | "email">;

const summary: UserSummary = { id: 1, name: "Alice" };
```

---

## Omit\<T, K>

The opposite of `Pick` — creates a new type by removing the specified keys.

```ts
// Remove password from User (safer than manually re-listing all other fields)
type PublicUser = Omit<User, "password">;

// Remove id when creating a new record (database generates it)
type NewUser = Omit<User, "id" | "createdAt">;
```

`Omit` is usually more convenient than `Pick` when you want most of the original type and just want to exclude a few fields.

---

## Record\<K, V>

Creates an object type where keys are `K` and values are `V`.

```ts
// Map of user IDs to users
type UserMap = Record<number, User>;
const users: UserMap = {
    1: { id: 1, name: "Alice", ... },
    2: { id: 2, name: "Bob", ... },
};

// Status to message mapping
type StatusMessage = Record<"success" | "error" | "loading", string>;
const messages: StatusMessage = {
    success: "Done!",
    error: "Something went wrong.",
    loading: "Please wait...",
};

// Generic cache
type Cache<T> = Record<string, T>;
```

`Record<string, T>` is a cleaner way to write `{ [key: string]: T }`.

---

## ReturnType\<T>

Extracts the return type of a function.

```ts
function getUser() {
    return { id: 1, name: "Alice", email: "alice@example.com" };
}

type UserFromFn = ReturnType<typeof getUser>;
// → { id: number; name: string; email: string }
```

Useful when a function's return type is complex and you don't want to define it separately. Also useful when the function is from a library and you don't control the type definition.

```ts
// Works with async functions too
async function fetchUser(): Promise<User> { ... }
type FetchResult = ReturnType<typeof fetchUser>;  // Promise<User>
type Awaited = Awaited<ReturnType<typeof fetchUser>>;  // User
```

---

## Parameters\<T>

Extracts the parameter types of a function as a tuple.

```ts
function createUser(name: string, age: number, email: string) { ... }

type CreateUserArgs = Parameters<typeof createUser>;
// → [name: string, age: number, email: string]

// Useful for wrapping or decorating functions
function withLogging<T extends (...args: any[]) => any>(fn: T) {
    return (...args: Parameters<T>): ReturnType<T> => {
        console.log("calling", fn.name);
        return fn(...args);
    };
}
```

---

## NonNullable\<T>

Removes `null` and `undefined` from a type.

```ts
type MaybeString = string | null | undefined;
type JustString = NonNullable<MaybeString>;  // string

// Useful after you've validated a value is present
function requireValue<T>(value: T): NonNullable<T> {
    if (value == null) throw new Error("Value is required");
    return value as NonNullable<T>;
}
```

---

## Awaited\<T>

Unwraps a `Promise<T>` to get `T`. Handles nested promises too.

```ts
type A = Awaited<Promise<string>>;           // string
type B = Awaited<Promise<Promise<number>>>;  // number

async function fetchUser(): Promise<User> { ... }
type User = Awaited<ReturnType<typeof fetchUser>>;  // User
```

---

## Combining Utility Types

Utility types compose naturally:

```ts
interface User {
    id: number;
    name: string;
    email: string;
    password: string;
    age?: number;
}

// A public user update request: no id/password, all optional
type UserUpdateRequest = Partial<Omit<User, "id" | "password">>;
// → { name?: string; email?: string; age?: number }

// Read-only summary
type ImmutableSummary = Readonly<Pick<User, "id" | "name">>;
// → { readonly id: number; readonly name: string }
```

---

## Common Pitfalls

**Readonly is shallow**
```ts
const state: Readonly<{ user: { name: string } }> = { user: { name: "Alice" } };
// state.user = { name: "Bob" };  // error — can't reassign user
state.user.name = "Bob";          // fine — Readonly doesn't go deep
```

For deep immutability, you need a recursive `DeepReadonly` type (not built-in).

**Pick vs Omit for large types**
If you have a 20-field type and want 19 of them, use `Omit` to exclude the one you don't want. If you want 2, use `Pick`.

**ReturnType needs `typeof`**
```ts
type X = ReturnType<getUser>;         // error — needs a type, not a value
type X = ReturnType<typeof getUser>;  // correct
```

---

## Quick Reference

```
Utility Types Cheat Sheet

Partial<T>           — all properties optional
Required<T>          — all properties required
Readonly<T>          — all properties read-only (shallow)

Pick<T, "a" | "b">  — keep only listed keys
Omit<T, "a" | "b">  — remove listed keys

Record<K, V>         — object with keys K and values V
  Record<string, number>       → { [key: string]: number }
  Record<"x" | "y", number>   → { x: number; y: number }

ReturnType<typeof fn>         — return type of a function
Parameters<typeof fn>         — parameter types as tuple
NonNullable<T>                 — removes null | undefined
Awaited<Promise<T>>           — unwraps Promise<T> to T

Combining
  Partial<Omit<T, "id">>     — omit id, make rest optional
  Readonly<Pick<T, "id">>    — pick id, make it read-only
```
