from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, Dict, List, Optional

from app.config.cache_config import cache_service
from app.core.cinema.domain.entities import Cinema


def _is_cache_available() -> bool:
    return cache_service is not None


def cache_cinema_by_id(expire: int = 3600) -> Callable[..., Callable[..., Awaitable[Cinema]]]:
    """
    Cache a single cinema by its ID.

    Intended for use on `GetCinemaByIdUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[Cinema]]) -> Callable[..., Awaitable[Cinema]]:
        @wraps(func)
        async def wrapper(self, cinema_id: int, *args: Any, **kwargs: Any) -> Cinema:
            if not _is_cache_available():
                return await func(self, cinema_id, *args, **kwargs)

            key = f"cinemas:{cinema_id}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return Cinema(**cached)

            result = await func(self, cinema_id, *args, **kwargs)
            await cache_service.set(key, result.model_dump(), expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_active_cinemas(expire: int = 3600) -> Callable[..., Callable[..., Awaitable[List[Cinema]]]]:
    """
    Cache the list of active cinemas.

    Intended for use on `ListActiveCinemasUseCase.execute`.
    """

    def decorator(func: Callable[..., Awaitable[List[Cinema]]]) -> Callable[..., Awaitable[List[Cinema]]]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> List[Cinema]:
            if not _is_cache_available():
                return await func(self, *args, **kwargs)

            key = "cinemas:active"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [Cinema(**c) for c in cached]

            result = await func(self, *args, **kwargs)
            await cache_service.set(
                key,
                [c.model_dump() for c in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_search_cinemas(
    expire: int = 1800,
) -> Callable[..., Callable[..., Awaitable[List[Cinema]]]]:
    """
    Cache cinema search results.

    Intended for use on `SearchCinemasUseCase.execute`.
    Keyed by page params and filter params, both treated as JSON-serialisable dicts.
    """

    def decorator(func: Callable[..., Awaitable[List[Cinema]]]) -> Callable[..., Awaitable[List[Cinema]]]:
        @wraps(func)
        async def wrapper(
            self,
            page_params: Dict[str, int],
            filter_params: Dict[str, Any],
            *args: Any,
            **kwargs: Any,
        ) -> List[Cinema]:
            if not _is_cache_available():
                return await func(self, page_params, filter_params, *args, **kwargs)

            key = f"cinemas:search:{sorted(page_params.items())}:{sorted(filter_params.items())}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                return [Cinema(**c) for c in cached]

            result = await func(self, page_params, filter_params, *args, **kwargs)
            await cache_service.set(
                key,
                [c.model_dump() for c in result],
                expire=expire,
            )  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def invalidate_cinema_cache(
    patterns: Optional[List[str]] = None,
) -> Callable[..., Callable[..., Awaitable[Any]]]:
    """
    Invalidate cinema-related cache entries after write operations.

    For cinemas, data is mostly static, but this ensures that if a cinema
    is created/updated/deleted, cached reads stay consistent.
    """

    if patterns is None:
        patterns = [
            "cinemas:*",
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

