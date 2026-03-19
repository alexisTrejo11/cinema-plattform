"""
Centralized container for Showtime FastAPI dependency providers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from . import dependencies


@dataclass(frozen=True)
class ShowtimeUseCaseContainer:
    # Query
    search_showtimes_use_case: Callable[..., Any] = dependencies.search_showtimes_use_case
    get_showtime_by_id_use_case: Callable[..., Any] = (
        dependencies.get_showtime_by_id_use_case
    )

    # Command
    draft_showtime_use_case: Callable[..., Any] = dependencies.draft_showtime_use_case
    launch_showtime_use_case: Callable[..., Any] = dependencies.launch_showtime_use_case
    cancel_showtime_use_case: Callable[..., Any] = dependencies.cancel_showtime_use_case
    restore_showtime_use_case: Callable[..., Any] = (
        dependencies.restore_showtime_use_case
    )
    update_showtime_use_case: Callable[..., Any] = dependencies.update_showtime_use_case
    delete_showtime_use_case: Callable[..., Any] = dependencies.delete_showtime_use_case


showtime_use_cases = ShowtimeUseCaseContainer()

