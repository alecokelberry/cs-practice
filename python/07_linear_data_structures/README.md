# Lesson 07 — Linear Data Structures

## What This Covers
Lists as stacks and (inefficient) queues, `collections.deque` as a proper fast queue,
implementing a singly-linked list from scratch, and building Stack and Queue classes
with a clean API. This lesson bridges "Python collections" and "CS concepts."

---

## Key Concepts

### Stack — LIFO (Last In, First Out)
A stack is a collection where the last item added is the first one removed. Think: a
stack of plates — you add and remove from the top.

Python's `list` works perfectly as a stack:
- `append(x)` — push (add to top) — O(1)
- `pop()` — pop (remove from top) — O(1)
- `lst[-1]` — peek (look at top without removing) — O(1)

```python
stack: list[int] = []
stack.append(1)   # push
stack.append(2)
stack.append(3)
stack.pop()       # → 3 (LIFO — last in, first out)
```

Use cases: undo/redo, function call stack, parsing balanced brackets, DFS.

---

### Queue — FIFO (First In, First Out)
A queue processes items in the order they arrive. Think: a checkout line.

**Do NOT use a list as a queue.** `list.pop(0)` is O(n) because it shifts every element
left. For large queues this is catastrophically slow.

```python
# BAD — O(n) pop from front
queue = [1, 2, 3]
queue.pop(0)   # shifts 2 and 3 left — O(n)
```

---

### collections.deque — the correct queue
`deque` (pronounced "deck") is a double-ended queue. Both ends support O(1) operations.

```python
from collections import deque

q: deque[int] = deque()
q.append(1)       # enqueue — add to right — O(1)
q.append(2)
q.append(3)
q.popleft()       # dequeue — remove from left — O(1)

# Left end:
q.appendleft(0)   # add to front — O(1)
q.popleft()       # remove from front — O(1)

# Right end (normal list behavior):
q.append(99)      # add to back — O(1)
q.pop()           # remove from back — O(1)
```

Also useful: `deque(maxlen=n)` creates a fixed-size circular buffer — old items are
automatically dropped when it fills up. Great for "keep last N events."

---

### Singly-Linked List
A linked list stores elements in nodes, where each node points to the next. Unlike
lists (arrays), insertions and deletions at the front are O(1) — no shifting needed.

```
[head] → Node(1) → Node(2) → Node(3) → None
```

| Operation | List (array) | Linked List |
|-----------|-------------|-------------|
| Access by index | O(1) | O(n) — must traverse |
| Insert at front | O(n) — shifts all | O(1) — update head |
| Insert at back | O(1) amortized | O(n) — must traverse (or O(1) with tail pointer) |
| Delete from front | O(n) — shifts all | O(1) — update head |
| Search | O(n) | O(n) |

In practice, Python's list (backed by a dynamic array) beats a pure linked list for
most tasks. You'll build linked lists in CS courses and interviews; deque covers the
real-world use cases.

---

### When Each Structure Makes Sense

| Structure | When to use |
|-----------|-------------|
| `list` as stack | Simple LIFO — small to medium size |
| `deque` as queue | FIFO — any size (fast O(1) both ends) |
| `deque(maxlen=n)` | Circular buffer — keep last N items |
| Linked list | Interview practice; insertion-heavy workloads at head |
| Stack class | Encapsulation — hide the implementation, expose clean API |
| Queue class | Encapsulation — ditto |

---

## Syntax Quick Reference

| Syntax | What it does |
|--------|-------------|
| `lst.append(x)` | Add to end of list — O(1) |
| `lst.pop()` | Remove from end of list — O(1) |
| `lst[-1]` | Peek at end of list — O(1) |
| `lst.pop(0)` | Remove from front — O(n) — AVOID for queues |
| `deque()` | Create empty deque |
| `d.append(x)` | Add to right — O(1) |
| `d.appendleft(x)` | Add to left — O(1) |
| `d.pop()` | Remove from right — O(1) |
| `d.popleft()` | Remove from left — O(1) |
| `deque(maxlen=n)` | Fixed-size circular buffer |
| `d[0]`, `d[-1]` | Peek both ends — O(1) |

---

## Common Pitfalls

- **`list.pop(0)` for queues** — O(n) per pop. Always use `deque.popleft()`.
- **Accessing an empty stack/queue** — both `list.pop()` and `deque.popleft()` raise `IndexError` on empty. Always check `if stack:` before popping.
- **`deque` vs `list` for random access** — `deque[n]` is O(n), not O(1). If you need random access, use a list.
- **Linked list head = None** — the empty list is just `None`. Functions that traverse need to handle this case.
- **Forgetting to update `tail` on linked list insert** — if you track a tail pointer for O(1) appends, keep it in sync.

---

## Big-O Summary

| Operation | list (stack) | deque (queue) | Linked List |
|-----------|-------------|---------------|-------------|
| Push/append | O(1) | O(1) | O(1) at head; O(n) at tail |
| Pop/remove last | O(1) | O(1) | O(n) |
| Pop/remove first | O(n) | O(1) | O(1) |
| Peek | O(1) | O(1) | O(1) |
| Access by index | O(1) | O(n) | O(n) |
