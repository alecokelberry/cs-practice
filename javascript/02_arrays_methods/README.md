# 02 — Array Methods

JavaScript's built-in array methods let you transform, filter, and aggregate data without writing manual loops. Most return a new array — the original is not modified.

---

## Mental Model

Think of array methods as a pipeline. Data flows in, gets transformed, and flows out.

```
original array
    │
    ├── filter()   → removes elements that don't match
    ├── map()      → transforms each element
    └── reduce()   → collapses all elements into one value
```

**Key distinction:**
- **Mutating methods** — change the original array: `push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse`
- **Non-mutating methods** — return a new array: `map`, `filter`, `reduce`, `slice`, `concat`, `flat`, `flatMap`

In modern code, prefer non-mutating methods. When you must sort or reverse, spread first to copy: `[...arr].sort(...)`.

---

## `map` — Transform Each Element

Returns a new array of the same length.

```js
const nums = [1, 2, 3, 4];

const doubled = nums.map(n => n * 2);    // [2, 4, 6, 8]
const strings = nums.map(n => String(n)); // ['1', '2', '3', '4']

// Common: extract a field from an array of objects
const users = [{ name: 'Alec' }, { name: 'Sam' }];
const names = users.map(u => u.name);    // ['Alec', 'Sam']

// map callback receives: (element, index, array)
const indexed = nums.map((n, i) => `${i}: ${n}`);
// ['0: 1', '1: 2', '2: 3', '3: 4']
```

---

## `filter` — Keep Matching Elements

Returns a new array containing only elements for which the callback returns true.

```js
const nums = [1, 2, 3, 4, 5, 6];

const evens = nums.filter(n => n % 2 === 0);  // [2, 4, 6]
const over3 = nums.filter(n => n > 3);         // [4, 5, 6]

// Remove falsy values
const clean = [0, 1, '', 'hello', null, true].filter(Boolean);
// [1, 'hello', true]

// Filter objects
const admins = users.filter(u => u.role === 'admin');
```

---

## `reduce` — Accumulate to a Single Value

The most flexible array method. Iterates through the array, building up an accumulator.

```js
// reduce(callback, initialValue)
// callback receives: (accumulator, element, index, array)

const nums = [1, 2, 3, 4];

const sum = nums.reduce((acc, n) => acc + n, 0);  // 10
const product = nums.reduce((acc, n) => acc * n, 1); // 24

// Build an object from an array
const users = [{ id: 1, name: 'Alec' }, { id: 2, name: 'Sam' }];

const byId = users.reduce((acc, user) => {
  acc[user.id] = user;
  return acc;
}, {});
// { 1: { id: 1, name: 'Alec' }, 2: { id: 2, name: 'Sam' } }

// Count occurrences
const words = ['a', 'b', 'a', 'c', 'a', 'b'];
const counts = words.reduce((acc, word) => {
  acc[word] = (acc[word] ?? 0) + 1;
  return acc;
}, {});
// { a: 3, b: 2, c: 1 }

// Flatten (use flat() instead — this is just to show reduce's power)
[[1, 2], [3, 4]].reduce((acc, arr) => [...acc, ...arr], []);
// [1, 2, 3, 4]
```

**Always provide the initial value** — omitting it uses the first element, which breaks on empty arrays.

---

## `forEach` — Side Effects Only

Like `map` but returns `undefined`. Use when you need to *do* something with each element, not transform it.

```js
const items = ['a', 'b', 'c'];

items.forEach((item, index) => {
  console.log(`${index}: ${item}`);
});

// Can't break out of forEach — use a for...of loop instead if you need to break
for (const item of items) {
  if (item === 'b') break;
}
```

---

## `find` and `findIndex`

```js
const users = [
  { id: 1, name: 'Alec' },
  { id: 2, name: 'Sam' },
];

// find — returns the first matching element (or undefined)
const user = users.find(u => u.id === 2);   // { id: 2, name: 'Sam' }
const none = users.find(u => u.id === 99);  // undefined

// findIndex — returns the index (or -1)
const idx = users.findIndex(u => u.id === 2);  // 1
const notFound = users.findIndex(u => u.id === 99); // -1
```

---

## `some` and `every`

```js
const nums = [1, 3, 5, 7, 8];

// some — true if at least one element matches
nums.some(n => n % 2 === 0);   // true (8 is even)
nums.some(n => n > 100);       // false

// every — true if all elements match
nums.every(n => n > 0);        // true
nums.every(n => n % 2 !== 0);  // false (8 is even)
```

Both short-circuit: `some` stops at the first `true`, `every` stops at the first `false`.

---

## `includes`

```js
[1, 2, 3].includes(2);       // true
[1, 2, 3].includes(99);      // false
['a', 'b'].includes('a');    // true
```

Uses strict equality (`===`). Won't work for objects — use `find` or `some` for those.

---

## `flat` and `flatMap`

```js
// flat — flatten nested arrays
const nested = [1, [2, 3], [4, [5, 6]]];
nested.flat();    // [1, 2, 3, 4, [5, 6]]  (depth 1)
nested.flat(2);   // [1, 2, 3, 4, 5, 6]   (depth 2)
nested.flat(Infinity); // fully flatten

// flatMap — map then flatten (depth 1)
const sentences = ['hello world', 'foo bar'];
const words = sentences.flatMap(s => s.split(' '));
// ['hello', 'world', 'foo', 'bar']
```

---

## `Array.from`

Creates an array from an array-like or iterable.

```js
// From a string
Array.from('hello');          // ['h', 'e', 'l', 'l', 'o']

// From a Set (removes duplicates)
Array.from(new Set([1, 2, 2, 3])); // [1, 2, 3]

// From NodeList (DOM)
Array.from(document.querySelectorAll('li'));

// With map function
Array.from({ length: 5 }, (_, i) => i);  // [0, 1, 2, 3, 4]
Array.from({ length: 5 }, (_, i) => i * 2); // [0, 2, 4, 6, 8]
```

---

## Sorting

**Default sort converts to strings — it doesn't sort numbers correctly.**

```js
[10, 9, 2, 1, 100].sort(); // [1, 10, 100, 2, 9]  — WRONG

// Numeric sort: compare function returns negative, 0, or positive
[10, 9, 2, 1, 100].sort((a, b) => a - b); // [1, 2, 9, 10, 100] ascending
[10, 9, 2, 1, 100].sort((a, b) => b - a); // [100, 10, 9, 2, 1] descending

// Sort objects by a field
users.sort((a, b) => a.name.localeCompare(b.name)); // alphabetical

// sort() mutates — copy first if you need the original
const sorted = [...arr].sort((a, b) => a - b);
```

---

## `slice` and `splice`

```js
const arr = [1, 2, 3, 4, 5];

// slice — non-mutating, returns a portion
arr.slice(1, 3);    // [2, 3] (index 1 up to but not including 3)
arr.slice(2);       // [3, 4, 5]
arr.slice(-2);      // [4, 5] (last 2)
arr.slice();        // shallow copy

// splice — mutating, removes/inserts elements
arr.splice(2, 1);        // removes 1 element at index 2; arr is now [1, 2, 4, 5]
arr.splice(1, 0, 9, 8);  // insert 9, 8 at index 1 (remove 0)
arr.splice(2, 2, 99);    // replace 2 elements at index 2 with 99
```

---

## Chaining

Methods that return arrays can be chained:

```js
const result = users
  .filter(u => u.active)
  .map(u => u.name)
  .sort((a, b) => a.localeCompare(b));
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `[10, 1, 9].sort()` expecting numeric order | Always pass a compare function for numbers |
| `sort()` on original when you need to preserve it | Copy with `[...arr].sort()` first |
| Forgetting initial value in `reduce` | Always pass `reduce(fn, initialValue)` |
| Using `map` when you want side effects | Use `forEach` or `for...of` for side effects |
| `arr.includes(obj)` for objects | Objects are compared by reference — use `arr.some(x => x.id === obj.id)` |
| `forEach` and expecting to break | Use `for...of` or `some` (return true to stop) instead |

---

## Quick Reference Card

```js
const nums = [1, 2, 3, 4, 5];
const users = [{ id: 1, name: 'A', active: true }, { id: 2, name: 'B', active: false }];

// Transform
nums.map(n => n * 2);                          // [2, 4, 6, 8, 10]

// Filter
nums.filter(n => n > 2);                       // [3, 4, 5]
users.filter(u => u.active);                   // [{ id: 1... }]

// Find
users.find(u => u.id === 1);                   // { id: 1, name: 'A', active: true }
users.findIndex(u => u.id === 1);              // 0

// Aggregate
nums.reduce((acc, n) => acc + n, 0);           // 15

// Check
nums.some(n => n > 4);                         // true
nums.every(n => n > 0);                        // true
nums.includes(3);                              // true

// Flatten
[[1, 2], [3, 4]].flat();                       // [1, 2, 3, 4]
['a b', 'c d'].flatMap(s => s.split(' '));     // ['a', 'b', 'c', 'd']

// Sort (numbers)
[...nums].sort((a, b) => b - a);              // [5, 4, 3, 2, 1]

// Copy portion
nums.slice(1, 3);                             // [2, 3]

// Create
Array.from({ length: 3 }, (_, i) => i + 1);  // [1, 2, 3]
```
