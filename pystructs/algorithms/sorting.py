"""Sorting algorithms — all in-place where possible, iterative-first."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from pystructs.core.complexity import complexity
from pystructs.core.exceptions import InvalidInputError

T = TypeVar("T")

_INSERTION_THRESHOLD = 16  # cutoff for hybrid sort


def _check_list(arr: list) -> None:
    if not isinstance(arr, list):
        raise InvalidInputError(f"Expected list, got {type(arr).__name__}.")


# ---------------------------------------------------------------------------
# Insertion sort (O(n²) but fast for small/nearly-sorted arrays)
# ---------------------------------------------------------------------------


@complexity(
    time_best="O(n)",
    time_average="O(n²)",
    time_worst="O(n²)",
    space="O(1)",
    stable=True,
    in_place=True,
)
def insertion_sort(arr: list[T], key: Callable | None = None, reverse: bool = False) -> None:
    """In-place insertion sort."""
    _check_list(arr)
    _key = key or (lambda x: x)
    n = len(arr)
    for i in range(1, n):
        pivot = arr[i]
        pivot_key = _key(pivot)
        j = i - 1
        if not reverse:
            while j >= 0 and _key(arr[j]) > pivot_key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and _key(arr[j]) < pivot_key:
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = pivot


# ---------------------------------------------------------------------------
# Merge sort (stable, O(n log n))
# ---------------------------------------------------------------------------


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(n)",
    stable=True,
    in_place=False,
)
def merge_sort(arr: list[T], key: Callable | None = None, reverse: bool = False) -> None:
    """In-place merge sort (iterative bottom-up)."""
    _check_list(arr)
    _key = key or (lambda x: x)
    n = len(arr)
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            _merge(arr, left, mid, right, _key, reverse)
        width *= 2


def _merge(arr: list, left: int, mid: int, right: int, key, reverse: bool) -> None:
    lpart = arr[left:mid]
    rpart = arr[mid:right]
    i = j = 0
    k = left
    if not reverse:
        while i < len(lpart) and j < len(rpart):
            if key(lpart[i]) <= key(rpart[j]):
                arr[k] = lpart[i]
                i += 1
            else:
                arr[k] = rpart[j]
                j += 1
            k += 1
    else:
        while i < len(lpart) and j < len(rpart):
            if key(lpart[i]) >= key(rpart[j]):
                arr[k] = lpart[i]
                i += 1
            else:
                arr[k] = rpart[j]
                j += 1
            k += 1
    while i < len(lpart):
        arr[k] = lpart[i]
        i += 1
        k += 1
    while j < len(rpart):
        arr[k] = rpart[j]
        j += 1
        k += 1


# ---------------------------------------------------------------------------
# Quick sort (iterative, 3-way partition)
# ---------------------------------------------------------------------------


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n²)",
    space="O(log n)",
    stable=False,
    in_place=True,
    notes="Median-of-three pivot selection",
)
def quick_sort(arr: list[T], key: Callable | None = None, reverse: bool = False) -> None:
    """Iterative 3-way quick sort with median-of-3 pivot."""
    _check_list(arr)
    if len(arr) < 2:
        return
    _key = key or (lambda x: x)
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        if hi - lo < _INSERTION_THRESHOLD:
            _insertion_slice(arr, lo, hi, _key, reverse)
            continue
        p = _partition3(arr, lo, hi, _key, reverse)
        stack.append((lo, p - 1))
        stack.append((p + 1, hi))


def _median_of_three(arr: list, lo: int, hi: int, key) -> int:
    mid = (lo + hi) // 2
    a, b, c = key(arr[lo]), key(arr[mid]), key(arr[hi])
    if a <= b <= c or c <= b <= a:
        return mid
    if b <= a <= c or c <= a <= b:
        return lo
    return hi


def _partition3(arr: list, lo: int, hi: int, key, reverse: bool) -> int:
    pivot_idx = _median_of_three(arr, lo, hi, key)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = key(arr[hi])
    i = lo - 1
    for j in range(lo, hi):
        cmp = key(arr[j]) < pivot if not reverse else key(arr[j]) > pivot
        if cmp:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def _insertion_slice(arr: list, lo: int, hi: int, key, reverse: bool) -> None:
    for i in range(lo + 1, hi + 1):
        pivot = arr[i]
        pivot_key = key(pivot)
        j = i - 1
        if not reverse:
            while j >= lo and key(arr[j]) > pivot_key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= lo and key(arr[j]) < pivot_key:
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = pivot


# ---------------------------------------------------------------------------
# Heap sort
# ---------------------------------------------------------------------------


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(1)",
    stable=False,
    in_place=True,
)
def heap_sort(arr: list[T], key: Callable | None = None, reverse: bool = False) -> None:
    """In-place heap sort."""
    _check_list(arr)
    _key = key or (lambda x: x)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n, _key)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _sift_down(arr, 0, i, _key)
    if reverse:
        arr.reverse()


def _sift_down(arr: list, root: int, end: int, key) -> None:
    while True:
        child = 2 * root + 1
        if child >= end:
            break
        if child + 1 < end and key(arr[child]) < key(arr[child + 1]):
            child += 1
        if key(arr[root]) < key(arr[child]):
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            break


# ---------------------------------------------------------------------------
# Smart sort — hybrid (like Python's Timsort philosophy)
# ---------------------------------------------------------------------------


@complexity(
    time_best="O(n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(n)",
    stable=True,
    in_place=False,
    notes="Delegates to insertion_sort for small inputs, merge_sort otherwise",
)
def smart_sort(arr: list[T], key: Callable | None = None, reverse: bool = False) -> None:
    """
    Hybrid sort: insertion for tiny arrays, merge for larger.
    Nearly optimal for both small and large inputs.
    """
    _check_list(arr)
    n = len(arr)
    if n <= _INSERTION_THRESHOLD:
        insertion_sort(arr, key=key, reverse=reverse)
    else:
        merge_sort(arr, key=key, reverse=reverse)
