"""
pystructs demo — showcasing the flat public API and key features.
Run with: python examples/demo.py
"""

from __future__ import annotations

import random

import pystructs as ps

SEP = "─" * 60


def section(title: str) -> None:
    print(f"\n{SEP}\n  {title}\n{SEP}")


# ---------------------------------------------------------------------------
# Flat public API
# ---------------------------------------------------------------------------
section("Flat public API")

s = ps.Stack()
s.push_all([10, 20, 30])
print(f"Stack (LIFO)       : {s.to_list()}")
print(f"Stack.pop()        : {s.pop()}")

q = ps.Queue()
q.enqueue_all([1, 2, 3])
print(f"Queue.dequeue()    : {q.dequeue()}")

d = ps.Deque()
d.push_front(0); d.push_back(1); d.push_back(2)
print(f"Deque to_list      : {d.to_list()}")

# ---------------------------------------------------------------------------
# Heap
# ---------------------------------------------------------------------------
section("MinHeap / MaxHeap")

vals = [random.randint(1, 100) for _ in range(10)]
h = ps.MinHeap.from_iterable(vals)
print(f"Input              : {vals}")
print(f"nsmallest(3)       : {h.nsmallest(3)}")

mx = ps.MaxHeap.from_iterable(vals)
print(f"nlargest(3)        : {mx.nlargest(3)}")

# ---------------------------------------------------------------------------
# TreeMap / TreeSet
# ---------------------------------------------------------------------------
section("TreeMap (AVL self-balancing) / TreeSet")

tm = ps.TreeMap()
for k in [5, 3, 8, 1, 4, 7, 9]:
    tm.put(k, f"val_{k}")
print(f"Sorted keys        : {tm.keys()}")
print(f"min_key / max_key  : {tm.min_key()} / {tm.max_key()}")

ts = ps.TreeSet()
ts.add_all([5, 2, 8, 1, 4])
print(f"TreeSet iteration  : {list(ts)}")

# ---------------------------------------------------------------------------
# HashMap — extended API
# ---------------------------------------------------------------------------
section("HashMap — extended dict-like API")

m = ps.HashMap()
m.put("visits", 0)
m.merge("visits", 1, lambda old, new: old + new)
m.merge("visits", 1, lambda old, new: old + new)
print(f"merge (visits += 1 twice): {m.get('visits')}")

m.compute_if_absent("greeting", lambda k: f"hello from {k}")
print(f"compute_if_absent  : {m.get('greeting')}")

# ---------------------------------------------------------------------------
# LinkedHashMap (insertion-order preserving)
# ---------------------------------------------------------------------------
section("LinkedHashMap — insertion-order map")

lhm = ps.LinkedHashMap()
for item in ["banana", "apple", "cherry", "date"]:
    lhm.put(item, len(item))
print(f"Keys (insertion order): {lhm.keys()}")
lhm.remove("apple")
print(f"After remove('apple') : {lhm.keys()}")

# ---------------------------------------------------------------------------
# Trie
# ---------------------------------------------------------------------------
section("Trie")

t = ps.Trie()
for word in ["apple", "app", "application", "apply", "banana"]:
    t.insert(word)
print(f"words_with_prefix('app'): {sorted(t.words_with_prefix('app'))}")
print(f"search('apply')         : {t.search('apply')}")
t.delete("apply")
print(f"after delete('apply')   : {sorted(t.words_with_prefix('app'))}")

# ---------------------------------------------------------------------------
# Sorting comparison
# ---------------------------------------------------------------------------
section("Sorting — all algorithms on the same dataset")

data = [random.randint(0, 10_000) for _ in range(5_000)]
fns = [ps.insertion_sort, ps.merge_sort, ps.quick_sort, ps.heap_sort, ps.smart_sort]
print(f"{'Algorithm':<20}  {'Median (ms)':>12}")
print("─" * 36)
for fn in fns:
    result = ps.benchmark(fn, data.copy(), runs=3, name=fn.__name__)
    print(f"  {fn.__name__:<18}  {result.median * 1000:>10.3f}")

# ---------------------------------------------------------------------------
# Graph + Dijkstra
# ---------------------------------------------------------------------------
section("Graph — Dijkstra shortest path")

g = ps.Graph(directed=True, weighted=True)
edges = [("A","B",1),("A","C",4),("B","C",2),("B","D",5),("C","D",1)]
for u, v, w in edges:
    g.add_edge(u, v, w)

dist, prev = ps.dijkstra(g, "A")
path = ps.reconstruct_path(prev, "A", "D")
print(f"Shortest path A → D : {' → '.join(path)}  (cost {dist['D']:.0f})")

# ---------------------------------------------------------------------------
# Dynamic Programming
# ---------------------------------------------------------------------------
section("Dynamic Programming")

length, seq = ps.longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
print(f"LIS of [10,9,2,5,3,7,101,18] : length={length}, seq={seq}")

value, items = ps.knapsack_01([2,3,4,5],[3,4,5,6], 5)
print(f"0/1 Knapsack (cap=5)         : value={value}")

print(f"edit_distance('kitten','sitting'): {ps.edit_distance('kitten','sitting')}")
print(f"coin_change([1,5,25], 36)        : {ps.coin_change([1,5,25],36)}")

# ---------------------------------------------------------------------------
# Benchmark compare
# ---------------------------------------------------------------------------
section("Benchmark — compare() utility")

sample = [random.randint(0, 10_000) for _ in range(3_000)]
results = ps.compare(
    ps.merge_sort, ps.quick_sort, ps.smart_sort,
    args_factory=lambda: (sample.copy(),),
    runs=5,
)
print(f"{'Rank':<6}{'Function':<20}{'Median (ms)':>12}")
print("─" * 40)
for rank, r in enumerate(results, 1):
    print(f"  #{rank}   {r.name:<18}  {r.median * 1000:>10.3f}")

# ---------------------------------------------------------------------------
# BatchProcessor
# ---------------------------------------------------------------------------
section("BatchProcessor")

bp = ps.BatchProcessor()
squares = bp.map(lambda x: x ** 2, range(10))
print(f"Serial map (x²)    : {squares}")

bp_parallel = ps.BatchProcessor(max_workers=4)
results_p = bp_parallel.map(lambda x: x * 3, range(8))
print(f"Parallel map (x*3) : {results_p}")

print(f"\n{SEP}\nAll demos complete.\n{SEP}\n")
