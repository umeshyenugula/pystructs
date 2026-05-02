"""
pystructs — Production-grade data structures and algorithms.

A modern, typed alternative and extension to Python's ``collections`` module.

Quick start
-----------
>>> from pystructs import Stack, MinHeap, TreeMap, Graph
>>> from pystructs import merge_sort, dijkstra, knapsack_01
>>> from pystructs import benchmark

Flat public API — no deep imports needed.
"""

from __future__ import annotations

from pystructs.algorithms.dp import (
    coin_change,
    edit_distance,
    knapsack_01,
    longest_common_subsequence,
    longest_increasing_subsequence,
    max_subarray,
)
from pystructs.algorithms.graph_algorithms import (
    bellman_ford,
    bfs,
    dfs,
    dijkstra,
    reconstruct_path,
    topological_sort,
)
from pystructs.algorithms.greedy import (
    activity_selection,
    fractional_knapsack,
    huffman_encoding,
    job_scheduling,
)
from pystructs.algorithms.searching import (
    binary_search,
    binary_search_leftmost,
    binary_search_rightmost,
    interpolation_search,
    linear_search,
)

# ── Algorithms ───────────────────────────────────────────────────────────────
from pystructs.algorithms.sorting import (
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    smart_sort,
)

# ── Engine ───────────────────────────────────────────────────────────────────
from pystructs.collections.batch import BatchProcessor

# ── Exceptions ───────────────────────────────────────────────────────────────
from pystructs.core.exceptions import (
    EmptyStructureError,
    GraphError,
    InvalidInputError,
    KeyNotFoundError,
    PyStructsError,
)
from pystructs.structures.graph import Graph
from pystructs.structures.hash_map import HashMap, HashSet
from pystructs.structures.heap import MaxHeap, MinHeap
from pystructs.structures.linked_hash import LinkedHashMap, LinkedHashSet
from pystructs.structures.linked_list import DoublyLinkedList, SinglyLinkedList
from pystructs.structures.queue import Deque, Queue

# ── Structures ──────────────────────────────────────────────────────────────
from pystructs.structures.stack import Stack
from pystructs.structures.tree_map import TreeMap, TreeSet
from pystructs.structures.trie import Trie

# ── Utils ────────────────────────────────────────────────────────────────────
from pystructs.utils.benchmark import benchmark, compare

__version__ = "0.9.0"
__author__ = "pystructs contributors"

__all__ = [
    # Structures
    "Stack",
    "Queue",
    "Deque",
    "SinglyLinkedList",
    "DoublyLinkedList",
    "MinHeap",
    "MaxHeap",
    "Trie",
    "Graph",
    "HashMap",
    "HashSet",
    "TreeMap",
    "TreeSet",
    "LinkedHashMap",
    "LinkedHashSet",
    # Sorting
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "smart_sort",
    # Searching
    "binary_search",
    "binary_search_leftmost",
    "binary_search_rightmost",
    "linear_search",
    "interpolation_search",
    # Graph algorithms
    "bfs",
    "dfs",
    "dijkstra",
    "reconstruct_path",
    "topological_sort",
    "bellman_ford",
    # Dynamic programming
    "longest_increasing_subsequence",
    "knapsack_01",
    "longest_common_subsequence",
    "max_subarray",
    "coin_change",
    "edit_distance",
    # Greedy
    "activity_selection",
    "fractional_knapsack",
    "huffman_encoding",
    "job_scheduling",
    # Exceptions
    "PyStructsError",
    "EmptyStructureError",
    "InvalidInputError",
    "KeyNotFoundError",
    "GraphError",
    # Utils
    "benchmark",
    "compare",
    # Engine
    "BatchProcessor",
    # Meta
    "__version__",
]
