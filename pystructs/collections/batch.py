"""Batch processing engine with optional multithreading.

Moved from ``engine/`` into ``collections/`` — a more descriptive home for
a utility that processes collections of tasks in bulk.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from pystructs.core.exceptions import InvalidInputError


def _safe_call(fn: Callable, args: tuple, kwargs: dict) -> Any:
    return fn(*args, **kwargs)


class BatchProcessor:
    """
    Process a list of ``(callable, args, kwargs)`` tasks efficiently.

    Supports serial and parallel (thread-pool) execution modes.

    Parameters
    ----------
    max_workers:
        1 = serial (safe for stateful operations).
        >1 = parallel via ``ThreadPoolExecutor`` (safe for pure functions).
    chunk_size:
        Used by ``map_chunked`` to split inputs into batches.

    Examples
    --------
    >>> bp = BatchProcessor()
    >>> bp.map(lambda x: x ** 2, range(5))
    [0, 1, 4, 9, 16]

    >>> bp = BatchProcessor(max_workers=4)
    >>> results = bp.map(expensive_pure_fn, large_list)
    """

    __slots__ = ("_max_workers", "_chunk_size")

    def __init__(self, max_workers: int = 1, chunk_size: int = 1000) -> None:
        if max_workers < 1:
            raise InvalidInputError("max_workers must be >= 1.")
        if chunk_size < 1:
            raise InvalidInputError("chunk_size must be >= 1.")
        self._max_workers = max_workers
        self._chunk_size = chunk_size

    def run(self, tasks: list[tuple[Callable, tuple, dict]]) -> list[Any]:
        """Execute a list of ``(callable, args, kwargs)`` tasks; return results in order."""
        if not tasks:
            return []
        if self._max_workers == 1:
            return [fn(*args, **kw) for fn, args, kw in tasks]
        results: list[Any] = [None] * len(tasks)
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {
                executor.submit(_safe_call, fn, args, kw): i
                for i, (fn, args, kw) in enumerate(tasks)
            }
            for future in as_completed(futures):
                results[futures[future]] = future.result()
        return results

    def map(self, fn: Callable, inputs: Iterable[Any]) -> list[Any]:
        """Apply ``fn`` to each item in ``inputs``."""
        items = list(inputs)
        if not items:
            return []
        return self.run([(fn, (item,), {}) for item in items])

    def map_chunked(self, fn: Callable, inputs: Iterable[Any]) -> list[Any]:
        """Apply ``fn`` to chunks of ``inputs``. ``fn`` receives a list (chunk)."""
        from pystructs.utils.helpers import chunk as _chunk

        items = list(inputs)
        chunks = list(_chunk(items, self._chunk_size))
        results_nested = self.map(fn, chunks)
        return [item for sub in results_nested for item in sub]

    def __repr__(self) -> str:
        return f"BatchProcessor(max_workers={self._max_workers}, chunk_size={self._chunk_size})"
