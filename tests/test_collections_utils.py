"""Tests for BatchProcessor, benchmark utilities, and helpers."""

from __future__ import annotations

import unittest

from pystructs.collections.batch import BatchProcessor
from pystructs.core.exceptions import InvalidInputError
from pystructs.utils.benchmark import BenchmarkResult, benchmark, compare
from pystructs.utils.helpers import chunk, clamp, flatten, is_sorted, random_list


class TestBatchProcessor(unittest.TestCase):
    def test_serial_map(self):
        bp = BatchProcessor()
        self.assertEqual(bp.map(lambda x: x * 2, [1, 2, 3]), [2, 4, 6])

    def test_parallel_map(self):
        bp = BatchProcessor(max_workers=4)
        self.assertEqual(bp.map(lambda x: x**2, range(20)), [x**2 for x in range(20)])

    def test_run_tasks(self):
        bp = BatchProcessor()
        tasks = [(lambda x: x + 1, (i,), {}) for i in range(5)]
        self.assertEqual(bp.run(tasks), [1, 2, 3, 4, 5])

    def test_empty(self):
        bp = BatchProcessor()
        self.assertEqual(bp.run([]), [])
        self.assertEqual(bp.map(lambda x: x, []), [])

    def test_invalid_workers(self):
        with self.assertRaises(InvalidInputError):
            BatchProcessor(max_workers=0)

    def test_invalid_chunk_size(self):
        with self.assertRaises(InvalidInputError):
            BatchProcessor(chunk_size=0)

    def test_map_chunked(self):
        bp = BatchProcessor(chunk_size=3)
        result = bp.map_chunked(lambda c: [x * 2 for x in c], range(7))
        self.assertEqual(result, [x * 2 for x in range(7)])

    def test_repr(self):
        bp = BatchProcessor(max_workers=2, chunk_size=500)
        self.assertIn("BatchProcessor", repr(bp))


class TestBenchmark(unittest.TestCase):
    def test_returns_result(self):
        result = benchmark(lambda: sum(range(1000)), runs=3, warmup=1)
        self.assertIsInstance(result, BenchmarkResult)
        self.assertEqual(result.runs, 3)
        self.assertEqual(len(result.times), 3)
        self.assertGreater(result.mean, 0)

    def test_summary_str(self):
        result = benchmark(lambda: None, runs=2)
        summary = result.summary()
        self.assertIn("Benchmark", summary)
        self.assertIn("Mean", summary)

    def test_mean_median_bounds(self):
        result = benchmark(lambda: None, runs=10)
        self.assertGreaterEqual(result.median, result.min_time)
        self.assertLessEqual(result.median, result.max_time)

    def test_compare(self):
        functions = [lambda: sum(range(100)), lambda: sum(range(200))]
        results = compare(*functions, common_args=(), runs=3)
        self.assertEqual(len(results), 2)
        self.assertLessEqual(results[0].median, results[1].median)

    def test_named_benchmark(self):
        result = benchmark(lambda: None, runs=2, name="my_fn")
        self.assertEqual(result.name, "my_fn")


class TestHelpers(unittest.TestCase):
    def test_random_list(self):
        values = random_list(100, 0, 50)
        self.assertEqual(len(values), 100)
        self.assertTrue(all(0 <= value <= 50 for value in values))

    def test_is_sorted_true(self):
        self.assertTrue(is_sorted([1, 2, 3, 4]))

    def test_is_sorted_false(self):
        self.assertFalse(is_sorted([1, 3, 2]))

    def test_is_sorted_reverse(self):
        self.assertTrue(is_sorted([4, 3, 2, 1], reverse=True))

    def test_is_sorted_empty(self):
        self.assertTrue(is_sorted([]))

    def test_is_sorted_single(self):
        self.assertTrue(is_sorted([42]))

    def test_chunk(self):
        self.assertEqual(list(chunk(range(7), 3)), [[0, 1, 2], [3, 4, 5], [6]])

    def test_chunk_exact(self):
        self.assertEqual(list(chunk(range(6), 3)), [[0, 1, 2], [3, 4, 5]])

    def test_flatten(self):
        self.assertEqual(flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

    def test_flatten_mixed(self):
        self.assertEqual(flatten([[1, 2], 3, [4]]), [1, 2, 3, 4])

    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-1, 0, 10), 0)
        self.assertEqual(clamp(15, 0, 10), 10)


if __name__ == "__main__":
    unittest.main()
