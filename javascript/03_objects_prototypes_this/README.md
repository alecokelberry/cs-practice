# 03 — Objects, Prototypes, and `this`

Objects are the fundamental data structure in JavaScript. Understanding how `this` works and how prototypes connect objects is essential for reading and writing class-based code.

---

## Object Literals

```js
// Basic
const user = {
  name: 'Alec',
  age: 22,
  greet() { return `Hi, I'm ${this.name}`; },
};

// Shorthand property (when variable name === key name)
const name = 'Alec';
const age = 22;
const user = { name, age };  // same as { name: name, age: age }

// Computed property names
const key = 'role';
const obj = { [key]: 'admin' };  // { role: 'admin' }

const prefix = 'get';
const obj = {
  [`${prefix}Name`]() { return this.name; },
};
obj.getName();
```

---

## Reading and Writing Properties

```js
// Dot notation
user.name;
user.name = 'Alex';

// Bracket notation — required for dynamic keys or special characters
user['name'];
const field = 'name';
user[field];

// Optional chaining
user?.address?.city;  // undefined instead of throw

// Delete a property
delete user.age;

// Check if a property exists
'name' in user;            // true (checks prototype chain too)
user.hasOwnProperty('name'); // true (own properties only)
Object.hasOwn(user, 'name'); // modern alternative
```

---

## `Object` Static Methods

```js
const user = { name: 'Alec', age: 22, role: 'student' };

// Keys, values, entries
Object.keys(user);    // ['name', 'age', 'role']
Object.values(user);  // ['Alec', 22, 'student']
Object.entries(user); // [['name', 'Alec'], ['age', 22], ['role', 'student']]

// Iterate entries
for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}

// Shallow copy (spread is usually preferred)
const copy = Object.assign({}, user);
const copy = { ...user };

// Merge objects
const merged = Object.assign({}, defaults, overrides);
const merged = { ...defaults, ...overrides };  // later keys win

// Rebuild object from entries
const uppercase = Object.fromEntries(
  Object.entries(user).map(([k, v]) => [k, String(v).toUpperCase()])
);

// Prevent mutation (shallow freeze)
const frozen = Object.freeze({ x: 1, y: 2 });
frozen.x = 99;  // silently fails (throws in strict mode)
```

---

## The Prototype Chain

Every object has an internal `[[Prototype]]` — a reference to another object. When you access a property, JavaScript walks up the chain until it finds it or reaches `null`.

```
myObj → Object.prototype → null
```

```js
const animal = {
  breathe() { return 'breathing'; },
};

const dog = Object.create(animal);  // dog's prototype is animal
dog.bark = function() { return 'woof'; };

dog.bark();     // 'woof'     — own property
dog.breathe();  // 'breathing' — found on prototype
```

In practice, you rarely use `Object.create` directly — **classes** are the modern way to set up prototype chains.

---

## `class` Syntax

`class` is syntactic sugar over prototypes. The behavior is the same under the hood.

```js
class User {
  // Fields (class fields proposal — no var/let/const needed)
  #secret = 'hidden';          // private field (#)
  role = 'user';               // public field

  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  // Method (goes on prototype — shared across all instances)
  greet() {
    return `Hi, I'm ${this.name}`;
  }

  // Getter/setter
  get info() {
    return `${this.name}, ${this.age}`;
  }
  set info(str) {
    [this.name] = str.split(', ');
  }

  // Static method (on the class itself, not instances)
  static create(data) {
    return new User(data.name, data.age);
  }
}

const alec = new User('Alec', 22);
alec.greet();         // 'Hi, I'm Alec'
alec.info;            // 'Alec, 22'
User.create({ name: 'Alec', age: 22 });
```

### Inheritance

```js
class Admin extends User {
  constructor(name, age, permissions) {
    super(name, age);  // must call super() before using this
    this.permissions = permissions;
  }

  greet() {
    return `${super.greet()} (admin)`;  // call parent method
  }
}

const admin = new Admin('Sam', 30, ['read', 'write']);
admin instanceof Admin;  // true
admin instanceof User;   // true — inherits up the chain
```

---

## `this` — Four Binding Rules

`this` is determined at **call time**, not at definition time (except for arrow functions).

### 1. Implicit binding — `this` is the object left of the dot

```js
const user = {
  name: 'Alec',
  greet() { return this.name; },
};
user.greet(); // 'Alec' — this is user
```

### 2. Explicit binding — `call`, `apply`, `bind`

```js
function greet(greeting) {
  return `${greeting}, ${this.name}`;
}

const user = { name: 'Alec' };

greet.call(user, 'Hello');         // 'Hello, Alec'
greet.apply(user, ['Hello']);      // 'Hello, Alec' (args as array)

const boundGreet = greet.bind(user); // returns a new function
boundGreet('Hey');                    // 'Hey, Alec'
```

### 3. `new` binding — `this` is the new object

```js
function User(name) {
  this.name = name;  // this = the new object being created
}
const alec = new User('Alec');
```

### 4. Default binding — `this` is `undefined` (strict mode) or `window`

```js
function show() {
  console.log(this); // undefined in strict mode, window in sloppy
}
show();
```

### Arrow functions — lexical `this`

Arrow functions don't have their own `this`. They capture it from the enclosing scope at definition time.

```js
class Timer {
  constructor() {
    this.count = 0;
  }

  start() {
    // Regular function loses `this` when called by setTimeout
    // setInterval(() => { this.count++; }) works because arrow captures this from start()
    setInterval(() => {
      this.count++;
      console.log(this.count);
    }, 1000);
  }
}
```

**Priority:** `new` > explicit (`bind/call/apply`) > implicit (method call) > default

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| Arrow function as class method | Arrow captures `this` at definition — fine for callbacks, confusing as methods |
| Destructuring a method — `const { greet } = user; greet()` | `this` is lost — bind it first or use arrow |
| `Object.freeze` thinking it's deep | `freeze` is shallow — nested objects can still be mutated |
| `Object.assign` thinking it deep-merges | It's a shallow merge — nested objects get overwritten, not merged |
| `for...in` looping over objects | It includes prototype properties — use `Object.keys()` or `for...of Object.entries()` instead |
| `class` fields set in constructor | Prefer class field syntax (`name = 'default'`) for clarity |

---

## Quick Reference Card

```js
// Object literal + shorthand
const { name, age } = data;
const user = { name, age, greet() { return this.name; } };

// Object methods
Object.keys(obj);
Object.values(obj);
Object.entries(obj);
Object.fromEntries(entries);
const copy = { ...obj };
const merged = { ...defaults, ...overrides };

// Class
class Animal {
  #sound;                          // private field
  static count = 0;               // static field

  constructor(name, sound) {
    this.name = name;
    this.#sound = sound;
    Animal.count++;
  }

  speak() { return `${this.name}: ${this.#sound}`; }
  static getCount() { return Animal.count; }
}

class Dog extends Animal {
  constructor(name) { super(name, 'woof'); }
}

// this binding
fn.call(obj, arg1, arg2);
fn.apply(obj, [arg1, arg2]);
const bound = fn.bind(obj);

// Check
'key' in obj;
Object.hasOwn(obj, 'key');
obj instanceof ClassName;
```
