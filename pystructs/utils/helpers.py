"""Utility helpers."""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def chunk(iterable: Iterable[T], size: int) -> Iterable[list[T]]:
    """Yield successive chunks of given size from iterable."""
    buf: list[T] = []
    for item in iterable:
        buf.append(item)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf


def flatten(nested: Iterable) -> list:
    """Flatten one level of nesting."""
    result = []
    for item in nested:
        try:
            result.extend(item)
        except TypeError:
            result.append(item)
    return result


def random_list(n: int, lo: int = 0, hi: int = 10_000) -> list[int]:
    """Generate a random integer list of length n."""
    return [random.randint(lo, hi) for _ in range(n)]


def is_sorted(arr: list, key: Callable | None = None, reverse: bool = False) -> bool:
    """Check if a list is sorted."""
    _key = key or (lambda x: x)
    for i in range(len(arr) - 1):
        a, b = _key(arr[i]), _key(arr[i + 1])
        if not reverse and a > b:
            return False
        if reverse and a < b:
            return False
    return True


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp value between lo and hi."""
    return max(lo, min(hi, value))
