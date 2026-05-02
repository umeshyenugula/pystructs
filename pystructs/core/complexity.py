"""Algorithm complexity metadata decorators and registry."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Complexity:
    time_best: str
    time_average: str
    time_worst: str
    space: str
    stable: bool | None = None
    in_place: bool | None = None
    notes: str = ""


def complexity(
    time_best: str,
    time_average: str,
    time_worst: str,
    space: str,
    stable: bool | None = None,
    in_place: bool | None = None,
    notes: str = "",
) -> Callable:
    """Decorator that attaches complexity metadata to a function."""

    def decorator(fn: Callable) -> Callable:
        fn.__complexity__ = Complexity(
            time_best=time_best,
            time_average=time_average,
            time_worst=time_worst,
            space=space,
            stable=stable,
            in_place=in_place,
            notes=notes,
        )
        return fn

    return decorator


def get_complexity(fn: Callable) -> Complexity | None:
    return getattr(fn, "__complexity__", None)
