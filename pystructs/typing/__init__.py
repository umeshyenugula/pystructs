"""Shared type aliases used across pystructs.

NOTE: This module shadows the stdlib typing module. This causes issues, but we work
around it by using lazy imports and __getattr__ to delegate to stdlib typing for
items we don't define locally.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable


# Minimal TypeVar implementation for runtime use with Generic classes
class TypeVar:
    """TypeVar implementation compatible with Generic."""

    def __init__(self, name, *constraints, bound=None):
        self.__name__ = name
        self.constraints = constraints
        self.bound = bound

    def __repr__(self):
        return self.__name__

    def __reduce__(self):
        return (TypeVar, (self.__name__,) + self.constraints, {"bound": self.bound})


# Minimal Generic implementation
class _GenericAlias:
    """Minimal Generic alias for runtime compatibility."""

    def __init__(self, origin, args):
        self.__origin__ = origin
        self.__args__ = args if isinstance(args, tuple) else (args,)

    def __repr__(self):
        args_str = ", ".join(repr(arg) for arg in self.__args__)
        return f"{self.__origin__.__name__}[{args_str}]"

    def __mro_entries__(self, bases):
        # Allow Generic[T] to be used in class bases
        return (self.__origin__,) if hasattr(self.__origin__, "__mro__") else ()


class _GenericMeta(type):
    """Metaclass for Generic that allows subscripting."""

    def __getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params,)
        return _GenericAlias(cls, params)


class Generic(metaclass=_GenericMeta):
    """Minimal Generic base class for runtime use."""

    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params,)
        return _GenericAlias(cls, params)


# Placeholder for Any
class Any:
    """Placeholder for typing.Any."""

    pass


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

# Keep track of what we've defined locally
_LOCAL_ITEMS = {
    "TypeVar",
    "Generic",
    "Any",
    "T",
    "K",
    "V",
    "N",
    "Number",
    "Comparator",
    "KeyFn",
    "GraphEdge",
    "WeightedAdj",
}

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
    "TypeVar",
    "Generic",
    "Any",
]


def __getattr__(name):
    """Delegate to stdlib typing for items we don't define locally."""
    # Avoid circular imports by using a delayed import mechanism
    if name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    # Try to get the item from stdlib typing
    import sys

    # Temporarily remove ourselves from sys.modules to allow stdlib typing to load
    local_module = sys.modules.pop(__name__, None)
    try:
        import typing as stdlib_typing

        result = getattr(stdlib_typing, name, None)
        if result is not None:
            return result
    finally:
        # Restore ourselves to sys.modules
        if local_module is not None:
            sys.modules[__name__] = local_module

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
