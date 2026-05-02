"""Dynamic programming algorithms — tabulation-first approach."""

from __future__ import annotations

from collections.abc import Sequence

from pystructs.core.complexity import complexity
from pystructs.core.exceptions import InvalidInputError


@complexity(
    time_best="O(n)",
    time_average="O(n²)",
    time_worst="O(n²)",
    space="O(n)",
)
def longest_increasing_subsequence(seq: Sequence[int]) -> tuple[int, list[int]]:
    """
    LIS via patience sorting / bisect — O(n log n).
    Returns (length, one valid subsequence).
    """
    import bisect

    if not seq:
        return 0, []
    n = len(seq)
    tails: list[int] = []
    idx_in_tails: list[int] = [0] * n

    for i, val in enumerate(seq):
        pos = bisect.bisect_left(tails, val)
        if pos == len(tails):
            tails.append(val)
        else:
            tails[pos] = val
        idx_in_tails[i] = pos

    length = len(tails)
    path: list[int] = []
    pos = length - 1
    for i in range(n - 1, -1, -1):
        if idx_in_tails[i] == pos:
            path.append(seq[i])
            pos -= 1
            if pos < 0:
                break
    path.reverse()
    return length, path


@complexity(
    time_best="O(n * W)",
    time_average="O(n * W)",
    time_worst="O(n * W)",
    space="O(W)",
    notes="0/1 knapsack; W = capacity",
)
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """
    0/1 Knapsack via tabulation with O(W) space.
    Returns (max_value, list of chosen item indices).
    """
    if len(weights) != len(values):
        raise InvalidInputError("weights and values must have equal length.")
    if capacity < 0:
        raise InvalidInputError("capacity must be non-negative.")

    n = len(weights)
    dp = [0] * (capacity + 1)
    keep = [[False] * (capacity + 1) for _ in range(n)]

    for i in range(n):
        w, v = weights[i], values[i]
        for c in range(capacity, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
                keep[i][c] = True

    chosen: list[int] = []
    c = capacity
    for i in range(n - 1, -1, -1):
        if keep[i][c]:
            chosen.append(i)
            c -= weights[i]
    chosen.reverse()
    return dp[capacity], chosen


@complexity(
    time_best="O(n²)",
    time_average="O(n²)",
    time_worst="O(n²)",
    space="O(n²)",
)
def longest_common_subsequence(a: str, b: str) -> tuple[int, str]:
    """LCS via tabulation. Returns (length, one LCS string)."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    i, j = m, n
    lcs: list[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            lcs.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs.reverse()
    return dp[m][n], "".join(lcs)


@complexity(
    time_best="O(n)",
    time_average="O(n)",
    time_worst="O(n)",
    space="O(1)",
)
def max_subarray(arr: list[int]) -> tuple[int, int, int]:
    """
    Kadane's algorithm — maximum subarray sum.
    Returns (max_sum, start_index, end_index).
    """
    if not arr:
        raise InvalidInputError("arr must not be empty.")
    max_sum = curr = arr[0]
    start = end = temp_start = 0
    for i in range(1, len(arr)):
        if curr + arr[i] < arr[i]:
            curr = arr[i]
            temp_start = i
        else:
            curr += arr[i]
        if curr > max_sum:
            max_sum = curr
            start = temp_start
            end = i
    return max_sum, start, end


@complexity(
    time_best="O(n)",
    time_average="O(n)",
    time_worst="O(n)",
    space="O(n)",
)
def coin_change(coins: list[int], amount: int) -> int:
    """Minimum coins to make amount. Returns -1 if impossible."""
    if amount < 0:
        raise InvalidInputError("amount must be non-negative.")
    INF = float("inf")
    dp: list[float | int] = [INF] * (amount + 1)
    dp[0] = 0
    for c in range(1, amount + 1):
        for coin in coins:
            if coin <= c and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1
    result = dp[amount]
    return int(result) if result != INF else -1


@complexity(
    time_best="O(n²)",
    time_average="O(n²)",
    time_worst="O(n²)",
    space="O(n)",
)
def edit_distance(s: str, t: str) -> int:
    """Levenshtein edit distance via tabulation with O(n) space."""
    m, n = len(s), len(t)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]
