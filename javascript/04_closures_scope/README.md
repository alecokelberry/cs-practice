# 04 — Closures and Scope

Scope determines where a variable is accessible. Closures are functions that "remember" the variables from the scope they were created in — even after that scope has finished executing.

---

## Scope

### Global scope

Variables declared outside any function or block. Accessible everywhere. Avoid polluting global scope.

### Function scope

`var` is scoped to the nearest containing function. `let` and `const` are block-scoped.

```js
function example() {
  var x = 1;  // function scope
  let y = 2;  // block scope (same as function scope here)

  if (true) {
    var a = 3;  // STILL function scope — leaks out of the if block
    let b = 4;  // block scope — only accessible inside the if
    console.log(b); // 4
  }

  console.log(a); // 3 — var leaked out
  console.log(b); // ReferenceError — b is block-scoped
}
```

### Block scope

`let` and `const` are confined to the nearest `{}` block: `if`, `for`, `while`, `{}` directly.

```js
{
  const x = 10;
}
console.log(x); // ReferenceError
```

---

## Hoisting

JavaScript moves declarations to the top of their scope before execution — but not initializations.

### `var` hoisting

```js
console.log(x); // undefined (not ReferenceError)
var x = 5;
console.log(x); // 5

// What JavaScript actually does:
var x;           // declaration hoisted to top
console.log(x);  // undefined
x = 5;           // assignment stays here
```

### `let` / `const` hoisting (TDZ)

They are hoisted but placed in the **Temporal Dead Zone** — accessing them before the declaration line throws `ReferenceError`.

```js
console.log(y); // ReferenceError: Cannot access 'y' before initialization
let y = 5;
```

### Function hoisting

Function *declarations* are fully hoisted (name + body). Function *expressions* are not.

```js
greet(); // 'hello' — function declaration is hoisted

function greet() { return 'hello'; }

// vs

sayHi(); // TypeError: sayHi is not a function — only var hoisted, not assignment
var sayHi = function() { return 'hi'; };
```

---

## Lexical Scope

Functions can access variables from the scope they were **defined** in, not where they are *called* from.

```js
const message = 'outer';

function outer() {
  const message = 'inner';

  function inner() {
    console.log(message); // 'inner' — from where inner was defined
  }

  inner();
}

outer();
```

Lexical scope is fixed at write time. It doesn't change based on how or where a function is called.

---

## What Is a Closure?

A closure is a function that retains access to its outer scope's variables even after the outer function has returned.

```js
function makeCounter() {
  let count = 0;  // this variable is "closed over"

  return function() {
    count++;
    return count;
  };
}

const counter = makeCounter();
counter(); // 1
counter(); // 2
counter(); // 3

const counter2 = makeCounter(); // independent counter
counter2(); // 1
```

`count` isn't in global scope — it's private to each closure. The returned function keeps a live reference to it.

---

## Practical Closure Patterns

### Counter with reset

```js
function makeCounter(start = 0) {
  let count = start;

  return {
    increment() { count++; },
    decrement() { count--; },
    reset()     { count = start; },
    value()     { return count; },
  };
}

const c = makeCounter(10);
c.increment();
c.value(); // 11
```

### Factory function

```js
function createUser(name, role) {
  // Private state — not accessible from outside
  const createdAt = new Date();

  return {
    getName()     { return name; },
    getRole()     { return role; },
    getInfo()     { return `${name} (${role}) joined ${createdAt.toDateString()}`; },
  };
}

const user = createUser('Alec', 'student');
user.getName(); // 'Alec'
// user.name is undefined — name is closed over, not exposed
```

### Memoization

```js
function memoize(fn) {
  const cache = new Map();

  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const slowDouble = n => n * 2;  // pretend this is expensive
const fastDouble = memoize(slowDouble);
fastDouble(5); // computed
fastDouble(5); // cached
```

### Event handler with data

```js
function addClickHandler(button, message) {
  button.addEventListener('click', function() {
    console.log(message);  // message is closed over
  });
}

addClickHandler(document.querySelector('#btn1'), 'Button 1 clicked');
addClickHandler(document.querySelector('#btn2'), 'Button 2 clicked');
```

---

## Classic Closure Bug with `var` in Loops

```js
// BROKEN — all callbacks share the same `i` (var leaks out of the loop block)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// logs: 3, 3, 3

// FIXED with let — each iteration gets its own block-scoped i
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// logs: 0, 1, 2
```

This is one of the main reasons `let` replaced `var` in loops.

---

## IIFE (Immediately Invoked Function Expression)

A function that runs immediately after being defined. Creates a private scope.

```js
(function() {
  const private = 'not accessible outside';
  console.log(private);
})();

// Arrow IIFE
(() => {
  // code here
})();
```

IIFEs were common before ES modules for isolating code. In modern JavaScript you use modules instead — but you'll still see IIFEs in older code.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `var` in loops with async callbacks | Use `let` — it creates a new binding per iteration |
| Thinking `const` prevents closure mutation | `const` prevents rebinding; the closed-over object can still be mutated |
| Unexpected `undefined` from hoisted `var` | Use `let`/`const` — no silent `undefined` from hoisting |
| Calling a hoisted `var` function expression before definition | Use function declarations if you need hoisting, or define before use |
| Memory leaks from long-lived closures | If a closure references a large object, that object won't be garbage collected until the closure is gone |

---

## Quick Reference Card

```js
// Block scope
{
  let x = 1;    // accessible only in this block
  const y = 2;  // same
}

// var is function-scoped — usually avoid it
function fn() {
  var x = 1;  // accessible anywhere in fn
}

// Closure — function remembers its outer scope
function outer() {
  let count = 0;
  return () => ++count;
}
const inc = outer();
inc(); // 1
inc(); // 2

// Factory pattern
function makeMultiplier(factor) {
  return n => n * factor;
}
const double = makeMultiplier(2);
const triple = makeMultiplier(3);

// IIFE
(() => {
  // isolated scope
})();

// let fixes the loop bug
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), i * 100); // 0, 1, 2, 3, 4
}
```
