# 02 — Flexbox

Flexbox is a one-dimensional layout system — it lays items out in a row OR a column. It's the go-to for aligning things and distributing space along a single axis.

---

## Mental Model

Flexbox has two parts: the **container** and the **items** inside it.

```
flex container (display: flex)
┌────────────────────────────────┐
│ ← main axis (row) →           │  ↑
│  [item 1] [item 2] [item 3]   │ cross axis
│                                │  ↓
└────────────────────────────────┘
```

- **Main axis** — the direction flex items flow (default: horizontal/row)
- **Cross axis** — perpendicular to the main axis (default: vertical)
- `justify-content` aligns along the **main axis**
- `align-items` aligns along the **cross axis**

---

## Setting Up a Flex Container

```css
.container {
  display: flex;       /* or inline-flex */
}
```

That's it. All direct children become **flex items** automatically.

---

## Container Properties

### `flex-direction` — which way do items flow?

```css
flex-direction: row;            /* → default: left to right */
flex-direction: row-reverse;    /* ← right to left */
flex-direction: column;         /* ↓ top to bottom */
flex-direction: column-reverse; /* ↑ bottom to top */
```

When you change direction, the main and cross axes swap. If `flex-direction: column`, then `justify-content` aligns vertically and `align-items` aligns horizontally.

### `flex-wrap` — do items wrap to the next line?

```css
flex-wrap: nowrap;    /* default — all items on one line, may overflow */
flex-wrap: wrap;      /* items wrap to next row/column when they run out of space */
flex-wrap: wrap-reverse; /* wraps in reverse direction */
```

### `justify-content` — alignment along the main axis

```css
justify-content: flex-start;     /* items at start (default) */
justify-content: flex-end;       /* items at end */
justify-content: center;         /* items in center */
justify-content: space-between;  /* even gaps between items, no edge gaps */
justify-content: space-around;   /* equal space around each item (half-gaps at edges) */
justify-content: space-evenly;   /* equal space between all items including edges */
```

### `align-items` — alignment along the cross axis (all items)

```css
align-items: stretch;       /* default — items stretch to fill container height */
align-items: flex-start;    /* items at start of cross axis */
align-items: flex-end;      /* items at end of cross axis */
align-items: center;        /* items centered on cross axis */
align-items: baseline;      /* items aligned by their text baseline */
```

### `align-content` — alignment when there are multiple rows/columns (requires `flex-wrap`)

Same values as `justify-content`. Controls spacing between the wrapped rows themselves.

### `gap` — space between items

```css
gap: 16px;           /* same gap between all items (row and column) */
gap: 16px 24px;      /* row-gap column-gap */
row-gap: 16px;
column-gap: 24px;
```

---

## Item Properties

### `flex` — shorthand for grow, shrink, and basis

```css
/* flex: grow shrink basis */
flex: 1;           /* flex: 1 1 0 — grow to fill space, shrink if needed, start at 0 */
flex: auto;        /* flex: 1 1 auto — grow/shrink based on content size */
flex: none;        /* flex: 0 0 auto — don't grow or shrink */
flex: 0 0 200px;   /* fixed 200px, no growing or shrinking */
```

- **`flex-grow`** — how much this item grows relative to others when there's extra space (0 = don't grow, 1 = grow equally)
- **`flex-shrink`** — how much this item shrinks relative to others when there's not enough space (0 = don't shrink)
- **`flex-basis`** — the starting size before growing/shrinking (`auto` uses the item's natural size; `0` ignores content size)

### `align-self` — override cross-axis alignment for one item

```css
align-self: auto;        /* inherit from container's align-items */
align-self: flex-start;
align-self: flex-end;
align-self: center;
align-self: stretch;
```

### `order` — change visual order without changing HTML

```css
order: 0;    /* default */
order: -1;   /* move before items with order 0 */
order: 1;    /* move after items with order 0 */
```

Use sparingly — it can confuse screen reader users who navigate by DOM order.

---

## Common Patterns

### Center anything (horizontally and vertically)

```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### Navigation bar

```css
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}
```

### Equal-width columns

```css
.container {
  display: flex;
  gap: 16px;
}
.column {
  flex: 1;  /* all columns grow equally */
}
```

### Sidebar layout (sidebar fixed, main content fills rest)

```css
.layout {
  display: flex;
  gap: 24px;
}
.sidebar {
  flex: 0 0 240px;  /* fixed 240px, doesn't grow or shrink */
}
.main {
  flex: 1;           /* takes up all remaining space */
}
```

### Push last item to the end

```css
.container {
  display: flex;
}
.spacer {
  flex: 1;  /* grows to fill all available space, pushing next item to end */
}
```

Or with `margin-left: auto` on the last item:

```css
.last-item {
  margin-left: auto;
}
```

### Card row that wraps

```css
.card-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.card {
  flex: 1 1 280px;  /* grow and shrink, but try to be at least 280px wide */
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Flexbox on the parent, but forgetting it only affects direct children | Nested elements need their own `display: flex` |
| Confusing `justify-content` and `align-items` after switching to `column` | When `flex-direction: column`, axes flip — `justify-content` is now vertical |
| Using `width: 50%` on flex items instead of `flex: 1` | `flex: 1` is more flexible and plays well with `gap` |
| `align-content` vs `align-items` | `align-content` only works with multiple rows (needs `flex-wrap: wrap`) |
| `gap` not working | Check that items haven't been given explicit margins that conflict |

---

## Quick Reference Card

```css
/* Container */
.container {
  display: flex;
  flex-direction: row;           /* row | column | row-reverse | column-reverse */
  flex-wrap: nowrap;             /* nowrap | wrap | wrap-reverse */
  justify-content: flex-start;   /* flex-start | center | flex-end | space-between | space-around | space-evenly */
  align-items: stretch;          /* stretch | flex-start | center | flex-end | baseline */
  gap: 16px;
}

/* Items */
.item {
  flex: 1;           /* grow to fill space */
  flex: 0 0 200px;   /* fixed size */
  align-self: center;
  order: 0;
}

/* Center anything */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Push item to far end */
.item:last-child { margin-left: auto; }
```
