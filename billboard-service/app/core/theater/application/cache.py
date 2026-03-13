from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, Dict, List, Optional

from app.config.cache_config import cache_service
from app.core.theater.domain.theater import Theater
from app.core.theater.domain.seat import TheaterSeat


def _is_cache_available() -> bool:
    return cache_service is not None


# ---------- THEATER CACHE ----------

def cache_theater_by_id(expire: int = 3600) -> Callable[..., Callable[..., Awaitable[Optional[Theater]]]]:
    """
    Cache a single theater by its ID.

    Intended for use on `GetTheaterByIdUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[Optional[Theater]]]) -> Callable[..., Awaitable[Optional[Theater]]]:
        @wraps(func)
        async def wrapper(self, theater_id: int, *args: Any, **kwargs: Any) -> Optional[Theater]:
            if not _is_cache_available():
                return await func(self, theater_id, *args, **kwargs)

            key = f"theaters:{theater_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return Theater(**cached)

            result = await func(self, theater_id, *args, **kwargs)
            if result is not None:
                await cache_service.set(key, result.__dict__, expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_theaters_by_cinema(expire: int = 3600) -> Callable[..., Callable[..., Awaitable[List[Theater]]]]:
    """
    Cache the list of theaters for a given cinema.

    Intended for use on `GetTheatersByCinemaUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[List[Theater]]]) -> Callable[..., Awaitable[List[Theater]]]:
        @wraps(func)
        async def wrapper(self, cinema_id: int, *args: Any, **kwargs: Any) -> List[Theater]:
            if not _is_cache_available():
                return await func(self, cinema_id, *args, **kwargs)

            key = f"theaters:by_cinema:{cinema_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [Theater(**t) for t in cached]

            result = await func(self, cinema_id, *args, **kwargs)
            await cache_service.set(
                key,
                [t.__dict__ for t in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_theaters_list(expire: int = 1800) -> Callable[..., Callable[..., Awaitable[List[Theater]]]]:
    """
    Cache the paginated list of theaters.

    Intended for use on `ListTheatersUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[List[Theater]]]) -> Callable[..., Awaitable[List[Theater]]]:
        @wraps(func)
        async def wrapper(self, page_params: Dict[str, Any], *args: Any, **kwargs: Any) -> List[Theater]:
            if not _is_cache_available():
                return await func(self, page_params, *args, **kwargs)

            # Normalize page params into a deterministic key
            key = f"theaters:list:{sorted((page_params or {}).items())}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [Theater(**t) for t in cached]

            result = await func(self, page_params, *args, **kwargs)
            await cache_service.set(
                key,
                [t.__dict__ for t in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def invalidate_theater_cache(
    patterns: Optional[List[str]] = None,
) -> Callable[..., Callable[..., Awaitable[Any]]]:
    """
    Invalidate theater-related cache entries after write operations.

    Theaters are relatively static, but we still invalidate so that
    any structural changes are reflected immediately.
    """

    if patterns is None:
        patterns = [
            "theaters:*",
            "seats:*",
        ]

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            if _is_cache_available():
                for pattern in patterns:  # type: ignore[union-attr]
                    await cache_service.delete_pattern(pattern)  # type: ignore[union-attr]

            return result

        return wrapper

    return decorator


# ---------- SEAT CACHE ----------

def cache_seat_by_id(expire: int = 3600) -> Callable[..., Callable[..., Awaitable[TheaterSeat]]]:
    """
    Cache a single theater seat by its ID.

    Intended for use on `GetTheaterSeatByIdUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[TheaterSeat]]) -> Callable[..., Awaitable[TheaterSeat]]:
        @wraps(func)
        async def wrapper(self, seat_id: int, *args: Any, **kwargs: Any) -> TheaterSeat:
            if not _is_cache_available():
                return await func(self, seat_id, *args, **kwargs)

            key = f"seats:{seat_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return TheaterSeat(**cached)

            result = await func(self, seat_id, *args, **kwargs)
            await cache_service.set(key, result.__dict__, expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_seats_by_theater(expire: int = 1800) -> Callable[..., Callable[..., Awaitable[List[TheaterSeat]]]]:
    """
    Cache all seats for a theater.

    Intended for use on `GetSeatsByTheaterUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[List[TheaterSeat]]]) -> Callable[..., Awaitable[List[TheaterSeat]]]:
        @wraps(func)
        async def wrapper(self, theater_id: int, *args: Any, **kwargs: Any) -> List[TheaterSeat]:
            if not _is_cache_available():
                return await func(self, theater_id, *args, **kwargs)

            key = f"seats:by_theater:{theater_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [TheaterSeat(**s) for s in cached]

            result = await func(self, theater_id, *args, **kwargs)
            await cache_service.set(
                key,
                [s.__dict__ for s in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def invalidate_seats_cache(
    patterns: Optional[List[str]] = None,
) -> Callable[..., Callable[..., Awaitable[Any]]]:
    """
    Invalidate seat-related cache entries after seat write operations.
    """

    if patterns is None:
        patterns = [
            "seats:*",
        ]

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            if _is_cache_available():
                for pattern in patterns:  # type: ignore[union-attr]
                    await cache_service.delete_pattern(pattern)  # type: ignore[union-attr]

            return result

        return wrapper

    return decorator

