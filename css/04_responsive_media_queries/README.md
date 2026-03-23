# 04 — Responsive Design & Media Queries

Responsive design makes a website look good at any screen size. Media queries let you apply different CSS depending on the device's screen width, height, orientation, or capabilities.

---

## Mental Model

Think of responsive design as a single codebase that adapts. You write CSS that works at small sizes, then use media queries to upgrade the layout for larger screens.

```
320px ── mobile ──── 768px ── tablet ──── 1024px ──── desktop ────▶
   ↑                     ↑                    ↑
base styles          breakpoint            breakpoint
(no query)           (md)                  (lg)
```

**Mobile-first** means your default styles (no media query) target small screens, and you add media queries to handle larger screens. This is the modern standard.

---

## Basic Media Query Syntax

```css
/* Applies only when viewport is at least 768px wide */
@media (min-width: 768px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Applies only when viewport is at most 767px wide */
@media (max-width: 767px) {
  .nav { display: none; }
}
```

---

## Mobile-First vs Desktop-First

### Mobile-first (preferred)

Write base styles for mobile. Add `min-width` queries to override for larger screens.

```css
/* Base: mobile */
.nav {
  display: flex;
  flex-direction: column;
}

/* Tablet and up */
@media (min-width: 768px) {
  .nav {
    flex-direction: row;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .nav {
    justify-content: space-between;
  }
}
```

**Why mobile-first?**
- Mobile browsers are slower — small screens get less CSS to parse
- Forces you to think about core content first
- Easier to progressively enhance than to subtract

### Desktop-first (legacy pattern)

Writes for large screens first, uses `max-width` to scale down. You'll see this in older codebases.

```css
/* Base: desktop */
.nav { flex-direction: row; }

/* Tablet and below */
@media (max-width: 1023px) {
  .nav { flex-direction: column; }
}
```

---

## Common Breakpoints

There's no single right answer. These are popular reference points (not Tailwind-specific):

| Name | Width | Typical use |
|---|---|---|
| `sm` | 640px | Large phones / small tablets |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large monitors |

You don't need to use all of them. Design-driven breakpoints (where the layout *breaks*) are often better than size-driven ones.

---

## Multiple Conditions

```css
/* AND — both must be true */
@media (min-width: 768px) and (max-width: 1023px) {
  /* tablet range only */
}

/* OR — either must be true */
@media (max-width: 767px), (orientation: portrait) {
  /* mobile or portrait */
}

/* NOT */
@media not (min-width: 768px) {
  /* same as max-width: 767px */
}
```

---

## Other Media Features

```css
/* Orientation */
@media (orientation: portrait)  { ... }
@media (orientation: landscape) { ... }

/* High-DPI screens (retina) */
@media (min-resolution: 2dppx)  { ... }
@media (-webkit-min-device-pixel-ratio: 2) { ... }  /* safari compat */

/* Hover capability — touch devices usually can't hover */
@media (hover: hover) {
  .button:hover { background: #ddd; }
}
@media (hover: none) {
  /* touch-only styles */
}

/* Pointer precision */
@media (pointer: fine)   { ... }  /* mouse */
@media (pointer: coarse) { ... }  /* touch */

/* User preferences */
@media (prefers-color-scheme: dark)  { ... }
@media (prefers-color-scheme: light) { ... }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Responsive Units

Instead of fixed `px`, use relative units to scale naturally:

| Unit | Relative to | Use case |
|---|---|---|
| `%` | Parent element's dimension | Widths in fluid layouts |
| `em` | Parent element's font-size | Scaling components relative to text |
| `rem` | Root (`<html>`) font-size | Consistent spacing/sizing across the page |
| `vw` | 1% of viewport width | Full-width sections, fluid typography |
| `vh` | 1% of viewport height | Full-height sections |
| `svh` | 1% of small viewport height | Safer `100vh` on mobile (excludes browser chrome) |
| `ch` | Width of the "0" character | Text column widths |
| `min()` | Smallest of the values | `width: min(100%, 600px)` |
| `max()` | Largest of the values | `font-size: max(16px, 2vw)` |
| `clamp()` | Clamped between min and max | Fluid typography |

### Fluid typography with `clamp()`

```css
/* Font scales from 16px to 24px between 320px and 1200px viewport */
font-size: clamp(1rem, 0.5rem + 2vw, 1.5rem);
/* clamp(minimum, preferred, maximum) */
```

---

## Responsive Images

```css
/* Never let an image overflow its container */
img {
  max-width: 100%;
  height: auto;
}
```

```html
<!-- srcset: browser picks the right image for the display density -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1600.jpg 1600w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Description"
/>

<!-- <picture>: art direction — different images at different sizes -->
<picture>
  <source srcset="hero-wide.jpg" media="(min-width: 768px)" />
  <img src="hero-tall.jpg" alt="Hero image" />
</picture>
```

---

## Common Patterns

### Responsive container

```css
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;  /* center horizontally */
}
```

### Stack to row

```css
.card-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 768px) {
  .card-group {
    flex-direction: row;
  }
}
```

### Hide on mobile, show on desktop

```css
.desktop-only { display: none; }

@media (min-width: 1024px) {
  .desktop-only { display: block; }
}
```

### Responsive grid (no media queries needed)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Missing `viewport` meta tag | Mobile browsers zoom out without `<meta name="viewport">` |
| Too many breakpoints | Start with 2–3; add more only if the layout breaks |
| Fixed `px` widths | Use `%`, `min()`, or `fr` for flexible widths |
| `100vh` on mobile | Use `100svh` to avoid the address bar covering content |
| `max-width` everywhere (desktop-first) | Switch to mobile-first with `min-width` |
| No `prefers-reduced-motion` check | Animations can cause issues for users with vestibular disorders |

---

## Quick Reference Card

```css
/* Mobile-first breakpoints */
/* Base styles: mobile */
.thing { flex-direction: column; }

@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ .thing { flex-direction: row; } }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }

/* Responsive container */
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

/* Fluid type */
font-size: clamp(1rem, 0.5rem + 2vw, 1.5rem);

/* Preferences */
@media (prefers-color-scheme: dark)   { ... }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Responsive image */
img { max-width: 100%; height: auto; }
```
