# 07 — DOM Manipulation and Events

The DOM (Document Object Model) is the browser's live representation of an HTML page as a tree of objects. JavaScript can read and modify it to change what the user sees.

---

## Mental Model

```
HTML                      DOM Tree
<body>              →     body (Element)
  <div id="app">    →       div#app (Element)
    <p>Hello</p>    →         p (Element)
  </div>                        "Hello" (Text)
</body>
```

Everything in the DOM is a node. Element nodes (tags) are the ones you'll interact with most.

---

## Selecting Elements

```js
// Single element — returns the first match, or null
document.querySelector('#app');           // by ID
document.querySelector('.card');          // by class
document.querySelector('h1');             // by tag
document.querySelector('nav a.active');   // any CSS selector

// Multiple elements — returns a static NodeList (array-like)
document.querySelectorAll('.card');        // all matches
document.querySelectorAll('ul > li');

// Older methods (still useful, slightly faster)
document.getElementById('app');
document.getElementsByClassName('card');  // live HTMLCollection
document.getElementsByTagName('li');      // live HTMLCollection

// Scoped query — search inside an element
const nav = document.querySelector('nav');
nav.querySelectorAll('a');  // only anchors inside nav
```

**NodeList vs Array:** NodeList has `forEach` but not `map`/`filter`. Convert with `Array.from(list)` or `[...list]`.

---

## Reading and Writing Content

```js
const el = document.querySelector('#message');

// Text content — safe, no HTML parsing
el.textContent;          // read
el.textContent = 'New text'; // write

// HTML content — parses HTML, XSS risk
el.innerHTML;                       // read
el.innerHTML = '<strong>Bold</strong>'; // write — ONLY safe with trusted content

// innerText — like textContent but respects visibility + triggers reflow (slower)
el.innerText;
```

**XSS warning:** Never put user-supplied data in `innerHTML`. Use `textContent` for user data, or sanitize first.

---

## Attributes and Data

```js
const link = document.querySelector('a');

// Standard attributes
link.getAttribute('href');
link.setAttribute('href', '/new-path');
link.removeAttribute('disabled');
link.hasAttribute('disabled');

// Properties (reflect HTML attributes, but some differ)
link.href;        // full absolute URL, not just the attribute value
input.value;      // current value typed by user
input.checked;    // current checkbox state
img.src;          // absolute URL

// Dataset (data-* attributes)
// <div data-user-id="42" data-role="admin">
el.dataset.userId; // '42'    (camelCase in JS, kebab-case in HTML)
el.dataset.role;   // 'admin'
el.dataset.userId = '99';  // sets data-user-id="99"
```

---

## Classes

```js
const el = document.querySelector('.card');

el.classList.add('active');
el.classList.remove('hidden');
el.classList.toggle('open');           // adds if absent, removes if present
el.classList.toggle('open', true);     // force add
el.classList.toggle('open', false);    // force remove
el.classList.contains('active');       // boolean
el.classList.replace('old', 'new');

// Multiple at once
el.classList.add('one', 'two', 'three');

// className — the raw string (avoid unless you need to read all classes)
el.className;  // 'card active visible'
```

---

## Creating and Inserting Elements

```js
// Create
const div = document.createElement('div');
div.textContent = 'New element';
div.classList.add('card');

// Insert
parent.append(child);         // add as last child
parent.prepend(child);        // add as first child
sibling.after(child);         // insert after sibling
sibling.before(child);        // insert before sibling

// Insert HTML string (careful with XSS)
parent.insertAdjacentHTML('beforeend', '<li>Item</li>');
// Positions: 'beforebegin', 'afterbegin', 'beforeend', 'afterend'

// Remove
el.remove();

// Clone
const copy = el.cloneNode(true);  // true = deep clone (includes children)
```

---

## Inline Style

```js
el.style.color = 'red';
el.style.backgroundColor = 'blue';   // camelCase for hyphenated CSS
el.style.fontSize = '16px';          // value must include units
el.style.display = 'none';           // hide
el.style.display = '';               // reset to CSS default

// Read computed style (what the browser actually applies)
const computed = getComputedStyle(el);
computed.fontSize;  // '16px'
```

Prefer toggling classes over setting inline styles — keeps CSS in CSS.

---

## Events

### `addEventListener`

```js
const btn = document.querySelector('#submit');

btn.addEventListener('click', function(event) {
  console.log('clicked', event);
});

// Arrow function (but can't remove later without a reference)
btn.addEventListener('click', (e) => {
  e.preventDefault();
});

// Named function reference — needed for removeEventListener
function handleClick(e) { ... }
btn.addEventListener('click', handleClick);
btn.removeEventListener('click', handleClick);
```

### The Event Object

```js
btn.addEventListener('click', (e) => {
  e.target;          // the element that triggered the event
  e.currentTarget;   // the element the listener is attached to (same as `this` in regular function)
  e.type;            // 'click'

  // Mouse events
  e.clientX; e.clientY;  // position relative to viewport
  e.pageX;   e.pageY;    // position relative to document

  // Keyboard events
  e.key;    // 'Enter', 'ArrowUp', 'a', etc.
  e.code;   // 'KeyA', 'Enter', 'Space' (physical key, layout-independent)
  e.ctrlKey; e.shiftKey; e.altKey; e.metaKey; // modifier keys

  // Form events
  e.target.value;   // current value of an input

  e.preventDefault();   // stop default browser behavior (form submit, link navigate)
  e.stopPropagation();  // stop event from bubbling up the DOM
});
```

### Common Event Types

| Event | When it fires |
|---|---|
| `click` | Element clicked |
| `input` | Input value changes (every keystroke) |
| `change` | Input value committed (blur, Enter, select change) |
| `submit` | Form submitted |
| `keydown` | Key pressed down |
| `keyup` | Key released |
| `focus` / `blur` | Element gains / loses focus |
| `mouseenter` / `mouseleave` | Mouse enters / leaves element (no bubbling) |
| `mouseover` / `mouseout` | Mouse over / out (bubbles) |
| `scroll` | Element or page scrolls |
| `DOMContentLoaded` | DOM parsed (before images/CSS load) |
| `load` | Page fully loaded (all resources) |

---

## Event Bubbling and Delegation

Events **bubble** up the DOM from the target to the root.

```
click on <button> → bubbles to <div> → bubbles to <body> → bubbles to <html>
```

**Event delegation** — attach one listener to a parent instead of many listeners to children:

```js
// INSTEAD OF attaching a listener to every button:
document.querySelectorAll('.list button').forEach(btn => {
  btn.addEventListener('click', handleClick);
});

// DO THIS — one listener on the parent:
document.querySelector('.list').addEventListener('click', (e) => {
  const btn = e.target.closest('button');  // find the button (even if clicked on a child)
  if (!btn) return;
  handleClick(e);
});
```

Benefits: works for dynamically added elements, fewer listeners = less memory.

---

## `DOMContentLoaded` vs `load`

```js
// DOM is ready — use this for most scripts
document.addEventListener('DOMContentLoaded', () => {
  // Safe to query and manipulate the DOM
});

// Everything loaded (images, stylesheets) — use for measuring layout
window.addEventListener('load', () => { ... });
```

Scripts in `<head>` run before the DOM is built — use `DOMContentLoaded` or move scripts to the end of `<body>` (or use `defer`).

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `innerHTML` with user input | Use `textContent` for text, or sanitize HTML |
| Querying the DOM before it's ready | Use `DOMContentLoaded` or put scripts at end of body |
| Adding listeners in a loop to each element | Use event delegation on the parent |
| `NodeList.map(...)` doesn't work | Convert: `Array.from(list).map(...)` or `[...list].map(...)` |
| `el.style.fontSize = 16` (no units) | Values need units: `'16px'` |
| `removeEventListener` with inline arrow | Arrows create new references each time — store the handler in a variable |
| `e.target` vs `e.currentTarget` confusion | `target` = where click happened; `currentTarget` = where listener is attached |

---

## Quick Reference Card

```js
// Select
document.querySelector('#id');
document.querySelectorAll('.class');
parent.querySelector('a');

// Content
el.textContent = 'safe text';
el.innerHTML = '<b>trusted html only</b>';

// Attributes
el.getAttribute('href');
el.setAttribute('data-id', '42');
el.dataset.userId; // from data-user-id attribute

// Classes
el.classList.add('active');
el.classList.remove('hidden');
el.classList.toggle('open');
el.classList.contains('active');

// Create + insert
const el = document.createElement('div');
el.textContent = 'Hello';
parent.append(el);
el.remove();

// Events
el.addEventListener('click', (e) => {
  e.preventDefault();
  e.stopPropagation();
  console.log(e.target);
});

// Event delegation
list.addEventListener('click', (e) => {
  const item = e.target.closest('li');
  if (!item) return;
  // handle item
});

// DOM ready
document.addEventListener('DOMContentLoaded', () => { ... });
```
