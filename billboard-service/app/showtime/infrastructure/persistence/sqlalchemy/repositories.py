from typing import Any, Dict, List, Optional
from datetime import datetime, timezone, timedelta

from sqlalchemy import and_, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.core.pagination import PaginationParams, Page
from app.showtime.application.dtos import SearchShowtimeFilters
from app.showtime.domain.repositories import (
    ShowtimeSeatRepository,
    ShowTimeRepository,
)
from app.showtime.domain.entities import Showtime, ShowtimeSeat
from app.showtime.domain.repositories import (
    ShowtimeSeatRepository,
    ShowTimeRepository,
)


from .mappers import ShowtimeSeatModelMapper, ShowtimeModelMapper
from .models import ShowtimeModel, ShowtimeSeatModel


class SQLAlchemyShowtimeSeatRepository(ShowtimeSeatRepository):
    """
    SQLAlchemy implementation of the ShowtimeSeatRepository interface.
    Defines the contract for operations related to ShowtimeSeat entities.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_showtime_and_seat(
        self, showtime_id: int, seat_id: int
    ) -> Optional[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where(
                ShowtimeSeatModel.showtime_id == showtime_id,
                ShowtimeSeatModel.theater_seat_id == seat_id,
            )
        )
        model = result.scalars().first()

        return ShowtimeSeatModelMapper.to_domain(model) if model else None

    async def find_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where(
                ShowtimeSeatModel.showtime_id == showtime_id
            )
        )
        models = result.scalars().all()

        return [ShowtimeSeatModelMapper.to_domain(model) for model in models]

    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        seat_models = [ShowtimeSeatModelMapper.from_domain(seat) for seat in seats]

        self.session.add_all(seat_models)
        await self.session.commit()

    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        seat_model = ShowtimeSeatModelMapper.from_domain(seat)

        try:
            if not seat.id:
                self.session.add(seat_model)
                await self.session.flush()
            else:
                seat_model = await self.session.merge(seat_model)

            await self.session.commit()
            await self.session.refresh(seat_model)

            return ShowtimeSeatModelMapper.to_domain(seat_model)
        except Exception:
            await self.session.rollback()
            raise

    async def get_by_id(self, seat_id: int) -> Optional[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where(ShowtimeSeatModel.id == seat_id)
        )
        model = result.scalars().first()

        return ShowtimeSeatModelMapper.to_domain(model) if model else None


class SQLAlchemyShowtimeRepository(ShowTimeRepository):
    """
    SQLAlchemy implementation of the ShowTimeRepository interface.
    Defines the contract for operations related to Showtime entities.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, entity_id: int) -> Optional[Showtime]:
        result = await self.session.execute(
            select(ShowtimeModel).where(ShowtimeModel.id == entity_id)
        )
        model = result.scalars().first()
        return ShowtimeModelMapper.to_domain(model) if model else None

    async def find_all(self, page_params: Dict[str, int]) -> List[Showtime]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 100)

        result = await self.session.execute(
            select(ShowtimeModel)
            .offset(offset)
            .limit(limit)
            .order_by(ShowtimeModel.start_time)
        )
        return [ShowtimeModelMapper.to_domain(model) for model in result.scalars()]

    async def find_deleted_by_id(self, showtime_id: int) -> Optional[Showtime]:
        result = await self.session.execute(
            select(ShowtimeModel).where(
                ShowtimeModel.id == showtime_id, ShowtimeModel.deleted_at.isnot(None)
            )
        )
        model = result.scalars().first()
        return ShowtimeModelMapper.to_domain(model) if model else None

    async def find_incoming_by_cinema(self, cinema_id: int) -> List[Showtime]:
        now_utc = datetime.now(timezone.utc)
        end_of_current_day_boundary_utc = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        query = select(ShowtimeModel).where(
            ShowtimeModel.cinema_id == cinema_id,
            ShowtimeModel.start_time >= now_utc,
            ShowtimeModel.start_time < end_of_current_day_boundary_utc,
        )

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def find_incoming_by_movie(self, movie_id: int) -> List[Showtime]:
        now_utc = datetime.now(timezone.utc)
        end_of_current_day_boundary_utc = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)

        query = select(ShowtimeModel).where(
            ShowtimeModel.movie_id == movie_id,
            ShowtimeModel.start_time >= now_utc,
            ShowtimeModel.start_time < end_of_current_day_boundary_utc,
        )

        result = await self.session.execute(query)
        models = result.scalars().all()

        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def find_by_theater_and_date_range(
        self,
        theater_id: int,
        start_time_to_check: datetime,
        end_time_to_check: datetime,
        exclude_showtime_id: Optional[int] = None,
    ) -> List[Showtime]:
        """
        Retrieves showtimes for a given theater within a specified date/time range.
        Optionally excludes a specific showtime by ID.

        """

        def _normalize_dt(dt: datetime) -> datetime:
            return (
                dt.replace(tzinfo=timezone.utc)
                if dt.tzinfo is None
                else dt.astimezone(timezone.utc)
            )

        normalized_start_time = _normalize_dt(start_time_to_check)
        normalized_end_time = _normalize_dt(end_time_to_check)

        query = select(ShowtimeModel).where(
            ShowtimeModel.theater_id == theater_id,
            ShowtimeModel.start_time < normalized_end_time,
            ShowtimeModel.end_time > normalized_start_time,
        )

        if exclude_showtime_id is not None:
            query = query.where(ShowtimeModel.id != exclude_showtime_id)

        result = await self.session.execute(query)
        models = result.scalars().all()

        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def save(self, entity: Showtime) -> Showtime:
        model = ShowtimeModelMapper.from_domain(entity)

        if entity.id is None:
            self.session.add(model)
        else:
            model = await self.session.merge(model)

        await self.session.commit()

        if entity.id is None:
            await self.session.refresh(model)

        return ShowtimeModelMapper.to_domain(model)

    async def delete(self, entity_id: int) -> None:
        await self.session.execute(
            delete(ShowtimeModel).where(ShowtimeModel.id == entity_id)
        )
        await self.session.commit()

    async def exists_by_id(self, entity_id: int) -> bool:
        result = await self.session.execute(
            select(ShowtimeModel).where(ShowtimeModel.id == entity_id)
        )
        return result.scalars().first() is not None

    async def search(
        self, params: PaginationParams, filters: SearchShowtimeFilters
    ) -> Page[Showtime]:
        # Build base query
        stmt = select(ShowtimeModel)
        count_stmt = select(func.count()).select_from(ShowtimeModel)

        # app. filters
        filter_conditions = self._build_search_filters(filters)
        if filter_conditions:
            stmt = stmt.where(and_(*filter_conditions))
            count_stmt = count_stmt.where(and_(*filter_conditions))

        # Get total count
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        # app. pagination and ordering
        stmt = stmt.order_by(ShowtimeModel.start_time)
        stmt = stmt.offset(params.offset).limit(params.limit)

        # Execute query
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        showtimes = [ShowtimeModelMapper.to_domain(model) for model in models]
        return Page.create(items=showtimes, total=total, params=params)

    def _build_search_filters(self, filters: SearchShowtimeFilters) -> List[Any]:
        """Build filter conditions from SearchShowtimeFilters."""
        conditions: List[Any] = []

        if filters.movie_id is not None:
            conditions.append(ShowtimeModel.movie_id == filters.movie_id)
        if filters.theater_id is not None:
            conditions.append(ShowtimeModel.theater_id == filters.theater_id)
        if filters.cinema_id is not None:
            conditions.append(ShowtimeModel.cinema_id == filters.cinema_id)
        if filters.type is not None:
            conditions.append(ShowtimeModel.type == filters.type)
        if filters.language is not None:
            conditions.append(ShowtimeModel.language == filters.language)
        if filters.start_time_after is not None:
            conditions.append(ShowtimeModel.start_time >= filters.start_time_after)
        if filters.start_time_before is not None:
            conditions.append(ShowtimeModel.start_time <= filters.start_time_before)
        if filters.is_upcoming is not None:
            now_utc = datetime.now(timezone.utc)
            if filters.is_upcoming:
                conditions.append(ShowtimeModel.start_time > now_utc)
            else:
                conditions.append(ShowtimeModel.start_time <= now_utc)

        return conditions
