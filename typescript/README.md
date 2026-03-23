# TypeScript Reference Course

TypeScript is a superset of JavaScript that adds static types. It compiles to plain JavaScript and runs everywhere JS runs. The type system catches bugs at compile time instead of runtime.

---

## Requirements

- **Node.js 18+** — install from [nodejs.org](https://nodejs.org)
- **TypeScript** — `npm install -g typescript` (gives you `tsc`)
- **Editor** — VS Code has first-class TypeScript support built in

### Run any lesson file

```bash
npx ts-node file.ts         # run directly (install: npm i -g ts-node)
tsc file.ts && node file.js # compile then run
```

---

## Lessons

| # | Topic | What You'll Learn |
|---|-------|------------------|
| 01 | [Basic Types & Interfaces](01_basic_types_interfaces/) | Primitives, arrays, tuples, objects, interface vs type |
| 02 | [Unions, Intersections & Literals](02_unions_intersections_literals/) | `\|`, `&`, string/number literal types, discriminated unions |
| 03 | [Type Narrowing & Guards](03_type_narrowing_guards/) | typeof, instanceof, in, custom type predicates |
| 04 | [Generics Basics](04_generics_basics/) | Generic functions, interfaces, constraints, default types |
| 05 | [Utility Types](05_utility_types/) | Partial, Required, Pick, Omit, Record, Readonly, ReturnType |
| 06 | [tsconfig Setup](06_tsconfig_setup/) | Compiler options, strict mode, module settings, project config |
| 07 | [Typing React Components](07_typing_react_components/) | Props, events, hooks, children, forwardRef, generics in JSX |

---

## Recommended Reading Order

Read the lessons in order. Each builds on the previous:
- Lessons 01–03 cover the core type language — start here
- Lessons 04–05 cover reusable/composable types
- Lesson 06 covers configuration — useful to understand before using TypeScript in a real project
- Lesson 07 applies everything to React (requires knowing JSX basics)

---

## Dialect Notes

These lessons use TypeScript in strict mode with modern settings (`ES2022` target, `"module": "NodeNext"` or `"bundler"`). Some older tutorials use loose settings — the differences are mostly in null-safety and module resolution.

---

## Key Mental Model

TypeScript's type system is **structural** (also called duck typing). Two types are compatible if their shapes match — the names don't matter.

```ts
interface Point { x: number; y: number; }
interface Location { x: number; y: number; }

const p: Point = { x: 1, y: 2 };
const l: Location = p;  // fine — same shape
```

This is different from languages like Java or C# where types must explicitly declare they implement an interface.
