from app.shared.core.exceptions import NotFoundException
from app.shared.core.pagination import PaginationParams, Page
from app.movies.domain.entities import Movie
from .dtos import SearchMovieFilters
from ..domain.repositories import MovieRepository
from .cache import (
    cache_movie_by_id,
    cache_movies_in_exhibition,
    cache_search_movies,
    invalidate_movies_cache,
)


class GetMovieByIdUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @cache_movie_by_id()
    async def execute(self, id: int) -> Movie:
        movie = await self.movie_repository.find_by_id(id)
        if not movie:
            raise NotFoundException("Movie", id)

        return movie


class GetMoviesInExhitionUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @cache_movies_in_exhibition()
    async def execute(self, params: PaginationParams) -> Page[Movie]:
        return await self.movie_repository.find_active(params)


class SearchMoviesUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @cache_search_movies()
    async def execute(
        self, params: PaginationParams, filters: SearchMovieFilters
    ) -> Page[Movie]:
        return await self.movie_repository.search(params, filters)


class CreateMovieUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @invalidate_movies_cache()
    async def execute(self, new_movie: Movie) -> Movie:
        movies = await self.movie_repository.save(new_movie)
        return movies


class UpdateMovieUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @invalidate_movies_cache()
    async def execute(self, movie_id: int, movie_updated: Movie) -> Movie:
        movie = await self.movie_repository.find_by_id(movie_id)
        if not movie:
            raise NotFoundException("Movie", movie_id)

        movie_updated.id = movie_id
        movies = await self.movie_repository.save(movie_updated)
        return movies


class DeleteMovieUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    @invalidate_movies_cache()
    async def execute(self, id: int) -> None:
        movie = await self.movie_repository.find_by_id(id)
        if not movie:
            raise NotFoundException("Movie", id)

        await self.movie_repository.delete(id)
