# ─────────────────────────────────────────────────────────────
#  Lesson 09 — Graphs and Trees
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

from __future__ import annotations
from collections import deque
import heapq
from dataclasses import dataclass, field
from typing import TypeAlias

# Type aliases — make signatures readable
Graph: TypeAlias = dict[str, list[str]]
WeightedGraph: TypeAlias = dict[str, list[tuple[str, int]]]


# ── GRAPH REPRESENTATION ──────────────────────────────────────
print("── graph representation ─────────────────────")

# Adjacency list: each node maps to a list of its neighbors.
# This is the standard representation — memory-efficient for sparse graphs.

#  A --- B
#  |   / |
#  |  /  |
#  | /   |
#  C --- D --- E
#              |
#              F

graph: Graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C", "E"],
    "E": ["D", "F"],
    "F": ["E"],
}

print("  Graph (adjacency list):")
for node, neighbors in graph.items():
    print(f"    {node} → {neighbors}")

print(f"\n  Nodes: {list(graph.keys())}")
print(f"  Edges from A: {graph['A']}")


# ── BFS — BREADTH-FIRST SEARCH ───────────────────────────────
print("\n── BFS — breadth-first search ───────────────")

def bfs(graph: Graph, start: str) -> list[str]:
    """
    Explore the graph level by level, starting from 'start'.
    Uses a QUEUE (deque) — first in, first out.

    Time:  O(V + E) — visits each vertex and edge once
    Space: O(V) — queue + visited set

    Key property: BFS finds the SHORTEST PATH (in terms of number of edges)
    from start to any reachable node.
    """
    visited: set[str] = set()
    queue: deque[str] = deque([start])   # deque for O(1) popleft
    visited.add(start)
    order: list[str] = []

    while queue:
        node = queue.popleft()    # O(1) — critical reason for using deque
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:    # skip already-visited nodes (avoid cycles)
                visited.add(neighbor)      # mark before enqueuing — not after popping
                queue.append(neighbor)     # enqueue for future exploration

    return order

print(f"  BFS from A: {bfs(graph, 'A')}")
print(f"  BFS from E: {bfs(graph, 'E')}")

def bfs_shortest_path(graph: Graph, start: str, end: str) -> list[str] | None:
    """
    BFS that tracks the path taken to reach each node.
    Returns the shortest path (fewest edges) from start to end.
    """
    if start == end:
        return [start]

    visited: set[str] = {start}
    queue: deque[list[str]] = deque([[start]])   # each item is a path

    while queue:
        path = queue.popleft()
        node = path[-1]    # current node is the last in the path

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path    # found it — BFS guarantees this is shortest
                visited.add(neighbor)
                queue.append(new_path)

    return None    # no path exists

path = bfs_shortest_path(graph, "A", "F")
print(f"\n  Shortest path A→F: {path}")
path2 = bfs_shortest_path(graph, "C", "F")
print(f"  Shortest path C→F: {path2}")


# ── DFS — DEPTH-FIRST SEARCH ─────────────────────────────────
print("\n── DFS — depth-first search ─────────────────")

def dfs_recursive(graph: Graph, node: str,
                  visited: set[str] | None = None) -> list[str]:
    """
    Recursive DFS — uses the CALL STACK as the stack.
    Explores one branch fully before backtracking.

    Time:  O(V + E)
    Space: O(V) for visited set + O(depth) for call stack frames
    """
    if visited is None:
        visited = set()   # mutable default — use None + initialize inside

    visited.add(node)
    order: list[str] = [node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order

def dfs_iterative(graph: Graph, start: str) -> list[str]:
    """
    Iterative DFS — uses an explicit STACK (list).
    Avoids Python's recursion limit for deep graphs.

    Note: iterative DFS may visit nodes in a different order than recursive DFS
    because we push all neighbors onto the stack (LIFO reverses order).
    """
    visited: set[str] = set()
    stack: list[str] = [start]
    order: list[str] = []

    while stack:
        node = stack.pop()            # LIFO — last pushed, first explored
        if node not in visited:
            visited.add(node)
            order.append(node)
            # Push neighbors in reverse so we explore in "natural" order
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order

print(f"  DFS recursive from A: {dfs_recursive(graph, 'A')}")
print(f"  DFS iterative from A: {dfs_iterative(graph, 'A')}")


# ── CYCLE DETECTION ───────────────────────────────────────────
print("\n── cycle detection ──────────────────────────")

def has_cycle_undirected(graph: Graph) -> bool:
    """
    Detect a cycle in an UNDIRECTED graph using DFS.
    A cycle exists if we reach an already-visited node that isn't our parent.

    We track 'parent' to avoid falsely detecting the edge we came from as a cycle.
    (In an undirected graph, every edge is bidirectional — A→B and B→A both exist.)
    """
    visited: set[str] = set()

    def dfs(node: str, parent: str | None) -> bool:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:     # visited AND not our parent → cycle
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False

# Add a cycle to test
cyclic_graph: Graph = {
    "A": ["B"],
    "B": ["A", "C"],
    "C": ["B", "D"],
    "D": ["C", "A"],   # D connects back to A — creates a cycle
}
acyclic_graph: Graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": [],
    "D": [],
}
print(f"  Cyclic graph has cycle:   {has_cycle_undirected(cyclic_graph)}")
print(f"  Acyclic graph has cycle:  {has_cycle_undirected(acyclic_graph)}")


# ── BINARY TREE ───────────────────────────────────────────────
print("\n── binary tree ──────────────────────────────")

class TreeNode:
    """A node in a binary tree."""

    def __init__(self, val: int) -> None:
        self.val: int = val
        self.left: TreeNode | None = None    # left child
        self.right: TreeNode | None = None   # right child

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"

# Build this tree manually:
#        4
#       / \
#      2   6
#     / \ / \
#    1  3 5  7

root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)
root.right.left = TreeNode(5)
root.right.right = TreeNode(7)


# ── TREE TRAVERSALS ───────────────────────────────────────────
print("\n── tree traversals ──────────────────────────")

def inorder(node: TreeNode | None) -> list[int]:
    """
    Inorder: LEFT → ROOT → RIGHT
    For a Binary Search Tree (BST), inorder traversal gives sorted output.
    """
    if node is None:
        return []   # base case — empty tree / leaf's child
    return inorder(node.left) + [node.val] + inorder(node.right)

def preorder(node: TreeNode | None) -> list[int]:
    """
    Preorder: ROOT → LEFT → RIGHT
    Useful for copying/serializing a tree (you see parents before children).
    """
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)

def postorder(node: TreeNode | None) -> list[int]:
    """
    Postorder: LEFT → RIGHT → ROOT
    Useful when you need to process children before parents (e.g., delete tree).
    """
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.val]

def level_order(root: TreeNode | None) -> list[list[int]]:
    """
    Level-order (BFS on a tree): visit nodes level by level.
    Returns a list of levels, each level is a list of values.
    """
    if root is None:
        return []

    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        level_size = len(queue)   # number of nodes at this level
        level: list[int] = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result

print(f"  Tree:         4")
print(f"               / \\")
print(f"              2   6")
print(f"             / \\ / \\")
print(f"            1  3 5  7")
print(f"\n  Inorder   (L→R→R): {inorder(root)}  ← sorted for BST")
print(f"  Preorder  (R→L→R): {preorder(root)}")
print(f"  Postorder (L→R→R): {postorder(root)}")
print(f"  Level-order (BFS): {level_order(root)}")

def tree_height(node: TreeNode | None) -> int:
    """Height of a tree = length of the longest path from root to a leaf."""
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))

print(f"  Height: {tree_height(root)}")


# ── HEAPQ — PRIORITY QUEUE ────────────────────────────────────
print("\n── heapq — min-heap / priority queue ────────")

# heapq implements a MIN-HEAP: heap[0] is always the smallest element.
# Push/pop are both O(log n). heapify is O(n).

min_heap: list[int] = []
for val in [5, 3, 8, 1, 9, 2, 7, 4, 6]:
    heapq.heappush(min_heap, val)

print(f"  Heap (internal representation): {min_heap}")
print(f"  Minimum is always at index 0: {min_heap[0]}")

print("  Popping in order:")
while min_heap:
    print(f"    {heapq.heappop(min_heap)}", end=" ")
print()

# heapify — convert a list to a heap in-place O(n) (faster than n pushes)
data = [5, 3, 8, 1, 9, 2]
heapq.heapify(data)   # rearranges data in-place to satisfy heap property
print(f"\n  heapify([5,3,8,1,9,2]): {data}")

# Max-heap: negate values (Python only has min-heap)
max_heap: list[int] = []
for val in [5, 3, 8, 1, 9]:
    heapq.heappush(max_heap, -val)   # negate on push

max_val = -heapq.heappop(max_heap)   # negate on pop
print(f"  Max-heap max value: {max_val}")

# Priority queue with (priority, item) tuples
# heapq compares tuples element by element — lower priority number = higher priority
task_queue: list[tuple[int, str]] = []
heapq.heappush(task_queue, (3, "low priority task"))
heapq.heappush(task_queue, (1, "critical task"))
heapq.heappush(task_queue, (2, "medium priority task"))

print("\n  Task queue (priority order):")
while task_queue:
    priority, task = heapq.heappop(task_queue)
    print(f"    [{priority}] {task}")

# Useful helpers
nums = [5, 1, 9, 3, 7, 2, 8]
print(f"\n  nsmallest(3): {heapq.nsmallest(3, nums)}")
print(f"  nlargest(3):  {heapq.nlargest(3, nums)}")


# ── DIJKSTRA'S ALGORITHM ──────────────────────────────────────
print("\n── Dijkstra's shortest path ─────────────────")

# Weighted directed graph for Dijkstra
#   A --4-- B --1-- D
#   |       |       |
#   2       3       2
#   |       |       |
#   C --1-- E --5-- F

weighted_graph: WeightedGraph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 1), ("E", 3)],
    "C": [("E", 1)],
    "D": [("F", 2)],
    "E": [("F", 5)],
    "F": [],
}

def dijkstra(graph: WeightedGraph, start: str) -> dict[str, int]:
    """
    Find the shortest distance from 'start' to all other nodes.

    Time:  O((V + E) log V) with a binary heap
    Space: O(V)

    How it works:
    1. Start with distance 0 to source, infinity to everything else.
    2. Use a min-heap to always process the cheapest known node next.
    3. When we pop a node, we've found its shortest distance (greedy — works
       because we always process smallest first and all weights are non-negative).
    4. Relax edges: if going through this node gives a shorter path to a neighbor,
       update the neighbor's distance.
    """
    # Initialize all distances as infinity except the start
    distances: dict[str, int] = {node: float("inf") for node in graph}
    distances[start] = 0

    # Min-heap: (distance, node)
    heap: list[tuple[int, str]] = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)

        # If we've already found a shorter path to this node, skip
        # (we may have pushed stale entries to the heap)
        if current_dist > distances[node]:
            continue

        # Relax all edges from this node
        for neighbor, weight in graph[node]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances

distances = dijkstra(weighted_graph, "A")
print("  Shortest distances from A:")
for node, dist in sorted(distances.items()):
    print(f"    A → {node}: {dist}")

# Version that also returns the actual paths
def dijkstra_with_paths(
    graph: WeightedGraph, start: str
) -> tuple[dict[str, int], dict[str, list[str]]]:
    """Dijkstra that reconstructs the actual shortest paths."""
    distances: dict[str, int] = {node: float("inf") for node in graph}
    distances[start] = 0
    previous: dict[str, str | None] = {node: None for node in graph}
    heap: list[tuple[int, str]] = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)
        if current_dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = node     # track how we got here
                heapq.heappush(heap, (new_dist, neighbor))

    # Reconstruct paths by following 'previous' pointers backward
    def reconstruct(target: str) -> list[str]:
        path: list[str] = []
        current: str | None = target
        while current is not None:
            path.append(current)
            current = previous[current]
        return list(reversed(path))

    paths = {node: reconstruct(node) for node in graph}
    return distances, paths

dists, paths = dijkstra_with_paths(weighted_graph, "A")
print("\n  Shortest paths from A:")
for node in sorted(paths):
    print(f"    A → {node}: {paths[node]} (cost={dists[node]})")


if __name__ == "__main__":
    pass
