"""Tests for pystructs data structures."""

from __future__ import annotations

import random
import unittest

from pystructs.core.exceptions import (
    EmptyStructureError,
    InvalidInputError,
    KeyNotFoundError,
    StructureOverflowError,
)
from pystructs.structures import (
    Deque,
    DoublyLinkedList,
    Graph,
    HashMap,
    HashSet,
    LinkedHashMap,
    LinkedHashSet,
    MaxHeap,
    MinHeap,
    Queue,
    SinglyLinkedList,
    Stack,
    TreeMap,
    TreeSet,
    Trie,
)


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)

    def test_empty_pop_raises(self):
        with self.assertRaises(EmptyStructureError):
            Stack().pop()

    def test_empty_peek_raises(self):
        with self.assertRaises(EmptyStructureError):
            Stack().peek()

    def test_peek_no_remove(self):
        stack = Stack()
        stack.push(42)
        self.assertEqual(stack.peek(), 42)
        self.assertEqual(len(stack), 1)

    def test_maxsize(self):
        stack = Stack(maxsize=2)
        stack.push(1)
        stack.push(2)
        with self.assertRaises(StructureOverflowError):
            stack.push(3)

    def test_invalid_maxsize(self):
        with self.assertRaises(InvalidInputError):
            Stack(maxsize=-1)

    def test_contains(self):
        stack = Stack()
        stack.push(10)
        self.assertIn(10, stack)
        self.assertNotIn(99, stack)

    def test_to_list_lifo(self):
        stack = Stack()
        for value in range(5):
            stack.push(value)
        self.assertEqual(stack.to_list(), [4, 3, 2, 1, 0])

    def test_large(self):
        stack = Stack()
        for value in range(100_000):
            stack.push(value)
        for value in range(99_999, -1, -1):
            self.assertEqual(stack.pop(), value)

    def test_clear(self):
        stack = Stack()
        stack.push(1)
        stack.clear()
        self.assertTrue(stack.is_empty)

    def test_bool(self):
        stack = Stack()
        self.assertFalse(bool(stack))
        stack.push(1)
        self.assertTrue(bool(stack))


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)

    def test_empty_raises(self):
        with self.assertRaises(EmptyStructureError):
            Queue().dequeue()

    def test_peek(self):
        queue = Queue()
        queue.enqueue(5)
        self.assertEqual(queue.peek(), 5)
        self.assertEqual(len(queue), 1)

    def test_large(self):
        queue = Queue()
        for value in range(50_000):
            queue.enqueue(value)
        for value in range(50_000):
            self.assertEqual(queue.dequeue(), value)


class TestDeque(unittest.TestCase):
    def test_both_ends(self):
        deque = Deque()
        deque.push_front(1)
        deque.push_back(2)
        deque.push_front(0)
        self.assertEqual(deque.pop_front(), 0)
        self.assertEqual(deque.pop_back(), 2)
        self.assertEqual(deque.pop_front(), 1)

    def test_empty_front_raises(self):
        with self.assertRaises(EmptyStructureError):
            Deque().pop_front()

    def test_empty_back_raises(self):
        with self.assertRaises(EmptyStructureError):
            Deque().pop_back()

    def test_peek(self):
        deque = Deque()
        deque.push_back(1)
        deque.push_back(2)
        self.assertEqual(deque.peek_front(), 1)
        self.assertEqual(deque.peek_back(), 2)


class TestSinglyLinkedList(unittest.TestCase):
    def test_append_iterate(self):
        linked_list = SinglyLinkedList()
        for value in [1, 2, 3]:
            linked_list.append(value)
        self.assertEqual(list(linked_list), [1, 2, 3])

    def test_prepend(self):
        linked_list = SinglyLinkedList()
        linked_list.append(2)
        linked_list.prepend(1)
        self.assertEqual(list(linked_list), [1, 2])

    def test_pop_front(self):
        linked_list = SinglyLinkedList()
        linked_list.append(10)
        linked_list.append(20)
        self.assertEqual(linked_list.pop_front(), 10)

    def test_remove(self):
        linked_list = SinglyLinkedList()
        linked_list.extend([1, 2, 3])
        self.assertTrue(linked_list.remove(2))
        self.assertEqual(list(linked_list), [1, 3])
        self.assertFalse(linked_list.remove(99))

    def test_reverse(self):
        linked_list = SinglyLinkedList()
        linked_list.extend([1, 2, 3, 4])
        linked_list.reverse()
        self.assertEqual(list(linked_list), [4, 3, 2, 1])

    def test_find_middle(self):
        linked_list = SinglyLinkedList()
        linked_list.extend([1, 2, 3, 4, 5])
        self.assertEqual(linked_list.find_middle(), 3)

    def test_cycle_detection(self):
        linked_list = SinglyLinkedList()
        linked_list.extend([1, 2, 3])
        self.assertFalse(linked_list.has_cycle())

    def test_empty_pop_raises(self):
        with self.assertRaises(EmptyStructureError):
            SinglyLinkedList().pop_front()

    def test_contains(self):
        linked_list = SinglyLinkedList()
        linked_list.extend([10, 20])
        self.assertIn(10, linked_list)
        self.assertNotIn(99, linked_list)

    def test_extend_len(self):
        linked_list = SinglyLinkedList()
        linked_list.extend(range(100))
        self.assertEqual(len(linked_list), 100)

    def test_empty_middle(self):
        self.assertIsNone(SinglyLinkedList().find_middle())


class TestDoublyLinkedList(unittest.TestCase):
    def test_append_reversed(self):
        linked_list = DoublyLinkedList()
        for value in [1, 2, 3]:
            linked_list.append(value)
        self.assertEqual(list(reversed(linked_list)), [3, 2, 1])

    def test_pop_both_ends(self):
        linked_list = DoublyLinkedList()
        linked_list.append(1)
        linked_list.append(2)
        linked_list.append(3)
        self.assertEqual(linked_list.pop_back(), 3)
        self.assertEqual(linked_list.pop_front(), 1)

    def test_empty_raises(self):
        with self.assertRaises(EmptyStructureError):
            DoublyLinkedList().pop_back()


class TestMinHeap(unittest.TestCase):
    def test_min_order(self):
        heap = MinHeap()
        for value in [5, 1, 3, 2, 4]:
            heap.push(value)
        self.assertEqual([heap.pop() for _ in range(5)], [1, 2, 3, 4, 5])

    def test_from_iterable(self):
        heap = MinHeap.from_iterable([9, 4, 7, 1])
        self.assertEqual(heap.peek(), 1)

    def test_empty_raises(self):
        with self.assertRaises(EmptyStructureError):
            MinHeap().pop()

    def test_nsmallest(self):
        heap = MinHeap.from_iterable(range(100))
        self.assertEqual(heap.nsmallest(3), [0, 1, 2])

    def test_large(self):
        values = random.sample(range(10_000), 1000)
        heap = MinHeap.from_iterable(values)
        self.assertEqual([heap.pop() for _ in range(len(values))], sorted(values))


class TestMaxHeap(unittest.TestCase):
    def test_max_order(self):
        heap = MaxHeap()
        for value in [3, 1, 4, 1, 5]:
            heap.push(value)
        self.assertEqual(heap.pop(), 5)
        self.assertEqual(heap.pop(), 4)

    def test_from_iterable(self):
        heap = MaxHeap.from_iterable([9, 4, 7, 1])
        self.assertEqual(heap.peek(), 9)

    def test_empty_raises(self):
        with self.assertRaises(EmptyStructureError):
            MaxHeap().pop()


class TestTrie(unittest.TestCase):
    def test_insert_search(self):
        trie = Trie()
        trie.insert("hello")
        self.assertTrue(trie.search("hello"))
        self.assertFalse(trie.search("hell"))
        self.assertTrue(trie.starts_with("hell"))

    def test_delete(self):
        trie = Trie()
        trie.insert("cat")
        trie.insert("car")
        self.assertTrue(trie.delete("cat"))
        self.assertFalse(trie.search("cat"))
        self.assertTrue(trie.search("car"))

    def test_words_with_prefix(self):
        trie = Trie()
        for word in ["apple", "app", "application", "banana"]:
            trie.insert(word)
        self.assertEqual(
            sorted(trie.words_with_prefix("app")),
            ["app", "apple", "application"],
        )

    def test_empty_search(self):
        self.assertFalse(Trie().search("x"))

    def test_len(self):
        trie = Trie()
        trie.insert("a")
        trie.insert("b")
        trie.insert("a")
        self.assertEqual(len(trie), 2)

    def test_delete_nonexistent(self):
        trie = Trie()
        trie.insert("abc")
        self.assertFalse(trie.delete("xyz"))


class TestGraph(unittest.TestCase):
    def test_add_edges(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        self.assertTrue(graph.has_vertex(1))
        self.assertTrue(graph.has_edge(1, 2))
        self.assertEqual(graph.vertex_count, 3)

    def test_directed(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "B")
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertFalse(graph.has_edge("B", "A"))

    def test_undirected_bidirectional(self):
        graph = Graph()
        graph.add_edge(1, 2)
        self.assertTrue(graph.has_edge(1, 2))
        self.assertTrue(graph.has_edge(2, 1))

    def test_neighbors(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        self.assertEqual(sorted(graph.neighbors(1)), [2, 3])

    def test_remove_edge(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "B")
        graph.remove_edge("A", "B")
        self.assertFalse(graph.has_edge("A", "B"))

    def test_len_iter(self):
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        self.assertEqual(len(graph), 3)
        self.assertEqual(set(graph), {1, 2, 3})


class TestHashMap(unittest.TestCase):
    def test_put_get(self):
        mapping = HashMap()
        mapping.put("a", 1)
        self.assertEqual(mapping.get("a"), 1)

    def test_missing_raises(self):
        with self.assertRaises(KeyNotFoundError):
            HashMap().get("x")

    def test_get_or_default(self):
        mapping = HashMap()
        self.assertEqual(mapping.get_or_default("x", 42), 42)

    def test_put_if_absent(self):
        mapping = HashMap()
        mapping.put("k", 1)
        mapping.put_if_absent("k", 99)
        self.assertEqual(mapping.get("k"), 1)

    def test_put_if_absent_new(self):
        mapping = HashMap()
        mapping.put_if_absent("new", 5)
        self.assertEqual(mapping.get("new"), 5)

    def test_remove(self):
        mapping = HashMap()
        mapping.put("a", 1)
        self.assertEqual(mapping.remove("a"), 1)
        self.assertNotIn("a", mapping)

    def test_remove_missing_raises(self):
        with self.assertRaises(KeyNotFoundError):
            HashMap().remove("nope")

    def test_merge(self):
        mapping = HashMap()
        mapping.put("c", 1)
        mapping.merge("c", 5, lambda old, new: old + new)
        self.assertEqual(mapping.get("c"), 6)

    def test_compute_if_absent(self):
        mapping = HashMap()
        result = mapping.compute_if_absent("k", lambda key: key.upper())
        self.assertEqual(result, "K")
        self.assertEqual(mapping.get("k"), "K")


class TestHashSet(unittest.TestCase):
    def test_add_contains(self):
        values = HashSet()
        values.add(1)
        values.add(2)
        self.assertIn(1, values)

    def test_union(self):
        left = HashSet()
        right = HashSet()
        left.add(1)
        right.add(2)
        result = left.union(right)
        self.assertIn(1, result)
        self.assertIn(2, result)

    def test_intersection(self):
        left = HashSet()
        right = HashSet()
        left.add_all([1, 2, 3])
        right.add_all([2, 3, 4])
        result = left.intersection(right)
        self.assertEqual(sorted(result.to_list()), [2, 3])

    def test_difference(self):
        left = HashSet()
        right = HashSet()
        left.add_all([1, 2, 3])
        right.add_all([2, 3])
        result = left.difference(right)
        self.assertEqual(sorted(result.to_list()), [1])

    def test_is_subset(self):
        left = HashSet()
        right = HashSet()
        left.add_all([1, 2])
        right.add_all([1, 2, 3])
        self.assertTrue(left.is_subset_of(right))
        self.assertFalse(right.is_subset_of(left))

    def test_no_duplicates(self):
        values = HashSet()
        values.add(1)
        values.add(1)
        self.assertEqual(len(values), 1)


class TestTreeMap(unittest.TestCase):
    def test_put_get(self):
        tree_map = TreeMap()
        tree_map.put(5, "five")
        self.assertEqual(tree_map.get(5), "five")

    def test_sorted_keys(self):
        tree_map = TreeMap()
        for key in [3, 1, 4, 1, 5, 9]:
            tree_map.put(key, key)
        self.assertEqual(tree_map.keys(), sorted(set([3, 1, 4, 1, 5, 9])))

    def test_min_max(self):
        tree_map = TreeMap()
        for key in [10, 3, 7]:
            tree_map.put(key, key)
        self.assertEqual(tree_map.min_key(), 3)
        self.assertEqual(tree_map.max_key(), 10)

    def test_delete(self):
        tree_map = TreeMap()
        tree_map.put(1, "a")
        tree_map.put(2, "b")
        tree_map.delete(1)
        self.assertFalse(tree_map.contains_key(1))

    def test_missing_raises(self):
        with self.assertRaises(KeyNotFoundError):
            TreeMap().get(99)

    def test_large_random(self):
        values = random.sample(range(10_000), 1000)
        tree_map = TreeMap()
        for value in values:
            tree_map.put(value, value)
        self.assertEqual(tree_map.keys(), sorted(values))

    def test_update(self):
        tree_map = TreeMap()
        tree_map.put(1, "old")
        tree_map.put(1, "new")
        self.assertEqual(tree_map.get(1), "new")


class TestTreeSet(unittest.TestCase):
    def test_sorted_iteration(self):
        tree_set = TreeSet()
        tree_set.add_all([5, 2, 8, 1])
        self.assertEqual(list(tree_set), [1, 2, 5, 8])

    def test_contains_remove(self):
        tree_set = TreeSet()
        tree_set.add(10)
        self.assertTrue(tree_set.contains(10))
        tree_set.remove(10)
        self.assertFalse(tree_set.contains(10))

    def test_no_duplicates(self):
        tree_set = TreeSet()
        tree_set.add(1)
        tree_set.add(1)
        self.assertEqual(len(tree_set), 1)

    def test_min_max(self):
        tree_set = TreeSet()
        tree_set.add_all([5, 2, 9, 1])
        self.assertEqual(tree_set.min_key(), 1)
        self.assertEqual(tree_set.max_key(), 9)


class TestLinkedHashMap(unittest.TestCase):
    def test_insertion_order(self):
        linked_hash_map = LinkedHashMap()
        for key, value in [("a", 1), ("b", 2), ("c", 3)]:
            linked_hash_map.put(key, value)
        self.assertEqual(linked_hash_map.keys(), ["a", "b", "c"])

    def test_update_preserves_order(self):
        linked_hash_map = LinkedHashMap()
        linked_hash_map.put("a", 1)
        linked_hash_map.put("b", 2)
        linked_hash_map.put("a", 99)
        self.assertEqual(linked_hash_map.keys(), ["a", "b"])
        self.assertEqual(linked_hash_map.get("a"), 99)

    def test_remove(self):
        linked_hash_map = LinkedHashMap()
        linked_hash_map.put("x", 10)
        linked_hash_map.remove("x")
        self.assertNotIn("x", linked_hash_map)

    def test_missing_raises(self):
        with self.assertRaises(KeyNotFoundError):
            LinkedHashMap().get("missing")


class TestLinkedHashSet(unittest.TestCase):
    def test_insertion_order(self):
        linked_hash_set = LinkedHashSet()
        linked_hash_set.add_all([3, 1, 2])
        self.assertEqual(list(linked_hash_set), [3, 1, 2])

    def test_no_duplicates(self):
        linked_hash_set = LinkedHashSet()
        linked_hash_set.add(1)
        linked_hash_set.add(1)
        self.assertEqual(len(linked_hash_set), 1)

    def test_remove(self):
        linked_hash_set = LinkedHashSet()
        linked_hash_set.add(5)
        linked_hash_set.add(6)
        linked_hash_set.remove(5)
        self.assertNotIn(5, linked_hash_set)
        self.assertEqual(list(linked_hash_set), [6])


if __name__ == "__main__":
    unittest.main()
