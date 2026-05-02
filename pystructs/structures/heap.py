"""MinHeap and MaxHeap backed by heapq."""

from __future__ import annotations

import heapq
from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import EmptyStructureError

T = TypeVar("T")


class MinHeap(Generic[T]):
    """
    Min-heap: smallest element at root.

    push    → O(log n)
    pop     → O(log n)
    peek    → O(1)
    heapify → O(n)
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: list[T] = []

    @classmethod
    def from_iterable(cls, items: list[T]) -> MinHeap[T]:
        h: MinHeap[T] = cls()
        h._data = list(items)
        heapq.heapify(h._data)
        return h

    def push(self, item: T) -> None:
        heapq.heappush(self._data, item)

    def pop(self) -> T:
        if not self._data:
            raise EmptyStructureError("MinHeap")
        return heapq.heappop(self._data)

    def peek(self) -> T:
        if not self._data:
            raise EmptyStructureError("MinHeap")
        return self._data[0]

    def push_pop(self, item: T) -> T:
        """Push then pop in a single O(log n) step."""
        if not self._data:
            return item
        return heapq.heappushpop(self._data, item)

    def nsmallest(self, n: int) -> list[T]:
        return heapq.nsmallest(n, self._data)

    def nlargest(self, n: int) -> list[T]:
        return heapq.nlargest(n, self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(sorted(self._data))

    def __repr__(self) -> str:
        return f"MinHeap(size={len(self._data)}, min={self._data[0] if self._data else None!r})"

    @property
    def is_empty(self) -> bool:
        return not self._data

    def to_list(self) -> list[T]:
        return list(self._data)


class MaxHeap(Generic[T]):
    """
    Max-heap: largest element at root.

    Internally negates values so heapq (min-heap) is reused.

    push    → O(log n)
    pop     → O(log n)
    peek    → O(1)
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: list = []

    @classmethod
    def from_iterable(cls, items: list) -> MaxHeap:
        h: MaxHeap = cls()
        h._data = [-x for x in items]
        heapq.heapify(h._data)
        return h

    def push(self, item) -> None:
        heapq.heappush(self._data, -item)

    def pop(self):
        if not self._data:
            raise EmptyStructureError("MaxHeap")
        return -heapq.heappop(self._data)

    def peek(self):
        if not self._data:
            raise EmptyStructureError("MaxHeap")
        return -self._data[0]

    def nlargest(self, n: int) -> list:
        return [-x for x in heapq.nsmallest(n, self._data)]

    def nsmallest(self, n: int) -> list:
        return [-x for x in heapq.nlargest(n, self._data)]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __iter__(self) -> Iterator:
        return iter(sorted((-x for x in self._data), reverse=True))

    def __repr__(self) -> str:
        top = -self._data[0] if self._data else None
        return f"MaxHeap(size={len(self._data)}, max={top!r})"

    @property
    def is_empty(self) -> bool:
        return not self._data

    def to_list(self) -> list:
        return [-x for x in self._data]
