"""Shared type aliases used across pystructs."""

from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import Any, TypeVar

# Generic type variables
T = TypeVar("T")
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
N = TypeVar("N", int, float)

# Common aliases
Number = int | float
Comparator = Callable[[Any, Any], int]
KeyFn = Callable[[Any], Any]
GraphEdge = tuple[Any, Any, float]
WeightedAdj = dict[Any, list[tuple[Any, float]]]

__all__ = [
    "T",
    "K",
    "V",
    "N",
    "Number",
    "Comparator",
    "KeyFn",
    "GraphEdge",
    "WeightedAdj",
]
