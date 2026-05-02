"""Input validation utilities."""

from __future__ import annotations

from typing import Any, TypeVar

from pystructs.core.exceptions import InvalidInputError

T = TypeVar("T")


def require_not_none(value: Any, name: str = "value") -> None:
    if value is None:
        raise InvalidInputError(f"{name} must not be None.")


def require_positive(value: int | float, name: str = "value") -> None:
    if not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} must be a number, got {type(value).__name__}.")
    if value <= 0:
        raise InvalidInputError(f"{name} must be positive, got {value}.")


def require_non_negative(value: int | float, name: str = "value") -> None:
    if not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} must be a number, got {type(value).__name__}.")
    if value < 0:
        raise InvalidInputError(f"{name} must be non-negative, got {value}.")


def require_iterable(value: Any, name: str = "value") -> None:
    try:
        iter(value)
    except TypeError:
        raise InvalidInputError(f"{name} must be iterable, got {type(value).__name__}.") from None


def require_comparable(value: Any, name: str = "value") -> None:
    if not hasattr(value, "__lt__"):
        raise InvalidInputError(
            f"{name} must be comparable (support '<'), got {type(value).__name__}."
        )
