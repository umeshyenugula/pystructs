"""Singly and Doubly Linked Lists."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import EmptyStructureError

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Singly Linked List
# ---------------------------------------------------------------------------


class _SNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _SNode[T] | None = None


class SinglyLinkedList(Generic[T]):
    """
    Singly linked list with O(1) head/tail insert and O(n) search.

    Extras: cycle detection, reverse (iterative), find middle (fast/slow).
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self) -> None:
        self._head: _SNode[T] | None = None
        self._tail: _SNode[T] | None = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def append(self, value: T) -> None:
        node = _SNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        node = _SNode(value)
        node.next = self._head
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def extend(self, items: list[T]) -> None:
        for item in items:
            self.append(item)

    # ------------------------------------------------------------------
    # Remove
    # ------------------------------------------------------------------

    def pop_front(self) -> T:
        if self._head is None:
            raise EmptyStructureError("SinglyLinkedList")
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return value

    def remove(self, value: T) -> bool:
        prev: _SNode[T] | None = None
        curr = self._head
        while curr is not None:
            if curr.value == value:
                if prev is None:
                    self._head = curr.next
                else:
                    prev.next = curr.next
                if curr.next is None:
                    self._tail = prev
                self._size -= 1
                return True
            prev, curr = curr, curr.next
        return False

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------

    def reverse(self) -> None:
        prev: _SNode[T] | None = None
        curr = self._head
        self._tail = self._head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self._head = prev

    def find_middle(self) -> T | None:
        slow = self._head
        fast = self._head
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
        return slow.value if slow else None

    def has_cycle(self) -> bool:
        slow = self._head
        fast = self._head
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __contains__(self, value: object) -> bool:
        curr = self._head
        while curr is not None:
            if curr.value == value:
                return True
            curr = curr.next
        return False

    def __iter__(self) -> Iterator[T]:
        curr = self._head
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __repr__(self) -> str:
        return " -> ".join(str(v) for v in self) + " -> None"

    def to_list(self) -> list[T]:
        return list(self)

    @property
    def is_empty(self) -> bool:
        return self._size == 0


# ---------------------------------------------------------------------------
# Doubly Linked List
# ---------------------------------------------------------------------------


class _DNode(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.prev: _DNode[T] | None = None
        self.next: _DNode[T] | None = None


class DoublyLinkedList(Generic[T]):
    """
    Doubly linked list with O(1) head/tail operations.
    """

    __slots__ = ("_head", "_tail", "_size")

    def __init__(self) -> None:
        self._head: _DNode[T] | None = None
        self._tail: _DNode[T] | None = None
        self._size: int = 0

    def append(self, value: T) -> None:
        node = _DNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value: T) -> None:
        node = _DNode(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def pop_back(self) -> T:
        if self._tail is None:
            raise EmptyStructureError("DoublyLinkedList")
        value = self._tail.value
        if self._tail.prev is None:
            self._head = self._tail = None
        else:
            self._tail = self._tail.prev
            self._tail.next = None
        self._size -= 1
        return value

    def pop_front(self) -> T:
        if self._head is None:
            raise EmptyStructureError("DoublyLinkedList")
        value = self._head.value
        if self._head.next is None:
            self._head = self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None
        self._size -= 1
        return value

    def remove(self, value: T) -> bool:
        curr = self._head
        while curr is not None:
            if curr.value == value:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self._head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self._tail = curr.prev
                self._size -= 1
                return True
            curr = curr.next
        return False

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __contains__(self, value: object) -> bool:
        curr = self._head
        while curr is not None:
            if curr.value == value:
                return True
            curr = curr.next
        return False

    def __iter__(self) -> Iterator[T]:
        curr = self._head
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __reversed__(self) -> Iterator[T]:
        curr = self._tail
        while curr is not None:
            yield curr.value
            curr = curr.prev

    def __repr__(self) -> str:
        return "None <-> " + " <-> ".join(str(v) for v in self) + " <-> None"

    def to_list(self) -> list[T]:
        return list(self)

    @property
    def is_empty(self) -> bool:
        return self._size == 0
