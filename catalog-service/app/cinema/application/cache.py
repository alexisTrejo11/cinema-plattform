from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, Dict, List, Optional, TYPE_CHECKING

from app.config.cache_config import cache_service
from app.cinema.domain.entities import Cinema
from app.shared.core.pagination import Page, PaginationParams

if TYPE_CHECKING:
    from app.cinema.application.dtos import SearchCinemaFilters


def _is_cache_available() -> bool:
    return cache_service is not None


def cache_cinema_by_id(
    expire: int = 3600,
) -> Callable[..., Callable[..., Awaitable[Cinema]]]:
    """
    Cache a single cinema by its ID.

    Intended for use on `GetCinemaByIdUseCase.execute`.
    """

    def decorator(
        func: Callable[..., Awaitable[Cinema]],
    ) -> Callable[..., Awaitable[Cinema]]:
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


def cache_active_cinemas(
    expire: int = 3600,
) -> Callable[..., Callable[..., Awaitable[Page[Cinema]]]]:
    """
    Cache the paginated list of active cinemas.

    Intended for use on `ListActiveCinemasUseCase.execute`.
    """

    def decorator(
        func: Callable[..., Awaitable[Page[Cinema]]],
    ) -> Callable[..., Awaitable[Page[Cinema]]]:
        @wraps(func)
        async def wrapper(
            self, params: PaginationParams, *args: Any, **kwargs: Any
        ) -> Page[Cinema]:
            if not _is_cache_available():
                return await func(self, params, *args, **kwargs)

            key = f"cinemas:active:{params.offset}:{params.limit}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                # Deserialize cached Page
                items = [Cinema(**c) for c in cached["items"]]
                return Page(
                    items=items,
                    total=cached["total"],
                    page=cached["page"],
                    page_size=cached["page_size"],
                    total_pages=cached["total_pages"],
                    has_next=cached["has_next"],
                    has_previous=cached["has_previous"],
                )

            result = await func(self, params, *args, **kwargs)
            # Serialize Page for caching
            cache_data = {
                "items": [c.model_dump() for c in result.items],
                "total": result.total,
                "page": result.page,
                "page_size": result.page_size,
                "total_pages": result.total_pages,
                "has_next": result.has_next,
                "has_previous": result.has_previous,
            }
            await cache_service.set(key, cache_data, expire=expire)  # type: ignore[union-attr]
            return result

        return wrapper

    return decorator


def cache_search_cinemas(
    expire: int = 1800,
) -> Callable[..., Callable[..., Awaitable[Page[Cinema]]]]:
    """
    Cache cinema search results.

    Intended for use on `SearchCinemasUseCase.execute`.
    Keyed by pagination params and filter params.
    """

    def decorator(
        func: Callable[..., Awaitable[Page[Cinema]]],
    ) -> Callable[..., Awaitable[Page[Cinema]]]:
        @wraps(func)
        async def wrapper(
            self,
            params: PaginationParams,
            filters: "SearchCinemaFilters",
            *args: Any,
            **kwargs: Any,
        ) -> Page[Cinema]:
            if not _is_cache_available():
                return await func(self, params, filters, *args, **kwargs)

            # Create cache key from params and filters
            filter_dict = filters.model_dump(exclude_none=True)
            key = f"cinemas:search:{params.offset}:{params.limit}:{sorted(filter_dict.items())}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                # Deserialize cached Page
                items = [Cinema(**c) for c in cached["items"]]
                return Page(
                    items=items,
                    total=cached["total"],
                    page=cached["page"],
                    page_size=cached["page_size"],
                    total_pages=cached["total_pages"],
                    has_next=cached["has_next"],
                    has_previous=cached["has_previous"],
                )

            result = await func(self, params, filters, *args, **kwargs)
            # Serialize Page for caching
            cache_data = {
                "items": [c.model_dump() for c in result.items],
                "total": result.total,
                "page": result.page,
                "page_size": result.page_size,
                "total_pages": result.total_pages,
                "has_next": result.has_next,
                "has_previous": result.has_previous,
            }
            await cache_service.set(
                key,
                cache_data,
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
