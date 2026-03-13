from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, List, TypeVar

from app.config.cache_config import cache_service
from app.core.movies.domain.entities import Movie


TMovie = TypeVar("TMovie", bound=Movie)


def _is_cache_available() -> bool:
    return cache_service is not None


def cache_movie_by_id(expire: int = 300) -> Callable[..., Callable[..., Awaitable[Movie]]]:
    """
    Cache a single movie by its ID.

    Intended for use on `GetMovieByIdUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[Movie]]) -> Callable[..., Awaitable[Movie]]:
        @wraps(func)
        async def wrapper(self, movie_id: int, *args: Any, **kwargs: Any) -> Movie:
            if not _is_cache_available():
                return await func(self, movie_id, *args, **kwargs)

            key = f"movies:{movie_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return Movie(**cached)

            result = await func(self, movie_id, *args, **kwargs)
            await cache_service.set(key, result.model_dump(), expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_movies_in_exhibition(
    expire: int = 300,
) -> Callable[..., Callable[..., Awaitable[List[Movie]]]]:
    """
    Cache the list of movies in exhibition.

    Intended for use on `GetMoviesInExhitionUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[List[Movie]]]) -> Callable[..., Awaitable[List[Movie]]]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> List[Movie]:
            if not _is_cache_available():
                return await func(self, *args, **kwargs)

            key = "movies:in_exhibition"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [Movie(**m) for m in cached]

            result = await func(self, *args, **kwargs)
            await cache_service.set(
                key,
                [m.model_dump() for m in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_movie_showtimes(
    expire: int = 120,
) -> Callable[..., Callable[..., Awaitable[List[Any]]]]:
    """
    Cache movie showtimes lists.

    Intended for use on `GetMovieShowtimesUseCase.execute`.
    It stores plain JSON-serialisable data (dicts), so the use case should
    return simple DTOs, not ORM models.
    """

    def decorator(func: Callable[..., Awaitable[List[Any]]]) -> Callable[..., Awaitable[List[Any]]]:
        @wraps(func)
        async def wrapper(self, filters, page_data, *args: Any, **kwargs: Any) -> List[Any]:
            if not _is_cache_available():
                return await func(self, filters, page_data, *args, **kwargs)

            # Build a deterministic key based on filters and pagination
            filters_part = getattr(filters, "model_dump_json", None)
            if callable(filters_part):
                filters_key = filters.model_dump_json(sort_keys=True)
            else:
                filters_key = str(filters)

            key = f"movie_showtimes:{filters_key}:{getattr(page_data, 'page', '')}:{getattr(page_data, 'page_size', '')}"

            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return cached

            result = await func(self, filters, page_data, *args, **kwargs)
            await cache_service.set(key, result, expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def invalidate_movies_cache(
    patterns: List[str] | None = None,
) -> Callable[..., Callable[..., Awaitable[Any]]]:
    """
    Invalidate movie-related cache entries after write operations.

    Intended for use on create / update / delete movie use cases.
    """

    if patterns is None:
        patterns = [
            "movies:*",
            "movie_showtimes:*",
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

