"""
Centralized container for Movie FastAPI dependency providers.

This reduces the number of imports required in controllers: instead of
importing every `get_*_use_case` function from `dependencies.py`, controllers
can use a single `movie_use_cases` instance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from . import dependencies


@dataclass(frozen=True)
class MovieUseCaseContainer:
    # Query
    get_movie_by_id_use_case: Callable[..., Any] = dependencies.get_movie_by_id_use_case
    get_active_movies_use_case: Callable[..., Any] = (
        dependencies.get_active_movies_use_case
    )
    search_movies_use_case: Callable[..., Any] = dependencies.search_movies_use_case

    # Command
    create_movie_use_case: Callable[..., Any] = dependencies.create_movie_use_case
    update_movie_use_case: Callable[..., Any] = dependencies.update_movie_use_case
    delete_movie_use_case: Callable[..., Any] = dependencies.delete_movie_use_case


movie_use_cases = MovieUseCaseContainer()

