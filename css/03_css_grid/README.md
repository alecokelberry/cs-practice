# 03 — CSS Grid

CSS Grid is a two-dimensional layout system — it handles rows AND columns simultaneously. Use Grid for overall page layout and complex two-dimensional arrangements. Use Flexbox for one-dimensional alignment within those sections.

---

## Mental Model

Grid divides a container into a table-like structure of rows and columns. Items are placed into cells (or span multiple cells).

```
grid container
┌────────────┬────────────┬────────────┐
│            │            │            │  row 1
│  item 1    │  item 2    │  item 3    │
├────────────┼────────────┼────────────┤
│            │                         │  row 2
│  item 4    │   item 5 (spans 2 cols) │
└────────────┴────────────┴────────────┘
     col 1        col 2        col 3
```

Grid lines are numbered starting at 1. The space between lines is a "track" (column track or row track).

---

## Setting Up a Grid

```css
.container {
  display: grid;
}
```

Without more properties, this just stacks items — you need to define columns and/or rows.

---

## Defining Columns and Rows

```css
/* 3 columns, each 1fr wide */
grid-template-columns: 1fr 1fr 1fr;

/* shorthand with repeat() */
grid-template-columns: repeat(3, 1fr);

/* fixed + flexible columns (sidebar layout) */
grid-template-columns: 240px 1fr;

/* named sizes */
grid-template-columns: 240px 1fr minmax(200px, 3fr);

/* Rows — usually let content drive row height */
grid-template-rows: auto;          /* default */
grid-template-rows: 80px 1fr auto; /* header, main, footer */
```

**`fr` unit** — a "fraction" of the remaining available space. `1fr 1fr 1fr` means three equal columns.

**`minmax(min, max)`** — tracks that can grow and shrink within a range:
```css
grid-template-columns: repeat(3, minmax(200px, 1fr));
```

---

## `auto-fill` vs `auto-fit`

Used with `repeat()` to automatically create as many tracks as fit:

```css
/* auto-fill: fill as many columns as fit, keep empty tracks */
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

/* auto-fit: fill as many columns as fit, collapse empty tracks */
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
```

For responsive card grids, `auto-fit` with `minmax` is the go-to pattern — no media queries needed.

---

## Gap

```css
gap: 16px;           /* same gap between rows and columns */
gap: 16px 24px;      /* row-gap column-gap */
row-gap: 16px;
column-gap: 24px;
```

---

## Placing Items

By default, grid items auto-place in order. You can override:

```css
.item {
  /* Column: start-line / end-line */
  grid-column: 1 / 3;        /* spans from line 1 to line 3 (2 columns) */
  grid-column: 1 / span 2;   /* span 2 columns from line 1 */
  grid-column: span 2;       /* span 2 columns wherever auto-placed */

  /* Row: start-line / end-line */
  grid-row: 1 / 3;           /* spans 2 rows */
  grid-row: span 2;

  /* Shorthand: row-start / column-start / row-end / column-end */
  grid-area: 1 / 1 / 3 / 3;
}
```

---

## Named Grid Areas

The most readable way to define complex layouts:

```css
.container {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main   main  "
    "footer  footer footer";
  grid-template-columns: 240px 1fr 1fr;
  grid-template-rows: auto 1fr auto;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

Use `.` for an empty cell in the template.

---

## Alignment

Grid has both container-level and item-level alignment.

### Container alignment (all items)

```css
/* Aligns items along the row axis (inline/horizontal) */
justify-items: stretch;    /* default — fills cell width */
justify-items: start;
justify-items: center;
justify-items: end;

/* Aligns items along the column axis (block/vertical) */
align-items: stretch;      /* default — fills cell height */
align-items: start;
align-items: center;
align-items: end;

/* Aligns the grid tracks within the container */
justify-content: start;    /* when grid is smaller than container */
align-content: center;
```

### Item alignment (individual items)

```css
.item {
  justify-self: center;   /* override horizontal alignment for this item */
  align-self: end;        /* override vertical alignment for this item */
}
```

---

## Common Patterns

### Responsive card grid (no media queries)

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
```

### Classic page layout (header, sidebar, main, footer)

```css
.layout {
  display: grid;
  grid-template-areas:
    "header  header"
    "sidebar main  "
    "footer  footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
```

### Fixed number of equal columns

```css
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
```

### Centered, max-width content

```css
.container {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr;
}
.container > * {
  grid-column: 2;  /* content in center column */
}
.full-bleed {
  grid-column: 1 / -1;  /* -1 = last grid line */
}
```

---

## Grid vs Flexbox — When to Use Which

| Situation | Use |
|---|---|
| Overall page structure (header/sidebar/main/footer) | Grid |
| Responsive card/image gallery | Grid |
| Items aligned in one direction (nav links, button groups) | Flexbox |
| Centering one item | Flexbox |
| Unknown number of items in a row | Flexbox with wrap |
| Items that need to align across rows AND columns | Grid |

They work great together. Grid for the macro layout, Flexbox inside each grid cell.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Confusing `fr` and `auto` | `1fr` takes equal share of remaining space; `auto` sizes to content |
| Using `grid-column: 1/3` when you have 2 columns (expecting to span all) | `1/3` means line 1 to line 3 — with 2 columns there are 3 lines, so this works, but use `1/-1` to always span all |
| Forgetting `gap` vs `margin` | Prefer `gap` — it doesn't add space at the outer edges |
| Using Grid when Flexbox is simpler | Grid has more syntax; if you just need a row of items, use Flexbox |

---

## Quick Reference Card

```css
/* Basic grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* Responsive auto-fit */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

/* Named areas */
.layout {
  display: grid;
  grid-template-areas:
    "header"
    "main  "
    "footer";
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
.header { grid-area: header; }
.main   { grid-area: main; }
.footer { grid-area: footer; }

/* Item placement */
.span-2 { grid-column: span 2; }
.full   { grid-column: 1 / -1; }

/* Centering */
.cell { place-items: center; }  /* shorthand: align-items + justify-items */
```
