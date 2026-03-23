# 06 — Variables, Transitions & Animations

CSS custom properties (variables) let you define reusable values. Transitions and animations add motion — making interfaces feel polished and communicating state changes.

---

## CSS Custom Properties (Variables)

### Defining and using variables

```css
/* Define on :root — makes them globally available */
:root {
  --color-primary: #0070f3;
  --color-text: #1a1a1a;
  --color-bg: #ffffff;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 32px;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius: 8px;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Use with var() */
.button {
  background: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius);
  font-family: var(--font-sans);
}
```

### Fallback values

```css
/* Second argument is the fallback if the variable isn't defined */
color: var(--color-text, #333);
```

### Scoped variables

Variables inherit — you can override them for a component:

```css
:root {
  --color-primary: #0070f3;
}

.dark-section {
  --color-primary: #60a5fa;  /* different value just for this scope */
}

/* All children of .dark-section use the overridden value */
.dark-section .button {
  background: var(--color-primary);  /* gets #60a5fa */
}
```

### Dark mode with variables

```css
:root {
  --bg: #ffffff;
  --text: #1a1a1a;
  --border: #e2e8f0;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f172a;
    --text: #e2e8f0;
    --border: #1e293b;
  }
}

body {
  background: var(--bg);
  color: var(--text);
}
```

---

## Transitions

Transitions animate a CSS property when it changes (hover, focus, class toggle). They're the simple, reactive animation tool.

### Basic syntax

```css
transition: property duration timing-function delay;

/* Single property */
transition: background-color 200ms ease;

/* Multiple properties */
transition: background-color 200ms ease, transform 150ms ease-out;

/* All properties (use sparingly — can be expensive) */
transition: all 200ms ease;
```

### Timing functions

```css
transition-timing-function: ease;          /* slow → fast → slow (default) */
transition-timing-function: ease-in;       /* slow → fast */
transition-timing-function: ease-out;      /* fast → slow */
transition-timing-function: ease-in-out;   /* slow → fast → slow (smoother than ease) */
transition-timing-function: linear;        /* constant speed */
transition-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);  /* custom curve */
```

### Common patterns

```css
/* Button hover */
.button {
  background: var(--color-primary);
  transition: background-color 150ms ease, transform 100ms ease;
}
.button:hover {
  background: color-mix(in srgb, var(--color-primary), black 15%);
  transform: translateY(-1px);  /* subtle lift */
}
.button:active {
  transform: translateY(0);     /* press down */
}

/* Link underline */
.link {
  text-decoration-color: transparent;
  transition: text-decoration-color 200ms ease;
}
.link:hover {
  text-decoration-color: currentColor;
}

/* Smooth opacity fade */
.overlay {
  opacity: 0;
  transition: opacity 200ms ease;
}
.overlay.visible {
  opacity: 1;
}
```

**Transitions only work between two defined states.** `display: none` ↔ `display: block` can't be transitioned (display isn't animatable). Use `opacity` + `visibility` instead.

---

## `@keyframes` Animations

Animations run independently on a schedule — they don't need a trigger like a hover. Define the animation with `@keyframes`, then apply it with the `animation` property.

### Defining keyframes

```css
/* From/to syntax (simple, start to end) */
@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* Percentage syntax (more control) */
@keyframes slide-in {
  0%   { transform: translateX(-100%); opacity: 0; }
  60%  { transform: translateX(10px); }
  100% { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.05); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
```

### Applying animations

```css
animation: name duration timing-function delay iteration-count direction fill-mode;

.modal {
  animation: fade-in 200ms ease-out;
}

/* Infinite spinner */
.spinner {
  animation: spin 1s linear infinite;
}

/* Pulse, back and forth */
.badge {
  animation: pulse 2s ease-in-out infinite alternate;
}

/* Run once, stay at final state */
.hero {
  animation: slide-in 600ms ease-out forwards;
  /* forwards: element keeps the final keyframe state after animation ends */
}
```

### Animation properties

```css
animation-name: fade-in;
animation-duration: 300ms;
animation-timing-function: ease-out;
animation-delay: 100ms;            /* wait before starting */
animation-iteration-count: 1;      /* or infinite */
animation-direction: normal;       /* normal | reverse | alternate | alternate-reverse */
animation-fill-mode: none;         /* none | forwards | backwards | both */
animation-play-state: running;     /* running | paused — control with JS */
```

---

## Respecting User Motion Preferences

Always wrap decorative animations in a motion query:

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Disable for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation: none;
  }
}
```

Or write it the other way — only animate if motion is OK:

```css
.spinner { /* no animation by default */ }

@media (prefers-reduced-motion: no-preference) {
  .spinner {
    animation: spin 1s linear infinite;
  }
}
```

---

## Performant Animations

The browser can animate some properties cheaply (GPU-accelerated) and others expensively (triggers layout recalculation).

**Cheap to animate (use these):**
- `transform` — translate, scale, rotate, skew
- `opacity`
- `filter`

**Expensive to animate (avoid):**
- `width`, `height`
- `margin`, `padding`
- `top`, `left`, `right`, `bottom`
- `background-color` (OK in small doses, but can't be GPU-accelerated)

```css
/* DON'T — triggers layout on every frame */
.box:hover { width: 200px; }

/* DO — GPU-accelerated */
.box:hover { transform: scaleX(1.2); }
```

`will-change: transform` hints to the browser that an element will animate — it can promote it to its own GPU layer. Use sparingly — only on elements you know will animate, since it uses GPU memory.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `transition: all 200ms` | Be specific — `all` is often wasteful and can animate things you didn't intend |
| `display: none` in a transition | Fade with `opacity` + `visibility`, or use `height: 0` trick |
| No `forwards` fill mode | Animation snaps back to initial state without `animation-fill-mode: forwards` |
| Animating layout properties | Animate `transform`/`opacity` instead |
| No reduced-motion check | Wrap decorative animations in `@media (prefers-reduced-motion: no-preference)` |
| CSS variable in `calc()` without units | Units must be on the number: `calc(var(--spacing) * 2)` — not `var(--spacing-px) * 2` |

---

## Quick Reference Card

```css
/* Variables */
:root {
  --primary: #0070f3;
  --radius: 8px;
  --spacing: 16px;
}
.element { color: var(--primary, fallback); }

/* Transition */
.button {
  transition: background-color 150ms ease, transform 100ms ease;
}
.button:hover { transform: translateY(-2px); }

/* Keyframe animation */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card { animation: fade-in 300ms ease-out forwards; }
.spinner { animation: spin 1s linear infinite; }

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode with variables */
@media (prefers-color-scheme: dark) {
  :root {
    --primary: #60a5fa;
  }
}
```
