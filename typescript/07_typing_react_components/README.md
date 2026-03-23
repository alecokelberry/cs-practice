# 07 — Typing React Components

TypeScript and React work together closely. You type component props, event handlers, hook return values, and ref forwarding. This lesson assumes you know JSX and React basics.

---

## Setup

In `tsconfig.json`:

```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "strict": true
  }
}
```

For Vite + React: `npm create vite@latest my-app -- --template react-ts` gives you everything pre-configured.

---

## Typing Component Props

The most common task: define the shape of what a component receives.

```tsx
// Define props as an interface (preferred for components)
interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
    variant?: "primary" | "secondary" | "danger";
}

function Button({ label, onClick, disabled = false, variant = "primary" }: ButtonProps) {
    return (
        <button onClick={onClick} disabled={disabled} className={variant}>
            {label}
        </button>
    );
}

// Usage
<Button label="Save" onClick={() => save()} />
<Button label="Delete" onClick={handleDelete} variant="danger" disabled={!canDelete} />
```

---

## The `children` Prop

`children` is not included by default — you must add it:

```tsx
import { ReactNode } from "react";

interface CardProps {
    title: string;
    children: ReactNode;  // any valid React content
}

function Card({ title, children }: CardProps) {
    return (
        <div className="card">
            <h2>{title}</h2>
            {children}
        </div>
    );
}

// Usage
<Card title="Settings">
    <p>Update your preferences here.</p>
</Card>
```

`ReactNode` accepts: JSX elements, strings, numbers, arrays, `null`, `undefined`, `boolean`. Use it when you want to accept anything renderable.

Other children types:
- `ReactElement` — a single JSX element (not string, not null)
- `ReactNode` — anything renderable (most flexible, most common)
- `string` — only strings allowed (rare)

---

## Typing Event Handlers

React event types live in `React` namespace or can be imported directly:

```tsx
import { ChangeEvent, MouseEvent, FormEvent, KeyboardEvent } from "react";

interface InputProps {
    value: string;
    onChange: (event: ChangeEvent<HTMLInputElement>) => void;
}

function TextInput({ value, onChange }: InputProps) {
    return <input value={value} onChange={onChange} />;
}
```

### Common event types

```tsx
// Click events
onClick: (e: MouseEvent<HTMLButtonElement>) => void

// Input change
onChange: (e: ChangeEvent<HTMLInputElement>) => void
onChange: (e: ChangeEvent<HTMLTextAreaElement>) => void
onChange: (e: ChangeEvent<HTMLSelectElement>) => void

// Form submit
onSubmit: (e: FormEvent<HTMLFormElement>) => void

// Keyboard
onKeyDown: (e: KeyboardEvent<HTMLInputElement>) => void

// Focus / blur
onFocus: (e: FocusEvent<HTMLInputElement>) => void
onBlur: (e: FocusEvent<HTMLInputElement>) => void
```

The generic parameter (`HTMLButtonElement`, `HTMLInputElement`) is the element type — determines what `e.target` and `e.currentTarget` are.

### Inline handlers (short form)

You usually don't need to annotate inline handlers — TypeScript infers the event type from context:

```tsx
<button onClick={(e) => console.log(e.currentTarget)}>Click</button>
// e is inferred as MouseEvent<HTMLButtonElement>
```

---

## useState

Type inference handles most cases. Annotate when the initial state doesn't reveal the full type:

```tsx
// Inferred — no annotation needed
const [count, setCount] = useState(0);         // number
const [name, setName] = useState("Alice");     // string
const [open, setOpen] = useState(false);       // boolean

// Annotate when initial value doesn't reveal the type
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);
const [status, setStatus] = useState<"idle" | "loading" | "done">("idle");
```

---

## useRef

Two use cases — ref on a DOM element, or a mutable value container:

```tsx
import { useRef } from "react";

// DOM ref — attach to a JSX element
function FocusInput() {
    const inputRef = useRef<HTMLInputElement>(null);  // null is required

    function focus() {
        inputRef.current?.focus();  // current is HTMLInputElement | null
    }

    return <input ref={inputRef} />;
}

// Mutable ref (like an instance variable — doesn't trigger re-render)
function Timer() {
    const intervalRef = useRef<number | null>(null);

    function start() {
        intervalRef.current = setInterval(() => console.log("tick"), 1000);
    }

    function stop() {
        if (intervalRef.current !== null) {
            clearInterval(intervalRef.current);
        }
    }
}
```

---

## useReducer

Type the state and actions explicitly:

```tsx
type State = {
    count: number;
    status: "idle" | "loading" | "error";
};

type Action =
    | { type: "increment" }
    | { type: "decrement" }
    | { type: "setStatus"; payload: State["status"] };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case "increment": return { ...state, count: state.count + 1 };
        case "decrement": return { ...state, count: state.count - 1 };
        case "setStatus": return { ...state, status: action.payload };
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0, status: "idle" });
    // state is State, dispatch accepts Action
}
```

---

## Custom Hooks

Return types are inferred, but it's good practice to type them explicitly for public hooks:

```tsx
interface UseToggleReturn {
    value: boolean;
    toggle: () => void;
    setTrue: () => void;
    setFalse: () => void;
}

function useToggle(initial = false): UseToggleReturn {
    const [value, setValue] = useState(initial);
    return {
        value,
        toggle: () => setValue(v => !v),
        setTrue:  () => setValue(true),
        setFalse: () => setValue(false),
    };
}
```

---

## Generic Components

Components that work with different types of data:

```tsx
interface ListProps<T> {
    items: T[];
    renderItem: (item: T) => ReactNode;
    keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
    return (
        <ul>
            {items.map(item => (
                <li key={keyExtractor(item)}>{renderItem(item)}</li>
            ))}
        </ul>
    );
}

// Usage — TypeScript infers T from items
<List
    items={users}
    renderItem={user => <span>{user.name}</span>}
    keyExtractor={user => String(user.id)}
/>
```

---

## forwardRef

`forwardRef` needs explicit typing because React can't infer the ref type:

```tsx
import { forwardRef } from "react";

interface InputProps {
    label: string;
    placeholder?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ label, placeholder }, ref) => (
        <label>
            {label}
            <input ref={ref} placeholder={placeholder} />
        </label>
    )
);
Input.displayName = "Input";

// Usage
const ref = useRef<HTMLInputElement>(null);
<Input ref={ref} label="Email" />
```

---

## Component Return Types

You rarely need to annotate the return type — TypeScript infers `JSX.Element`. But if needed:

```tsx
import { JSX, ReactElement } from "react";

function Greeting(): JSX.Element {
    return <h1>Hello</h1>;
}

// For components that can return null
function ConditionalBanner(): ReactElement | null {
    if (!shouldShow) return null;
    return <div>Banner</div>;
}
```

---

## Common Pitfalls

**Not including `children` in props**
If you pass children to a component that doesn't declare it in props, TypeScript will error. Always add `children: ReactNode` when you intend to nest content.

**Using `any` for event types**
```tsx
// Wrong — loses all type info
onClick={(e: any) => { ... }}

// Right — use the real event type
onClick={(e: MouseEvent<HTMLButtonElement>) => { ... }}
// or let inference do it inline:
onClick={(e) => { e.preventDefault(); }}  // inferred from context
```

**`useRef<HTMLInputElement>()` without `null`**
For DOM refs, you must pass `null` as the initial value: `useRef<HTMLInputElement>(null)`. Without `null`, `current` is mutable but not automatically assigned when React renders the element.

**Over-typing inline props**
Don't annotate every prop inline — TypeScript infers them from the interface. Just write the interface and destructure.

---

## Quick Reference

```
Props interface
  interface ButtonProps { label: string; onClick: () => void; disabled?: boolean }
  function Button({ label, onClick }: ButtonProps) { ... }

children
  children: ReactNode     -- any renderable content (most common)
  children: ReactElement  -- single JSX element only

Event handler types
  MouseEvent<HTMLButtonElement>
  ChangeEvent<HTMLInputElement>
  FormEvent<HTMLFormElement>
  KeyboardEvent<HTMLInputElement>

useState
  useState(0)                     -- inferred as number
  useState<User | null>(null)     -- annotate when init doesn't reveal type

useRef
  useRef<HTMLInputElement>(null)  -- DOM ref (null required)
  useRef<number | null>(null)     -- mutable value ref

useReducer
  type Action = { type: "inc" } | { type: "dec"; payload: number }
  function reducer(state: State, action: Action): State { ... }

Generic component
  function List<T>({ items, render }: { items: T[]; render: (item: T) => ReactNode }) { ... }

forwardRef
  const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => ...)
```
