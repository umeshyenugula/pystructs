# pystructs

**A production-grade, typed alternative to Python's `collections` module.**

Pure Python · Zero dependencies · Full type hints · 159 tests · PEP 561 compliant

```bash
pip install pystructs-toolkit
```

---

## Why pystructs?

Python's `collections` is great but limited: no sorted map, no trie, no graph, no heap with full control, no insertion-ordered set. `pystructs-toolkit` fills that gap with a single coherent library that feels like a natural extension of the standard library — not a practice toolkit.

| Need | stdlib | pystructs-toolkit |
|---|---|---|
| LIFO stack | `list` (no bounds, no typed API) | `Stack` (bounded, typed, O(1)) |
| Sorted map | ❌ | `TreeMap` (AVL, O(log n)) |
| Insertion-order map | `OrderedDict` (limited API) | `LinkedHashMap` (full map API) |
| Min/max heap | `heapq` (module, not object) | `MinHeap` / `MaxHeap` (OO, typed) |
| Prefix search | ❌ | `Trie` |
| Graph | ❌ | `Graph` (directed/undirected/weighted) |
| Batch processing | `concurrent.futures` (manual) | `BatchProcessor` (map/run/chunked) |

---

## Quick Start

```python
import pystructs as ps

# Everything available at the top level — no deep imports needed
s = ps.Stack()
s.push(1); s.push(2); s.push(3)
print(s.pop())          # 3

h = ps.MinHeap.from_iterable([9, 3, 7, 1])
print(h.pop())          # 1

data = [5, 2, 8, 1, 9]
ps.smart_sort(data)
print(data)             # [1, 2, 5, 8, 9]

g = ps.Graph(directed=True, weighted=True)
g.add_edge("A", "B", 1)
g.add_edge("B", "C", 2)
dist, prev = ps.dijkstra(g, "A")
print(dist["C"])        # 3

tm = ps.TreeMap()
for k in [5, 3, 8, 1, 4]:
    tm.put(k, str(k))
print(tm.keys())        # [1, 3, 4, 5, 8]

result = ps.benchmark(lambda: ps.smart_sort([5, 3, 1, 2, 4]), runs=10)
print(result.summary())
```

---

## Data Structures

### Stack
```python
from pystructs import Stack

s = Stack(maxsize=100)   # 0 = unlimited
s.push(42)
val = s.pop()            # 42
s.peek()                 # peek without removing
s.push_all([1, 2, 3])
```

### Queue / Deque
```python
from pystructs import Queue, Deque

q = Queue()
q.enqueue("hello")
q.dequeue()              # "hello"

d = Deque()
d.push_front(1); d.push_back(2)
d.pop_front(); d.pop_back()
```

### Linked Lists
```python
from pystructs import SinglyLinkedList, DoublyLinkedList

ll = SinglyLinkedList()
ll.extend([1, 2, 3, 4, 5])
ll.reverse()
mid = ll.find_middle()   # 3
has_cycle = ll.has_cycle()
```

### MinHeap / MaxHeap
```python
from pystructs import MinHeap, MaxHeap

h = MinHeap.from_iterable([9, 3, 7, 1])
h.peek()                 # 1 (no removal)
h.pop()                  # 1
h.nsmallest(3)           # [1, 3, 7]

mx = MaxHeap.from_iterable([9, 3, 7, 1])
mx.nlargest(2)           # [9, 7]
```

### Trie
```python
from pystructs import Trie

t = Trie()
t.insert("apple")
t.search("apple")           # True
t.starts_with("app")        # True
t.words_with_prefix("app")  # ["apple", ...]
t.delete("apple")
```

### Graph
```python
from pystructs import Graph

g = Graph(directed=True, weighted=True)
g.add_edge("A", "B", weight=2.5)
g.neighbors("A")            # ["B"]
g.has_edge("A", "B")        # True
g.vertex_count              # 2
```

### HashMap / HashSet
```python
from pystructs import HashMap, HashSet

m = HashMap()
m.put("a", 1)
m.get_or_default("b", 0)         # 0
m.put_if_absent("a", 99)         # returns 1 (no overwrite)
m.merge("count", 1, lambda o, n: o + n)
m.compute_if_absent("key", str.upper)

s = HashSet()
s.add_all([1, 2, 3])
s.intersection(other)
s.union(other)
s.difference(other)
s.is_subset_of(other)
```

### TreeMap / TreeSet
```python
from pystructs import TreeMap, TreeSet

tm = TreeMap()
tm.put(3, "three")
tm.get(3)                # "three"
tm.min_key()             # smallest key
tm.max_key()             # largest key
tm.delete(3)
tm.keys()                # always sorted

ts = TreeSet()
ts.add_all([5, 1, 3])
list(ts)                 # [1, 3, 5]
ts.min_key(); ts.max_key()
```

### LinkedHashMap / LinkedHashSet
```python
from pystructs import LinkedHashMap, LinkedHashSet

m = LinkedHashMap()
m.put("b", 2); m.put("a", 1)
m.keys()     # ["b", "a"]  — insertion order preserved

s = LinkedHashSet()
s.add_all([3, 1, 2])
list(s)      # [3, 1, 2]
```

---

## Algorithms

### Sorting
```python
from pystructs import insertion_sort, merge_sort, quick_sort, heap_sort, smart_sort

data = [3, 1, 4, 1, 5, 9]
smart_sort(data)                       # in-place, ascending
merge_sort(data, reverse=True)         # descending
quick_sort(data, key=lambda x: -x)    # custom key
```

All sort functions are **in-place** and accept `reverse` and `key` arguments.

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| `insertion_sort` | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| `merge_sort` | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ |
| `quick_sort` | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ |
| `heap_sort` | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ |
| `smart_sort` | O(n) | O(n log n) | O(n log n) | O(n) | ✓ |

### Searching
```python
from pystructs import binary_search, binary_search_leftmost, binary_search_rightmost

arr = list(range(0, 1000, 2))
idx = binary_search(arr, 500)          # returns index or -1
lo  = binary_search_leftmost(arr, 500)
hi  = binary_search_rightmost(arr, 500)
```

### Graph Algorithms
```python
from pystructs import bfs, dfs, dijkstra, reconstruct_path, topological_sort, bellman_ford

order = bfs(graph, start="A")
order = dfs(graph, start="A")

dist, prev = dijkstra(graph, source="A")
path = reconstruct_path(prev, "A", "D")   # ["A", "B", "C", "D"]

topo = topological_sort(dag)              # raises GraphError on cycle

dist, prev = bellman_ford(graph, "A")     # handles negative weights
```

### Dynamic Programming
```python
from pystructs import (
    longest_increasing_subsequence, knapsack_01,
    coin_change, edit_distance, max_subarray,
    longest_common_subsequence,
)

length, seq = longest_increasing_subsequence([3, 1, 4, 1, 5, 9])
value, items = knapsack_01(weights=[2, 3, 4], values=[3, 4, 5], capacity=6)
coins  = coin_change([1, 5, 25], 36)
dist   = edit_distance("kitten", "sitting")
s, lo, hi = max_subarray([-2, 1, -3, 4, -1, 2, 1])
```

### Greedy
```python
from pystructs import activity_selection, huffman_encoding, fractional_knapsack, job_scheduling

selected = activity_selection([(1, 3), (2, 5), (4, 6)])
codes    = huffman_encoding({"a": 5, "b": 9, "c": 12})
```

---

## BatchProcessor

```python
from pystructs import BatchProcessor

# Serial (safe for stateful operations)
bp = BatchProcessor()
results = bp.map(lambda x: x ** 2, range(1_000_000))

# Parallel (safe for pure functions)
bp = BatchProcessor(max_workers=8)
results = bp.map(expensive_pure_fn, large_list)

# Chunked (fn receives a list of items)
bp = BatchProcessor(chunk_size=500)
results = bp.map_chunked(bulk_insert_fn, records)

# Raw task list
tasks = [(fn, (arg,), {}) for arg in inputs]
results = bp.run(tasks)
```

---

## Benchmarking

```python
from pystructs import benchmark, compare
from pystructs import merge_sort, quick_sort, smart_sort

# Single function
result = benchmark(my_fn, arg1, arg2, runs=10, warmup=2)
print(result.summary())
# ──────────────────────────────────────────────────
#   Benchmark : my_fn
#   Runs      : 10
#   Mean      : 1.2345 ms
#   Median    : 1.2100 ms
#   Std Dev   : 0.0412 ms
#   Min       : 1.1900 ms
#   Max       : 1.3200 ms
# ──────────────────────────────────────────────────

# Compare functions (returns sorted by median)
results = compare(merge_sort, quick_sort, smart_sort,
                  args_factory=lambda: ([random.randint(0, 10000) for _ in range(10000)],))
for r in results:
    print(f"{r.name:20s}  {r.median * 1000:.3f} ms")
```

### Benchmark: sorting algorithms on n=10,000 random integers

| Algorithm | Median (ms) | vs Python `sorted` |
|---|---|---|
| `smart_sort` | ~4.1 | ~1.3× |
| `merge_sort` | ~5.8 | ~1.9× |
| `quick_sort` | ~6.2 | ~2.0× |
| `heap_sort`  | ~9.5 | ~3.1× |
| `insertion_sort` | ~1800 | — (n=10k) |

*Pure Python overhead is expected. Use `smart_sort` for best performance.*

---

## CLI

```bash
# Benchmark a single sorting algorithm
pystructs sort merge --size 100000 --runs 5

# Compare all sorting algorithms side-by-side
pystructs benchmark --size 50000 --runs 10

# Binary search benchmark
pystructs search --size 1000000

# Complexity info for any algorithm
pystructs info merge_sort
pystructs info dijkstra

# List all available algorithm functions
pystructs list
```

---

## Installation

```bash
# From PyPI (when published)
pip install pystructs-toolkit

# From source (development)
git clone https://github.com/umeshyenugula/pystructs
cd pystructs
pip install -e ".[dev]"
```

---

## Running Tests

```bash
# All tests (unittest, no extra deps)
python -m unittest discover -s tests -p "test_*.py" -v

# With coverage (requires pytest-cov)
pytest tests/ --cov=pystructs --cov-report=term-missing
```

---

## Design Principles

- **Pure Python** — zero external dependencies; only the standard library.
- **`__slots__` everywhere** — reduced per-instance memory overhead on every node and structure.
- **Iterative over recursive** — no stack overflow on deep inputs (DFS, tree traversal, etc.).
- **Built-ins first** — `heapq`, `bisect`, `collections.deque` for proven performance where appropriate.
- **Tabulation > memoisation** in DP for cache-friendly access patterns.
- **Custom typed exceptions** — `pystructs-toolkitError`, `EmptyStructureError`, `InvalidInputError`, `KeyNotFoundError`, `GraphError`, `StructureOverflowError`.
- **Full type hints** via `from __future__ import annotations` and `py.typed` (PEP 561).
- **Flat public API** — `from pystructs import Stack, dijkstra, benchmark` just works.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT
