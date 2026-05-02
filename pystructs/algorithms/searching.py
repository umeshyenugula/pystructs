"""Searching algorithms using bisect for binary search."""

from __future__ import annotations

import bisect
from collections.abc import Callable
from typing import TypeVar

from pystructs.core.complexity import complexity
from pystructs.core.exceptions import InvalidInputError

T = TypeVar("T")


@complexity(
    time_best="O(1)",
    time_average="O(log n)",
    time_worst="O(log n)",
    space="O(1)",
    notes="Requires sorted input",
)
def binary_search(arr: list[T], target: T, key: Callable | None = None) -> int:
    """
    Binary search using bisect. Returns index or -1 if not found.
    Input must be sorted.
    """
    if not isinstance(arr, list):
        raise InvalidInputError("arr must be a list.")
    if key is None:
        idx = bisect.bisect_left(arr, target)
    else:
        keys = [key(x) for x in arr]
        target_key = key(target)
        idx = bisect.bisect_left(keys, target_key)
    if idx < len(arr) and (key(arr[idx]) if key else arr[idx]) == (key(target) if key else target):
        return idx
    return -1


@complexity(
    time_best="O(1)",
    time_average="O(log n)",
    time_worst="O(log n)",
    space="O(1)",
    notes="Returns insertion point for sorted maintenance",
)
def binary_search_leftmost(arr: list[T], target: T) -> int:
    """Returns the leftmost insertion index (bisect_left)."""
    return bisect.bisect_left(arr, target)


@complexity(
    time_best="O(1)",
    time_average="O(log n)",
    time_worst="O(log n)",
    space="O(1)",
)
def binary_search_rightmost(arr: list[T], target: T) -> int:
    """Returns the rightmost insertion index (bisect_right)."""
    return bisect.bisect_right(arr, target)


@complexity(
    time_best="O(1)",
    time_average="O(n)",
    time_worst="O(n)",
    space="O(1)",
)
def linear_search(arr: list[T], target: T, key: Callable | None = None) -> int:
    """Linear search. Returns index or -1."""
    _key = key or (lambda x: x)
    target_key = key(target) if key else target
    for i, item in enumerate(arr):
        if _key(item) == target_key:
            return i
    return -1


@complexity(
    time_best="O(log log n)",
    time_average="O(log log n)",
    time_worst="O(n)",
    space="O(1)",
    notes="Only for uniformly distributed sorted data",
)
def interpolation_search(arr: list[int], target: int) -> int:
    """Interpolation search for uniformly distributed integer arrays."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[hi] == arr[lo]:
            if arr[lo] == target:
                return lo
            break
        pos = lo + ((target - arr[lo]) * (hi - lo)) // (arr[hi] - arr[lo])
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1
