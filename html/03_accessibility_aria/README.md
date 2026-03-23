# 03 — Accessibility & ARIA

Accessibility (a11y) means making your site usable by people who use screen readers, keyboard navigation, voice control, or other assistive technologies. Good accessibility also improves SEO and is often legally required.

---

## Mental Model

The browser exposes an **accessibility tree** alongside the DOM — a simplified version that screen readers and other tools consume. Every HTML element has a role, a name, and a state in that tree.

```
button: role=button, name="Submit", state=enabled
input:  role=textbox, name="Email", state=focused
nav:    role=navigation, name="Main navigation"
```

**The rule:** First try to use native semantic HTML to communicate role and meaning. Add ARIA only when native HTML can't express what you need.

> "No ARIA is better than bad ARIA." — W3C WAI

---

## Semantic HTML IS Accessibility

Before reaching for ARIA, check if a semantic tag solves it:

| Instead of... | Use... |
|---|---|
| `<div onclick="...">Click me</div>` | `<button>Click me</button>` |
| `<div class="nav">` | `<nav>` |
| `<span class="title">Heading</span>` | `<h1>` – `<h6>` |
| `<div class="list"><div class="item">` | `<ul><li>` |
| `<img src="..." >` | `<img src="..." alt="description">` |

Native elements handle keyboard behavior, focus management, and roles automatically. A `<button>` is keyboard-focusable and triggerable with Enter/Space out of the box. A `<div>` is not.

---

## Keyboard Navigation

Sighted keyboard users (and screen reader users) navigate with the keyboard. Your site must work without a mouse.

| Key | What it should do |
|---|---|
| `Tab` | Move focus forward through interactive elements |
| `Shift+Tab` | Move focus backward |
| `Enter` | Activate links and buttons |
| `Space` | Activate buttons (and checkboxes) |
| Arrow keys | Move within components (menus, tabs, sliders) |
| `Escape` | Close modals, menus, tooltips |

**Interactive elements that are focusable by default:** `<a href>`, `<button>`, `<input>`, `<select>`, `<textarea>`, `<details>`.

`tabindex="0"` — makes any element focusable in normal tab order.
`tabindex="-1"` — focusable by JavaScript only (not Tab key). Used for focus management in custom components.
`tabindex="1+"` — **avoid** — creates a custom tab order that's confusing and hard to maintain.

---

## Focus Styles

Browsers show an outline around the focused element. Never do this:

```css
/* DON'T — hides focus from keyboard users */
:focus { outline: none; }
```

If the default focus ring is ugly, replace it — don't remove it:

```css
/* OK — custom style */
:focus-visible {
  outline: 2px solid #0070f3;
  outline-offset: 2px;
}
```

`:focus-visible` only shows on keyboard navigation, not on mouse clicks — best of both worlds.

---

## ARIA — When to Use It

**ARIA (Accessible Rich Internet Applications)** adds accessibility information that HTML alone can't express. It does NOT change visual appearance or behavior — only what assistive technologies see.

The three kinds of ARIA attributes:

| Kind | Example | What it does |
|---|---|---|
| Roles | `role="dialog"` | Tells AT what the element is |
| Properties | `aria-label="Close"` | Gives the element an accessible name or description |
| States | `aria-expanded="true"` | Communicates dynamic state |

---

## Common ARIA Attributes

### Naming elements

```html
<!-- aria-label: use when there's no visible text label -->
<button aria-label="Close dialog">✕</button>

<!-- aria-labelledby: points to an existing element as the label -->
<section aria-labelledby="settings-heading">
  <h2 id="settings-heading">Settings</h2>
  ...
</section>

<!-- aria-describedby: adds extra description (not the name) -->
<input type="password" id="pwd" aria-describedby="pwd-hint" />
<p id="pwd-hint">Must be at least 8 characters.</p>
```

### Dynamic states

```html
<!-- Expanded/collapsed (accordion, dropdown) -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden>...</ul>

<!-- Update aria-expanded with JS when state changes -->

<!-- Hidden from assistive technology (decorative) -->
<img src="decorative-wave.svg" aria-hidden="true" alt="" />
<span aria-hidden="true">👋</span>  <!-- hide emoji from screen readers -->

<!-- Live regions — announce dynamic content changes -->
<div role="status" aria-live="polite">Item saved successfully.</div>
<div role="alert" aria-live="assertive">Error: form submission failed.</div>
```

### Roles

```html
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Delete</h2>
  ...
</div>

<ul role="listbox">
  <li role="option" aria-selected="true">Option A</li>
  <li role="option" aria-selected="false">Option B</li>
</ul>
```

---

## Landmark Regions

Screen readers let users jump between landmark regions. Use these semantic elements (they have implicit roles):

| Element | Implicit role | When to use |
|---|---|---|
| `<header>` | `banner` | Site header (once per page, at top level) |
| `<nav>` | `navigation` | Navigation links — label multiple navs: `aria-label="Main"` |
| `<main>` | `main` | Primary content — one per page |
| `<section>` | `region` (if has accessible name) | Thematic section — add `aria-labelledby` |
| `<aside>` | `complementary` | Sidebar, related links |
| `<footer>` | `contentinfo` | Site footer (at top level) |
| `<form>` | `form` (if has accessible name) | Form region |
| `<search>` | `search` | Search widget (HTML5.2) |

If you have multiple `<nav>` elements, label them:
```html
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Breadcrumb">...</nav>
```

---

## Images and Alt Text

```html
<!-- Informative image — describe what it shows -->
<img src="revenue-chart.png" alt="Bar chart showing Q1 revenue grew 40% over Q4" />

<!-- Decorative image — empty alt, no title -->
<img src="divider.svg" alt="" />

<!-- Image as a link — describe the destination -->
<a href="/home">
  <img src="logo.png" alt="Acme Corp — Home" />
</a>

<!-- Complex image — link to longer description -->
<figure>
  <img src="org-chart.png" alt="Company org chart — see table below for full details" />
  <figcaption>Organization structure as of 2026</figcaption>
</figure>
```

---

## Color and Contrast

Text must meet minimum contrast ratios against its background:

| Size | Minimum ratio (WCAG AA) |
|---|---|
| Normal text (< 18pt / < 14pt bold) | 4.5:1 |
| Large text (≥ 18pt / ≥ 14pt bold) | 3:1 |
| UI components, icons | 3:1 |

**Never convey information by color alone** — always pair color with a second indicator (icon, text, pattern):

```html
<!-- Bad: only color differentiates states -->
<span style="color: red;">Error</span>

<!-- Good: icon + color + text -->
<span>⚠️ Error: Invalid email address</span>
```

---

## Skip Links

For keyboard users, a "skip to main content" link at the top of the page lets them jump past the nav on every page load.

```html
<!-- First element in <body> -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- CSS — visually hidden until focused -->
<style>
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
  }
  .skip-link:focus {
    top: 0;
  }
</style>

<!-- Target -->
<main id="main-content">
  ...
</main>
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `outline: none` on `:focus` | Replace with custom style — never remove the outline |
| Icon buttons with no text | Add `aria-label="Close"` or visually hidden text |
| `<div>` as a button | Use `<button>` — gets keyboard support for free |
| `aria-label` on every element | Only use when native semantics aren't enough |
| Missing alt on images | Always present — empty string for decorative |
| Emoji without hiding | Wrap emoji in `<span aria-hidden="true">` |
| Color-only feedback | Add text or icon alongside color |
| `tabindex="1"` or higher | Creates unpredictable tab order — use `tabindex="0"` or `-1` only |
| Multiple `<h1>` tags | One per page — use `<h2>`–`<h6>` for subsections |

---

## Quick Reference Card

```html
<!-- Skip link (first in body) -->
<a href="#main" class="skip-link">Skip to main content</a>

<!-- Landmarks -->
<header><nav aria-label="Main">...</nav></header>
<main id="main">
  <section aria-labelledby="sec-title">
    <h2 id="sec-title">Section Title</h2>
  </section>
</main>
<footer>...</footer>

<!-- Naming -->
<button aria-label="Close">✕</button>
<input aria-describedby="hint" />
<p id="hint">Helper text.</p>

<!-- States -->
<button aria-expanded="false">Toggle</button>
<div aria-live="polite" role="status">Dynamic message</div>

<!-- Decorative -->
<img src="deco.svg" alt="" aria-hidden="true" />
<span aria-hidden="true">🎉</span>

<!-- Focus -->
<div tabindex="0">Focusable div</div>    <!-- in tab order -->
<div tabindex="-1">JS-only focus</div>   <!-- not in tab order -->
```
