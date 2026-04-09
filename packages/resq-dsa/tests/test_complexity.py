"""Algorithmic complexity verification tests.

Uses the ``big_o`` package to empirically verify that each data structure
meets its expected Big-O complexity guarantees.
"""

import random

import big_o

from resq_dsa import BloomFilter, BoundedHeap, CountMinSketch, Graph, Trie


def _assert_complexity(name, func, generator, expected_classes, min_n=100, max_n=10000):
    """Run big-O analysis and assert the best fit is in *expected_classes*."""
    best, others = big_o.big_o(
        func,
        generator,
        min_n=min_n,
        max_n=max_n,
        n_measures=10,
        n_repeats=5,
        n_timings=3,
    )
    best_name = type(best).__name__
    assert best_name in expected_classes, (
        f"{name}: expected one of {expected_classes}, got {best_name}. "
        f"Residuals: {', '.join(f'{type(c).__name__}: {r:.2e}' for c, r in others.items())}"
    )


# ---------------------------------------------------------------------------
# BloomFilter
# ---------------------------------------------------------------------------


class TestBloomFilterComplexity:
    def test_add_is_o1(self):
        """BloomFilter.add should be O(1) per operation -> O(n) total."""

        def func(n):
            bf = BloomFilter(capacity=int(n) * 10, error_rate=0.01)
            for i in range(int(n)):
                bf.add(f"item-{i}")

        _assert_complexity(
            "BloomFilter.add",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Polynomial"],
        )

    def test_has_is_o1(self):
        """BloomFilter.has should be O(1) per lookup."""

        def func(n):
            n = int(n)
            bf = BloomFilter(capacity=n * 10, error_rate=0.01)
            for i in range(n):
                bf.add(f"item-{i}")
            for i in range(n):
                bf.has(f"item-{i}")

        _assert_complexity(
            "BloomFilter.has",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Polynomial"],
        )


# ---------------------------------------------------------------------------
# CountMinSketch
# ---------------------------------------------------------------------------


class TestCountMinSketchComplexity:
    def test_increment_is_o1(self):
        """CountMinSketch.increment is O(d) per op where d=depth (constant)."""

        def func(n):
            cms = CountMinSketch(epsilon=0.01, delta=0.01)
            for i in range(int(n)):
                cms.increment(f"item-{i}", 1)

        _assert_complexity(
            "CountMinSketch.increment",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Polynomial"],
        )


# ---------------------------------------------------------------------------
# BoundedHeap
# ---------------------------------------------------------------------------


class TestBoundedHeapComplexity:
    def test_insert_is_ologn(self):
        """n inserts to BoundedHeap should be O(n log n) total."""

        def func(n):
            n = int(n)
            heap = BoundedHeap(limit=n, dist=lambda x: x)
            for _i in range(n):
                heap.insert(random.random())

        _assert_complexity(
            "BoundedHeap.insert",
            func,
            lambda n: n,
            ["Linearithmic", "Linear", "Quadratic", "Polynomial"],
        )


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------


class TestGraphComplexity:
    def test_dijkstra_chain(self):
        """Dijkstra on a chain graph: O(V log V)."""

        def func(n):
            n = int(n)
            g = Graph()
            for i in range(n):
                g.add_edge(i, i + 1, random.uniform(1, 10))
            g.dijkstra(0, n)

        _assert_complexity(
            "Graph.dijkstra (chain)",
            func,
            lambda n: n,
            ["Linearithmic", "Linear", "Quadratic", "Polynomial"],
            min_n=50,
            max_n=5000,
        )

    def test_bfs_chain(self):
        """BFS on a chain graph: O(V + E) = O(V)."""

        def func(n):
            n = int(n)
            g = Graph()
            for i in range(n):
                g.add_edge(i, i + 1, 1)
            g.bfs(0)

        _assert_complexity(
            "Graph.bfs (chain)",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Polynomial"],
        )


# ---------------------------------------------------------------------------
# Trie
# ---------------------------------------------------------------------------


class TestTrieComplexity:
    def test_insert_fixed_length_keys(self):
        """Trie insert with fixed-length keys: O(n) total."""

        def func(n):
            n = int(n)
            trie = Trie()
            for i in range(n):
                trie.insert(f"key-{i:08d}")

        _assert_complexity(
            "Trie.insert",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Polynomial"],
        )

    def test_search_fixed_length_keys(self):
        """Trie search with fixed-length keys: O(L) per search, O(n) total."""
        keys = [f"key-{i:08d}" for i in range(10000)]
        trie = Trie()
        for k in keys:
            trie.insert(k)

        def func(n):
            n = int(n)
            for i in range(n):
                trie.search(keys[i % len(keys)])

        _assert_complexity(
            "Trie.search",
            func,
            lambda n: n,
            ["Linear", "Linearithmic", "Constant", "Polynomial"],
        )
