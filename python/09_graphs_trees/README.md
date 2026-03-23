# Lesson 09 — Graphs and Trees

## What This Covers
Representing graphs as adjacency lists, BFS (breadth-first search) with `deque`, DFS
(depth-first search, recursive and iterative), cycle detection, binary tree nodes,
tree traversals (inorder, preorder, postorder), `heapq` for priority queues, and
Dijkstra's shortest-path algorithm.

---

## Key Concepts

### Graph Representation — Adjacency List
An adjacency list maps each node to its neighbors. It's the most common and memory-
efficient representation for sparse graphs (most real-world graphs are sparse).

```python
# Undirected graph
graph: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B"],
    "F": ["C"],
}

# Weighted graph — edges have a cost
weighted: dict[str, list[tuple[str, int]]] = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 5), ("E", 1)],
    ...
}
```

---

### BFS — Breadth-First Search
Explores all neighbors at depth 1, then depth 2, etc. Uses a **queue** (FIFO).
Finds the *shortest path* (fewest edges) in an unweighted graph.

```
Start: A
Level 0: A
Level 1: B, C          (neighbors of A)
Level 2: D, E, F      (neighbors of B and C, not already visited)
```

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()   # O(1) — this is why we use deque, not list
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

---

### DFS — Depth-First Search
Explores as far as possible down one path before backtracking. Uses a **stack** (LIFO) —
either the call stack (recursive) or an explicit stack (iterative).

```python
# Recursive DFS
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

BFS vs DFS:
| | BFS | DFS |
|--|-----|-----|
| Data structure | Queue | Stack |
| Finds | Shortest path (unweighted) | Any path |
| Memory | O(width) — can be large | O(depth) |
| When to use | Shortest path, level-order | Connected components, cycle detection, topological sort |

---

### Binary Tree
Each node has at most two children: left and right.

```python
class TreeNode:
    def __init__(self, val: int) -> None:
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None
```

Tree traversals — order in which nodes are visited:

| Traversal | Order | Pattern | Typical use |
|-----------|-------|---------|------------|
| Inorder | Left → Root → Right | LRR | BST gives sorted order |
| Preorder | Root → Left → Right | RLL | Copy/serialize tree |
| Postorder | Left → Right → Root | LRR | Delete tree, evaluate expressions |

---

### heapq — Min-Heap / Priority Queue
`heapq` implements a min-heap — always gives you the *smallest* element first.
In Python, it's a regular list maintained in heap order.

```python
import heapq

heap: list[int] = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heapq.heappop(heap)   # → 1  (smallest always at index 0)

# Max-heap: negate values (Python only has min-heap)
heapq.heappush(max_heap, -5)   # -5 sorts before -1, so 5 comes out first
heapq.heappop(max_heap)        # → -5, so negate → 5
```

For priority queues with objects: push `(priority, item)` tuples.

---

### Dijkstra's Shortest Path
Finds the shortest path from a source node to all others in a **weighted graph with
non-negative edge weights**. Uses a priority queue (min-heap) to always process the
cheapest unvisited node next.

```
Time:  O((V + E) log V) with a binary heap
Space: O(V)
```

---

## Syntax Quick Reference

| Pattern | What it does |
|---------|-------------|
| `graph: dict[str, list[str]]` | Adjacency list |
| `deque([start])` | BFS queue |
| `queue.popleft()` | O(1) dequeue for BFS |
| `visited: set[str] = set()` | Track visited nodes |
| `heapq.heappush(h, x)` | Push to min-heap |
| `heapq.heappop(h)` | Pop minimum from heap |
| `heapq.heapify(lst)` | Convert list to heap in-place O(n) |
| `heapq.nsmallest(k, lst)` | k smallest elements |
| `(priority, item)` | Priority queue tuple pattern |

---

## Common Pitfalls

- **Not tracking visited nodes in BFS/DFS** — infinite loops on graphs with cycles. Always use a `visited` set.
- **Using `list.pop(0)` for BFS** — O(n) per step. Use `deque.popleft()`.
- **Dijkstra with negative weights** — Dijkstra is incorrect with negative edges. Use Bellman-Ford for negative weights.
- **Heap with mutable objects** — if you push objects and later modify them, the heap order breaks. Use immutable tuples.
- **Tree traversal with no base case** — recursive traversals must handle `None` nodes.
- **Treating a tree as a graph** — trees have no cycles; you don't need a `visited` set for trees (unlike graphs).

---

## When to Use What

| Need | Use |
|------|-----|
| Shortest path, fewest hops | BFS |
| Detect cycles | DFS |
| Connected components | DFS or BFS |
| Topological sort | DFS |
| Shortest path, weighted | Dijkstra (non-negative weights) |
| Always-get-minimum efficiently | `heapq` |
| BST sorted output | Inorder traversal |
| Tree serialization | Preorder traversal |
