"""Data structures module."""

from pystructs.structures.graph import Graph
from pystructs.structures.hash_map import HashMap, HashSet
from pystructs.structures.heap import MaxHeap, MinHeap
from pystructs.structures.linked_hash import LinkedHashMap, LinkedHashSet
from pystructs.structures.linked_list import DoublyLinkedList, SinglyLinkedList
from pystructs.structures.queue import Deque, Queue
from pystructs.structures.stack import Stack
from pystructs.structures.tree_map import TreeMap, TreeSet
from pystructs.structures.trie import Trie

__all__ = [
    "Stack",
    "Queue",
    "Deque",
    "SinglyLinkedList",
    "DoublyLinkedList",
    "MinHeap",
    "MaxHeap",
    "Trie",
    "Graph",
    "HashMap",
    "HashSet",
    "TreeMap",
    "TreeSet",
    "LinkedHashMap",
    "LinkedHashSet",
]
