# 05 — Structuring a Page

Page structure is about using the right HTML elements to define regions of the page — so browsers, screen readers, search engines, and other developers can understand what each part is for.

---

## Mental Model

A well-structured HTML page is like a newspaper:
- **Banner/header** — masthead with logo and navigation
- **Main content** — the article you're reading
- **Sidebar** — related stories, ads
- **Footer** — small print, links

Each of these maps to a semantic landmark element. A screen reader user can pull up a list of landmarks and jump directly to the one they want.

```
page
├── <header>         ← logo, site-wide nav
├── <nav>            ← breadcrumb or secondary nav
├── <main>           ← the primary content
│   ├── <article>    ← self-contained content (blog post, product)
│   │   ├── <header> ← article title, author, date
│   │   ├── <section> ← part 1 of the article
│   │   └── <section> ← part 2 of the article
│   └── <aside>      ← sidebar: related posts, table of contents
└── <footer>         ← copyright, site links
```

---

## The Landmark Elements

### `<header>`

The introductory content for its parent element. At the page level, it's the site header (logo, nav). Inside an `<article>`, it's the article's header (title, author, date).

```html
<!-- Site header -->
<header>
  <a href="/" aria-label="Acme Corp — Home">
    <img src="/logo.svg" alt="" />
  </a>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/about">About</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>
```

### `<nav>`

A set of navigation links. A page can have multiple `<nav>` elements — label each one:

```html
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/blog">Blog</a></li>
    <li aria-current="page">My Post</li>  <!-- current page indicator -->
  </ol>
</nav>
<nav aria-label="Pagination">...</nav>
```

### `<main>`

The primary content unique to this page. There should be **exactly one** `<main>` per page. Screen readers have a keyboard shortcut to jump directly to it.

```html
<main id="main-content">
  <!-- The page's primary content goes here -->
</main>
```

Give it an `id` so skip links can target it.

### `<section>`

A thematic grouping of content. Always give it a heading — otherwise it's semantically meaningless:

```html
<section aria-labelledby="features-heading">
  <h2 id="features-heading">Features</h2>
  <ul>
    <li>Feature one</li>
    <li>Feature two</li>
  </ul>
</section>
```

Without an accessible name (`aria-labelledby` or `aria-label`), `<section>` doesn't create a landmark region for screen readers.

### `<article>`

Self-contained content that could be lifted out of the page and still make sense: a blog post, a news article, a product card, a comment, a widget. Can be nested (comments within an article).

```html
<article>
  <header>
    <h1>How to Make Coffee</h1>
    <p>By <a href="/authors/alec">Alec</a> · <time datetime="2026-03-18">March 18, 2026</time></p>
  </header>

  <section>
    <h2>Ingredients</h2>
    <p>...</p>
  </section>

  <section>
    <h2>Steps</h2>
    <ol>...</ol>
  </section>

  <footer>
    <p>Tags: <a href="/tag/coffee">coffee</a></p>
  </footer>
</article>
```

### `<aside>`

Content that's tangentially related to the surrounding content — a sidebar, pull quote, related links, or ads.

```html
<aside aria-label="Related posts">
  <h2>You might also like</h2>
  <ul>
    <li><a href="/post-2">Another post</a></li>
  </ul>
</aside>
```

At the page level, `<aside>` maps to the `complementary` landmark role.

### `<footer>`

Closing content for its parent. At the page level, it contains copyright, site links, legal info, social links.

```html
<footer>
  <nav aria-label="Footer links">
    <ul>
      <li><a href="/privacy">Privacy Policy</a></li>
      <li><a href="/terms">Terms of Service</a></li>
    </ul>
  </nav>
  <p>© 2026 Acme Corp. All rights reserved.</p>
</footer>
```

---

## Heading Hierarchy

Headings (`<h1>`–`<h6>`) are a navigation tool for screen reader users who jump between them. Follow these rules:

- One `<h1>` per page — the page's main title
- Don't skip levels (`<h1>` → `<h3>` skips `<h2>`)
- Use heading level to convey outline depth, not visual size
- Use CSS to control visual appearance

```
<h1> Page title
  <h2> Major section
    <h3> Subsection
    <h3> Subsection
  <h2> Another major section
    <h3> Subsection
```

---

## Common Page Layouts

### Blog post

```html
<body>
  <header>
    <a href="/">Logo</a>
    <nav aria-label="Main">...</nav>
  </header>

  <main>
    <article>
      <header>
        <h1>Article Title</h1>
        <p>By Author · <time datetime="2026-03-18">March 18</time></p>
      </header>
      <section>...</section>
      <section>...</section>
    </article>

    <aside>
      <h2>Related</h2>
      ...
    </aside>
  </main>

  <footer>...</footer>
</body>
```

### Landing page

```html
<body>
  <header>
    <nav aria-label="Main">...</nav>
  </header>

  <main>
    <!-- Hero -->
    <section aria-labelledby="hero-heading">
      <h1 id="hero-heading">The headline</h1>
      <p>Subheading</p>
      <a href="/signup">Get started</a>
    </section>

    <!-- Features -->
    <section aria-labelledby="features-heading">
      <h2 id="features-heading">Features</h2>
      <ul>...</ul>
    </section>

    <!-- Testimonials -->
    <section aria-labelledby="testimonials-heading">
      <h2 id="testimonials-heading">What people say</h2>
      ...
    </section>
  </main>

  <footer>...</footer>
</body>
```

### App shell (dashboard)

```html
<body>
  <header>
    <nav aria-label="Top bar">...</nav>
  </header>

  <div class="layout">  <!-- layout div — CSS grid/flex target -->
    <nav aria-label="Sidebar">
      <ul>
        <li><a href="/dashboard" aria-current="page">Dashboard</a></li>
        <li><a href="/reports">Reports</a></li>
      </ul>
    </nav>

    <main>
      <h1>Dashboard</h1>
      ...
    </main>
  </div>
</body>
```

`aria-current="page"` marks the current page in a nav — screen readers announce it.

---

## `<div>` as a Layout Wrapper

`<div>` has no semantic meaning and doesn't appear in the accessibility tree as a landmark. Use it when you need a CSS hook but no semantic meaning:

```html
<!-- Layout wrapper — div is fine here -->
<div class="container">
  <main>...</main>
  <aside>...</aside>
</div>

<!-- Grid layout — div is fine here -->
<div class="card-grid">
  <article class="card">...</article>
  <article class="card">...</article>
</div>
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Multiple `<main>` elements | Only one per page |
| `<section>` without a heading | Add a heading or use `<div>` |
| All `<nav>` elements with no labels | Add `aria-label` to distinguish them |
| Heading levels chosen by size (`<h3>` because it looks right) | Pick level by outline depth, style with CSS |
| `<div>` for everything | Check if a semantic element fits first |
| `<article>` for anything | Use it only for self-contained content that works in isolation |
| Skip link missing | Add `<a href="#main-content" class="skip-link">` as the first element in `<body>` |
| No `id` on `<main>` | Skip links need a target: `<main id="main-content">` |

---

## Quick Reference Card

```html
<body>
  <!-- Skip link (first in body) -->
  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- Page landmarks -->
  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/" aria-current="page">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>

  <nav aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li aria-current="page">Current Page</li>
    </ol>
  </nav>

  <main id="main">
    <article>
      <header>
        <h1>Title</h1>
        <time datetime="2026-03-18">March 18, 2026</time>
      </header>
      <section aria-labelledby="s1">
        <h2 id="s1">Section</h2>
        <p>Content.</p>
      </section>
    </article>

    <aside aria-label="Related">
      <h2>Related</h2>
    </aside>
  </main>

  <footer>
    <p>© 2026 Site Name</p>
  </footer>
</body>
```
