"""Custom exceptions for pystructs."""

from __future__ import annotations


class PyStructsError(Exception):
    """Base exception for all pystructs errors."""


# Backwards-compatible alias
DSAError = PyStructsError


class EmptyStructureError(PyStructsError):
    """Raised when an operation is attempted on an empty data structure."""

    def __init__(self, structure_name: str = "structure") -> None:
        super().__init__(f"Cannot perform operation on empty {structure_name}.")


class InvalidInputError(PyStructsError):
    """Raised when invalid input is provided to a function or data structure."""

    def __init__(self, message: str = "Invalid input provided.") -> None:
        super().__init__(message)


class StructureOverflowError(PyStructsError):
    """Raised when a bounded data structure exceeds its maximum capacity."""

    def __init__(self, structure_name: str = "structure", capacity: int = 0) -> None:
        super().__init__(f"{structure_name} has reached its maximum capacity of {capacity}.")


# Keep old name accessible for compatibility
OverflowError_ = StructureOverflowError


class KeyNotFoundError(PyStructsError):
    """Raised when a key is not found in a mapping structure."""

    def __init__(self, key: object) -> None:
        super().__init__(f"Key not found: {key!r}")


class GraphError(PyStructsError):
    """Raised for invalid graph operations (missing vertex/edge, negative cycles, etc.)."""
