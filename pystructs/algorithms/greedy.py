"""Greedy algorithms."""

from __future__ import annotations

import heapq

from pystructs.core.complexity import complexity
from pystructs.core.exceptions import InvalidInputError


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(n)",
)
def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Greedy activity selection (interval scheduling maximization).

    activities: list of (start, end) tuples.
    Returns list of non-overlapping activities with maximum count.
    """
    if not all(isinstance(a, tuple) and len(a) == 2 for a in activities):
        raise InvalidInputError("activities must be list of (start, end) tuples.")
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected: list[tuple[int, int]] = []
    last_end = float("-inf")
    for start, end in sorted_acts:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(n)",
)
def fractional_knapsack(
    weights: list[float], values: list[float], capacity: float
) -> tuple[float, list[tuple[int, float]]]:
    """
    Fractional knapsack — items can be split.
    Returns (max_value, [(item_index, fraction_taken), ...]).
    """
    if len(weights) != len(values):
        raise InvalidInputError("weights and values must have equal length.")
    items = sorted(
        enumerate(zip(weights, values, strict=True)),
        key=lambda x: x[1][1] / x[1][0] if x[1][0] > 0 else 0,
        reverse=True,
    )
    total = 0.0
    taken: list[tuple[int, float]] = []
    remaining = capacity
    for idx, (w, v) in items:
        if remaining <= 0:
            break
        fraction = min(1.0, remaining / w)
        total += v * fraction
        taken.append((idx, fraction))
        remaining -= w * fraction
    return total, taken


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(n)",
    notes="Huffman encoding tree",
)
def huffman_encoding(frequencies: dict[str, int]) -> dict[str, str]:
    """
    Huffman coding — returns symbol -> binary code mapping.
    """
    if not frequencies:
        raise InvalidInputError("frequencies must not be empty.")
    heap: list[tuple[int, int, object]] = []
    counter = 0
    for char, freq in frequencies.items():
        heapq.heappush(heap, (freq, counter, char))
        counter += 1

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, (left, right)))
        counter += 1

    codes: dict[str, str] = {}
    if not heap:
        return codes

    _, _, root = heap[0]

    stack = [(root, "")]
    while stack:
        node, code = stack.pop()
        if isinstance(node, str):
            codes[node] = code if code else "0"
        else:
            left, right = node
            stack.append((right, code + "1"))
            stack.append((left, code + "0"))
    return codes


@complexity(
    time_best="O(n log n)",
    time_average="O(n log n)",
    time_worst="O(n log n)",
    space="O(1)",
)
def job_scheduling(jobs: list[tuple[int, int, int]]) -> tuple[int, list[int]]:
    """
    Greedy job scheduling to maximize profit within deadlines.

    jobs: list of (job_id, deadline, profit)
    Returns (total_profit, [job_ids scheduled]).
    """
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(j[1] for j in jobs) if jobs else 0
    slot: list[int] = [-1] * (max_deadline + 1)
    total_profit = 0
    scheduled: list[int] = []

    for job_id, deadline, profit in sorted_jobs:
        for t in range(min(deadline, max_deadline), 0, -1):
            if slot[t] == -1:
                slot[t] = job_id
                total_profit += profit
                scheduled.append(job_id)
                break
    return total_profit, scheduled
