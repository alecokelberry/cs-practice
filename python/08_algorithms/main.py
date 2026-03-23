# ─────────────────────────────────────────────────────────────
#  Lesson 08 — Algorithms
#  Run: python main.py
# ─────────────────────────────────────────────────────────────

import bisect
import time
from collections.abc import Callable


# ── BIG-O VISUALIZATION ───────────────────────────────────────
print("── Big-O: growth rates ──────────────────────")

# These aren't algorithm implementations — they show how different complexities
# SCALE as n grows. This is what Big-O is really about.
import math

print(f"  {'n':>8} {'O(1)':>8} {'O(log n)':>10} {'O(n)':>8} {'O(n log n)':>12} {'O(n²)':>10}")
print("  " + "-" * 60)
for n in [10, 100, 1_000, 10_000]:
    print(
        f"  {n:>8,} "
        f"{'1':>8} "
        f"{math.log2(n):>10.1f} "
        f"{n:>8,} "
        f"{n * math.log2(n):>12,.0f} "
        f"{n**2:>10,}"
    )
print()
print("  At n=10,000: O(n²) is 1,000,000 steps; O(log n) is only 13.")


# ── LINEAR SEARCH — O(n) ──────────────────────────────────────
print("\n── linear search — O(n) ─────────────────────")

def linear_search(lst: list[int], target: int) -> int:
    """
    Search for target by checking every element.

    Time:  O(n) — worst case, target is last or not present
    Space: O(1) — no extra memory
    When to use: small lists, or unsorted lists where you can't sort first.
    """
    for i, val in enumerate(lst):
        if val == target:
            return i     # return index on first match
    return -1            # -1 = not found (convention)

data = [7, 3, 9, 1, 5, 8, 2, 6, 4]
print(f"  data: {data}")
print(f"  find 8:  index {linear_search(data, 8)}")
print(f"  find 99: index {linear_search(data, 99)}")


# ── BINARY SEARCH — O(log n) ──────────────────────────────────
print("\n── binary search — O(log n) ─────────────────")

def binary_search(lst: list[int], target: int) -> int:
    """
    Search a SORTED list by repeatedly halving the search space.

    Time:  O(log n) — with n=1,000,000, this is ~20 comparisons
    Space: O(1)
    Requirement: list MUST be sorted. Undefined behavior on unsorted input.
    """
    lo: int = 0
    hi: int = len(lst) - 1

    while lo <= hi:              # continue while search space is valid
        mid = (lo + hi) // 2    # integer midpoint — never risks float issues
        if lst[mid] == target:
            return mid           # found
        elif lst[mid] < target:
            lo = mid + 1         # target must be in the RIGHT half — discard left
        else:
            hi = mid - 1         # target must be in the LEFT half — discard right

    return -1   # loop ended without finding target

sorted_data = sorted(data)
print(f"  sorted data: {sorted_data}")
print(f"  find 8:  index {binary_search(sorted_data, 8)}")
print(f"  find 99: index {binary_search(sorted_data, 99)}")

# Recursive version — same logic, shows the "divide and conquer" pattern clearly
def binary_search_recursive(lst: list[int], target: int,
                             lo: int = 0, hi: int = -1) -> int:
    """Recursive binary search. hi=-1 means 'use end of list'."""
    if hi == -1:
        hi = len(lst) - 1

    if lo > hi:          # base case: empty search space
        return -1

    mid = (lo + hi) // 2
    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return binary_search_recursive(lst, target, mid + 1, hi)  # search right
    else:
        return binary_search_recursive(lst, target, lo, mid - 1)  # search left

print(f"  recursive find 5: index {binary_search_recursive(sorted_data, 5)}")

# Python stdlib: bisect — use this in real code
# bisect_left returns the insertion point for target in a sorted list
idx = bisect.bisect_left(sorted_data, 8)
found = idx < len(sorted_data) and sorted_data[idx] == 8
print(f"  bisect find 8: index {idx if found else -1}")


# ── BUBBLE SORT — O(n²) ───────────────────────────────────────
print("\n── bubble sort — O(n²) ──────────────────────")

def bubble_sort(lst: list[int]) -> list[int]:
    """
    Repeatedly compare adjacent pairs and swap if out of order.
    After each full pass, the largest unsorted element "bubbles" to its position.

    Time:  O(n²) — never use in production for n > ~1000
    Space: O(n) — creates a copy
    Purpose: understanding sorting — shows why comparison-based O(n²) is slow.
    """
    arr = lst[:]       # work on a copy — don't mutate the input
    n = len(arr)

    for i in range(n):
        swapped = False
        # Each pass puts the largest remaining element in its correct spot.
        # The last i elements are already sorted, so we only go to n-i-1.
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Pythonic swap — no temp variable needed
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            # Early exit: if no swaps happened, the list is already sorted
            break

    return arr

unsorted = [64, 34, 25, 12, 22, 11, 90]
print(f"  input:  {unsorted}")
print(f"  sorted: {bubble_sort(unsorted)}")


# ── PYTHON'S SORTED() — TIMSORT O(n log n) ───────────────────
print("\n── sorted() — Timsort, O(n log n) ──────────")

# Timsort is a hybrid of merge sort and insertion sort.
# It's adaptive (fast on partially-sorted data) and stable (equal elements keep order).
# ALWAYS use this in real code instead of implementing your own sort.

nums = [5, 2, 8, 1, 9, 3, 7, 4, 6]
print(f"  sorted():                {sorted(nums)}")
print(f"  sorted(reverse=True):    {sorted(nums, reverse=True)}")

# key= function — what to sort BY (doesn't change what's returned)
words = ["banana", "Apple", "cherry", "date", "Elderberry"]
print(f"  case-insensitive:        {sorted(words, key=str.lower)}")
print(f"  by length:               {sorted(words, key=len)}")
print(f"  by length desc, alpha:   {sorted(words, key=lambda w: (-len(w), w.lower()))}")

# Sorting custom objects
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    gpa: float
    year: int

students = [
    Student("Alice", 3.8, 3),
    Student("Bob", 3.5, 2),
    Student("Carol", 3.8, 2),
    Student("Dave", 3.2, 4),
]

# Sort by GPA descending, then name ascending (multi-key sort)
ranked = sorted(students, key=lambda s: (-s.gpa, s.name))
print("\n  Students ranked by GPA (desc), then name:")
for s in ranked:
    print(f"    {s.name:8} GPA={s.gpa} Year={s.year}")


# ── MERGE SORT — O(n log n) ───────────────────────────────────
print("\n── merge sort — O(n log n) ──────────────────")

def merge_sort(lst: list[int]) -> list[int]:
    """
    Divide and conquer:
    1. Split list in half (recursively until each half has 1 element)
    2. Merge the sorted halves back together

    Time:  O(n log n) — log n levels of splitting, O(n) work to merge each level
    Space: O(n) — creates new lists during merge
    """
    if len(lst) <= 1:
        return lst[:]   # base case: a list of 0 or 1 is already sorted

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])    # recursively sort left half
    right = merge_sort(lst[mid:])   # recursively sort right half
    return _merge(left, right)      # merge two sorted halves

def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list — O(n)."""
    result: list[int] = []
    i = j = 0

    # Compare front elements of each list, take the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One list might have leftover elements — append them all
    result.extend(left[i:])
    result.extend(right[j:])
    return result

data = [38, 27, 43, 3, 9, 82, 10]
print(f"  input:  {data}")
print(f"  sorted: {merge_sort(data)}")

# Verify correctness
import random
random.seed(42)
test = random.sample(range(1000), 20)
assert merge_sort(test) == sorted(test), "merge_sort disagrees with sorted()"
print("  Verified: merge_sort matches sorted() on 20 random elements")


# ── RECURSION AND THE CALL STACK ──────────────────────────────
print("\n── recursion and the call stack ─────────────")

def factorial(n: int) -> int:
    """
    Classic recursion example.
    Each call adds a frame to the call stack. Python's default limit is 1000 frames.
    For deep recursion, use iteration or sys.setrecursionlimit (carefully).
    """
    if n <= 1:          # BASE CASE — must always have one; without it → infinite recursion
        return 1
    return n * factorial(n - 1)   # RECURSIVE CASE — moves toward base case

# Call trace for factorial(4):
# factorial(4) = 4 * factorial(3)
#   factorial(3) = 3 * factorial(2)
#     factorial(2) = 2 * factorial(1)
#       factorial(1) = 1     ← base case
#     = 2 * 1 = 2
#   = 3 * 2 = 6
# = 4 * 6 = 24

for n in range(8):
    print(f"  factorial({n}) = {factorial(n)}")


def flatten(nested: list) -> list:
    """
    Recursively flatten a nested list — shows recursion with variable depth.
    Works for any depth of nesting.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))   # recurse into sub-list
        else:
            result.append(item)
    return result

nested = [1, [2, 3], [4, [5, 6]], 7, [[8, 9], 10]]
print(f"\n  flatten({nested})")
print(f"  result: {flatten(nested)}")


# ── TWO-POINTER TECHNIQUE ─────────────────────────────────────
print("\n── two-pointer technique ────────────────────")

# Two pointers that move toward each other (or same direction) to solve
# problems in O(n) that would naively be O(n²).

def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    """
    Find indices of two numbers that sum to target in a SORTED array.
    Time: O(n) — each pointer moves at most n times
    Space: O(1)

    Why two pointers work: if sum is too small, moving lo right increases it.
    If sum is too large, moving hi left decreases it. We can't miss a valid pair.
    """
    lo, hi = 0, len(arr) - 1

    while lo < hi:        # stop when pointers meet — pair must have two different elements
        current_sum = arr[lo] + arr[hi]
        if current_sum == target:
            return lo, hi
        elif current_sum < target:
            lo += 1       # sum too small — increase it by moving left pointer right
        else:
            hi -= 1       # sum too large — decrease it by moving right pointer left

    return None

sorted_nums = [1, 3, 5, 7, 9, 11, 15, 20]
target = 16
result = two_sum_sorted(sorted_nums, target)
if result:
    lo, hi = result
    print(f"  two_sum({sorted_nums}, {target})")
    print(f"  Found: indices {result} → {sorted_nums[lo]} + {sorted_nums[hi]} = {target}")

# Two-pointer: check if a string is a palindrome
def is_palindrome(s: str) -> bool:
    """
    Check palindrome without reversing the string.
    Time: O(n), Space: O(1)
    """
    s = s.lower()
    lo, hi = 0, len(s) - 1

    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1

    return True

for word in ["racecar", "hello", "madam", "python", "level"]:
    print(f"  is_palindrome({word!r}): {is_palindrome(word)}")


# ── SLIDING WINDOW TECHNIQUE ──────────────────────────────────
print("\n── sliding window technique ─────────────────")

def max_subarray_sum(arr: list[int], k: int) -> tuple[int, int, int]:
    """
    Find the maximum sum of any k consecutive elements.
    Time: O(n) — compute first window, then slide one element at a time
    Space: O(1)

    Returns: (max_sum, start_index, end_index)

    Naive O(n²): recalculate sum from scratch for each window position.
    Sliding O(n): subtract the element leaving the window, add the one entering.
    """
    if k > len(arr):
        raise ValueError(f"k={k} is larger than array length {len(arr)}")

    # Compute the first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    max_start = 0

    # Slide the window: move right edge forward, update sum
    for i in range(k, len(arr)):
        window_sum += arr[i]        # add incoming element (right edge)
        window_sum -= arr[i - k]    # remove outgoing element (left edge) — key insight
        if window_sum > max_sum:
            max_sum = window_sum
            max_start = i - k + 1  # window starts here

    return max_sum, max_start, max_start + k - 1

arr = [2, 1, 5, 1, 3, 2, 8, 1, 4]
k = 3
total, start, end = max_subarray_sum(arr, k)
print(f"  array: {arr}")
print(f"  max sum of {k} consecutive: {total} at indices [{start}:{end+1}] = {arr[start:end+1]}")

# Sliding window: longest substring with at most 2 distinct characters
def longest_substr_two_distinct(s: str) -> int:
    """
    Sliding window with variable width — expand right, contract left when invalid.
    Time: O(n), Space: O(1) — window maps at most 3 distinct chars at any time.
    """
    if len(s) <= 2:
        return len(s)

    freq: dict[str, int] = {}
    lo = 0
    max_len = 0

    for hi, char in enumerate(s):
        freq[char] = freq.get(char, 0) + 1       # expand window right

        while len(freq) > 2:                       # window has too many distinct chars
            left_char = s[lo]
            freq[left_char] -= 1
            if freq[left_char] == 0:
                del freq[left_char]                # remove char that's no longer in window
            lo += 1                                # contract window left

        max_len = max(max_len, hi - lo + 1)       # update best valid window

    return max_len

for test_str in ["eceba", "ccaabbb", "aab"]:
    result = longest_substr_two_distinct(test_str)
    print(f"  longest_substr_two_distinct({test_str!r}): {result}")


# ── PERFORMANCE COMPARISON ────────────────────────────────────
print("\n── performance: linear vs binary search ─────")

import random as rng
rng.seed(0)
big_list = sorted(rng.sample(range(1_000_000), 100_000))
target = big_list[55_000]   # something we know is in the list

def time_it(fn: Callable, *args) -> float:
    """Return execution time in microseconds."""
    start = time.perf_counter()
    fn(*args)
    return (time.perf_counter() - start) * 1_000_000

lin_time = time_it(linear_search, big_list, target)
bin_time = time_it(binary_search, big_list, target)
bis_time = time_it(bisect.bisect_left, big_list, target)

print(f"  n = {len(big_list):,}, target at index 55,000")
print(f"  linear search: {lin_time:8.1f} µs")
print(f"  binary search: {bin_time:8.1f} µs")
print(f"  bisect:        {bis_time:8.1f} µs")
print(f"  speedup (linear/binary): {lin_time/bin_time:.0f}x")


if __name__ == "__main__":
    pass
