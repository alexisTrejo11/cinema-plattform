from typing import Optional, Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func
from app.movies.domain.repositories import MovieRepository
from app.movies.application.dtos import SearchMovieFilters
from app.movies.domain.entities import Movie
from app.shared.core.pagination import PaginationParams, Page
from .models import MovieModel


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_active(self, params: PaginationParams) -> Page[Movie]:
        # Count total active movies
        count_stmt = (
            select(func.count())
            .select_from(MovieModel)
            .where(MovieModel.is_active == True)
        )
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        # Get paginated active movies
        stmt = select(MovieModel).where(MovieModel.is_active == True)
        stmt = stmt.offset(params.offset).limit(params.limit)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        movies = [Movie.model_validate(model) for model in models]
        return Page.create(items=movies, total=total, params=params)

    async def search(
        self, params: PaginationParams, filters: SearchMovieFilters
    ) -> Page[Movie]:
        # Build base query
        stmt = select(MovieModel)
        count_stmt = select(func.count()).select_from(MovieModel)

        # app. filters
        filter_conditions = self._build_filters(filters)
        if filter_conditions:
            stmt = stmt.where(and_(*filter_conditions))
            count_stmt = count_stmt.where(and_(*filter_conditions))

        # Get total count
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        # app. pagination
        stmt = stmt.offset(params.offset).limit(params.limit)

        # Execute query
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        movies = [Movie.model_validate(model) for model in models]
        return Page.create(items=movies, total=total, params=params)

    async def find_by_id(self, entity_id: int) -> Optional[Movie]:
        model = await self.session.get(MovieModel, entity_id)

        return Movie.model_validate(model) if model else None

    async def find_all(self, page_params: Dict[str, int]) -> List[Movie]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 10)

        stmt = select(MovieModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [Movie.model_validate(model) for model in models]

    async def save(self, entity: Movie) -> Movie:
        model = MovieModel.from_domain(entity)

        if entity.id is None:
            self.session.add(model)
        else:
            model = await self.session.merge(model)

        await self.session.commit()
        await self.session.refresh(model)

        return Movie.model_validate(model)

    async def delete(self, entity_id: int) -> None:
        stmt = delete(MovieModel).where(MovieModel.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def exists_by_id(self, entity_id: int) -> bool:
        stmt = select(MovieModel).where(MovieModel.id == entity_id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    def _build_filters(self, filters: SearchMovieFilters) -> List[Any]:
        """Build filter conditions from SearchMovieFilters."""
        conditions: List[Any] = []

        if filters.title:
            conditions.app.d(MovieModel.title.ilike(f"%{filters.title}%"))
        if filters.genre:
            conditions.app.d(MovieModel.genre == filters.genre)
        if filters.rating:
            conditions.app.d(MovieModel.rating == filters.rating)
        if filters.is_active is not None:
            conditions.app.d(MovieModel.is_active == filters.is_active)
        if filters.release_date_from:
            conditions.app.d(MovieModel.release_date >= filters.release_date_from)
        if filters.release_date_to:
            conditions.app.d(MovieModel.release_date <= filters.release_date_to)
        if filters.min_duration is not None:
            conditions.app.d(MovieModel.minute_duration >= filters.min_duration)
        if filters.max_duration is not None:
            conditions.app.d(MovieModel.minute_duration <= filters.max_duration)

        return conditions
