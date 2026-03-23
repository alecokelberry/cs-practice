# 09 — Error Handling and Debugging

Errors are inevitable. Handling them well means your app fails gracefully instead of crashing. Debugging tools mean you can find problems fast.

---

## `try` / `catch` / `finally`

```js
try {
  // Code that might throw
  const data = JSON.parse(text);
  doSomethingRisky(data);
} catch (error) {
  // Runs if anything in the try block throws
  console.error(error.message);
} finally {
  // Always runs — success or failure
  cleanup();
}
```

- `catch` receives the Error object
- `finally` is optional; useful for cleanup (closing connections, hiding spinners)
- If you re-throw in `catch`, `finally` still runs

### Async/await with try/catch

```js
async function load() {
  try {
    const r = await fetch('/api/data');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (err) {
    console.error('Load failed:', err.message);
    return null;
  }
}
```

---

## The Error Object

```js
const err = new Error('Something went wrong');

err.message;  // 'Something went wrong'
err.name;     // 'Error'
err.stack;    // stack trace as a string (very useful for debugging)
```

### Built-in Error Types

| Type | When it's thrown |
|---|---|
| `Error` | Generic — use this for custom errors |
| `TypeError` | Wrong type: calling a non-function, accessing property of `null` |
| `ReferenceError` | Variable doesn't exist |
| `SyntaxError` | Invalid JavaScript (usually caught before runtime) |
| `RangeError` | Value out of allowed range (`new Array(-1)`, recursion limit) |
| `URIError` | Bad URI encoding |

```js
null.name;            // TypeError: Cannot read properties of null
undeclaredVar;        // ReferenceError: undeclaredVar is not defined
JSON.parse('{bad}');  // SyntaxError: Unexpected token b in JSON
```

---

## Custom Error Classes

Extend `Error` to create domain-specific errors you can catch selectively.

```js
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

class NetworkError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'NetworkError';
    this.status = status;
  }
}

// Throw
throw new ValidationError('email', 'Email is required');

// Catch selectively
try {
  validateForm(data);
} catch (err) {
  if (err instanceof ValidationError) {
    showFieldError(err.field, err.message);
  } else {
    throw err;  // re-throw — not our responsibility to handle
  }
}
```

---

## Re-throwing

Don't catch errors you can't handle — re-throw them so something higher up can.

```js
async function loadUser(id) {
  try {
    const r = await fetch(`/api/users/${id}`);
    return await r.json();
  } catch (err) {
    if (err instanceof NetworkError) {
      logToMonitoring(err);  // handle what you can
    }
    throw err;  // re-throw everything
  }
}
```

---

## `console` Methods

```js
console.log('Basic output', value);
console.warn('Warning — not an error but notable');
console.error('Error — shows in red in DevTools');

// Object inspection
console.table([{ name: 'Alec', age: 22 }, { name: 'Sam', age: 25 }]);
// Displays as a formatted table

// Collapsible groups
console.group('User data');
console.log(user);
console.log(permissions);
console.groupEnd();

// Timing
console.time('fetch');
await fetchData();
console.timeEnd('fetch');  // 'fetch: 234.5ms'

// Count calls
console.count('loop');  // 'loop: 1', 'loop: 2', etc.
console.countReset('loop');

// Assert (logs only if false)
console.assert(arr.length > 0, 'Array is empty!');

// Stack trace
console.trace('How did I get here?');
```

---

## The `debugger` Statement

Pauses execution and opens DevTools at that line — like setting a breakpoint in code.

```js
function calculateTotal(items) {
  debugger;  // execution pauses here when DevTools is open
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

Remove `debugger` before committing — it has no effect when DevTools is closed, but it's noise.

---

## DevTools Debugging Workflow

1. **Sources panel** — set breakpoints by clicking line numbers
2. **Step over** (F10) — execute current line, stay in current function
3. **Step into** (F11) — execute current line, enter function calls
4. **Step out** (Shift+F11) — run to end of current function
5. **Watch expressions** — add variables to monitor their values
6. **Scope panel** — see all variables in current scope
7. **Call stack** — see how you got to the current line
8. **Network tab** — inspect HTTP requests, responses, timing

---

## Common JavaScript Bugs

### `TypeError: Cannot read properties of null/undefined`

```js
// Bug: assuming element exists
document.querySelector('#missing').addEventListener('click', fn);
// querySelector returned null — null has no addEventListener

// Fix: guard check
const el = document.querySelector('#missing');
el?.addEventListener('click', fn);
```

### Type coercion surprises

```js
// Loose equality — avoid ==
0 == false;      // true
'' == false;     // true
null == undefined; // true

// Always use strict equality ===
0 === false;     // false

// typeof null is 'object' — historical bug
typeof null === 'object'; // true (not 'null')
// Check for null explicitly:
value === null;
```

### `this` binding lost

```js
class Timer {
  start() {
    // 'this' is lost when setTimeout calls the function
    setTimeout(function() {
      this.tick();  // TypeError: this.tick is not a function
    }, 1000);

    // Fix: use arrow function
    setTimeout(() => {
      this.tick();  // correctly refers to Timer instance
    }, 1000);
  }
}
```

### Async errors not caught

```js
// Bug: catch doesn't see async errors
try {
  fetchData();  // forgot await — returns a Promise, doesn't throw
} catch (err) {
  // never runs
}

// Fix: await it
try {
  await fetchData();
} catch (err) {
  // now caught
}
```

### `NaN` comparisons

```js
NaN === NaN;    // false — NaN is never equal to itself
typeof NaN;     // 'number' — unhelpful

// Check for NaN:
Number.isNaN(value);   // correct
isNaN('hello');        // true — coerces first, avoid
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Swallowing errors with empty `catch` | At minimum, log them: `catch(err) { console.error(err); }` |
| Catching `Error` when you only expect one type | Check `instanceof` and re-throw what you can't handle |
| `try/catch` around a non-awaited async call | You must `await` for `try/catch` to catch async errors |
| `console.log` debugging left in production | Remove debug logs before committing; use a logger with levels |
| Using `==` for comparisons | Always use `===` |
| Not reading the stack trace | The stack trace tells you exactly where the error originated |

---

## Quick Reference Card

```js
// try/catch/finally
try {
  riskyOperation();
} catch (err) {
  if (err instanceof TypeError) { ... }
  else throw err;  // re-throw unknown errors
} finally {
  cleanup();
}

// Custom error
class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'AppError';
    this.code = code;
  }
}

throw new AppError('Not found', 404);

// Async errors
async function safe() {
  try {
    return await fetchData();
  } catch (err) {
    console.error(err);
    return null;
  }
}

// Console
console.log(value);
console.error(err);
console.table(arrayOfObjects);
console.time('label'); ... console.timeEnd('label');
console.assert(condition, 'message if false');

// debugger
function debug() {
  debugger;  // pauses here in DevTools
}

// Type checking
typeof value === 'string';
value instanceof Date;
Number.isNaN(value);
Array.isArray(value);
value === null;
value == null;  // true for both null and undefined
```
