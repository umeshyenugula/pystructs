"""Compressed Trie for string operations."""

from __future__ import annotations

from collections.abc import Iterator


class _TrieNode:
    __slots__ = ("children", "is_end", "count")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_end: bool = False
        self.count: int = 0


class Trie:
    """
    Prefix tree for efficient string storage and retrieval.

    insert      → O(m)  where m = word length
    search      → O(m)
    starts_with → O(m)
    delete      → O(m)
    """

    __slots__ = ("_root", "_size")

    def __init__(self) -> None:
        self._root = _TrieNode()
        self._size: int = 0

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
            node.count += 1
        if not node.is_end:
            node.is_end = True
            self._size += 1

    def search(self, word: str) -> bool:
        node = self._root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def delete(self, word: str) -> bool:
        stack: list[tuple] = []
        node = self._root
        for ch in word:
            if ch not in node.children:
                return False
            stack.append((node, ch))
            node = node.children[ch]
        if not node.is_end:
            return False
        node.is_end = False
        self._size -= 1
        for parent, ch in reversed(stack):
            child = parent.children[ch]
            child.count -= 1
            if not child.children and not child.is_end:
                del parent.children[ch]
        return True

    def words_with_prefix(self, prefix: str) -> list[str]:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results: list[str] = []
        self._dfs(node, list(prefix), results)
        return results

    def _dfs(self, node: _TrieNode, path: list[str], results: list[str]) -> None:
        stack = [(node, path)]
        while stack:
            curr, curr_path = stack.pop()
            if curr.is_end:
                results.append("".join(curr_path))
            for ch, child in curr.children.items():
                stack.append((child, curr_path + [ch]))

    def __len__(self) -> int:
        return self._size

    def __contains__(self, word: object) -> bool:
        return self.search(str(word))

    def __iter__(self) -> Iterator[str]:
        results: list[str] = []
        self._dfs(self._root, [], results)
        return iter(sorted(results))

    def __repr__(self) -> str:
        return f"Trie(size={self._size})"
