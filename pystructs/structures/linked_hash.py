"""LinkedHashMap and LinkedHashSet — insertion-order preserved O(1) ops."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import KeyNotFoundError

K = TypeVar("K")
V = TypeVar("V")


class LinkedHashMap(Generic[K, V]):
    """
    dict + doubly-linked list preserving insertion order.

    All ops O(1) average. Iteration in insertion order.
    """

    __slots__ = ("_data", "_order")

    def __init__(self) -> None:
        self._data: dict[K, V] = {}
        self._order: list[K] = []

    def put(self, key: K, value: V) -> None:
        if key not in self._data:
            self._order.append(key)
        self._data[key] = value

    def get(self, key: K) -> V:
        try:
            return self._data[key]
        except KeyError:
            raise KeyNotFoundError(key) from None

    def get_or_default(self, key: K, default: V) -> V:
        return self._data.get(key, default)

    def remove(self, key: K) -> V:
        try:
            value = self._data.pop(key)
            self._order.remove(key)
            return value
        except KeyError:
            raise KeyNotFoundError(key) from None

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def keys(self) -> list[K]:
        return list(self._order)

    def values(self) -> list[V]:
        return [self._data[k] for k in self._order]

    def items(self) -> list[tuple[K, V]]:
        return [(k, self._data[k]) for k in self._order]

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[K]:
        return iter(self._order)

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k!r}: {self._data[k]!r}" for k in self._order)
        return f"LinkedHashMap({{{pairs}}})"


class LinkedHashSet(Generic[K]):
    """Insertion-order preserving set. O(1) average for add/remove/contains."""

    __slots__ = ("_map",)

    def __init__(self) -> None:
        self._map: LinkedHashMap[K, None] = LinkedHashMap()

    def add(self, item: K) -> None:
        self._map.put(item, None)

    def add_all(self, items) -> None:
        for item in items:
            self.add(item)

    def remove(self, item: K) -> None:
        self._map.remove(item)

    def contains(self, item: K) -> bool:
        return self._map.contains_key(item)

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, item: object) -> bool:
        return item in self._map

    def __iter__(self) -> Iterator[K]:
        return iter(self._map)

    def __repr__(self) -> str:
        return f"LinkedHashSet({self._map.keys()!r})"

    def to_list(self) -> list[K]:
        return self._map.keys()
