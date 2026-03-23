# 05 — Positioning

CSS positioning controls where an element is placed on the page and whether it stays in the normal document flow or breaks out of it.

---

## Mental Model

By default, elements flow one after another — block elements stack vertically, inline elements sit side by side. The `position` property lets you step outside that flow.

Think of it like layers. Normal flow is the base layer. Positioned elements can be lifted off that layer and placed anywhere.

---

## `position` Values

### `static` (default)

The element is in normal document flow. `top`, `right`, `bottom`, `left`, and `z-index` have no effect.

```css
position: static; /* default — no need to declare this */
```

### `relative`

The element stays in normal flow but can be *offset* from where it would normally be. Other elements don't shift to fill the original space.

```css
.nudge {
  position: relative;
  top: 10px;    /* shifts 10px down from its normal position */
  left: 20px;   /* shifts 20px right from its normal position */
}
```

Common use: creating a **containing block** for absolutely positioned children.

### `absolute`

Removed from normal flow entirely. Positioned relative to its **nearest positioned ancestor** (an ancestor with `position` other than `static`). If no such ancestor exists, it's positioned relative to the initial containing block (the `<html>` element).

```css
.parent {
  position: relative; /* creates the containing block */
}

.child {
  position: absolute;
  top: 0;
  right: 0;  /* pinned to top-right corner of parent */
}
```

Other elements flow as if the absolutely positioned element doesn't exist.

### `fixed`

Removed from normal flow. Positioned relative to the **viewport** — stays in place even when you scroll.

```css
.sticky-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}

.modal-overlay {
  position: fixed;
  inset: 0;        /* shorthand for top:0 right:0 bottom:0 left:0 */
  background: rgba(0, 0, 0, 0.5);
}
```

### `sticky`

Hybrid: acts like `relative` within normal flow until it hits the scroll threshold — then it acts like `fixed` and sticks in place.

```css
.sticky-nav {
  position: sticky;
  top: 0;        /* sticks when it reaches 0px from the top of the viewport */
}

th {
  position: sticky;
  top: 0;        /* sticky table headers */
}
```

**Key requirement:** `sticky` only works if the parent is tall enough to scroll past the element. If `overflow: hidden` or `overflow: auto` is on an ancestor, sticky may not work.

---

## `top`, `right`, `bottom`, `left`

These offsets only work on elements with `position` other than `static`.

```css
position: absolute;
top: 20px;      /* 20px from the top edge of the containing block */
right: 20px;    /* 20px from the right edge */
bottom: 0;      /* flush with the bottom */
left: 50%;      /* 50% from the left */
```

**`inset` shorthand:**
```css
inset: 0;            /* top: 0; right: 0; bottom: 0; left: 0 */
inset: 20px 40px;    /* top/bottom: 20px, left/right: 40px */
```

---

## `z-index`

Controls stacking order when positioned elements overlap. Higher value = in front.

```css
.modal   { z-index: 200; }
.overlay { z-index: 100; }
.header  { z-index: 10; }
```

`z-index` only works on positioned elements (not `static`). Elements in the same stacking context compete with each other.

**Stacking contexts** — certain properties create a new stacking context where `z-index` is local:
- `position` + `z-index` (not `auto`)
- `opacity < 1`
- `transform`
- `filter`
- `isolation: isolate`

If a child has `z-index: 9999` but its parent has a lower `z-index` than another element, the child stays behind that other element.

---

## Common Patterns

### Absolutely position a badge/overlay on a card

```html
<div class="card">
  <img src="product.jpg" alt="Product" />
  <span class="badge">Sale</span>
</div>
```

```css
.card {
  position: relative;  /* containing block for badge */
}
.badge {
  position: absolute;
  top: 8px;
  right: 8px;
}
```

### Center an element with absolute positioning

```css
.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);  /* offset by half its own size */
}
```

### Fixed fullscreen modal overlay

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  position: relative;  /* for close button inside */
  z-index: 101;
  background: white;
  padding: 32px;
  border-radius: 8px;
}
```

### Sticky header (disappears on scroll but returns on scroll up — pure CSS)

```css
header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: white;
}
```

### Sticky sidebar (scrolls with page until end of parent)

```css
.sidebar {
  position: sticky;
  top: 24px;  /* sticks 24px from viewport top */
  align-self: start;  /* needed in grid/flex to not stretch to parent height */
}
```

### Tooltip

```css
.tooltip-wrapper {
  position: relative;
  display: inline-block;
}
.tooltip {
  position: absolute;
  bottom: 100%;       /* just above the element */
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
}
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `z-index` not working | Check if `position` is set (not `static`) and if a stacking context is trapping it |
| `position: absolute` going to wrong place | Make sure a parent has `position: relative` to act as the containing block |
| `position: sticky` not sticking | Parent may have `overflow: hidden` — remove it; also ensure the parent is tall enough |
| Fixed navbar covers content | Add `padding-top` to the `<body>` equal to the navbar height |
| Using `position: absolute` for layout | Use Grid or Flexbox for layout; absolute positioning is for overlays and decorations |

---

## Quick Reference Card

```css
/* Static (default — no positioning) */
position: static;

/* Relative — stays in flow, offset from normal position */
.parent { position: relative; }

/* Absolute — out of flow, relative to nearest positioned ancestor */
.badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

/* Fixed — relative to viewport */
.fixed-header {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  z-index: 100;
}

/* Sticky — in flow until scroll threshold */
.sticky-nav {
  position: sticky;
  top: 0;
  z-index: 50;
}

/* Fullscreen overlay */
.overlay {
  position: fixed;
  inset: 0;      /* top: 0; right: 0; bottom: 0; left: 0 */
}

/* Center with absolute */
.centered {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}

/* Isolate stacking context */
.isolated { isolation: isolate; }
```
