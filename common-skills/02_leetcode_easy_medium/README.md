# 02 — LeetCode Easy / Medium

This is a curated problem set organized by **technique**, not by difficulty. The goal isn't to memorize answers — it's to recognize which pattern applies and build the muscle memory to implement it under pressure.

---

## How to Use This Guide

1. Read the technique description and the "when to reach for it" section.
2. Try each problem yourself first — even for 15 minutes.
3. If stuck, look at the approach, then implement it yourself (don't copy-paste).
4. After solving, check the time/space complexity.

---

## Pattern 1 — Two Pointers

**Idea:** Use two indices (`left`, `right`) that move toward or away from each other. Eliminates a nested loop — `O(n²)` → `O(n)`.

**When:** Sorted array problems involving pairs, subarrays, or partitioning.

```
[1, 2, 3, 4, 6], target = 6
 ↑              ↑
left           right   → 1+6=7, too big → move right left
 ↑           ↑
left        right      → 1+5, still too big
 ↑        ↑
left     right         → 1+4=5, too small → move left right
    ↑    ↑             → 2+4=6, found!
```

**Problems:**
- [167] Two Sum II — Input Array Is Sorted ← start here
- [125] Valid Palindrome
- [15] 3Sum
- [11] Container With Most Water
- [26] Remove Duplicates from Sorted Array
- [977] Squares of a Sorted Array

**Template:**
```python
def two_pointer(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
```

---

## Pattern 2 — Sliding Window

**Idea:** Maintain a window (subarray or substring) that expands right and shrinks left. Avoids recomputing the whole window on each step — `O(n²)` → `O(n)`.

**When:** Subarray/substring problems asking for a maximum/minimum length or count with a constraint.

**Fixed-size window:**
```
[2, 1, 5, 1, 3, 2], k=3
 [─────]               sum=8
    [─────]            sum=7
       [─────]         sum=9  ← max
          [─────]      sum=6
```

**Variable-size window:**
```
Expand right until constraint violated → shrink left until valid again
```

**Problems:**
- [643] Maximum Average Subarray I (fixed window) ← start here
- [3] Longest Substring Without Repeating Characters (variable)
- [121] Best Time to Buy and Sell Stock
- [209] Minimum Size Subarray Sum
- [424] Longest Repeating Character Replacement
- [567] Permutation in String

**Template (variable):**
```python
def sliding_window(s):
    left = 0
    window = {}  # or Counter
    result = 0
    for right in range(len(s)):
        window[s[right]] = window.get(s[right], 0) + 1  # expand
        while <constraint violated>:
            window[s[left]] -= 1                         # shrink
            left += 1
        result = max(result, right - left + 1)
    return result
```

---

## Pattern 3 — Fast & Slow Pointers

**Idea:** Two pointers moving at different speeds. The fast pointer moves 2 steps, the slow 1. If there's a cycle, they'll meet. Also useful for finding the middle of a linked list.

**When:** Linked list problems — cycle detection, finding middle, finding kth from end.

```
1 → 2 → 3 → 4 → 5 → 3 (cycle back)
s                        slow: 1 step
f                        fast: 2 steps
After a few iterations, slow == fast → cycle exists
```

**Problems:**
- [141] Linked List Cycle ← start here
- [142] Linked List Cycle II (find where cycle starts)
- [876] Middle of the Linked List
- [234] Palindrome Linked List
- [287] Find the Duplicate Number

**Template:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

## Pattern 4 — Binary Search

**Idea:** Cut the search space in half each step. Requires a sorted array (or a search space with a monotonic property). `O(log n)`.

**When:** Finding a value in a sorted array, or any problem with "find the minimum X that satisfies condition Y".

```
[1, 3, 5, 7, 9, 11], target=7
 left           right
        mid=5  → 5 < 7, go right
              left right
              mid=9  → 9 > 7, go left
              left/right
              mid=7  → found!
```

**Problems:**
- [704] Binary Search ← start here
- [35] Search Insert Position
- [153] Find Minimum in Rotated Sorted Array
- [33] Search in Rotated Sorted Array
- [74] Search a 2D Matrix
- [875] Koko Eating Bananas (binary search on answer)

**Template:**
```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2  # avoids integer overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Important:** `mid = left + (right - left) // 2` is safer than `(left + right) // 2` — no overflow risk.

---

## Pattern 5 — Hash Map / Hash Set

**Idea:** Trade space for time. Store seen values in a dictionary or set to check membership in `O(1)`.

**When:** "Find two elements with property X", frequency counts, detecting duplicates.

**Problems:**
- [1] Two Sum ← start here
- [217] Contains Duplicate
- [49] Group Anagrams
- [347] Top K Frequent Elements
- [128] Longest Consecutive Sequence
- [242] Valid Anagram

**Template:**
```python
def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

---

## Pattern 6 — Stack

**Idea:** A stack (LIFO) keeps track of "pending" items. When you see a closing element, pop and compare with the top. Also used for monotonic stacks (next greater element problems).

**When:** Matching brackets, "next greater element", expression evaluation, nested structure problems.

**Problems:**
- [20] Valid Parentheses ← start here
- [155] Min Stack
- [739] Daily Temperatures (monotonic stack)
- [84] Largest Rectangle in Histogram (monotonic stack)
- [150] Evaluate Reverse Polish Notation

**Template (matching brackets):**
```python
def is_valid(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in '({[':
            stack.append(c)
        elif not stack or stack[-1] != pairs[c]:
            return False
        else:
            stack.pop()
    return len(stack) == 0
```

**Template (monotonic stack — next greater element):**
```python
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # indices of elements waiting for their answer
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
```

---

## Pattern 7 — BFS (Breadth-First Search)

**Idea:** Explore all neighbors at the current depth before going deeper. Uses a queue. Guarantees the **shortest path** in an unweighted graph.

**When:** Shortest path, level-by-level tree traversal, "minimum number of steps" problems.

```
        1
       / \
      2   3
     / \
    4   5

BFS order: 1, 2, 3, 4, 5  (level by level)
```

**Problems:**
- [102] Binary Tree Level Order Traversal ← start here
- [200] Number of Islands
- [994] Rotting Oranges
- [127] Word Ladder
- [286] Walls and Gates

**Template:**
```python
from collections import deque

def bfs(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

## Pattern 8 — DFS (Depth-First Search)

**Idea:** Go as deep as possible before backtracking. Implemented recursively (implicit stack) or with an explicit stack. Useful for path problems, connected components, and exploring all possibilities.

**When:** Path existence, connected components, tree problems, backtracking.

```
        1
       / \
      2   3
     / \
    4   5

DFS order: 1, 2, 4, 5, 3  (go deep, then backtrack)
```

**Problems:**
- [104] Maximum Depth of Binary Tree ← start here
- [112] Path Sum
- [133] Clone Graph
- [695] Max Area of Island
- [417] Pacific Atlantic Water Flow

**Template (tree):**
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Template (grid DFS):**
```python
def dfs(grid, r, c, visited):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if (r, c) in visited or grid[r][c] == '0':
        return
    visited.add((r, c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r + dr, c + dc, visited)
```

---

## Pattern 9 — Backtracking

**Idea:** Build solutions incrementally, abandon (backtrack) a path as soon as it violates constraints. Explores all possibilities but prunes dead branches early.

**When:** Generate all combinations/permutations/subsets, constraint-satisfaction problems (N-Queens, Sudoku).

```
choose → explore → unchoose
```

**Problems:**
- [78] Subsets ← start here
- [46] Permutations
- [39] Combination Sum
- [40] Combination Sum II (with duplicates)
- [22] Generate Parentheses
- [51] N-Queens

**Template:**
```python
def backtrack(start, current, result, nums):
    result.append(list(current))  # record current state
    for i in range(start, len(nums)):
        current.append(nums[i])       # choose
        backtrack(i + 1, current, result, nums)  # explore
        current.pop()                 # unchoose (backtrack)
```

---

## Pattern 10 — Dynamic Programming (Bottom-Up)

**Idea:** Break a problem into overlapping subproblems. Solve each subproblem once and store results in a table. Build from base cases up to the final answer.

**When:** "How many ways", "minimum cost", "maximum profit" — where the answer depends on smaller versions of the same problem.

**Fibonacci (classic intro):**
```python
# O(n) time, O(1) space
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

**Problems:**
- [70] Climbing Stairs ← start here
- [198] House Robber
- [322] Coin Change
- [300] Longest Increasing Subsequence
- [1143] Longest Common Subsequence
- [416] Partition Equal Subset Sum (0/1 knapsack)

**Template (1D DP):**
```python
def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

---

## Pattern 11 — Heap / Priority Queue

**Idea:** A heap keeps the min (or max) element at the top. `heapq` in Python is a min-heap. Use `heappush` / `heappop` for `O(log n)` insertion/extraction.

**When:** "Top K", "Kth largest/smallest", merge K sorted lists, streaming median.

**Problems:**
- [215] Kth Largest Element in an Array ← start here
- [347] Top K Frequent Elements
- [973] K Closest Points to Origin
- [295] Find Median from Data Stream
- [23] Merge K Sorted Lists

**Template:**
```python
import heapq

def top_k_frequent(nums, k):
    freq = {}
    for n in nums:
        freq[n] = freq.get(n, 0) + 1
    # min-heap of size k — keeps k largest frequencies
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for count, num in heap]
```

**Tip:** Python's `heapq` is a min-heap. For max-heap, negate values: push `-x`, pop and negate back.

---

## Pattern 12 — Prefix Sum

**Idea:** Precompute cumulative sums so any subarray sum can be answered in `O(1)` after `O(n)` setup.

**When:** Range sum queries, "subarray sum equals K", counting subarrays with a property.

```
nums    = [1, 2, 3, 4, 5]
prefix  = [0, 1, 3, 6, 10, 15]

Sum of nums[1..3] = prefix[4] - prefix[1] = 10 - 1 = 9
```

**Problems:**
- [303] Range Sum Query - Immutable ← start here
- [560] Subarray Sum Equals K
- [724] Find Pivot Index
- [525] Contiguous Array

**Template:**
```python
# prefix[i] = sum of nums[0..i-1]
prefix = [0] * (len(nums) + 1)
for i, n in enumerate(nums):
    prefix[i+1] = prefix[i] + n

# sum of nums[l..r] = prefix[r+1] - prefix[l]
```

---

## Pattern 13 — Trie (Prefix Tree)

**Idea:** A tree where each node represents one character. Paths from root to node spell out prefixes. Efficient for prefix lookups and word storage.

**When:** Word search, autocomplete, "does any word start with prefix".

**Problems:**
- [208] Implement Trie ← start here
- [211] Design Add and Search Words Data Structure
- [212] Word Search II

**Template:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
```

---

## Pattern 14 — Union Find (Disjoint Set)

**Idea:** A data structure that tracks connected components. `find` returns the root of a component. `union` merges two components. Both operations are nearly `O(1)` with path compression.

**When:** Connected components in a graph, cycle detection in undirected graph, grouping problems.

**Problems:**
- [547] Number of Provinces ← start here
- [684] Redundant Connection (cycle detection)
- [200] Number of Islands (also solvable with BFS/DFS)
- [1061] Lexicographically Smallest Equivalent String

**Template:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

---

## Big-O Quick Reference

| Pattern | Time | Space | Key insight |
|---------|------|-------|-------------|
| Two Pointers | O(n) | O(1) | Sorted array, pair problems |
| Sliding Window | O(n) | O(k) | Subarray/substring with constraint |
| Binary Search | O(log n) | O(1) | Sorted, or monotonic property |
| Hash Map | O(n) | O(n) | Membership in O(1) |
| Stack | O(n) | O(n) | Matching, "next greater" |
| BFS | O(V+E) | O(V) | Shortest path, levels |
| DFS | O(V+E) | O(V) | Paths, connected components |
| Backtracking | O(2ⁿ) worst | O(n) | All combos/perms |
| DP (1D) | O(n) | O(n) | Overlapping subproblems |
| Heap | O(n log k) | O(k) | Top K problems |
| Prefix Sum | O(n) setup, O(1) query | O(n) | Range sums |
| Union Find | O(α(n)) ≈ O(1) | O(n) | Connected components |

---

## Problem List by Pattern

| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Two Sum | Hash Map | Easy |
| 15 | 3Sum | Two Pointers | Medium |
| 20 | Valid Parentheses | Stack | Easy |
| 22 | Generate Parentheses | Backtracking | Medium |
| 23 | Merge K Sorted Lists | Heap | Hard |
| 26 | Remove Duplicates from Sorted Array | Two Pointers | Easy |
| 33 | Search in Rotated Sorted Array | Binary Search | Medium |
| 35 | Search Insert Position | Binary Search | Easy |
| 39 | Combination Sum | Backtracking | Medium |
| 40 | Combination Sum II | Backtracking | Medium |
| 46 | Permutations | Backtracking | Medium |
| 49 | Group Anagrams | Hash Map | Medium |
| 51 | N-Queens | Backtracking | Hard |
| 70 | Climbing Stairs | DP | Easy |
| 74 | Search a 2D Matrix | Binary Search | Medium |
| 78 | Subsets | Backtracking | Medium |
| 84 | Largest Rectangle in Histogram | Stack | Hard |
| 102 | Binary Tree Level Order Traversal | BFS | Medium |
| 104 | Maximum Depth of Binary Tree | DFS | Easy |
| 112 | Path Sum | DFS | Easy |
| 121 | Best Time to Buy and Sell Stock | Sliding Window | Easy |
| 125 | Valid Palindrome | Two Pointers | Easy |
| 127 | Word Ladder | BFS | Hard |
| 128 | Longest Consecutive Sequence | Hash Set | Medium |
| 133 | Clone Graph | DFS | Medium |
| 141 | Linked List Cycle | Fast & Slow | Easy |
| 142 | Linked List Cycle II | Fast & Slow | Medium |
| 150 | Evaluate Reverse Polish Notation | Stack | Medium |
| 153 | Find Minimum in Rotated Sorted Array | Binary Search | Medium |
| 155 | Min Stack | Stack | Medium |
| 167 | Two Sum II | Two Pointers | Medium |
| 198 | House Robber | DP | Medium |
| 200 | Number of Islands | BFS / DFS | Medium |
| 208 | Implement Trie | Trie | Medium |
| 209 | Minimum Size Subarray Sum | Sliding Window | Medium |
| 211 | Design Add and Search Words | Trie | Medium |
| 212 | Word Search II | Trie + DFS | Hard |
| 215 | Kth Largest Element | Heap | Medium |
| 217 | Contains Duplicate | Hash Set | Easy |
| 234 | Palindrome Linked List | Fast & Slow | Easy |
| 242 | Valid Anagram | Hash Map | Easy |
| 287 | Find the Duplicate Number | Fast & Slow | Medium |
| 295 | Find Median from Data Stream | Heap | Hard |
| 300 | Longest Increasing Subsequence | DP | Medium |
| 303 | Range Sum Query | Prefix Sum | Easy |
| 322 | Coin Change | DP | Medium |
| 347 | Top K Frequent Elements | Heap / Hash | Medium |
| 416 | Partition Equal Subset Sum | DP | Medium |
| 417 | Pacific Atlantic Water Flow | DFS | Medium |
| 424 | Longest Repeating Character Replacement | Sliding Window | Medium |
| 525 | Contiguous Array | Prefix Sum | Medium |
| 547 | Number of Provinces | Union Find | Medium |
| 560 | Subarray Sum Equals K | Prefix Sum | Medium |
| 567 | Permutation in String | Sliding Window | Medium |
| 643 | Maximum Average Subarray I | Sliding Window | Easy |
| 684 | Redundant Connection | Union Find | Medium |
| 695 | Max Area of Island | DFS | Medium |
| 704 | Binary Search | Binary Search | Easy |
| 724 | Find Pivot Index | Prefix Sum | Easy |
| 739 | Daily Temperatures | Stack | Medium |
| 875 | Koko Eating Bananas | Binary Search | Medium |
| 876 | Middle of the Linked List | Fast & Slow | Easy |
| 973 | K Closest Points to Origin | Heap | Medium |
| 977 | Squares of a Sorted Array | Two Pointers | Easy |
| 994 | Rotting Oranges | BFS | Medium |
| 1061 | Lexicographically Smallest Equiv String | Union Find | Medium |
| 1143 | Longest Common Subsequence | DP | Medium |

---

## Quick Reference

```
Pattern recognition

Two Pointers      — sorted array, pair/triplet problems, palindrome
Sliding Window    — subarray/substring with max/min length or constraint
Fast & Slow       — linked list cycle, find middle, kth from end
Binary Search     — sorted input, monotonic property, "minimum valid X"
Hash Map/Set      — O(1) lookup, two sum, frequency counts, duplicates
Stack             — matching brackets, next greater element, expression eval
BFS               — shortest path, level-by-level, minimum steps
DFS               — path problems, connected components, backtracking
Backtracking      — all combinations/permutations, constraint satisfaction
DP                — "how many ways", min cost, max profit, overlapping subs
Heap              — top K, Kth largest/smallest, merge K sorted
Prefix Sum        — range sum query, subarray sum equals K
Trie              — prefix search, word dictionary, autocomplete
Union Find        — connected components, cycle detection

Interview tips
  - Say your approach out loud before coding
  - Start with brute force, then optimize
  - Write examples with edge cases before coding
  - Test with empty input, single element, duplicates
  - State time and space complexity when done
```
