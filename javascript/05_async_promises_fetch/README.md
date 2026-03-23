# 05 — Async: Promises and Fetch

JavaScript is single-threaded — it runs one thing at a time. Async patterns let it handle waiting (network requests, timers, file reads) without blocking. Promises are the foundation of all modern async code.

---

## Mental Model

```
Synchronous code:
  step 1 → step 2 → step 3 (each waits for the previous)

Asynchronous code:
  kick off request → do other work while waiting → handle result when ready
```

JavaScript delegates waiting to the browser (or Node.js runtime) and moves on. When the work finishes, the callback is queued.

---

## The Callback Problem

Callbacks were the original async pattern:

```js
getData(function(data) {
  processData(data, function(result) {
    saveResult(result, function(saved) {
      logSuccess(saved, function() {
        // "Callback hell" / "Pyramid of doom"
      });
    });
  });
});
```

Problems: deeply nested, hard to read, error handling is inconsistent, can't use `try/catch`.

---

## Promises

A `Promise` represents a value that will be available in the future. It's in one of three states:

| State | Meaning |
|---|---|
| `pending` | Work is in progress |
| `fulfilled` | Completed successfully, has a value |
| `rejected` | Failed, has a reason (error) |

Once settled (fulfilled or rejected), a Promise never changes state.

### Creating a Promise

```js
const promise = new Promise((resolve, reject) => {
  // Do async work here
  if (success) {
    resolve(value);  // fulfills the promise
  } else {
    reject(new Error('Something went wrong'));  // rejects it
  }
});
```

### `.then`, `.catch`, `.finally`

```js
fetch('/api/user')
  .then(response => response.json())     // runs on success, returns new promise
  .then(data => console.log(data))       // chains
  .catch(error => console.error(error))  // runs on any error in the chain
  .finally(() => console.log('done'));   // always runs
```

Each `.then` returns a new Promise — this is what enables chaining.

```js
// Returning a value from .then wraps it in a fulfilled Promise
promise
  .then(data => data.users)           // extract users array
  .then(users => users.filter(...))   // transform
  .then(filtered => console.log(filtered));
```

---

## Promise Combinators

### `Promise.all` — all must succeed

```js
const [user, posts, comments] = await Promise.all([
  fetch('/api/user').then(r => r.json()),
  fetch('/api/posts').then(r => r.json()),
  fetch('/api/comments').then(r => r.json()),
]);
// Runs in parallel. If ANY fails, the whole thing rejects.
```

### `Promise.allSettled` — wait for all, don't fail on rejection

```js
const results = await Promise.allSettled([
  fetch('/api/user').then(r => r.json()),
  fetch('/api/posts').then(r => r.json()),
]);

results.forEach(result => {
  if (result.status === 'fulfilled') {
    console.log(result.value);
  } else {
    console.error(result.reason);
  }
});
```

### `Promise.race` — first to settle wins

```js
// Useful for timeouts
const timeout = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Timeout')), 5000)
);

const data = await Promise.race([fetch('/api/data'), timeout]);
```

### `Promise.any` — first to *succeed* wins

```js
// Try multiple sources, use whichever responds first
const data = await Promise.any([
  fetch('https://primary.api/data'),
  fetch('https://fallback.api/data'),
]);
// Rejects only if ALL fail (AggregateError)
```

---

## `fetch` API

`fetch` is the browser's built-in way to make HTTP requests. It returns a Promise.

### Basic GET request

```js
fetch('https://api.example.com/users')
  .then(response => {
    // response is a Response object — NOT the data yet
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();  // parse JSON body — also returns a Promise
  })
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### POST request with JSON body

```js
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ name: 'Alec', age: 22 }),
})
  .then(r => r.json())
  .then(data => console.log(data));
```

### Response object

```js
response.ok;         // true if status is 200–299
response.status;     // 200, 404, 500, etc.
response.statusText; // 'OK', 'Not Found', etc.
response.headers;    // Headers object

// Body parsing (each returns a Promise — call only once)
response.json();    // parse as JSON
response.text();    // parse as plain text
response.blob();    // binary data (images, files)
```

**Important:** `fetch` only rejects on network failure (can't connect). A 404 or 500 is NOT a rejection — you must check `response.ok`.

---

## Error Handling with Promises

```js
fetch('/api/data')
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(data => process(data))
  .catch(error => {
    // Catches: network errors, manual throws, JSON parse errors
    console.error('Failed:', error.message);
  });
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Forgetting to check `response.ok` | `fetch` resolves on 404/500 — always check `response.ok` |
| Forgetting to call `.json()` | `response` is not the data — parse it first |
| Calling `.json()` twice | Body stream can only be consumed once |
| `.then` without `.catch` | Unhandled rejections are silent bugs — always add `.catch` |
| Not returning from `.then` | Returning nothing passes `undefined` to the next `.then` |
| `Promise.all` when you want partial results | Use `Promise.allSettled` so one failure doesn't kill the rest |

---

## Quick Reference Card

```js
// Create a promise
new Promise((resolve, reject) => {
  resolve(value);   // fulfill
  reject(error);    // reject
});

// Chain
fetch(url)
  .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(data => console.log(data))
  .catch(err => console.error(err))
  .finally(() => cleanup());

// Parallel
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// All results, even if some fail
const results = await Promise.allSettled([fetchA(), fetchB()]);
results.forEach(r => r.status === 'fulfilled' ? use(r.value) : log(r.reason));

// First success
const data = await Promise.any([primary(), fallback()]);

// POST with fetch
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload),
});
```
