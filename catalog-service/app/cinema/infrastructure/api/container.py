"""
Centralized container for Cinema FastAPI dependency providers.

Controllers can depend on these callables without importing every provider
function individually.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any

from . import depedencies


@dataclass(frozen=True)
class CinemaUseCaseContainer:
    # Query
    get_cinema_by_id_use_case: Callable[..., Any] = depedencies.get_cinema_by_id_use_case
    get_active_cinemas_use_case: Callable[..., Any] = (
        depedencies.get_active_cinemas_use_case
    )
    search_cinemas_use_case: Callable[..., Any] = depedencies.search_cinemas_use_case

    # Command
    create_cinema_use_case: Callable[..., Any] = depedencies.create_cinema_use_case
    update_cinema_use_case: Callable[..., Any] = depedencies.update_cinema_use_case
    delete_cinema_use_case: Callable[..., Any] = depedencies.delete_cinema_use_case
    restore_cinema_use_case: Callable[..., Any] = depedencies.restore_cinema_use_case

    # Filter dependencies
    get_filters: Callable[..., Any] = depedencies.get_filters


cinema_use_cases = CinemaUseCaseContainer()

