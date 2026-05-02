"""Command-line interface for pystructs."""

from __future__ import annotations

import argparse
import random
import sys


def _run_sort(args: argparse.Namespace) -> None:
    from pystructs.algorithms.sorting import (
        heap_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
        smart_sort,
    )
    from pystructs.utils.benchmark import benchmark

    algos = {
        "insertion": insertion_sort,
        "merge": merge_sort,
        "quick": quick_sort,
        "heap": heap_sort,
        "smart": smart_sort,
    }
    fn = algos.get(args.algorithm)
    if fn is None:
        print(f"Unknown algorithm: {args.algorithm!r}. Choose from: {list(algos)}", file=sys.stderr)
        sys.exit(1)

    data: list[int] = [random.randint(0, 1_000_000) for _ in range(args.size)]

    def task() -> None:
        arr = data.copy()
        fn(arr)

    result = benchmark(task, runs=args.runs, name=f"{args.algorithm}_sort(n={args.size:,})")
    print(result.summary())


def _run_search(args: argparse.Namespace) -> None:
    from pystructs.algorithms.searching import binary_search
    from pystructs.utils.benchmark import benchmark

    data = list(range(args.size))
    target = args.size // 2

    def task() -> None:
        binary_search(data, target)

    result = benchmark(task, runs=args.runs, name=f"binary_search(n={args.size:,})")
    print(result.summary())


def _run_benchmark(args: argparse.Namespace) -> None:
    from pystructs.algorithms.sorting import (
        heap_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
        smart_sort,
    )
    from pystructs.utils.benchmark import benchmark

    n = args.size
    data = [random.randint(0, n * 10) for _ in range(n)]
    fns = [insertion_sort, merge_sort, quick_sort, heap_sort, smart_sort]

    print(f"\nSorting benchmark  —  n={n:,} random integers  —  {args.runs} runs each\n")
    results = []
    for fn in fns:
        arr = data.copy()
        result = benchmark(fn, arr, runs=args.runs, name=fn.__name__)
        results.append(result)

    results.sort(key=lambda r: r.median)
    for r in results:
        print(r.summary())

    print(f"\n🏆  Fastest: {results[0].name}  (median {results[0].median * 1000:.4f} ms)\n")


def _run_info(args: argparse.Namespace) -> None:
    from pystructs.algorithms import dp, graph_algorithms, greedy, searching, sorting
    from pystructs.core.complexity import get_complexity

    all_modules = [sorting, searching, dp, greedy, graph_algorithms]
    for mod in all_modules:
        fn = getattr(mod, args.function, None)
        if fn is not None:
            c = get_complexity(fn)
            if c:
                print(f"\nComplexity for '{args.function}':")
                print(f"  Time (best)    : {c.time_best}")
                print(f"  Time (average) : {c.time_average}")
                print(f"  Time (worst)   : {c.time_worst}")
                print(f"  Space          : {c.space}")
                if c.stable is not None:
                    print(f"  Stable sort    : {c.stable}")
                if c.in_place is not None:
                    print(f"  In-place       : {c.in_place}")
                if c.notes:
                    print(f"  Notes          : {c.notes}")
            else:
                print(f"No complexity metadata found for '{args.function}'.")
            return
    print(
        f"Function '{args.function}' not found. Check spelling or run 'pystructs list'.",
        file=sys.stderr,
    )
    sys.exit(1)


def _run_list(_args: argparse.Namespace) -> None:
    from pystructs.algorithms import (
        dp,
        graph_algorithms,
        greedy,
        searching,
        sorting,
    )

    sections = {
        "Sorting": sorting,
        "Searching": searching,
        "Dynamic Programming": dp,
        "Greedy": greedy,
        "Graph Algorithms": graph_algorithms,
    }
    print("\nAvailable algorithms in pystructs:\n")
    for section, mod in sections.items():
        fns = [
            name for name in dir(mod) if not name.startswith("_") and callable(getattr(mod, name))
        ]
        print(f"  {section}:")
        for fn in fns:
            print(f"    • {fn}")
        print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pystructs",
        description=(
            "pystructs CLI — run, benchmark, and inspect data structures and algorithms.\n\n"
            "Examples:\n"
            "  pystructs sort merge --size 100000\n"
            "  pystructs benchmark --size 50000\n"
            "  pystructs info merge_sort\n"
            "  pystructs list\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    # sort
    p_sort = sub.add_parser(
        "sort",
        help="Run and benchmark a single sorting algorithm.",
        description="Benchmark a specific sorting algorithm on random data.",
    )
    p_sort.add_argument(
        "algorithm",
        choices=["insertion", "merge", "quick", "heap", "smart"],
        help="Sorting algorithm to benchmark.",
    )
    p_sort.add_argument(
        "--size",
        type=int,
        default=10_000,
        metavar="N",
        help="Number of random integers to sort (default: 10,000).",
    )
    p_sort.add_argument(
        "--runs", type=int, default=5, metavar="R", help="Number of timed runs (default: 5)."
    )
    p_sort.set_defaults(func=_run_sort)

    # search
    p_search = sub.add_parser(
        "search",
        help="Benchmark binary search.",
        description="Benchmark binary_search on a sorted integer list.",
    )
    p_search.add_argument(
        "--size",
        type=int,
        default=1_000_000,
        metavar="N",
        help="Size of the sorted list (default: 1,000,000).",
    )
    p_search.add_argument(
        "--runs", type=int, default=5, metavar="R", help="Number of timed runs (default: 5)."
    )
    p_search.set_defaults(func=_run_search)

    # benchmark
    p_bench = sub.add_parser(
        "benchmark",
        help="Compare all sorting algorithms side-by-side.",
        description="Run all sorting algorithms on the same dataset and rank by speed.",
    )
    p_bench.add_argument(
        "--size",
        type=int,
        default=10_000,
        metavar="N",
        help="Number of random integers to sort (default: 10,000).",
    )
    p_bench.add_argument(
        "--runs",
        type=int,
        default=5,
        metavar="R",
        help="Number of timed runs per algorithm (default: 5).",
    )
    p_bench.set_defaults(func=_run_benchmark)

    # info
    p_info = sub.add_parser(
        "info",
        help="Show complexity info for an algorithm.",
        description="Display Big-O complexity metadata for a named algorithm function.",
    )
    p_info.add_argument("function", help="Algorithm name, e.g. merge_sort, dijkstra.")
    p_info.set_defaults(func=_run_info)

    # list
    p_list = sub.add_parser("list", help="List all available algorithms.")
    p_list.set_defaults(func=_run_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
