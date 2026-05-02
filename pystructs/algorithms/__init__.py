"""Algorithms module."""

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
from pystructs.algorithms.sorting import (
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    smart_sort,
)

__all__ = [
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "smart_sort",
    "binary_search",
    "binary_search_leftmost",
    "binary_search_rightmost",
    "linear_search",
    "interpolation_search",
    "bfs",
    "dfs",
    "dijkstra",
    "reconstruct_path",
    "topological_sort",
    "bellman_ford",
    "longest_increasing_subsequence",
    "knapsack_01",
    "longest_common_subsequence",
    "max_subarray",
    "coin_change",
    "edit_distance",
    "activity_selection",
    "fractional_knapsack",
    "huffman_encoding",
    "job_scheduling",
]
