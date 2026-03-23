# 06 — tsconfig Setup

`tsconfig.json` is the configuration file for the TypeScript compiler. It controls which files are compiled, how strict the type checking is, and what JavaScript gets generated as output. Understanding the key options makes TypeScript dramatically more useful.

---

## Creating a tsconfig

```bash
tsc --init         # generates a tsconfig.json with defaults and comments
```

Or create it manually — the minimal useful config:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "strict": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

---

## The Most Important Option: `strict`

`"strict": true` is a shorthand that enables several checks at once. Without it, TypeScript is much less useful.

What `strict` enables:
- **`strictNullChecks`** — `null` and `undefined` are not assignable to other types. You must handle them.
- **`noImplicitAny`** — variables can't silently be `any` — you must annotate them.
- **`strictFunctionTypes`** — function parameters are checked contravariantly (more precise).
- **`strictPropertyInitialization`** — class properties must be initialized.
- **`noImplicitThis`** — `this` must have a known type.

**Always use `"strict": true`** in new projects. Turning it off is trading type safety for convenience.

---

## `target` — Output JavaScript Version

```json
"target": "ES2022"
```

Controls what JavaScript version `tsc` outputs. Newer targets produce smaller, more readable output. Set to the minimum version your runtime supports.

| Target | Supports |
|--------|----------|
| `ES5` | Old browsers, widest compatibility |
| `ES2015` (ES6) | Arrow functions, classes, const/let |
| `ES2017` | async/await |
| `ES2020` | Optional chaining `?.`, nullish coalescing `??` |
| `ES2022` | Top-level await, `at()` method |
| `ESNext` | Latest features — use only if your runtime is current |

For Node.js 18+, `ES2022` is a good choice. For modern browsers (no IE), `ES2020` or later.

---

## `module` — Module System

```json
"module": "NodeNext"       // Node.js with ESM (modern)
"module": "CommonJS"       // Node.js with require() (older)
"module": "ESNext"         // bundlers (Vite, webpack, esbuild)
"module": "bundler"        // TypeScript 5+ — for bundler-managed projects
```

- **`NodeNext`** — use when running TypeScript directly in Node.js with `"type": "module"` in package.json. Requires `.js` extensions on imports.
- **`CommonJS`** — use for older Node.js projects or if you're not using ESM.
- **`bundler`** — use when a bundler (Vite, webpack) handles module resolution. Most frontend projects use this.

`moduleResolution` is often set alongside `module`:
```json
"module": "NodeNext",
"moduleResolution": "NodeNext"

"module": "ESNext",
"moduleResolution": "bundler"
```

---

## `outDir` and `rootDir`

```json
"rootDir": "./src",    // where TypeScript source files are
"outDir": "./dist"     // where compiled JavaScript goes
```

This keeps your source and output separate. `src/` contains `.ts` files; `dist/` contains compiled `.js` files.

---

## `lib` — Built-in Type Definitions

```json
"lib": ["ES2022", "DOM"]
```

Controls which built-in APIs TypeScript knows about:
- `ES2022` — standard JavaScript APIs (Promise, Map, Set, etc.)
- `DOM` — browser APIs (document, window, fetch, etc.)
- `DOM.Iterable` — `for...of` on DOM collections

If you're writing for Node.js only, omit `DOM` to prevent accidentally using browser APIs.

---

## `paths` — Path Aliases

Lets you use short import paths instead of long relative ones:

```json
"compilerOptions": {
  "baseUrl": ".",
  "paths": {
    "@/*": ["./src/*"],
    "@components/*": ["./src/components/*"],
    "@utils/*": ["./src/utils/*"]
  }
}
```

```ts
// Before: long relative path
import { Button } from "../../components/Button";

// After: short alias
import { Button } from "@components/Button";
```

Note: `paths` tells TypeScript where to find the files, but your bundler/runtime also needs to be configured separately (Vite, webpack, or Node.js `--experimental-specifier-resolution`).

---

## Other Useful Options

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "bundler",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src",

    "noUnusedLocals": true,       // error on unused variables
    "noUnusedParameters": true,   // error on unused function params
    "noFallthroughCasesInSwitch": true,  // error on switch fallthrough
    "exactOptionalPropertyTypes": true,  // { x?: string } doesn't allow x: undefined

    "skipLibCheck": true,         // skip type checking .d.ts files (faster)
    "declaration": true,          // generate .d.ts files (for library authors)
    "sourceMap": true,            // generate .map files for debugging
    "esModuleInterop": true,      // allow default imports from CJS modules

    "jsx": "react-jsx",           // for React projects (lesson 07)
    "jsxImportSource": "react"    // for React 17+ automatic JSX transform
  }
}
```

---

## tsconfig for Different Project Types

### Node.js (backend / scripts)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

### React + Vite (frontend)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "react-jsx",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "noEmit": true,          // Vite handles the output — tsc is type-check only
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

`"noEmit": true` means `tsc` only type-checks — it doesn't produce output files. The bundler handles compilation.

### Library (publishing to npm)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "declaration": true,       // emit .d.ts files
    "declarationMap": true,    // map .d.ts back to source
    "sourceMap": true,
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["**/*.test.ts"]
}
```

---

## `include`, `exclude`, and `files`

```json
"include": ["src/**/*"],          // glob patterns — what to compile
"exclude": ["node_modules", "dist"],  // what to skip (node_modules excluded by default)
"files": ["src/main.ts"]          // explicit list — rarely used
```

If `include` is omitted, TypeScript compiles everything in the project directory (except `exclude`).

---

## Common Pitfalls

**Not enabling `strict`**
TypeScript without `strict` allows implicit `any` and doesn't enforce null checks. This makes it barely better than plain JavaScript. Always use `strict: true`.

**Wrong `module` for the runtime**
Using `"module": "ESNext"` for a Node.js project that uses `require()` will break at runtime. Match the module system to what actually runs the code.

**Forgetting to configure the bundler for `paths` aliases**
TypeScript's `paths` option only helps the compiler. If you use Vite or webpack, you must configure the same aliases there too.

**Using `skipLibCheck: false` in a slow project**
`skipLibCheck: true` dramatically speeds up type checking by skipping `.d.ts` library files. It's safe for most projects — keep it on.

---

## Quick Reference

```
Key options in tsconfig.json

Target / Output
  "target": "ES2022"        -- output JS version
  "outDir": "./dist"        -- compiled output folder
  "rootDir": "./src"        -- source root
  "noEmit": true            -- type-check only, no output (bundler projects)
  "sourceMap": true         -- generate .map files

Type Checking
  "strict": true            -- ALWAYS enable (enables all strict checks)
  "noUnusedLocals": true    -- error on unused vars
  "noUnusedParameters": true -- error on unused params
  "exactOptionalPropertyTypes": true -- optional ≠ undefined-assignable

Module System
  "module": "NodeNext"      -- Node.js + ESM
  "module": "CommonJS"      -- Node.js + require()
  "module": "bundler"       -- Vite/webpack (TypeScript 5+)
  "moduleResolution": "NodeNext" | "bundler"

React / JSX
  "jsx": "react-jsx"        -- React 17+ automatic transform
  "lib": ["ES2020", "DOM"]  -- enable browser APIs

Library Publishing
  "declaration": true       -- emit .d.ts files
  "declarationMap": true    -- source maps for .d.ts

File Selection
  "include": ["src/**/*"]
  "exclude": ["node_modules"]

Aliases
  "baseUrl": ".",
  "paths": { "@/*": ["./src/*"] }
```
