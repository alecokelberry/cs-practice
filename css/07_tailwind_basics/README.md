# 07 — Tailwind Basics

Tailwind is a utility-first CSS framework. Instead of writing CSS classes like `.card { padding: 16px; }`, you apply small single-purpose utility classes directly in HTML: `class="p-4"`. It's the dominant CSS approach in 2026 React/Next.js jobs.

---

## Mental Model

In traditional CSS you write a class name in HTML, then describe it in CSS. In Tailwind, the class *is* the style — the name describes what it does.

```html
<!-- Traditional CSS -->
<button class="btn btn-primary">Click me</button>

<!-- Tailwind -->
<button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
  Click me
</button>
```

This feels verbose at first but it means:
- No naming things
- No switching between files
- No CSS that grows over time and becomes hard to delete
- Styles are local to the element — no accidental side effects

---

## Setup (Next.js / Vite)

```bash
# Next.js (Tailwind is included by default in Next.js 13+)
npx create-next-app@latest

# Existing project with npm
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

In `tailwind.config.js`:
```js
export default {
  content: ["./src/**/*.{js,ts,jsx,tsx,html}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

In your main CSS file:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## The Spacing Scale

Tailwind uses a numeric scale where each unit = 4px (by default):

| Class | Value |
|---|---|
| `p-0` | 0 |
| `p-1` | 4px |
| `p-2` | 8px |
| `p-3` | 12px |
| `p-4` | 16px |
| `p-6` | 24px |
| `p-8` | 32px |
| `p-12` | 48px |
| `p-16` | 64px |

The same scale applies to: `p` (padding), `m` (margin), `gap`, `w` (width), `h` (height), `space-x`, `space-y`.

---

## Core Utility Categories

### Spacing

```html
<!-- Padding -->
<div class="p-4">           <!-- all sides: 16px -->
<div class="px-4 py-2">    <!-- horizontal: 16px, vertical: 8px -->
<div class="pt-2 pb-4">    <!-- top: 8px, bottom: 16px -->

<!-- Margin -->
<div class="m-4">
<div class="mx-auto">      <!-- center horizontally -->
<div class="mt-8 mb-4">

<!-- Gap (flex/grid) -->
<div class="gap-4">
<div class="gap-x-8 gap-y-4">
```

### Sizing

```html
<div class="w-full">       <!-- width: 100% -->
<div class="w-1/2">        <!-- width: 50% -->
<div class="w-64">         <!-- width: 256px (64 × 4) -->
<div class="max-w-lg">     <!-- max-width: 512px -->
<div class="max-w-screen-xl"> <!-- max-width: 1280px -->
<div class="min-w-0">      <!-- prevents flex overflow -->

<div class="h-full">
<div class="h-screen">     <!-- height: 100vh -->
<div class="h-svh">        <!-- height: 100svh (safe, mobile-aware) -->
<div class="min-h-screen">
```

### Flexbox

```html
<div class="flex">
<div class="flex items-center justify-between">
<div class="flex flex-col gap-4">
<div class="flex flex-wrap">
<div class="flex-1">       <!-- flex: 1 1 0 -->
<div class="flex-none">    <!-- flex: none -->
<div class="grow">         <!-- flex-grow: 1 -->
<div class="shrink-0">     <!-- flex-shrink: 0 -->
```

### Grid

```html
<div class="grid grid-cols-3 gap-4">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
<div class="col-span-2">
<div class="col-span-full">
```

### Colors

```html
<!-- Background -->
<div class="bg-white bg-gray-100 bg-blue-600 bg-transparent">

<!-- Text -->
<p class="text-gray-900 text-gray-500 text-blue-600 text-white">

<!-- Border -->
<div class="border border-gray-200 border-blue-500">

<!-- Opacity modifier (Tailwind v3+) -->
<div class="bg-blue-600/80">   <!-- blue-600 at 80% opacity -->
<p class="text-gray-900/60">
```

Tailwind's color palette: slate, gray, zinc, neutral, stone, red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose — each with shades 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950.

### Typography

```html
<p class="text-sm">     <!-- font-size: 14px -->
<p class="text-base">   <!-- font-size: 16px -->
<p class="text-lg">     <!-- font-size: 18px -->
<p class="text-xl">     <!-- font-size: 20px -->
<p class="text-2xl">    <!-- font-size: 24px -->
<p class="text-4xl">    <!-- font-size: 36px -->

<p class="font-normal">   <!-- font-weight: 400 -->
<p class="font-medium">   <!-- font-weight: 500 -->
<p class="font-semibold"> <!-- font-weight: 600 -->
<p class="font-bold">     <!-- font-weight: 700 -->

<p class="leading-tight">  <!-- line-height: 1.25 -->
<p class="leading-normal"> <!-- line-height: 1.5 -->
<p class="leading-relaxed"><!-- line-height: 1.625 -->

<p class="tracking-tight"> <!-- letter-spacing: -0.025em -->
<p class="tracking-wide">  <!-- letter-spacing: 0.025em -->

<p class="text-center text-right text-left">
<p class="truncate">       <!-- overflow: hidden; text-overflow: ellipsis; white-space: nowrap -->
<p class="line-clamp-3">   <!-- limit to 3 lines with ellipsis -->
```

### Borders and Radius

```html
<div class="border">          <!-- 1px border (uses currentColor) -->
<div class="border-2">        <!-- 2px border -->
<div class="border-gray-200"> <!-- border color -->

<div class="rounded">         <!-- border-radius: 4px -->
<div class="rounded-md">      <!-- border-radius: 6px -->
<div class="rounded-lg">      <!-- border-radius: 8px -->
<div class="rounded-xl">      <!-- border-radius: 12px -->
<div class="rounded-full">    <!-- border-radius: 9999px (pill/circle) -->
<div class="rounded-none">    <!-- border-radius: 0 -->
```

### Shadows

```html
<div class="shadow-sm">   <!-- subtle shadow -->
<div class="shadow">      <!-- default shadow -->
<div class="shadow-md">
<div class="shadow-lg">
<div class="shadow-xl">
<div class="shadow-none">
```

### Display and Visibility

```html
<div class="block">
<div class="inline-block">
<div class="hidden">          <!-- display: none -->
<div class="invisible">       <!-- visibility: hidden (keeps space) -->
<div class="overflow-hidden">
<div class="overflow-auto">
<div class="overflow-x-auto">
```

---

## Responsive Prefixes

Tailwind is mobile-first. Prefix any utility with a breakpoint to apply it at that size and above.

| Prefix | Min-width |
|---|---|
| (none) | all sizes |
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

```html
<!-- Stack on mobile, row on tablet -->
<div class="flex flex-col md:flex-row gap-4">

<!-- 1 column mobile, 2 tablet, 3 desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

<!-- Hide on mobile, show on desktop -->
<div class="hidden lg:block">

<!-- Responsive text size -->
<h1 class="text-2xl md:text-4xl lg:text-5xl">
```

---

## State Variants

```html
<!-- Hover -->
<button class="bg-blue-600 hover:bg-blue-700">

<!-- Focus -->
<input class="border focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none">

<!-- Active (pressed) -->
<button class="active:scale-95">

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed">

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">

<!-- First/last child -->
<li class="border-b last:border-b-0">

<!-- Odd/even rows -->
<tr class="bg-white even:bg-gray-50">

<!-- Group hover (hover the parent, style the child) -->
<div class="group">
  <img class="group-hover:scale-105 transition-transform" />
</div>

<!-- Peer (sibling state — input checked/invalid, style adjacent element) -->
<input class="peer" type="checkbox" />
<label class="peer-checked:text-blue-600">Label</label>
```

---

## Arbitrary Values

When no utility covers your exact value, use square brackets:

```html
<div class="w-[350px]">
<div class="top-[117px]">
<div class="bg-[#1da1f2]">
<div class="text-[13px]">
<div class="grid-cols-[240px_1fr]">
<div class="mt-[calc(100vh-80px)]">
```

---

## `@apply` — Extracting Classes

When a pattern repeats too much, extract it to a CSS class using `@apply`:

```css
/* In your CSS file */
@layer components {
  .btn {
    @apply px-4 py-2 rounded font-medium transition-colors;
  }
  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
  }
}
```

```html
<button class="btn btn-primary">Submit</button>
```

Use `@apply` sparingly — it can undermine the point of utility-first CSS. Best for truly reused component patterns.

---

## `tailwind.config.js` — Customization

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eff6ff',
          500: '#0070f3',
          900: '#1e3a5f',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        18: '72px',  /* adds p-18, m-18, etc. */
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
}
```

`extend` adds to Tailwind's defaults. Replacing `theme.colors` (without `extend`) removes all defaults.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Building class names dynamically with JS template literals | Tailwind purges unused classes at build — the full class name must appear as a string somewhere |
| `content` misconfigured | If classes aren't showing up in production, check `content` paths in config |
| Over-using `@apply` | If everything is `@apply`, you lose the benefits of utility-first |
| Forgetting mobile-first order | Add responsive prefixes for larger screens — don't override small screens with `sm:` |
| `dark:` not working | Check `darkMode` in config: `'media'` (system pref) or `'class'` (manual `.dark` class) |

---

## Quick Reference Card

```html
<!-- Layout -->
<div class="flex items-center justify-between gap-4">
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="container mx-auto px-4 max-w-5xl">

<!-- Spacing -->
<div class="p-4 px-6 py-3 mt-8 mb-4 mx-auto">

<!-- Typography -->
<h1 class="text-3xl font-bold tracking-tight text-gray-900">
<p class="text-base leading-relaxed text-gray-600">
<span class="text-sm font-medium text-blue-600">

<!-- Common button -->
<button class="
  bg-blue-600 text-white
  px-4 py-2 rounded-lg
  font-medium
  hover:bg-blue-700
  active:scale-95
  transition-colors
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Button
</button>

<!-- Card -->
<div class="bg-white rounded-xl shadow-md p-6 border border-gray-100">

<!-- Responsive -->
<div class="flex flex-col md:flex-row">
<p class="text-lg md:text-xl lg:text-2xl">
<div class="hidden md:block">

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900">
<p class="text-gray-900 dark:text-white">
```
