"""AVL Tree-based TreeMap and TreeSet — O(log n) operations."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import EmptyStructureError, KeyNotFoundError

K = TypeVar("K")
V = TypeVar("V")


class _AVLNode(Generic[K, V]):
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key: K, value: V) -> None:
        self.key: K = key
        self.value: V = value
        self.left: _AVLNode[K, V] | None = None
        self.right: _AVLNode[K, V] | None = None
        self.height: int = 1


def _height(node: _AVLNode | None) -> int:
    return node.height if node else 0


def _update_height(node: _AVLNode) -> None:
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node: _AVLNode) -> int:
    return _height(node.left) - _height(node.right)


def _rotate_right(y: _AVLNode) -> _AVLNode:
    x = y.left  # type: ignore[assignment]
    t = x.right
    x.right = y
    y.left = t
    _update_height(y)
    _update_height(x)
    return x


def _rotate_left(x: _AVLNode) -> _AVLNode:
    y = x.right  # type: ignore[assignment]
    t = y.left
    y.left = x
    x.right = t
    _update_height(x)
    _update_height(y)
    return y


def _rebalance(node: _AVLNode) -> _AVLNode:
    _update_height(node)
    bf = _balance_factor(node)
    if bf > 1:
        if _balance_factor(node.left) < 0:  # type: ignore[arg-type]
            node.left = _rotate_left(node.left)  # type: ignore[arg-type]
        return _rotate_right(node)
    if bf < -1:
        if _balance_factor(node.right) > 0:  # type: ignore[arg-type]
            node.right = _rotate_right(node.right)  # type: ignore[arg-type]
        return _rotate_left(node)
    return node


class TreeMap(Generic[K, V]):
    """
    Self-balancing AVL tree map.

    put     → O(log n)
    get     → O(log n)
    delete  → O(log n)
    min/max → O(log n)
    """

    __slots__ = ("_root", "_size")

    def __init__(self) -> None:
        self._root: _AVLNode[K, V] | None = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def put(self, key: K, value: V) -> None:
        inserted = [False]
        self._root = self._insert(self._root, key, value, inserted)
        if inserted[0]:
            self._size += 1

    def get(self, key: K) -> V:
        node = self._find(self._root, key)
        if node is None:
            raise KeyNotFoundError(key)
        return node.value

    def get_or_default(self, key: K, default: V) -> V:
        node = self._find(self._root, key)
        return node.value if node else default

    def delete(self, key: K) -> None:
        deleted = [False]
        self._root = self._delete(self._root, key, deleted)
        if deleted[0]:
            self._size -= 1
        else:
            raise KeyNotFoundError(key)

    def contains_key(self, key: K) -> bool:
        return self._find(self._root, key) is not None

    def min_key(self) -> K:
        if self._root is None:
            raise EmptyStructureError("TreeMap")
        return self._min_node(self._root).key

    def max_key(self) -> K:
        if self._root is None:
            raise EmptyStructureError("TreeMap")
        return self._max_node(self._root).key

    def keys(self) -> list[K]:
        return [k for k, _ in self._inorder()]

    def values(self) -> list[V]:
        return [v for _, v in self._inorder()]

    def items(self) -> list[tuple[K, V]]:
        return list(self._inorder())

    # ------------------------------------------------------------------
    # Private helpers (iterative where possible)
    # ------------------------------------------------------------------

    def _find(self, node: _AVLNode[K, V] | None, key: K) -> _AVLNode[K, V] | None:
        while node is not None:
            if key < node.key:  # type: ignore[operator]
                node = node.left
            elif key > node.key:  # type: ignore[operator]
                node = node.right
            else:
                return node
        return None

    def _insert(
        self,
        node: _AVLNode[K, V] | None,
        key: K,
        value: V,
        inserted: list,
    ) -> _AVLNode[K, V]:
        if node is None:
            inserted[0] = True
            return _AVLNode(key, value)
        if key < node.key:  # type: ignore[operator]
            node.left = self._insert(node.left, key, value, inserted)
        elif key > node.key:  # type: ignore[operator]
            node.right = self._insert(node.right, key, value, inserted)
        else:
            node.value = value
        return _rebalance(node)

    def _delete(
        self,
        node: _AVLNode[K, V] | None,
        key: K,
        deleted: list,
    ) -> _AVLNode[K, V] | None:
        if node is None:
            return None
        if key < node.key:  # type: ignore[operator]
            node.left = self._delete(node.left, key, deleted)
        elif key > node.key:  # type: ignore[operator]
            node.right = self._delete(node.right, key, deleted)
        else:
            deleted[0] = True
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key, [True])
        return _rebalance(node)

    def _min_node(self, node: _AVLNode[K, V]) -> _AVLNode[K, V]:
        while node.left is not None:
            node = node.left
        return node

    def _max_node(self, node: _AVLNode[K, V]) -> _AVLNode[K, V]:
        while node.right is not None:
            node = node.right
        return node

    def _inorder(self) -> Iterator[tuple[K, V]]:
        stack: list[_AVLNode[K, V]] = []
        curr = self._root
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            yield curr.key, curr.value
            curr = curr.right

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: object) -> bool:
        return self._find(self._root, key) is not None  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[K]:
        return (k for k, _ in self._inorder())

    def __repr__(self) -> str:
        return f"TreeMap(size={self._size})"


class TreeSet(Generic[K]):
    """Sorted set built on TreeMap — O(log n) add/remove/contains."""

    __slots__ = ("_map",)

    def __init__(self) -> None:
        self._map: TreeMap[K, None] = TreeMap()

    def add(self, key: K) -> None:
        self._map.put(key, None)

    def add_all(self, items) -> None:
        for item in items:
            self.add(item)

    def remove(self, key: K) -> None:
        self._map.delete(key)

    def contains(self, key: K) -> bool:
        return self._map.contains_key(key)

    def min_key(self) -> K:
        return self._map.min_key()

    def max_key(self) -> K:
        return self._map.max_key()

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: object) -> bool:
        return self._map.contains_key(key)  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[K]:
        return iter(self._map)

    def __repr__(self) -> str:
        return f"TreeSet(size={len(self._map)})"

    def to_list(self) -> list[K]:
        return self._map.keys()
