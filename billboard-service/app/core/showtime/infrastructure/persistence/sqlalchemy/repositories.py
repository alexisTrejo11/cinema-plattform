from typing import Any, Dict, List, Optional
from datetime import datetime, timezone, timedelta
from collections import defaultdict

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.showtime.domain.entities import Showtime, ShowtimeSeat
from app.core.shared.pagination import PaginationParams
from app.core.movies.application.dtos import MovieShowtimesFilters
from app.core.showtime.domain.repositories import (
    ShowtimeSeatRepository,
    ShowTimeRepository,
)
from app.core.showtime.domain.entities import Showtime, ShowtimeSeat
from app.core.showtime.domain.repositories import (
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

    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
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

    async def get_by_id(self, entity_id: int) -> Optional[Showtime]:
        result = await self.session.execute(
            select(ShowtimeModel).where(ShowtimeModel.id == entity_id)
        )
        model = result.scalars().first()
        return ShowtimeModelMapper.to_domain(model) if model else None

    async def list_all(self, page_params: Dict[str, int]) -> List[Showtime]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 100)

        result = await self.session.execute(
            select(ShowtimeModel)
            .offset(offset)
            .limit(limit)
            .order_by(ShowtimeModel.start_time)
        )
        return [ShowtimeModelMapper.to_domain(model) for model in result.scalars()]

    async def list_incoming_by_cinema(self, cinema_id: int) -> List[Showtime]:
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

    async def list_incoming_by_movie(self, movie_id: int) -> List[Showtime]:
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

    async def list_by_theater_and_date_range(
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

    # MOVE?
    async def list_by_filters_group_by_movie(
        self, showtime_filters: MovieShowtimesFilters, page_data: PaginationParams
    ) -> Dict[int, List[Showtime]]:
        stmt = select(ShowtimeModel)

        filters: List[Any] = []

        if showtime_filters.incoming:
            filters.append(ShowtimeModel.start_time > datetime.now())
        if showtime_filters.cinema_id_list:
            filters.append(ShowtimeModel.cinema_id.in_(showtime_filters.cinema_id_list))
        if showtime_filters.movie_id:
            filters.append(ShowtimeModel.movie_id == showtime_filters.movie_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(page_data.offset).limit(page_data.limit)

        result = await self.session.execute(stmt)

        models = result.scalars().all()
        if not models:
            return {}

        showtimes_by_movie: Dict[int, List[Showtime]] = defaultdict(list)

        for model in models:
            showtimes_by_movie[model.movie_id].append(
                ShowtimeModelMapper.to_domain(model)
            )

        return dict(showtimes_by_movie)
