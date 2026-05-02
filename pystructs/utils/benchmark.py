"""Benchmarking utilities using time.perf_counter."""

from __future__ import annotations

import gc
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BenchmarkResult:
    name: str
    runs: int
    times: list[float]
    mean: float = field(init=False)
    median: float = field(init=False)
    stdev: float = field(init=False)
    min_time: float = field(init=False)
    max_time: float = field(init=False)

    def __post_init__(self) -> None:
        self.mean = statistics.mean(self.times)
        self.median = statistics.median(self.times)
        self.stdev = statistics.stdev(self.times) if len(self.times) > 1 else 0.0
        self.min_time = min(self.times)
        self.max_time = max(self.times)

    def __repr__(self) -> str:
        return (
            f"BenchmarkResult({self.name!r}, runs={self.runs}, "
            f"mean={self.mean * 1000:.4f}ms, "
            f"median={self.median * 1000:.4f}ms, "
            f"min={self.min_time * 1000:.4f}ms, "
            f"max={self.max_time * 1000:.4f}ms)"
        )

    def summary(self) -> str:
        lines = [
            f"{'─' * 50}",
            f"  Benchmark : {self.name}",
            f"  Runs      : {self.runs}",
            f"  Mean      : {self.mean * 1000:.4f} ms",
            f"  Median    : {self.median * 1000:.4f} ms",
            f"  Std Dev   : {self.stdev * 1000:.4f} ms",
            f"  Min       : {self.min_time * 1000:.4f} ms",
            f"  Max       : {self.max_time * 1000:.4f} ms",
            f"{'─' * 50}",
        ]
        return "\n".join(lines)


def benchmark(
    fn: Callable,
    *args: Any,
    runs: int = 5,
    warmup: int = 1,
    name: str | None = None,
    **kwargs: Any,
) -> BenchmarkResult:
    """
    Benchmark a callable.

    Args:
        fn: Function to benchmark.
        *args: Positional arguments for fn.
        runs: Number of timed runs.
        warmup: Number of warmup runs (not counted).
        name: Display name. Defaults to fn.__name__.
        **kwargs: Keyword arguments for fn.

    Returns:
        BenchmarkResult with timing statistics.
    """
    label = name or getattr(fn, "__name__", str(fn))
    gc_was_enabled = gc.isenabled()
    gc.disable()

    try:
        for _ in range(warmup):
            fn(*args, **kwargs)

        times: list[float] = []
        for _ in range(runs):
            t0 = time.perf_counter()
            fn(*args, **kwargs)
            t1 = time.perf_counter()
            times.append(t1 - t0)
    finally:
        if gc_was_enabled:
            gc.enable()

    return BenchmarkResult(name=label, runs=runs, times=times)


def compare(
    *fns: Callable,
    args_factory: Callable | None = None,
    common_args: tuple | None = None,
    common_kwargs: dict | None = None,
    runs: int = 5,
    warmup: int = 1,
) -> list[BenchmarkResult]:
    """
    Compare multiple functions with the same input.

    args_factory: called before each function to generate fresh args.
    common_args: static args passed to all functions.
    """
    results: list[BenchmarkResult] = []
    for fn in fns:
        if args_factory is not None:
            args = args_factory()
            kwargs: dict = {}
        else:
            args = common_args or ()
            kwargs = common_kwargs or {}
        result = benchmark(fn, *args, runs=runs, warmup=warmup, **kwargs)
        results.append(result)
    results.sort(key=lambda r: r.median)
    return results
