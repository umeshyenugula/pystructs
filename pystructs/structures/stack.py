"""Stack — LIFO data structure backed by a Python list."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import EmptyStructureError, InvalidInputError

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Thread-unsafe LIFO stack.

    push  → O(1) amortised
    pop   → O(1) amortised
    peek  → O(1)
    """

    __slots__ = ("_data", "_maxsize")

    def __init__(self, maxsize: int = 0) -> None:
        if maxsize < 0:
            raise InvalidInputError("maxsize must be >= 0 (0 = unlimited).")
        self._data: list[T] = []
        self._maxsize: int = maxsize

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def push(self, item: T) -> None:
        if self._maxsize and len(self._data) >= self._maxsize:
            from pystructs.core.exceptions import StructureOverflowError as DSAOverflow

            raise DSAOverflow("Stack", self._maxsize)
        self._data.append(item)

    def pop(self) -> T:
        if not self._data:
            raise EmptyStructureError("Stack")
        return self._data.pop()

    def peek(self) -> T:
        if not self._data:
            raise EmptyStructureError("Stack")
        return self._data[-1]

    def push_all(self, items: list[T]) -> None:
        for item in items:
            self.push(item)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[T]:
        return reversed(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @property
    def is_empty(self) -> bool:
        return not self._data

    def clear(self) -> None:
        self._data.clear()

    def to_list(self) -> list[T]:
        return list(reversed(self._data))
