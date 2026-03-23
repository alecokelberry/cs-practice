# 01 — Basics & Semantic Tags

HTML (HyperText Markup Language) structures the content of a webpage. Tags describe what content *is*, not what it looks like. Appearance is CSS's job.

---

## Mental Model

Think of HTML as the skeleton of a page. Every element is a box. Some boxes contain text, others contain other boxes. The browser reads your tags top to bottom and builds a tree called the **DOM (Document Object Model)**.

```
html
├── head      ← metadata, title, CSS links — not visible on page
└── body      ← everything the user sees
    ├── header
    ├── main
    │   ├── h1
    │   └── p
    └── footer
```

**Semantic tags** tell the browser (and screen readers and search engines) what a piece of content *means*, not just how to display it. `<article>` means "this is a self-contained piece of content." `<div>` means "this is a box with no particular meaning."

---

## The Boilerplate

Every HTML file starts with this:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <!-- content goes here -->
  </body>
</html>
```

| Line | Why it's there |
|---|---|
| `<!DOCTYPE html>` | Tells the browser: "use modern HTML5 rules" |
| `<html lang="en">` | Declares language — used by screen readers and search engines |
| `<meta charset="UTF-8">` | Supports all characters including emoji and accented letters |
| `<meta name="viewport" ...>` | Makes the page responsive on mobile — without this, mobile zooms out |
| `<title>` | Shows in the browser tab and in search results |

---

## Semantic Elements

### Document-level

| Tag | Use it for |
|---|---|
| `<header>` | Site header or section header (logo, nav) |
| `<nav>` | Navigation links |
| `<main>` | The primary content of the page — only one per page |
| `<section>` | A thematic grouping of content with its own heading |
| `<article>` | Self-contained content that makes sense on its own (blog post, comment, card) |
| `<aside>` | Tangentially related content (sidebar, pull quote) |
| `<footer>` | Bottom of page or section (copyright, links) |

### Text content

| Tag | Use it for |
|---|---|
| `<h1>` – `<h6>` | Headings — only one `<h1>` per page, don't skip levels |
| `<p>` | Paragraph |
| `<ul>` / `<ol>` | Unordered / ordered list |
| `<li>` | List item (inside `<ul>` or `<ol>`) |
| `<dl>` / `<dt>` / `<dd>` | Definition list / term / description |
| `<blockquote>` | Long quote from another source |
| `<figure>` / `<figcaption>` | Image or diagram with its caption |

### Inline text

| Tag | Use it for |
|---|---|
| `<strong>` | Important text (bold by default, but the meaning is "important") |
| `<em>` | Emphasized text (italic by default, meaning "stress emphasis") |
| `<code>` | Inline code |
| `<pre>` | Preformatted text (whitespace preserved — wrap `<code>` inside it) |
| `<abbr>` | Abbreviation — use `title` attribute: `<abbr title="HyperText">HTML</abbr>` |
| `<time>` | A date/time — machine-readable: `<time datetime="2026-03-18">March 18</time>` |
| `<mark>` | Highlighted/relevant text |
| `<br>` | Line break (use sparingly — use `<p>` for paragraphs instead) |
| `<hr>` | Thematic break (a horizontal rule) |
| `<span>` | Generic inline container, no meaning (use only when no semantic tag fits) |

### Non-semantic containers

| Tag | Use it for |
|---|---|
| `<div>` | Generic block container — use when no semantic tag fits |
| `<span>` | Generic inline container — use when no semantic tag fits |

Prefer semantic tags. Use `<div>` and `<span>` only as layout wrappers when you need a hook for CSS.

---

## Links and Images

```html
<!-- Link -->
<a href="https://example.com">Link text</a>
<a href="/about">Relative link</a>
<a href="#section-id">Jump to section on same page</a>
<a href="https://example.com" target="_blank" rel="noopener noreferrer">Open in new tab</a>

<!-- Image -->
<img src="dog.jpg" alt="A golden retriever sitting in the sun" />
<img src="logo.svg" alt="Company logo" width="200" height="100" />
```

**`alt` text rules:**
- Describe what the image shows — imagine reading it aloud to someone who can't see it
- For decorative images that add no meaning: `alt=""`  (empty, not missing)
- Never: `alt="image"` or `alt="photo of"`

**`rel="noopener noreferrer"` on `target="_blank"` links** — prevents the opened page from accessing your page via `window.opener`. Always add this.

---

## Lists

```html
<!-- Unordered (bullets) -->
<ul>
  <li>Apples</li>
  <li>Bananas</li>
</ul>

<!-- Ordered (numbers) -->
<ol>
  <li>Preheat oven</li>
  <li>Mix ingredients</li>
</ol>

<!-- Nested list -->
<ul>
  <li>Fruit
    <ul>
      <li>Apple</li>
      <li>Pear</li>
    </ul>
  </li>
</ul>
```

---

## Tables

Use tables for **tabular data** (rows and columns that relate to each other), never for page layout.

```html
<table>
  <caption>Q1 Sales</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>January</td>
      <td>$12,000</td>
    </tr>
    <tr>
      <td>February</td>
      <td>$15,000</td>
    </tr>
  </tbody>
</table>
```

`<th scope="col">` or `scope="row"` helps screen readers understand which header belongs to which data.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Skipping heading levels (`<h1>` → `<h4>`) | Use headings in order; don't skip for visual size — use CSS for that |
| Using `<br>` for spacing | Use CSS margin/padding instead |
| `<b>` and `<i>` instead of `<strong>` and `<em>` | `<b>`/`<i>` are visual only; `<strong>`/`<em>` have meaning |
| Nesting block elements inside inline elements | `<a>` can wrap block elements in HTML5, but `<span>` cannot contain `<div>` |
| Missing `alt` on images | Always include `alt` — empty string `alt=""` for decorative images |
| Using `<div>` for everything | Check if a semantic tag fits first |
| Unclosed tags | Self-closing void tags: `<img />`, `<br />`, `<input />` |

---

## Quick Reference Card

```html
<!-- Document structure -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Title</title>
  </head>
  <body>
    <header>...</header>
    <nav>...</nav>
    <main>
      <section>
        <h1>Heading</h1>
        <p>Paragraph <strong>important</strong> <em>emphasis</em></p>
      </section>
      <article>...</article>
    </main>
    <aside>...</aside>
    <footer>...</footer>
  </body>
</html>

<!-- Link / image -->
<a href="/page">Link</a>
<img src="img.jpg" alt="Description" />

<!-- Lists -->
<ul><li>Item</li></ul>
<ol><li>Step</li></ol>
```
