# 08 — Modules: Import and Export

Modules let you split code into separate files, each with its own scope. Nothing is global unless explicitly exported. This prevents naming collisions and makes code easier to maintain.

---

## Mental Model

Before modules: every `<script>` shared the global scope — variables from one file could collide with another.

With modules: each file is its own isolated scope. You explicitly choose what to expose (`export`) and what to bring in (`import`).

---

## Named Exports

A file can export multiple named values:

```js
// math.js
export const PI = 3.14159;

export function add(a, b) {
  return a + b;
}

export function multiply(a, b) {
  return a * b;
}

// Or export at the bottom (easier to see what's exported)
const PI = 3.14159;
function add(a, b) { return a + b; }
function multiply(a, b) { return a * b; }

export { PI, add, multiply };
```

```js
// main.js
import { PI, add, multiply } from './math.js';

console.log(add(2, 3));  // 5
```

### Renaming imports

```js
import { add as sum, multiply as times } from './math.js';

sum(1, 2);  // 3
```

### Import everything as a namespace

```js
import * as Math from './math.js';

Math.add(1, 2);
Math.PI;
```

---

## Default Export

One default export per file. Can be a function, class, or value.

```js
// user.js
export default class User {
  constructor(name) { this.name = name; }
}

// Or a function
export default function greet(name) {
  return `Hello, ${name}`;
}
```

```js
// main.js — import with any name you choose (no braces)
import User from './user.js';
import greet from './user.js';
```

### Named + Default together

```js
// api.js
export default async function fetchUser(id) { ... }  // default
export const API_URL = 'https://api.example.com';    // named
```

```js
import fetchUser, { API_URL } from './api.js';
```

---

## Re-exports

Forward exports from one module through another — used for organizing public APIs.

```js
// utils/index.js — barrel file
export { formatDate } from './date.js';
export { truncate, capitalize } from './string.js';
export { debounce } from './function.js';
```

```js
// Now consumers can import from one place
import { formatDate, truncate } from './utils/index.js';
// instead of from three different files
```

### Re-export a default as named

```js
export { default as User } from './user.js';
```

---

## Barrel Files (`index.js`)

A common pattern: an `index.js` that re-exports everything from a folder, making imports cleaner.

```
components/
├── Button.js
├── Card.js
├── Modal.js
└── index.js  ← barrel
```

```js
// components/index.js
export { default as Button } from './Button.js';
export { default as Card } from './Card.js';
export { default as Modal } from './Modal.js';
```

```js
// Instead of:
import Button from './components/Button.js';
import Card from './components/Card.js';

// You can write:
import { Button, Card } from './components/index.js';
// or even just './components/' — resolves to index.js
```

---

## Dynamic `import()`

Import a module lazily at runtime — returns a Promise. Useful for code splitting: load a module only when needed.

```js
// Instead of at the top:
import { heavyLibrary } from './heavy.js';

// On demand:
async function handleClick() {
  const { heavyLibrary } = await import('./heavy.js');
  heavyLibrary.doSomething();
}

// Conditionally load based on environment
const config = await import(`./config.${env}.js`);
```

Bundlers (Vite, webpack) use dynamic imports as split points — they create separate chunks.

---

## ES Modules vs CommonJS

Two module systems exist in JavaScript:

| | ES Modules (ESM) | CommonJS (CJS) |
|---|---|---|
| Syntax | `import` / `export` | `require()` / `module.exports` |
| Where used | Browsers, modern Node.js | Node.js (older style) |
| Loading | Static (analyzed at compile time) | Dynamic (runs at runtime) |
| Default | Live bindings (value stays in sync) | Copied value at require time |

```js
// CommonJS (Node.js older style)
const fs = require('fs');
module.exports = { add, multiply };
module.exports.default = mainFunction;

// ES Modules (modern, works in browser and Node.js)
import fs from 'fs';
export { add, multiply };
export default mainFunction;
```

In modern projects, use ESM. Node.js supports ESM in `.mjs` files or when `"type": "module"` is in `package.json`.

---

## Using Modules in the Browser

```html
<!-- type="module" enables ES module behavior -->
<script type="module" src="main.js"></script>

<!-- Deferred by default — runs after DOM is parsed -->
<!-- Strict mode by default -->
<!-- Module scope — no global leakage -->
<!-- CORS required for cross-origin modules -->
```

```js
// main.js (top-level await works in modules)
const data = await fetch('/api/config').then(r => r.json());
```

---

## Module Scope Rules

- Each module file has its own scope
- `import`/`export` are static — they can't be inside `if` blocks or functions (use dynamic `import()` for that)
- Modules are strict mode by default (`'use strict'` not needed)
- A module is only executed once, even if imported by multiple files — the same instance is shared

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Mixing named and default import syntax | Named uses `{}`, default doesn't: `import Foo, { bar }` |
| Circular imports | A imports B, B imports A — can cause undefined values; restructure to break the cycle |
| `import` inside a function or conditional | Use dynamic `import()` instead |
| `require()` in an ES module file | Use `import` instead, or rename to `.cjs` |
| Barrel file importing everything | Bundlers may not tree-shake properly — import specific files if bundle size matters |
| `<script src="...">` without `type="module"` | Browser modules require `type="module"` |

---

## Quick Reference Card

```js
// Named export
export const name = 'value';
export function fn() {}
export { a, b, c };

// Default export
export default function main() {}
export default class MyClass {}

// Named import
import { fn, name } from './module.js';
import { fn as alias } from './module.js';
import * as ns from './module.js';

// Default import
import main from './module.js';

// Both
import main, { helper } from './module.js';

// Re-export
export { fn } from './other.js';
export { default as Foo } from './other.js';

// Dynamic
const { fn } = await import('./module.js');

// Barrel (index.js)
export { Button } from './Button.js';
export { Card } from './Card.js';
```
