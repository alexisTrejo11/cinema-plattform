"""
Centralized container for Theater FastAPI dependency providers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from . import depdencies


@dataclass(frozen=True)
class TheaterUseCaseContainer:
    get_theater_by_id_use_case: Callable[..., Any] = depdencies.get_theater_by_id_use_case
    get_theaters_by_cinema_use_case: Callable[..., Any] = (
        depdencies.get_theaters_by_cinema_use_case
    )
    list_theaters_use_case: Callable[..., Any] = depdencies.list_theaters_use_case
    search_theaters_use_case: Callable[..., Any] = depdencies.search_theaters_use_case
    create_theater_use_case: Callable[..., Any] = depdencies.create_theater_use_case
    update_theater_use_case: Callable[..., Any] = depdencies.update_theater_use_case
    delete_theater_use_case: Callable[..., Any] = depdencies.delete_theater_use_case
    restore_theater_use_case: Callable[..., Any] = depdencies.restore_theater_use_case


theater_use_cases = TheaterUseCaseContainer()

