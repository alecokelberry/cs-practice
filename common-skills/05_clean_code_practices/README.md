# 05 — Clean Code Practices

Clean code isn't about aesthetics — it's about maintainability. Code is read far more often than it's written. Clear code reduces bugs, speeds up collaboration, and makes future-you grateful.

---

## Mental Model

Code has two audiences: the computer (which runs it) and humans (who read and change it). The computer doesn't care how readable your code is. The humans do — and you are one of them.

> "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live." — Martin Golding

The core question to ask about any piece of code: **could someone unfamiliar with this codebase understand what it does and why in under a minute?**

---

## Naming

Good names are the cheapest and most impactful thing you can do for readability.

### Name things for what they are, not how they're implemented

```python
# Bad — describes the implementation
user_list = get_all_users()
temp = calculate_total(items)
flag = True
d = 7

# Good — describes what the value means
users = get_all_users()
total_price = calculate_total(items)
is_logged_in = True
days_until_expiry = 7
```

### Functions: verb phrases that describe the action

```python
# Bad — noun, unclear what it does
def user(id): ...
def data(items): ...

# Good — clear intent
def get_user(id): ...
def filter_expired_items(items): ...
def send_welcome_email(user): ...
def calculate_monthly_revenue(orders): ...
```

### Booleans: use `is_`, `has_`, `can_`, `should_` prefixes

```python
# Bad
active = True
permission = False
email = True

# Good
is_active = True
has_admin_permission = False
has_verified_email = True
```

### Don't abbreviate unless it's a universally understood convention

```python
# Bad — what does 'u', 'p', 'n' mean?
def calc(u, p, n):
    return u * p * n

# Good
def calculate_total_cost(unit_price, quantity, num_units):
    return unit_price * quantity * num_units

# Acceptable abbreviations
i, j, k   # loop indices
x, y, z   # coordinates
n         # count/number (in algorithms)
e         # exception
```

### Avoid noise words that add nothing

```python
# Bad — 'Info', 'Data', 'Manager', 'Handler' add no meaning
user_info = get_user_data_info()
account_manager = AccountDataHandler()

# Good
user = get_user()
account = Account()
```

---

## Functions

### Do one thing

A function that does one thing is easy to name, test, and understand. If you can't summarize it in one sentence without "and", it's probably doing too much.

```python
# Bad — does too many things
def process_order(order):
    # validate
    if not order.user_id:
        raise ValueError("User required")
    if order.total <= 0:
        raise ValueError("Invalid total")
    # save
    db.save(order)
    # send email
    email.send(order.user.email, "Order confirmed")
    # update inventory
    for item in order.items:
        inventory.decrement(item.id, item.quantity)

# Good — each step is its own function
def process_order(order):
    validate_order(order)
    save_order(order)
    send_order_confirmation(order)
    update_inventory(order.items)
```

### Keep functions short

There's no magic number, but if a function doesn't fit on your screen, consider breaking it up. Functions under ~20 lines are easier to reason about.

### Arguments: fewer is better

```python
# Bad — 7 arguments, hard to remember the order
def create_user(name, email, password, role, plan, is_active, send_email):
    ...

# Good — group related data into an object
@dataclass
class CreateUserRequest:
    name: str
    email: str
    password: str
    role: str = "user"
    plan: str = "free"
    is_active: bool = True
    send_welcome_email: bool = True

def create_user(request: CreateUserRequest):
    ...
```

### Prefer returning over mutating

Functions that return a new value are easier to reason about and test than functions that modify a shared object.

```python
# Harder to reason about — modifies in place
def normalize_user(user):
    user.name = user.name.strip().title()
    user.email = user.email.lower()
    user.role = user.role or "user"

# Easier — returns a new value
def normalize_user(user: User) -> User:
    return User(
        name=user.name.strip().title(),
        email=user.email.lower(),
        role=user.role or "user",
    )
```

---

## Comments

Comments should explain **why**, not **what**. The code already shows what it does — a comment that just restates the code adds noise.

```python
# Bad comment — restates the code
# increment i by 1
i += 1

# Bad comment — obvious from the variable name
# get the user
user = get_user(id)

# Good comment — explains WHY
# We use a 100ms delay here because the payment provider's API
# has a race condition if requests are sent back-to-back.
time.sleep(0.1)
charge_card(card)

# Good comment — explains a non-obvious algorithm choice
# Binary search instead of linear because this list has 10,000+ items
# and is always sorted on import.
index = bisect.bisect_left(sorted_ids, target_id)

# Good comment — documents a workaround or known limitation
# TODO: This validation will fail for international phone numbers.
# Tracked in issue #142. For now, only US numbers are supported.
if not re.match(r'^\d{10}$', phone):
    raise ValueError("Invalid phone number")
```

### When NOT to comment

- When a better name would make the comment unnecessary
- When the logic is simple and the code reads clearly
- To explain what the language feature does (assume the reader knows the language)

---

## Avoiding Magic Numbers and Strings

A **magic number** is a literal value in code with no obvious meaning. Replace them with named constants.

```python
# Bad — what does 86400 mean? what are these statuses?
if seconds > 86400:
    status = 2

# Good
SECONDS_PER_DAY = 86400
STATUS_EXPIRED = 2

if seconds > SECONDS_PER_DAY:
    status = STATUS_EXPIRED
```

```cpp
// Bad
if (user.role == 3) { ... }
double price = amount * 1.0825;

// Good
constexpr int ROLE_ADMIN = 3;
constexpr double TAX_RATE = 0.0825;

if (user.role == ROLE_ADMIN) { ... }
double price = amount * (1 + TAX_RATE);
```

---

## Don't Repeat Yourself (DRY)

If you write the same logic in two places, it's a bug waiting to happen. When you need to change it, you'll probably only change one of them.

```python
# Bad — same validation duplicated
def register_user(email, password):
    if len(password) < 8:
        raise ValueError("Password too short")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password needs uppercase")
    # ... rest of register

def reset_password(email, new_password):
    if len(new_password) < 8:
        raise ValueError("Password too short")
    if not re.search(r'[A-Z]', new_password):
        raise ValueError("Password needs uppercase")
    # ... rest of reset

# Good — extract the shared logic
def validate_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password too short")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password needs uppercase")

def register_user(email, password):
    validate_password(password)
    # ...

def reset_password(email, new_password):
    validate_password(new_password)
    # ...
```

**Caveat:** Don't extract code just because it looks similar. Extract when it represents the same *concept*. Two functions that do similar things for different reasons shouldn't be merged.

---

## Error Handling

### Be specific

Catch the specific exception you expect. Catching everything hides bugs.

```python
# Bad — catches every exception, including bugs
try:
    result = process(data)
except Exception:
    return default_value

# Good — only catch what you expect
try:
    result = process(data)
except ValueError as e:
    logger.warning("Invalid input: %s", e)
    return default_value
```

### Fail fast

Check preconditions early and raise immediately rather than letting invalid state propagate.

```python
# Bad — invalid state silently propagates
def calculate_discount(price, discount_pct):
    return price * (1 - discount_pct / 100)  # what if discount_pct > 100?

# Good — fail at the boundary
def calculate_discount(price: float, discount_pct: float) -> float:
    if not 0 <= discount_pct <= 100:
        raise ValueError(f"discount_pct must be 0–100, got {discount_pct}")
    return price * (1 - discount_pct / 100)
```

---

## SOLID Basics

SOLID is a set of five principles for object-oriented design. You don't need to memorize them as rules — they're descriptions of patterns that make code easier to change.

### S — Single Responsibility Principle

A class should have one reason to change. If changing the database schema requires editing the same class as changing the email template, that class has too many responsibilities.

```python
# Bad — one class does database + email + formatting
class UserService:
    def save_user(self, user): db.save(user)
    def send_email(self, user): email.send(user.email, ...)
    def format_name(self, user): return f"{user.first} {user.last}"

# Better — each class has one job
class UserRepository:
    def save(self, user): db.save(user)

class UserEmailer:
    def send_welcome(self, user): email.send(user.email, ...)

class UserFormatter:
    def full_name(self, user): return f"{user.first} {user.last}"
```

### O — Open/Closed Principle

Open for extension, closed for modification. Add new behavior without changing existing code.

```python
# Bad — every new shape requires modifying area()
def area(shape):
    if shape.type == "circle":
        return math.pi * shape.r ** 2
    elif shape.type == "rect":
        return shape.w * shape.h
    # adding a triangle requires editing this function

# Better — each shape knows its own area
class Circle:
    def area(self): return math.pi * self.r ** 2

class Rect:
    def area(self): return self.w * self.h

class Triangle:
    def area(self): return 0.5 * self.base * self.height

# Adding Triangle didn't touch Circle or Rect
```

### L — Liskov Substitution Principle

Subclasses should be usable anywhere the parent class is used, without breaking anything. A subclass that overrides a method but changes its contract (what it accepts, what it guarantees) violates this.

```python
# Violation — Square breaks the Rectangle contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # side effect! breaks callers expecting independent w/h

# Callers that do rect.set_width(5); rect.set_height(10); area() will get wrong results with a Square
```

### I — Interface Segregation Principle

Don't force classes to implement methods they don't use. Split large interfaces into smaller, more specific ones.

```python
# Bad — every class must implement all methods even if irrelevant
class Worker:
    def work(self): ...
    def eat(self): ...
    def sleep(self): ...

class Robot(Worker):
    def work(self): print("working")
    def eat(self): raise NotImplementedError  # robots don't eat!
    def sleep(self): raise NotImplementedError

# Better — split into focused interfaces
class Workable(Protocol):
    def work(self) -> None: ...

class Eatable(Protocol):
    def eat(self) -> None: ...

class Robot:
    def work(self): print("working")  # only implements what it uses
```

### D — Dependency Inversion Principle

Depend on abstractions (interfaces), not concrete implementations. This makes components swappable and testable.

```python
# Bad — tightly coupled to a specific database
class UserService:
    def __init__(self):
        self.db = PostgresDatabase()  # can't swap this out

    def get_user(self, id): return self.db.query(f"SELECT * FROM users WHERE id={id}")

# Better — depends on an abstraction
class UserRepository(Protocol):
    def get_by_id(self, id: int) -> User: ...

class UserService:
    def __init__(self, repo: UserRepository):  # pass the dependency in
        self.repo = repo

    def get_user(self, id: int) -> User:
        return self.repo.get_by_id(id)

# Can now pass PostgresRepository, SQLiteRepository, InMemoryRepository, MockRepository
```

---

## Refactoring Patterns

### Extract function

When a block of code can be named, extract it:

```python
# Before
def process_invoice(invoice):
    # validate
    if not invoice.customer_id:
        raise ValueError("Customer required")
    if invoice.amount <= 0:
        raise ValueError("Amount must be positive")
    # charge
    charge_result = payment_gateway.charge(invoice.customer_id, invoice.amount)
    if not charge_result.success:
        raise PaymentError(charge_result.error)
    # record
    db.save_invoice(invoice, charge_result.transaction_id)

# After
def process_invoice(invoice):
    validate_invoice(invoice)
    transaction_id = charge_customer(invoice)
    record_invoice(invoice, transaction_id)
```

### Replace magic number with constant

```python
if age >= 18:  →  if age >= MINIMUM_LEGAL_AGE:
```

### Replace conditional with polymorphism

See the Open/Closed example above — instead of `if type == X`, give each type its own behavior.

### Introduce parameter object

When a function takes 4+ parameters, group them into a dataclass.

---

## Common Pitfalls

**Over-commenting**
More comments isn't better. Comments that restate the code create maintenance burden — when the code changes, someone has to update the comment too (and they often don't).

**Premature abstraction**
Don't create a base class or utility function until you have at least two concrete uses. "Rule of three" — write it twice, extract on the third.

**Long parameter lists**
If a function needs 6+ arguments, it's a sign the function is doing too much or the arguments belong together in an object.

**Inconsistent style**
Pick a style (naming, indentation, where to put opening braces) and apply it uniformly. Inconsistency slows down reading because the reader can't build pattern recognition.

---

## Quick Reference

```
Naming
  Variables  — describe what the value represents, not how it's stored
  Functions  — verb phrase: get_, calculate_, send_, validate_
  Booleans   — is_, has_, can_, should_ prefix
  Constants  — UPPER_SNAKE_CASE in Python; constexpr in C++
  No abbreviations unless universal (i, n, e are fine)

Functions
  Do one thing — if you can't name it without "and", split it
  Fewer arguments — group related ones into an object
  Prefer returning over mutating
  Short enough to see on one screen

Comments
  Good: explain WHY, document edge cases, note workarounds
  Bad: restate what the code does, obvious observations

DRY
  Extract logic when it represents the same concept in 2+ places
  Don't extract just because two things look similar

Error handling
  Catch specific exceptions, not bare Exception
  Validate at the boundary, fail fast

SOLID (one-liner version)
  S — one reason to change
  O — extend without modifying
  L — subclasses work as drop-in replacements
  I — small, focused interfaces
  D — depend on abstractions, not concrete implementations
```
