from __future__ import annotations

from functools import wraps
from typing import Any, Awaitable, Callable, List, TypeVar, TYPE_CHECKING

from app.config.cache_config import cache_service
from app.core.movies.domain.entities import Movie
from app.core.shared.pagination import Page, PaginationParams

if TYPE_CHECKING:
    from .dtos import SearchMovieFilters


TMovie = TypeVar("TMovie", bound=Movie)


def _is_cache_available() -> bool:
    return cache_service is not None


def cache_movie_by_id(
    expire: int = 300,
) -> Callable[..., Callable[..., Awaitable[Movie]]]:
    """
    Cache a single movie by its ID.

    Intended for use on `GetMovieByIdUseCase.execute`.
    """

    def decorator(
        func: Callable[..., Awaitable[Movie]],
    ) -> Callable[..., Awaitable[Movie]]:
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
) -> Callable[..., Callable[..., Awaitable[Page[Movie]]]]:
    """
    Cache the paginated list of movies in exhibition.

    Intended for use on `GetMoviesInExhitionUseCase.execute`.
    """

    def decorator(
        func: Callable[..., Awaitable[Page[Movie]]],
    ) -> Callable[..., Awaitable[Page[Movie]]]:
        @wraps(func)
        async def wrapper(
            self, params: PaginationParams, *args: Any, **kwargs: Any
        ) -> Page[Movie]:
            if not _is_cache_available():
                return await func(self, params, *args, **kwargs)

            key = f"movies:in_exhibition:{params.offset}:{params.limit}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                # Deserialize cached Page
                items = [Movie(**m) for m in cached["items"]]
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
                "items": [m.model_dump() for m in result.items],
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


def cache_search_movies(
    expire: int = 300,
) -> Callable[..., Callable[..., Awaitable[Page[Movie]]]]:
    """
    Cache movie search results.

    Intended for use on `SearchMoviesUseCase.execute`.
    Keyed by pagination params and filter params.
    """

    def decorator(
        func: Callable[..., Awaitable[Page[Movie]]],
    ) -> Callable[..., Awaitable[Page[Movie]]]:
        @wraps(func)
        async def wrapper(
            self,
            params: PaginationParams,
            filters: "SearchMovieFilters",
            *args: Any,
            **kwargs: Any,
        ) -> Page[Movie]:
            if not _is_cache_available():
                return await func(self, params, filters, *args, **kwargs)

            # Create cache key from params and filters
            filter_dict = filters.model_dump(exclude_none=True)
            key = f"movies:search:{params.offset}:{params.limit}:{sorted(filter_dict.items())}"
            cached = await cache_service.get(key)  # type: ignore[union-attr]
            if cached is not None:
                # Deserialize cached Page
                items = [Movie(**m) for m in cached["items"]]
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
                "items": [m.model_dump() for m in result.items],
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


def cache_movie_showtimes(
    expire: int = 120,
) -> Callable[..., Callable[..., Awaitable[List[Any]]]]:
    """
    Cache movie showtimes lists.

    Intended for use on `GetMovieShowtimesUseCase.execute`.
    It stores plain JSON-serialisable data (dicts), so the use case should
    return simple DTOs, not ORM models.
    """

    def decorator(
        func: Callable[..., Awaitable[List[Any]]],
    ) -> Callable[..., Awaitable[List[Any]]]:
        @wraps(func)
        async def wrapper(
            self, filters, page_data, *args: Any, **kwargs: Any
        ) -> List[Any]:
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
