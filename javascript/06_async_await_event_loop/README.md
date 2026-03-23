# 06 — Async/Await and the Event Loop

`async/await` is syntax sugar over Promises — it makes async code look and behave like synchronous code, which is much easier to read and reason about. Understanding the event loop explains *why* async code works the way it does.

---

## `async` / `await`

### `async` functions

An `async` function always returns a Promise. If you return a value, it's wrapped in `Promise.resolve()`.

```js
async function greet() {
  return 'hello';  // actually returns Promise.resolve('hello')
}

greet().then(v => console.log(v)); // 'hello'
```

### `await`

`await` pauses execution of the `async` function until the Promise resolves, then returns the resolved value.

```js
async function getUser() {
  const response = await fetch('/api/user');  // wait for fetch
  const data = await response.json();         // wait for JSON parse
  return data;
}
```

`await` can only be used inside `async` functions (or at the top level of a module).

---

## Replacing `.then` Chains with `async/await`

```js
// Promise chain
function loadUser(id) {
  return fetch(`/api/users/${id}`)
    .then(r => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(user => {
      return fetch(`/api/posts?userId=${user.id}`);
    })
    .then(r => r.json())
    .then(posts => ({ user, posts }));
}

// Same thing with async/await (easier to read)
async function loadUser(id) {
  const r = await fetch(`/api/users/${id}`);
  if (!r.ok) throw new Error(r.status);
  const user = await r.json();

  const postsR = await fetch(`/api/posts?userId=${user.id}`);
  const posts = await postsR.json();

  return { user, posts };
}
```

---

## Error Handling

Use `try/catch` — it works with `await` just like with synchronous code.

```js
async function loadData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to load:', error.message);
    return null;  // or re-throw, or return a default
  } finally {
    hideSpinner();  // always runs
  }
}
```

---

## Sequential vs Parallel

A common mistake is `await`-ing requests one at a time when they could run in parallel.

```js
// SLOW — sequential (each waits for the previous)
const user = await fetchUser();   // 200ms
const posts = await fetchPosts(); // then 150ms = 350ms total

// FAST — parallel with Promise.all
const [user, posts] = await Promise.all([
  fetchUser(),   // both start immediately
  fetchPosts(),  // runs concurrently
]);
// total ≈ 200ms (the slower one)
```

Only run sequentially when the second request depends on the first.

```js
// Sequential is correct here — need user.id before fetching posts
const user = await fetchUser();
const posts = await fetchPosts(user.id);
```

---

## The Event Loop

JavaScript is single-threaded — one thing runs at a time. The event loop is how it handles asynchronous work without blocking.

```
┌─────────────────────────┐
│       Call Stack        │  ← where code executes
└────────────┬────────────┘
             │ delegates async work
┌────────────▼────────────┐
│    Web APIs / Node APIs │  ← timers, fetch, DOM events
└────────────┬────────────┘
             │ when done, queues the callback
     ┌───────┴────────┐
     │                │
┌────▼────┐     ┌─────▼──────┐
│ Microtask│     │ Task Queue │
│  Queue  │     │(macrotasks)│
└────┬────┘     └─────┬──────┘
     │                │
     │    Event Loop checks: stack empty? → run microtasks first, then tasks
     └────────────────┘
```

### Call Stack

Where executing code runs. Functions are pushed on when called, popped off when they return.

### Web APIs

Browser-provided: `setTimeout`, `fetch`, `addEventListener`, etc. They run *outside* the call stack.

### Task Queue (Macrotasks)

Callbacks from: `setTimeout`, `setInterval`, DOM events, `fetch` response.

### Microtask Queue

Higher-priority than the task queue. Runs after every task and after every microtask: `Promise.then/catch/finally`, `queueMicrotask`, `MutationObserver`.

### Order of execution

1. Run current synchronous code (empty the call stack)
2. Run **all** microtasks (drain the microtask queue)
3. Run one macrotask (from the task queue)
4. Go to step 2

```js
console.log('1');                              // sync

setTimeout(() => console.log('2'), 0);         // macrotask

Promise.resolve().then(() => console.log('3')); // microtask

console.log('4');                              // sync

// Output: 1, 4, 3, 2
// Sync runs first, then microtask (Promise), then macrotask (setTimeout)
```

---

## Common Patterns

### Top-level await (in modules)

```js
// In an ES module (.mjs or type="module") — no async wrapper needed
const config = await fetch('/config.json').then(r => r.json());
```

### Timeout helper

```js
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function example() {
  console.log('start');
  await sleep(1000);
  console.log('after 1 second');
}
```

### Retry with backoff

```js
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.json();
    } catch (err) {
      if (i === retries - 1) throw err;
      await sleep(delay * (i + 1));  // exponential backoff
    }
  }
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `await` outside `async` function | Wrap in `async function` or use top-level await in modules |
| Sequential `await` when parallel is possible | Use `Promise.all` for independent requests |
| Forgetting `await` — treating a Promise as the value | `const data = fetch(url)` — `data` is a Promise, not the response |
| `async` in `forEach` — doesn't await | Use `for...of` or `Promise.all(arr.map(async ...))` instead |
| Try/catch not catching async errors | Make sure the `try` block has `await` — catching a Promise doesn't catch its rejection |

### `async` in `forEach` gotcha

```js
// BROKEN — forEach doesn't await async callbacks
const results = [];
ids.forEach(async id => {
  const data = await fetchById(id);
  results.push(data);
});
console.log(results); // [] — nothing awaited yet

// FIXED with for...of
for (const id of ids) {
  const data = await fetchById(id);
  results.push(data);
}

// FIXED with Promise.all (parallel)
const results = await Promise.all(ids.map(id => fetchById(id)));
```

---

## Quick Reference Card

```js
// Async function
async function load() {
  const r = await fetch(url);
  if (!r.ok) throw new Error(r.status);
  return r.json();
}

// Error handling
async function safe() {
  try {
    return await load();
  } catch (err) {
    console.error(err);
    return null;
  }
}

// Parallel requests
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// All, even if some fail
const results = await Promise.allSettled([fetchA(), fetchB()]);

// Iteration
for (const id of ids) {
  const data = await fetchById(id);  // sequential
}
const all = await Promise.all(ids.map(id => fetchById(id)));  // parallel

// Event loop order
console.log('sync 1');
setTimeout(() => console.log('macro'), 0);
Promise.resolve().then(() => console.log('micro'));
console.log('sync 2');
// Output: sync 1, sync 2, micro, macro
```
