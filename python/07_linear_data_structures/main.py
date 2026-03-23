# ─────────────────────────────────────────────────────────────
#  Lesson 07 — Linear Data Structures
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

from __future__ import annotations
from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")   # Generic type variable — lets our classes work with any type


# ── LIST AS STACK ─────────────────────────────────────────────
print("── list as stack (LIFO) ─────────────────────")

# A stack is LIFO: Last In, First Out.
# Python's list is a perfect stack — append/pop are both O(1).

stack: list[int] = []

# Push
stack.append(10)
stack.append(20)
stack.append(30)
print(f"  After pushing 10, 20, 30: {stack}")

# Peek — look at top without removing
if stack:
    print(f"  Peek (top): {stack[-1]}")   # -1 index = last element = top

# Pop
print(f"  Pop: {stack.pop()}")   # 30 — LIFO
print(f"  Pop: {stack.pop()}")   # 20
print(f"  Stack now: {stack}")

# Real use: check for balanced brackets
def is_balanced(s: str) -> bool:
    """Return True if all brackets in s are properly balanced and nested."""
    stack: list[str] = []
    pairs: dict[str, str] = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in "({[":
            stack.append(char)          # opening bracket — push
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False            # no matching opener
            stack.pop()                 # matched — pop the opener

    return len(stack) == 0             # balanced if nothing left on stack

tests = ["({[]})", "([)]", "{[}", "((()))"]
for test in tests:
    print(f"  is_balanced({test!r}): {is_balanced(test)}")


# ── LIST AS QUEUE (WHY IT'S SLOW) ────────────────────────────
print("\n── list as queue — why it's slow ────────────")

# A queue is FIFO: First In, First Out.
# list.pop(0) removes from the FRONT — this is O(n) because
# every element after index 0 must shift one position to the left.

slow_queue: list[int] = [1, 2, 3, 4, 5]
print(f"  list queue: {slow_queue}")
removed = slow_queue.pop(0)   # O(n) — shifts [2,3,4,5] left
print(f"  pop(0) removed: {removed}, remaining: {slow_queue}")
print("  (This is O(n) — for large queues, use deque instead)")


# ── DEQUE AS FAST QUEUE ───────────────────────────────────────
print("\n── collections.deque as queue (FIFO) ────────")

# deque (double-ended queue) — O(1) on both ends.
# Use deque whenever you need queue behavior.

q: deque[str] = deque()

# Enqueue — add to right (back of line)
q.append("Alice")
q.append("Bob")
q.append("Carol")
print(f"  Queue: {list(q)}")

# Dequeue — remove from left (front of line) — O(1)
served = q.popleft()
print(f"  Served: {served}")
print(f"  Queue: {list(q)}")

# Peek at front and back
if q:
    print(f"  Front: {q[0]}, Back: {q[-1]}")

# appendleft — add to the front (priority insertion)
q.appendleft("VIP")
print(f"  After VIP added to front: {list(q)}")


# ── DEQUE AS CIRCULAR BUFFER ──────────────────────────────────
print("\n── deque(maxlen=n) — circular buffer ────────")

# maxlen creates a fixed-size deque. When full, adding to one end
# automatically removes from the other. Perfect for "last N events."

recent: deque[int] = deque(maxlen=3)   # keep only last 3 items

for i in range(1, 8):
    recent.append(i)
    print(f"  After append({i}): {list(recent)}")

print(f"\n  Final (last 3): {list(recent)}")

# Real use: sliding window of recent sensor readings
sensor_readings: list[float] = [1.1, 2.3, 0.9, 4.2, 3.1, 5.0, 2.8]
window: deque[float] = deque(maxlen=3)
print("\n  Sliding window average (size 3):")
for reading in sensor_readings:
    window.append(reading)
    if len(window) == window.maxlen:
        avg = sum(window) / len(window)
        print(f"    window={list(window)}, avg={avg:.2f}")


# ── SINGLY-LINKED LIST ────────────────────────────────────────
print("\n── singly-linked list ───────────────────────")

class Node(Generic[T]):
    """A single node in the linked list."""

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: Node[T] | None = None   # points to the next node (or None at end)

    def __repr__(self) -> str:
        return f"Node({self.value!r})"

class LinkedList(Generic[T]):
    """
    Singly-linked list — nodes hold values and a 'next' pointer.

    Advantages over list:
    - O(1) insert/delete at head (no shifting)

    Disadvantages:
    - O(n) access by index (must traverse from head)
    - More memory (each node stores a pointer)
    """

    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self._size: int = 0

    def prepend(self, value: T) -> None:
        """Insert at the front — O(1). No shifting needed."""
        new_node = Node(value)
        new_node.next = self.head   # new node points to old head
        self.head = new_node        # head now points to new node
        self._size += 1

    def append(self, value: T) -> None:
        """Insert at the back — O(n) because we must find the tail."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node    # list was empty
        else:
            current = self.head
            while current.next is not None:
                current = current.next  # walk to the last node
            current.next = new_node     # link last node to new node
        self._size += 1

    def remove_front(self) -> T:
        """Remove and return the front element — O(1)."""
        if self.head is None:
            raise IndexError("remove from empty linked list")
        value = self.head.value
        self.head = self.head.next  # head skips the removed node
        self._size -= 1
        return value

    def find(self, value: T) -> bool:
        """Search for a value — O(n) — must traverse every node."""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_list(self) -> list[T]:
        """Convert to a Python list for display."""
        result: list[T] = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        nodes = " → ".join(str(v) for v in self.to_list())
        return f"LinkedList([{nodes}])"

ll: LinkedList[int] = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.prepend(5)   # O(1) — adds to front
print(f"  {ll}")
print(f"  length: {len(ll)}")
print(f"  find(20): {ll.find(20)}")
print(f"  find(99): {ll.find(99)}")
print(f"  remove_front: {ll.remove_front()}")
print(f"  After remove: {ll}")


# ── STACK CLASS ───────────────────────────────────────────────
print("\n── Stack class ──────────────────────────────")

class Stack(Generic[T]):
    """
    Stack — LIFO. Backed by a list.
    Exposes a clean, intention-revealing API (push/pop/peek)
    rather than exposing list methods directly.
    """

    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, item: T) -> None:
        """Add an item to the top — O(1)."""
        self._data.append(item)

    def pop(self) -> T:
        """Remove and return the top item — O(1). Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> T:
        """Return the top item without removing it — O(1)."""
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack(top={self._data[-1]!r})" if self._data else "Stack(empty)"

s: Stack[str] = Stack()
s.push("first")
s.push("second")
s.push("third")
print(f"  {s}")
print(f"  peek: {s.peek()}")
print(f"  pop: {s.pop()}")
print(f"  pop: {s.pop()}")
print(f"  {s}")
print(f"  empty: {s.is_empty()}")


# ── QUEUE CLASS ───────────────────────────────────────────────
print("\n── Queue class ──────────────────────────────")

class Queue(Generic[T]):
    """
    Queue — FIFO. Backed by collections.deque for O(1) on both ends.
    Encapsulates deque so callers can't accidentally use it as a stack.
    """

    def __init__(self) -> None:
        self._data: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        """Add to the back of the queue — O(1)."""
        self._data.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item — O(1). Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def front(self) -> T:
        """Return the front item without removing it — O(1)."""
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        if not self._data:
            return "Queue(empty)"
        return f"Queue(front={self._data[0]!r}, size={len(self._data)})"

print("  Simulating a print job queue:")
print_queue: Queue[str] = Queue()
for job in ["report.pdf", "photo.jpg", "spreadsheet.xlsx"]:
    print_queue.enqueue(job)
    print(f"    Queued: {job}")

print()
while not print_queue.is_empty():
    job = print_queue.dequeue()
    print(f"    Printing: {job}")


if __name__ == "__main__":
    pass
