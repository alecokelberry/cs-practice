# 01 — Modern ES6+ Basics

ES6 (2015) modernized JavaScript significantly. These features appear in every modern codebase — understanding them cold is a prerequisite for everything else.

---

## `var` vs `let` vs `const`

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Function | Block | Block |
| Hoisted | Yes (value: `undefined`) | Yes (TDZ — unusable) | Yes (TDZ — unusable) |
| Re-declarable | Yes | No | No |
| Re-assignable | Yes | Yes | No |

**TDZ (Temporal Dead Zone):** `let` and `const` are hoisted to the top of their block but can't be accessed until the declaration line. Accessing them before that throws a `ReferenceError`.

```js
console.log(x); // undefined — var is hoisted with value
var x = 5;

console.log(y); // ReferenceError — TDZ
let y = 5;
```

**Rule of thumb:** Always use `const`. Use `let` when you need to reassign. Never use `var`.

`const` doesn't make objects immutable — it prevents reassigning the *binding*:

```js
const user = { name: 'Alec' };
user.name = 'Alex';     // fine — mutating the object
user = { name: 'Bob' }; // TypeError — reassigning the binding
```

---

## Arrow Functions

```js
// Traditional function
function add(a, b) {
  return a + b;
}

// Arrow function (single expression — implicit return)
const add = (a, b) => a + b;

// Arrow function (body with braces — explicit return required)
const add = (a, b) => {
  const result = a + b;
  return result;
};

// Single parameter — parens optional
const double = n => n * 2;

// No parameters — parens required
const greet = () => 'hello';
```

### When NOT to use arrow functions

Arrow functions don't have their own `this`. They inherit `this` from the surrounding scope.

```js
const obj = {
  name: 'Alec',

  // DON'T — arrow inherits this from module scope (not obj)
  greet: () => console.log(this.name),  // undefined

  // DO — regular method has its own this
  greet() { console.log(this.name); },  // 'Alec'
};
```

Also avoid for: object methods, `prototype` methods, constructors, event handlers where you need `this` to be the element.

---

## Template Literals

```js
const name = 'Alec';
const score = 95;

// Old way
const msg = 'Hello, ' + name + '! Score: ' + score;

// Template literal (backticks)
const msg = `Hello, ${name}! Score: ${score}`;

// Expressions work too
const msg = `Score: ${score > 90 ? 'A' : 'B'}`;

// Multi-line (no \n needed)
const html = `
  <div class="card">
    <p>${name}</p>
  </div>
`;
```

---

## Destructuring

### Array destructuring

```js
const coords = [10, 20, 30];

// Old way
const x = coords[0];
const y = coords[1];

// Destructuring
const [x, y, z] = coords;

// Skip elements
const [, second, third] = coords;

// Default values
const [a, b, c = 0] = [1, 2];

// Swap variables
let p = 1, q = 2;
[p, q] = [q, p];

// Rest — collect the remainder
const [first, ...rest] = [1, 2, 3, 4];
// first = 1, rest = [2, 3, 4]
```

### Object destructuring

```js
const user = { name: 'Alec', age: 22, role: 'student' };

// Basic
const { name, age } = user;

// Rename
const { name: userName, age: userAge } = user;

// Default value
const { name, theme = 'light' } = user;

// Nested
const { address: { city } } = { address: { city: 'Dallas' } };

// Rest
const { name, ...rest } = user;
// rest = { age: 22, role: 'student' }

// In function parameters (very common)
function greet({ name, age = 0 }) {
  return `${name} is ${age}`;
}
greet(user);
```

---

## Default Parameters

```js
function greet(name = 'stranger', greeting = 'Hello') {
  return `${greeting}, ${name}!`;
}

greet();               // 'Hello, stranger!'
greet('Alec');         // 'Hello, Alec!'
greet('Alec', 'Hey'); // 'Hey, Alec!'
```

Default values are evaluated at call time, not at definition time. Can be expressions or function calls.

---

## Rest and Spread (`...`)

### Rest — collect remaining arguments into an array

```js
function sum(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4); // 10

// Must be last parameter
function log(label, ...items) { ... }
```

### Spread — expand an iterable into individual elements

```js
// Arrays
const a = [1, 2, 3];
const b = [4, 5, 6];
const combined = [...a, ...b];      // [1, 2, 3, 4, 5, 6]
const copy = [...a];                // shallow copy

// Objects
const defaults = { theme: 'light', lang: 'en' };
const settings = { ...defaults, lang: 'fr' }; // override lang
// { theme: 'light', lang: 'fr' }

// Passing array as individual args
Math.max(...[1, 5, 3]); // 5
```

Spread creates **shallow copies** — nested objects/arrays are still references.

---

## Optional Chaining (`?.`)

Safely access deeply nested values without throwing if something is `null` or `undefined`.

```js
const user = { address: { city: 'Dallas' } };
const noAddress = {};

// Old way — verbose
const city = user && user.address && user.address.city;

// Optional chaining
const city = user?.address?.city;           // 'Dallas'
const city2 = noAddress?.address?.city;    // undefined (no throw)

// Works on method calls and array access too
const result = obj?.method?.();            // calls method if it exists
const item = arr?.[0];                     // undefined if arr is null/undefined
```

---

## Nullish Coalescing (`??`)

Returns the right side only if the left is `null` or `undefined` (not falsy).

```js
// Old way — || has a bug with 0, '', false
const name = user.name || 'Anonymous'; // wrong if name is ''

// Nullish coalescing — only triggers on null/undefined
const name = user.name ?? 'Anonymous';
const count = user.count ?? 0;  // safe when count could be 0
```

| Expression | `||` triggers if | `??` triggers if |
|---|---|---|
| `0 \|\| default` | Yes — 0 is falsy | No — 0 is not null/undefined |
| `'' \|\| default` | Yes — '' is falsy | No |
| `null \|\| default` | Yes | Yes |
| `undefined \|\| default` | Yes | Yes |

### Nullish assignment

```js
// Only assign if current value is null/undefined
user.name ??= 'Anonymous';   // equivalent to: user.name = user.name ?? 'Anonymous'
user.count ||= 0;            // assign if falsy
user.count &&= user.count * 2; // assign if truthy
```

---

## Short-circuit Evaluation

```js
// && — returns first falsy value, or last value if all truthy
false && doSomething();   // doSomething never called
true && doSomething();    // doSomething is called

// Conditional rendering pattern (common in JSX/templates)
const isAdmin = true;
isAdmin && showAdminPanel();

// || — returns first truthy value, or last value if all falsy
const name = input || 'default';
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `var` in loops | Use `let` — `var` leaks out of the loop block |
| Arrow function as object method | Use regular `function` or shorthand method syntax |
| `const obj = {}` thinking it's frozen | `const` prevents rebinding, not mutation |
| `undefined || 0` gives `0` but `undefined ?? 0` gives `0` | Use `??` when `0`/`''`/`false` are valid values |
| Spread of non-iterables | `...null` throws — check for nulls first |
| Deeply nested destructuring silently gives `undefined` | Use optional chaining or defaults |

---

## Quick Reference Card

```js
// Variables
const x = 1;        // prefer const
let y = 2;          // use when reassignment needed

// Arrow function
const fn = (a, b) => a + b;
const fn = x => x * 2;
const fn = () => ({ key: 'value' });  // returning object literal needs parens

// Template literal
`Hello, ${name}!`

// Destructuring
const [a, b, ...rest] = array;
const { name, age = 0, role: userRole } = obj;

// Spread
const copy = [...arr];
const merged = { ...defaults, ...overrides };

// Rest params
const sum = (...nums) => nums.reduce((a, n) => a + n, 0);

// Optional chaining + nullish coalescing
const city = user?.address?.city ?? 'Unknown';

// Default params
function greet(name = 'stranger') { ... }
```
