# 01 — Box Model & Specificity

Every element on a webpage is a rectangular box. The box model defines how that box is sized. Specificity defines which CSS rule wins when multiple rules target the same element.

---

## Mental Model: The Box Model

```
┌─────────────────────────────────┐  ← margin (outside, transparent)
│  ┌───────────────────────────┐  │
│  │  border                  │  │
│  │  ┌─────────────────────┐ │  │
│  │  │  padding             │ │  │
│  │  │  ┌───────────────┐  │ │  │
│  │  │  │  content      │  │ │  │
│  │  │  └───────────────┘  │ │  │
│  │  └─────────────────────┘ │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

- **Content** — the text, image, or whatever is inside the element
- **Padding** — space between content and the border (inside, background-colored)
- **Border** — the edge line around the padding
- **Margin** — space outside the border (transparent, pushes other elements away)

---

## `box-sizing`

The most important CSS rule to set globally. Controls whether `width`/`height` include padding and border.

```css
/* Default (confusing) — width means content only */
/* box-sizing: content-box */
.box {
  width: 200px;
  padding: 20px;
  border: 2px solid;
  /* total width = 200 + 20 + 20 + 2 + 2 = 244px */
}

/* Better — width means the full visible box */
/* box-sizing: border-box */
.box {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  border: 2px solid;
  /* total width = 200px — padding and border eat into content area */
}
```

**Set globally — always include this at the top of every stylesheet:**

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

---

## Margin, Padding, Border

### Shorthand syntax

```css
/* All four sides */
margin: 20px;

/* Top/bottom, left/right */
margin: 20px 40px;

/* Top, left/right, bottom */
margin: 10px 40px 20px;

/* Top, right, bottom, left (clockwise from top) */
margin: 10px 20px 30px 40px;

/* Individual sides */
margin-top: 10px;
margin-right: 20px;
margin-bottom: 10px;
margin-left: 20px;

/* Same syntax for padding */
padding: 16px;
padding: 8px 16px;
```

### Border

```css
border: 2px solid #333;          /* width style color */
border-top: 1px dashed #ccc;
border-radius: 8px;               /* rounded corners */
border-radius: 50%;               /* circle (on equal width/height) */
border-radius: 4px 8px 4px 8px;  /* clockwise from top-left */
```

### Margin collapse

Top and bottom margins between adjacent block elements **collapse** — only the larger of the two is applied (they don't add up). This only happens vertically, never horizontally.

```css
/* p1 has margin-bottom: 20px, p2 has margin-top: 30px */
/* Space between them = 30px (the larger), NOT 50px */
```

---

## Display

Controls how an element participates in layout.

| Value | Behavior |
|---|---|
| `block` | Takes full width, stacks vertically. `<div>`, `<p>`, `<h1>`, etc. |
| `inline` | Wraps with text, can't set width/height. `<span>`, `<a>`, `<strong>` |
| `inline-block` | Wraps with text, but respects width/height |
| `flex` | Creates a flex container (see lesson 02) |
| `grid` | Creates a grid container (see lesson 03) |
| `none` | Removes element from layout completely (invisible and takes no space) |

---

## The Cascade

CSS stands for *Cascading* Style Sheets. When multiple rules could style the same element, the browser uses this order to decide which wins:

1. **`!important`** — overrides everything (avoid using)
2. **Specificity** — more specific selector wins
3. **Source order** — last rule wins if specificity is equal

---

## Specificity

Each selector has a "score" in three columns: **(id, class/attr/pseudo-class, element/pseudo-element)**.

| Selector | Score | Notes |
|---|---|---|
| `*` | (0,0,0) | Universal selector — zero specificity |
| `p` | (0,0,1) | Element selector |
| `.warning` | (0,1,0) | Class selector |
| `p.warning` | (0,1,1) | Element + class |
| `#header` | (1,0,0) | ID selector |
| `[type="text"]` | (0,1,0) | Attribute selector |
| `:hover` | (0,1,0) | Pseudo-class |
| `::before` | (0,0,1) | Pseudo-element |
| `style="..."` | (1,0,0,0) | Inline style — beats all selectors |
| `!important` | ∞ | Nuclear option — overrides everything |

Higher column wins regardless of the lower columns. `(1,0,0)` beats `(0,99,99)`.

```css
/* Specificity: (0,0,1) */
p { color: black; }

/* Specificity: (0,1,0) — wins over plain p */
.warning { color: orange; }

/* Specificity: (0,1,1) — wins over .warning alone */
p.warning { color: red; }

/* Specificity: (1,0,0) — wins over all of the above */
#alert { color: darkred; }
```

---

## Inheritance

Some CSS properties are **inherited** (child elements get the parent's value automatically):
- `color`, `font-family`, `font-size`, `font-weight`, `line-height`, `text-align`

Others are **not inherited** by default:
- `margin`, `padding`, `border`, `background`, `width`, `height`, `display`

Force inheritance: `color: inherit;`
Reset to default: `color: initial;`
Use browser default: `color: revert;`

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Not setting `box-sizing: border-box` globally | Add `*, *::before, *::after { box-sizing: border-box; }` |
| Overusing `!important` | Fix specificity problems instead — `!important` creates technical debt |
| Confused why margin isn't 50px (collapsed) | Vertical margins between blocks collapse to the larger value — expected behavior |
| ID selectors everywhere (`#header`, `#nav`) | Use classes — IDs are hard to override and can't be reused |
| Setting `display: none` for accessibility hiding | Use `visibility: hidden` (keeps space) or visually-hidden pattern (keeps accessible) |

---

## Visually Hidden Pattern (for a11y)

Hides an element visually but keeps it accessible to screen readers. Better than `display: none` when you still want the element read aloud.

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Quick Reference Card

```css
/* Global reset — always include */
*, *::before, *::after {
  box-sizing: border-box;
}

/* Box model */
.box {
  width: 300px;
  padding: 16px;
  border: 2px solid #333;
  margin: 24px auto;  /* auto centers block elements horizontally */
  border-radius: 8px;
}

/* Shorthand: top right bottom left */
padding: 8px 16px 8px 16px;
margin: 0 auto;        /* 0 top/bottom, auto left/right = center */

/* Specificity: low → high */
p { ... }          /* (0,0,1) */
.class { ... }     /* (0,1,0) */
#id { ... }        /* (1,0,0) */

/* Display */
display: block;
display: inline;
display: inline-block;
display: none;      /* remove from layout */
```
