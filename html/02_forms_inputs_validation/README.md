# 02 — Forms, Inputs & Validation

HTML forms collect data from users. Browsers provide a lot of built-in behavior for free — validation, keyboard navigation, mobile keyboard types — as long as you use the right tags and attributes.

---

## Mental Model

A form is a container that groups related inputs together. When the user submits, the browser packages up all the named fields and sends them somewhere (a URL via `action`, or handled by JavaScript).

```
<form>
  label + input  ← one pair per field
  label + input
  label + select
  <button type="submit">
</form>
```

**Always pair every input with a `<label>`.** This is the single most important rule for both accessibility and usability.

---

## The `<form>` Element

```html
<form action="/submit" method="POST">
  <!-- inputs here -->
</form>
```

| Attribute | Values | Purpose |
|---|---|---|
| `action` | URL or path | Where to send data on submit. Omit if handled by JS. |
| `method` | `GET`, `POST` | `GET` puts data in the URL. `POST` sends it in the request body. Use `POST` for sensitive data. |
| `novalidate` | (boolean) | Disables built-in browser validation (useful when you handle it in JS) |

---

## Labels

```html
<!-- Option 1: label wraps the input (implicit association) -->
<label>
  Email
  <input type="email" name="email" />
</label>

<!-- Option 2: label points to input by id (explicit association) — preferred -->
<label for="email">Email</label>
<input type="email" id="email" name="email" />
```

Why labels matter:
- Clicking the label focuses the input — bigger tap target
- Screen readers announce the label when the input is focused
- Without a label, screen reader users hear "edit text" with no context

---

## Input Types

The `type` attribute controls what keyboard appears on mobile, what validation runs, and how the browser renders the input.

```html
<input type="text" />        <!-- default, single line -->
<input type="email" />       <!-- validates email format, shows email keyboard on mobile -->
<input type="password" />    <!-- hides characters -->
<input type="number" />      <!-- numeric keyboard, min/max/step attributes -->
<input type="tel" />         <!-- phone keyboard on mobile (no format validation) -->
<input type="url" />         <!-- validates URL format -->
<input type="search" />      <!-- search semantics, shows search keyboard -->
<input type="date" />        <!-- date picker -->
<input type="time" />        <!-- time picker -->
<input type="datetime-local" /> <!-- date + time picker -->
<input type="checkbox" />    <!-- true/false toggle -->
<input type="radio" />       <!-- one-of-many choice -->
<input type="range" />       <!-- slider -->
<input type="color" />       <!-- color picker -->
<input type="file" />        <!-- file upload -->
<input type="hidden" />      <!-- not shown, but submitted with form -->
<input type="submit" />      <!-- submit button (use <button> instead) -->
```

---

## Common Input Attributes

```html
<input
  type="email"
  id="email"
  name="email"
  placeholder="you@example.com"
  value=""
  required
  autocomplete="email"
  disabled
  readonly
  minlength="3"
  maxlength="100"
/>
```

| Attribute | What it does |
|---|---|
| `name` | The key sent with the form data — required for the value to be submitted |
| `id` | Connects to `<label for="...">` — for accessibility |
| `placeholder` | Hint text shown when empty — not a substitute for a label |
| `value` | Default/initial value |
| `required` | Browser refuses to submit if empty |
| `disabled` | Grayed out, not interactive, not submitted |
| `readonly` | Visible, not editable, but still submitted |
| `autocomplete` | Hints browser autocomplete: `"email"`, `"name"`, `"off"`, etc. |
| `autofocus` | Focuses this input when the page loads |
| `min` / `max` | For number/date inputs |
| `minlength` / `maxlength` | Min/max character count for text inputs |
| `pattern` | Regex the value must match: `pattern="[0-9]{5}"` |
| `step` | For number/range: increment size |

---

## Built-in Validation Attributes

```html
<!-- Required field -->
<input type="text" name="username" required />

<!-- Email format -->
<input type="email" name="email" required />

<!-- Number range -->
<input type="number" name="age" min="18" max="120" />

<!-- Min/max length -->
<input type="password" name="password" minlength="8" maxlength="128" />

<!-- Custom pattern (5-digit ZIP code) -->
<input type="text" name="zip" pattern="[0-9]{5}" title="5-digit ZIP code" />
```

When validation fails, the browser shows its own error UI (tooltip). The `title` attribute provides extra context in some browsers.

---

## Checkboxes and Radio Buttons

```html
<!-- Checkbox (independent true/false) -->
<label>
  <input type="checkbox" name="newsletter" value="yes" checked />
  Subscribe to newsletter
</label>

<!-- Radio buttons (one choice from a group — same name, different values) -->
<fieldset>
  <legend>Preferred contact method</legend>

  <label>
    <input type="radio" name="contact" value="email" checked />
    Email
  </label>

  <label>
    <input type="radio" name="contact" value="phone" />
    Phone
  </label>
</fieldset>
```

**Radio buttons must share the same `name` attribute** to form a group where only one can be selected.

`<fieldset>` + `<legend>` groups related inputs and labels the group — important for accessibility.

---

## Select (Dropdown)

```html
<label for="country">Country</label>
<select id="country" name="country">
  <option value="">-- Select a country --</option>
  <option value="us">United States</option>
  <option value="ca">Canada</option>
  <option value="uk" selected>United Kingdom</option>
</select>

<!-- Group options with optgroup -->
<select name="car">
  <optgroup label="American">
    <option value="ford">Ford</option>
    <option value="chevy">Chevrolet</option>
  </optgroup>
  <optgroup label="Japanese">
    <option value="toyota">Toyota</option>
  </optgroup>
</select>

<!-- Multiple selections -->
<select name="skills" multiple size="4">
  <option value="html">HTML</option>
  <option value="css">CSS</option>
  <option value="js">JavaScript</option>
</select>
```

---

## Textarea

```html
<label for="message">Message</label>
<textarea
  id="message"
  name="message"
  rows="5"
  cols="40"
  placeholder="Write your message..."
  maxlength="500"
></textarea>
```

Note: `<textarea>` has no `value` attribute — the default content goes between the tags.

---

## Buttons

```html
<!-- Submit the form -->
<button type="submit">Send</button>

<!-- Reset all inputs to their default values (rarely useful, often annoying) -->
<button type="reset">Reset</button>

<!-- Does nothing by default — use for JS-driven actions inside a form -->
<button type="button" onclick="doSomething()">Click Me</button>
```

Always specify `type` on buttons inside forms. Without it, the default is `type="submit"` — which can cause accidental form submissions.

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Missing `<label>` | Every input needs a label — screen readers and usability depend on it |
| Using `placeholder` as a label | Placeholder disappears on focus — always have a real `<label>` |
| Radio buttons with different `name` values | They won't behave as a group — give them all the same `name` |
| `<button>` without `type` inside a form | Defaults to `type="submit"` — add `type="button"` for non-submit buttons |
| `<input type="submit">` instead of `<button>` | `<button>` is more flexible and styleable |
| Missing `for`/`id` pairing | Label click won't focus input, screen reader won't announce label |
| `name` attribute missing | Input won't be included in form submission data |

---

## Quick Reference Card

```html
<!-- Form shell -->
<form action="/submit" method="POST">

  <!-- Text inputs -->
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required />

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required autocomplete="email" />

  <label for="pass">Password</label>
  <input type="password" id="pass" name="password" minlength="8" required />

  <!-- Dropdown -->
  <label for="role">Role</label>
  <select id="role" name="role">
    <option value="">-- Pick one --</option>
    <option value="dev">Developer</option>
    <option value="designer">Designer</option>
  </select>

  <!-- Textarea -->
  <label for="msg">Message</label>
  <textarea id="msg" name="message" rows="4"></textarea>

  <!-- Checkbox -->
  <label>
    <input type="checkbox" name="agree" value="yes" required />
    I agree to the terms
  </label>

  <!-- Radio group -->
  <fieldset>
    <legend>Plan</legend>
    <label><input type="radio" name="plan" value="free" checked /> Free</label>
    <label><input type="radio" name="plan" value="pro" /> Pro</label>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```
