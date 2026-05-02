"""Queue and Deque — backed by collections.deque for O(1) ends."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import EmptyStructureError, InvalidInputError

T = TypeVar("T")


class Queue(Generic[T]):
    """
    FIFO queue.

    enqueue  → O(1)
    dequeue  → O(1)
    peek     → O(1)
    """

    __slots__ = ("_data", "_maxsize")

    def __init__(self, maxsize: int = 0) -> None:
        if maxsize < 0:
            raise InvalidInputError("maxsize must be >= 0.")
        self._data: deque[T] = deque()
        self._maxsize = maxsize

    def enqueue(self, item: T) -> None:
        if self._maxsize and len(self._data) >= self._maxsize:
            from pystructs.core.exceptions import StructureOverflowError as DSAOverflow

            raise DSAOverflow("Queue", self._maxsize)
        self._data.append(item)

    def dequeue(self) -> T:
        if not self._data:
            raise EmptyStructureError("Queue")
        return self._data.popleft()

    def peek(self) -> T:
        if not self._data:
            raise EmptyStructureError("Queue")
        return self._data[0]

    def enqueue_all(self, items: list[T]) -> None:
        for item in items:
            self.enqueue(item)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)!r})"

    @property
    def is_empty(self) -> bool:
        return not self._data

    def clear(self) -> None:
        self._data.clear()

    def to_list(self) -> list[T]:
        return list(self._data)


class Deque(Generic[T]):
    """
    Double-ended queue.

    push_front / push_back  → O(1)
    pop_front  / pop_back   → O(1)
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: deque[T] = deque()

    def push_front(self, item: T) -> None:
        self._data.appendleft(item)

    def push_back(self, item: T) -> None:
        self._data.append(item)

    def pop_front(self) -> T:
        if not self._data:
            raise EmptyStructureError("Deque")
        return self._data.popleft()

    def pop_back(self) -> T:
        if not self._data:
            raise EmptyStructureError("Deque")
        return self._data.pop()

    def peek_front(self) -> T:
        if not self._data:
            raise EmptyStructureError("Deque")
        return self._data[0]

    def peek_back(self) -> T:
        if not self._data:
            raise EmptyStructureError("Deque")
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Deque({list(self._data)!r})"

    @property
    def is_empty(self) -> bool:
        return not self._data

    def clear(self) -> None:
        self._data.clear()

    def to_list(self) -> list[T]:
        return list(self._data)
