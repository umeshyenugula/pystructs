"""Tests for pystructs algorithms."""

from __future__ import annotations

import random
import unittest

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
from pystructs.core.exceptions import GraphError, InvalidInputError
from pystructs.structures import Graph

SORT_FNS = [insertion_sort, merge_sort, quick_sort, heap_sort, smart_sort]


class TestSorting(unittest.TestCase):
    def _test_all(self, arr, expected):
        for fn in SORT_FNS:
            values = arr.copy()
            fn(values)
            self.assertEqual(values, expected, msg=f"{fn.__name__} failed")

    def test_basic(self):
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        self._test_all(values, sorted(values))

    def test_empty(self):
        self._test_all([], [])

    def test_single(self):
        self._test_all([42], [42])

    def test_already_sorted(self):
        values = list(range(100))
        self._test_all(values, values)

    def test_reverse_order(self):
        values = list(range(100, 0, -1))
        self._test_all(values, list(range(1, 101)))

    def test_reverse_flag(self):
        for fn in SORT_FNS:
            values = [3, 1, 2]
            fn(values, reverse=True)
            self.assertEqual(values, [3, 2, 1], msg=fn.__name__)

    def test_key_fn(self):
        for fn in SORT_FNS:
            values = ["banana", "apple", "cherry"]
            fn(values, key=len)
            self.assertEqual(values[0], "apple", msg=fn.__name__)

    def test_large(self):
        values = [random.randint(0, 1_000_000) for _ in range(10_000)]
        expected = sorted(values)
        for fn in SORT_FNS:
            sorted_values = values.copy()
            fn(sorted_values)
            self.assertEqual(sorted_values, expected, msg=fn.__name__)

    def test_invalid_input(self):
        for fn in SORT_FNS:
            with self.assertRaises(InvalidInputError, msg=fn.__name__):
                fn((1, 2, 3))

    def test_duplicates(self):
        self._test_all([1] * 1000, [1] * 1000)

    def test_two_elements(self):
        self._test_all([2, 1], [1, 2])


class TestBinarySearch(unittest.TestCase):
    def test_found(self):
        values = list(range(0, 100, 2))
        self.assertEqual(binary_search(values, 50), 25)

    def test_not_found(self):
        self.assertEqual(binary_search([1, 3, 5, 7], 4), -1)

    def test_empty(self):
        self.assertEqual(binary_search([], 0), -1)

    def test_single_match(self):
        self.assertEqual(binary_search([7], 7), 0)

    def test_single_no_match(self):
        self.assertEqual(binary_search([7], 5), -1)

    def test_with_key(self):
        values = [{"v": 1}, {"v": 3}, {"v": 5}]
        self.assertEqual(binary_search(values, {"v": 3}, key=lambda x: x["v"]), 1)

    def test_invalid_input(self):
        with self.assertRaises(InvalidInputError):
            binary_search("nope", "x")

    def test_first_element(self):
        values = list(range(100))
        self.assertEqual(binary_search(values, 0), 0)

    def test_last_element(self):
        values = list(range(100))
        self.assertEqual(binary_search(values, 99), 99)


class TestLinearSearch(unittest.TestCase):
    def test_found(self):
        self.assertEqual(linear_search([10, 20, 30], 20), 1)

    def test_not_found(self):
        self.assertEqual(linear_search([1, 2, 3], 99), -1)

    def test_empty(self):
        self.assertEqual(linear_search([], 5), -1)


class TestInterpolationSearch(unittest.TestCase):
    def test_found(self):
        values = list(range(0, 1000, 10))
        index = interpolation_search(values, 500)
        self.assertGreaterEqual(index, 0)
        self.assertEqual(values[index], 500)

    def test_not_found(self):
        self.assertEqual(interpolation_search(list(range(0, 100, 2)), 7), -1)


class TestGraphAlgorithms(unittest.TestCase):
    def _simple_graph(self):
        graph = Graph()
        for left, right in [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]:
            graph.add_edge(left, right)
        return graph

    def test_bfs_order(self):
        graph = self._simple_graph()
        order = bfs(graph, 1)
        self.assertEqual(order[0], 1)
        self.assertEqual(set(order), {1, 2, 3, 4, 5})

    def test_dfs_order(self):
        graph = self._simple_graph()
        order = dfs(graph, 1)
        self.assertEqual(order[0], 1)
        self.assertEqual(set(order), {1, 2, 3, 4, 5})

    def test_bfs_invalid_start(self):
        with self.assertRaises(GraphError):
            bfs(Graph(), 99)

    def test_dijkstra(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_edge("A", "B", 1)
        graph.add_edge("A", "C", 4)
        graph.add_edge("B", "C", 2)
        graph.add_edge("B", "D", 5)
        graph.add_edge("C", "D", 1)
        dist, prev = dijkstra(graph, "A")
        self.assertEqual(dist["D"], 4)
        self.assertEqual(reconstruct_path(prev, "A", "D"), ["A", "B", "C", "D"])

    def test_dijkstra_negative_weight(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_edge("A", "B", -1)
        with self.assertRaises(InvalidInputError):
            dijkstra(graph, "A")

    def test_topological_sort(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "C")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        order = topological_sort(graph)
        self.assertLess(order.index("C"), order.index("D"))

    def test_topological_sort_cycle(self):
        graph = Graph(directed=True)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)
        with self.assertRaises(GraphError):
            topological_sort(graph)

    def test_bellman_ford_no_neg_cycle(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", -1)
        dist, _ = bellman_ford(graph, "A")
        self.assertEqual(dist["C"], 0)


class TestDP(unittest.TestCase):
    def test_lis(self):
        length, _ = longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        self.assertEqual(length, 4)

    def test_lis_empty(self):
        self.assertEqual(longest_increasing_subsequence([]), (0, []))

    def test_knapsack(self):
        value, _ = knapsack_01([2, 3, 4, 5], [3, 4, 5, 6], 5)
        self.assertEqual(value, 7)

    def test_knapsack_mismatch(self):
        with self.assertRaises(InvalidInputError):
            knapsack_01([1, 2], [1], 5)

    def test_lcs(self):
        length, _ = longest_common_subsequence("ABCBDAB", "BDCAB")
        self.assertEqual(length, 4)

    def test_max_subarray(self):
        total, _, _ = max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        self.assertEqual(total, 6)

    def test_max_subarray_empty(self):
        with self.assertRaises(InvalidInputError):
            max_subarray([])

    def test_coin_change(self):
        self.assertEqual(coin_change([1, 5, 10, 25], 36), 3)

    def test_coin_change_impossible(self):
        self.assertEqual(coin_change([3, 5], 7), -1)

    def test_edit_distance(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance("", "abc"), 3)
        self.assertEqual(edit_distance("abc", "abc"), 0)

    def test_all_same_in_subarray(self):
        total, _, _ = max_subarray([5, 5, 5])
        self.assertEqual(total, 15)


class TestGreedy(unittest.TestCase):
    def test_activity_selection(self):
        activities = [(1, 3), (2, 5), (4, 6), (6, 7), (5, 8), (8, 9)]
        self.assertEqual(len(activity_selection(activities)), 4)

    def test_activity_selection_invalid(self):
        with self.assertRaises(InvalidInputError):
            activity_selection([1, 2, 3])

    def test_fractional_knapsack(self):
        value, _ = fractional_knapsack([10, 20, 30], [60, 100, 120], 50)
        self.assertAlmostEqual(value, 240.0, places=4)

    def test_huffman(self):
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        codes = huffman_encoding(frequencies)
        self.assertEqual(set(codes.keys()), set(frequencies.keys()))
        self.assertTrue(all(isinstance(value, str) for value in codes.values()))

    def test_job_scheduling(self):
        jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
        result = job_scheduling(jobs)
        total, scheduled_jobs = result
        self.assertIsInstance(total, (int, float))
        self.assertIsInstance(scheduled_jobs, list)


if __name__ == "__main__":
    unittest.main()
