"""Graph — adjacency list representation supporting directed/undirected, weighted."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar

from pystructs.core.exceptions import GraphError

V = TypeVar("V", bound=Hashable)


class Graph(Generic[V]):
    """
    Adjacency list graph.

    add_vertex   → O(1)
    add_edge     → O(1)
    neighbors    → O(1)
    has_edge     → O(degree)
    """

    __slots__ = ("_adj", "_directed", "_weighted", "_vertex_count", "_edge_count")

    def __init__(self, directed: bool = False, weighted: bool = False) -> None:
        self._adj: dict[V, list[tuple[V, float]]] = defaultdict(list)
        self._directed = directed
        self._weighted = weighted
        self._vertex_count: int = 0
        self._edge_count: int = 0

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_vertex(self, vertex: V) -> None:
        if vertex not in self._adj:
            self._adj[vertex] = []
            self._vertex_count += 1

    def add_edge(self, u: V, v: V, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].append((v, weight))
        self._edge_count += 1
        if not self._directed:
            self._adj[v].append((u, weight))

    def remove_edge(self, u: V, v: V) -> None:
        before = len(self._adj[u])
        self._adj[u] = [(nb, w) for nb, w in self._adj[u] if nb != v]
        removed = before - len(self._adj[u])
        if removed == 0:
            raise GraphError(f"Edge ({u}, {v}) does not exist.")
        self._edge_count -= removed
        if not self._directed:
            self._adj[v] = [(nb, w) for nb, w in self._adj[v] if nb != u]

    def remove_vertex(self, vertex: V) -> None:
        if vertex not in self._adj:
            raise GraphError(f"Vertex {vertex!r} does not exist.")
        del self._adj[vertex]
        self._vertex_count -= 1
        for v in self._adj:
            before = len(self._adj[v])
            self._adj[v] = [(nb, w) for nb, w in self._adj[v] if nb != vertex]
            self._edge_count -= before - len(self._adj[v])

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def has_vertex(self, vertex: V) -> bool:
        return vertex in self._adj

    def has_edge(self, u: V, v: V) -> bool:
        return any(nb == v for nb, _ in self._adj.get(u, []))

    def neighbors(self, vertex: V) -> list[V]:
        return [nb for nb, _ in self._adj.get(vertex, [])]

    def weighted_neighbors(self, vertex: V) -> list[tuple[V, float]]:
        return list(self._adj.get(vertex, []))

    @property
    def vertices(self) -> list[V]:
        return list(self._adj.keys())

    @property
    def vertex_count(self) -> int:
        return self._vertex_count

    @property
    def edge_count(self) -> int:
        return self._edge_count

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __contains__(self, vertex: object) -> bool:
        return vertex in self._adj

    def __len__(self) -> int:
        return self._vertex_count

    def __iter__(self) -> Iterator[V]:
        return iter(self._adj)

    def __repr__(self) -> str:
        mode = "Directed" if self._directed else "Undirected"
        return f"Graph({mode}, V={self._vertex_count}, E={self._edge_count})"
