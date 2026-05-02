"""HashMap and HashSet — extended dict/set wrappers with a Java-inspired API.

Both structures are O(1) average for all core operations.
They wrap Python's native ``dict`` and ``set`` rather than re-implementing
hashing, so they benefit from CPython's highly-optimised hash table.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import KeyNotFoundError

K = TypeVar("K")
Val = TypeVar("Val")


class HashMap(Generic[K, Val]):
    """
    dict wrapper with an extended, ergonomic API.

    Adds: ``get_or_default``, ``put_if_absent``, ``merge``, ``compute_if_absent``.

    All operations: O(1) average.

    Examples
    --------
    >>> m = HashMap()
    >>> m.put("a", 1)
    >>> m.get_or_default("b", 0)
    0
    >>> m.put_if_absent("a", 99)  # won't overwrite
    1
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: dict[K, Val] = {}

    # ── Mutation ──────────────────────────────────────────────────────────

    def put(self, key: K, value: Val) -> None:
        """Insert or overwrite ``key → value``."""
        self._data[key] = value

    def put_if_absent(self, key: K, value: Val) -> Val:
        """Insert ``key → value`` only if ``key`` is absent; return current value."""
        if key not in self._data:
            self._data[key] = value
        return self._data[key]

    def merge(self, key: K, value: Val, remapping_fn) -> Val:
        """
        If ``key`` is absent, store ``value``.
        Otherwise, store ``remapping_fn(old, value)`` and return it.
        """
        if key not in self._data:
            self._data[key] = value
        else:
            self._data[key] = remapping_fn(self._data[key], value)
        return self._data[key]

    def compute_if_absent(self, key: K, mapping_fn) -> Val:
        """Compute and store a value for ``key`` if not already present."""
        if key not in self._data:
            self._data[key] = mapping_fn(key)
        return self._data[key]

    def remove(self, key: K) -> Val:
        """Remove and return ``key``'s value; raises ``KeyNotFoundError`` if absent."""
        try:
            return self._data.pop(key)
        except KeyError:
            raise KeyNotFoundError(key) from None

    def clear(self) -> None:
        self._data.clear()

    # ── Query ─────────────────────────────────────────────────────────────

    def get(self, key: K) -> Val:
        """Return value for ``key``; raises ``KeyNotFoundError`` if absent."""
        try:
            return self._data[key]
        except KeyError:
            raise KeyNotFoundError(key) from None

    def get_or_default(self, key: K, default: Val) -> Val:
        """Return value for ``key`` or ``default`` if absent."""
        return self._data.get(key, default)

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    # ── Dunder ────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"HashMap({self._data!r})"

    def to_list(self) -> list:
        return list(self._data.items())


class HashSet(Generic[K]):
    """
    set wrapper with bulk operations and a fluent set-algebra API.

    Examples
    --------
    >>> s = HashSet()
    >>> s.add_all([1, 2, 3])
    >>> t = HashSet(); t.add_all([2, 3, 4])
    >>> list(s.intersection(t))
    [2, 3]
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: set[K] = set()

    # ── Mutation ──────────────────────────────────────────────────────────

    def add(self, item: K) -> None:
        self._data.add(item)

    def add_all(self, items) -> None:
        self._data.update(items)

    def remove(self, item: K) -> None:
        """Remove item (no-op if absent)."""
        self._data.discard(item)

    def clear(self) -> None:
        self._data.clear()

    # ── Set algebra ───────────────────────────────────────────────────────

    def union(self, other: HashSet[K]) -> HashSet[K]:
        result: HashSet[K] = HashSet()
        result._data = self._data | other._data
        return result

    def intersection(self, other: HashSet[K]) -> HashSet[K]:
        result: HashSet[K] = HashSet()
        result._data = self._data & other._data
        return result

    def difference(self, other: HashSet[K]) -> HashSet[K]:
        result: HashSet[K] = HashSet()
        result._data = self._data - other._data
        return result

    def is_subset_of(self, other: HashSet[K]) -> bool:
        return self._data.issubset(other._data)

    # ── Query ─────────────────────────────────────────────────────────────

    def contains(self, item: K) -> bool:
        return item in self._data

    # ── Dunder ────────────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"HashSet({self._data!r})"

    def to_list(self) -> list:
        return list(self._data)
