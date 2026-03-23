# 04 — Meta Tags & SEO

Meta tags live in `<head>` and communicate information about your page to browsers, search engines, and social media platforms. They're invisible to users but affect how your page appears in Google, how it looks when shared, and how it behaves on mobile.

---

## Mental Model

The `<head>` is the instruction set for your page — not content, but metadata about the content. Search engines and social platforms read it to build their previews. The browser reads it to know how to render correctly.

```
<head>
  charset → how to decode the file
  viewport → how to scale on mobile
  title → tab name + search result headline
  description → search result snippet
  og:image → social share preview card
  canonical → which URL is "the real one"
  robots → what search engines are allowed to do
</head>
```

---

## Required Tags (Always Include)

```html
<head>
  <!-- Character encoding — always first in <head> -->
  <meta charset="UTF-8" />

  <!-- Mobile scaling — required or mobile browsers zoom out -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Page title — shows in tab, browser history, and search results -->
  <title>Page Title | Site Name</title>
</head>
```

These three are non-negotiable for any real page.

---

## SEO Meta Tags

Search engines use these to decide what to show in results.

```html
<!-- Search result snippet — 150–160 characters ideal -->
<meta name="description" content="A clear, specific description of what this page is about. Shows under the title in search results." />

<!-- Tell crawlers what to do -->
<meta name="robots" content="index, follow" />        <!-- default behavior -->
<meta name="robots" content="noindex, nofollow" />    <!-- don't show in search, don't follow links -->
<meta name="robots" content="noindex, follow" />      <!-- follow links, but don't index this page -->
```

**`description` best practices:**
- Unique on every page — never duplicate across pages
- 150–160 characters (Google may truncate longer descriptions)
- Include relevant keywords naturally — don't keyword-stuff
- Write for humans, not just bots

**`robots` defaults to `index, follow`** — only add it if you need to restrict something.

---

## Canonical URL

Tells search engines which URL is the "official" version of this page. Prevents duplicate content penalties.

```html
<!-- On every page, pointing to itself -->
<link rel="canonical" href="https://example.com/blog/my-post" />

<!-- On paginated pages, pointing to the first page -->
<link rel="canonical" href="https://example.com/products" />
```

When to use:
- Your page is accessible at multiple URLs (`/page`, `/page?ref=twitter`)
- You have paginated content (`/blog/page/2`)
- You have `http://` and `https://` versions

---

## Open Graph (Social Share Cards)

When someone shares your URL on Slack, Twitter/X, LinkedIn, or iMessage, the platform fetches Open Graph tags to build a preview card.

```html
<!-- Required OG tags -->
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Description shown in the preview card." />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta property="og:url" content="https://example.com/this-page" />
<meta property="og:type" content="website" />  <!-- or "article" for blog posts -->

<!-- Optional but recommended -->
<meta property="og:site_name" content="Site Name" />
<meta property="og:locale" content="en_US" />
```

**OG image guidelines:**
- Minimum: 1200×630px
- Ratio: 1.91:1 (landscape)
- Max file size: ~8MB, ideally under 1MB
- Use an absolute URL — not a relative path

---

## Twitter Card Tags

Twitter uses its own tags (though it falls back to OG if these are missing):

```html
<meta name="twitter:card" content="summary_large_image" />  <!-- or "summary" for small image -->
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Description." />
<meta name="twitter:image" content="https://example.com/image.jpg" />
<meta name="twitter:site" content="@yourtwitterhandle" />
```

If you already have OG tags, Twitter will use them. The Twitter tags let you customize further.

---

## Favicon

```html
<!-- Modern approach — SVG scales to any size -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />

<!-- Fallback for older browsers -->
<link rel="icon" href="/favicon.ico" sizes="any" />

<!-- iOS home screen icon -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
```

Favicons appear in browser tabs, bookmarks, and home screens.

---

## Other Useful Tags

```html
<!-- Theme color — colors the browser chrome on mobile (Chrome, Edge) -->
<meta name="theme-color" content="#0070f3" />

<!-- Author -->
<meta name="author" content="Alec Kelberry" />

<!-- Language (also set on <html lang="en">) -->
<meta http-equiv="content-language" content="en" />

<!-- Refresh/redirect (avoid — use server-side or JS instead) -->
<meta http-equiv="refresh" content="5; url=https://example.com/new-page" />

<!-- Disable phone number auto-detection on iOS -->
<meta name="format-detection" content="telephone=no" />
```

---

## Structured Data (JSON-LD)

Goes in `<head>` or `<body>`. Tells Google the semantic meaning of your content, enabling "rich results" (star ratings, FAQs, event info in search results).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Learn HTML",
  "author": {
    "@type": "Person",
    "name": "Alec Kelberry"
  },
  "datePublished": "2026-03-18"
}
</script>
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Missing `viewport` meta | Mobile browsers zoom way out — add it to every page |
| Same `description` on every page | Write unique descriptions — duplicate descriptions are flagged by Google |
| Relative URL in `og:image` | Must be an absolute URL with domain |
| `<title>` too long | Keep under 60 characters or Google truncates it |
| Missing `<title>` | Page shows as "Untitled" in tabs and "No title" in search |
| No canonical on paginated pages | Causes duplicate content issues |
| `charset` not first in `<head>` | Can cause character rendering issues — always put it first |

---

## Full `<head>` Template

```html
<head>
  <!-- Required -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title | Site Name</title>

  <!-- SEO -->
  <meta name="description" content="150-160 char description of this specific page." />
  <link rel="canonical" href="https://example.com/this-page" />

  <!-- Open Graph -->
  <meta property="og:title" content="Page Title" />
  <meta property="og:description" content="Description for social shares." />
  <meta property="og:image" content="https://example.com/og.jpg" />
  <meta property="og:url" content="https://example.com/this-page" />
  <meta property="og:type" content="website" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />

  <!-- Favicon -->
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <!-- Theme -->
  <meta name="theme-color" content="#0070f3" />

  <!-- Styles -->
  <link rel="stylesheet" href="/styles.css" />
</head>
```
