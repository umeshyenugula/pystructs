"""Graph algorithms: BFS, DFS (iterative), Dijkstra, topological sort."""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Hashable
from typing import TypeVar

from pystructs.core.complexity import complexity
from pystructs.core.exceptions import GraphError, InvalidInputError
from pystructs.structures.graph import Graph

V = TypeVar("V", bound=Hashable)


@complexity(
    time_best="O(V + E)",
    time_average="O(V + E)",
    time_worst="O(V + E)",
    space="O(V)",
)
def bfs(graph: Graph, start) -> list:
    """Iterative BFS. Returns list of visited vertices in BFS order."""
    if start not in graph:
        raise GraphError(f"Vertex {start!r} not in graph.")
    visited: set = set()
    order: list = []
    queue: deque = deque([start])
    visited.add(start)
    neighbors = graph.neighbors
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for nb in neighbors(vertex):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


@complexity(
    time_best="O(V + E)",
    time_average="O(V + E)",
    time_worst="O(V + E)",
    space="O(V)",
)
def dfs(graph: Graph, start) -> list:
    """Iterative DFS. Returns list of visited vertices in DFS order."""
    if start not in graph:
        raise GraphError(f"Vertex {start!r} not in graph.")
    visited: set = set()
    order: list = []
    stack = [start]
    neighbors = graph.neighbors
    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)
        for nb in reversed(neighbors(vertex)):
            if nb not in visited:
                stack.append(nb)
    return order


@complexity(
    time_best="O((V + E) log V)",
    time_average="O((V + E) log V)",
    time_worst="O((V + E) log V)",
    space="O(V)",
    notes="Requires non-negative edge weights",
)
def dijkstra(graph: Graph, source) -> tuple[dict, dict]:
    """
    Dijkstra's shortest path.

    Returns:
        (dist, prev) where dist[v] = shortest distance from source to v
                       and prev[v] = predecessor on shortest path.
    """
    if source not in graph:
        raise GraphError(f"Source vertex {source!r} not in graph.")
    INF = float("inf")
    dist: dict = {v: INF for v in graph.vertices}
    dist[source] = 0.0
    prev: dict = {v: None for v in graph.vertices}
    heap: list[tuple[float, object]] = [(0.0, source)]
    visited: set = set()
    wneighbors = graph.weighted_neighbors

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in wneighbors(u):
            if w < 0:
                raise InvalidInputError("Dijkstra requires non-negative weights.")
            alt = d + w
            if alt < dist.get(v, INF):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))
    return dist, prev


def reconstruct_path(prev: dict, source, target) -> list:
    """Reconstruct shortest path from dijkstra prev map."""
    path: list = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = prev.get(curr)
    path.reverse()
    if not path or path[0] != source:
        return []
    return path


@complexity(
    time_best="O(V + E)",
    time_average="O(V + E)",
    time_worst="O(V + E)",
    space="O(V)",
    notes="Only valid for DAGs",
)
def topological_sort(graph: Graph) -> list:
    """Kahn's algorithm topological sort for DAGs."""
    in_degree: dict = {v: 0 for v in graph.vertices}
    for u in graph.vertices:
        for nb in graph.neighbors(u):
            in_degree[nb] = in_degree.get(nb, 0) + 1

    queue: deque = deque(v for v in in_degree if in_degree[v] == 0)
    order: list = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for nb in graph.neighbors(u):
            in_degree[nb] -= 1
            if in_degree[nb] == 0:
                queue.append(nb)

    if len(order) != graph.vertex_count:
        raise GraphError("Graph has a cycle; topological sort not possible.")
    return order


@complexity(
    time_best="O(V * E)",
    time_average="O(V * E)",
    time_worst="O(V * E)",
    space="O(V)",
    notes="Handles negative weights; detects negative cycles",
)
def bellman_ford(graph: Graph, source) -> tuple[dict, bool]:
    """
    Bellman-Ford shortest paths.

    Returns:
        (dist, has_negative_cycle)
    """
    if source not in graph:
        raise GraphError(f"Source {source!r} not in graph.")
    INF = float("inf")
    dist: dict = {v: INF for v in graph.vertices}
    dist[source] = 0
    vertices = graph.vertices
    n = len(vertices)

    for _ in range(n - 1):
        for u in vertices:
            for v, w in graph.weighted_neighbors(u):
                if dist[u] + w < dist.get(v, INF):
                    dist[v] = dist[u] + w

    for u in vertices:
        for v, w in graph.weighted_neighbors(u):
            if dist[u] + w < dist.get(v, INF):
                return dist, True

    return dist, False
