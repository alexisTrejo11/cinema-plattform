from typing import Dict, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func

from app.theater.domain.theater import Theater
from app.theater.domain.seat import TheaterSeat as Seat
from app.shared.core.pagination import PaginationParams, Page
from app.theater.application.dtos import SearchTheaterFilters
from app.theater.domain.repositories import (
    TheaterRepository,
    TheaterSeatRepository,
)
from .models import TheaterModel, TheaterSeatModel
from .mappers import TheaterModelMapper, TheaterSeatModelMapper


class SQLAlchemyTheaterRepository(TheaterRepository):
    """
    SQLAlchemy implementation of the TheaterRepository interface.
    Defines the contract for operations related to Theater entities.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: int) -> Optional[Theater]:
        result = await self.session.execute(
            select(TheaterModel).where(TheaterModel.id == entity_id)
        )
        model = result.scalars().first()

        return TheaterModelMapper.to_domain(model) if model else None

    async def find_by_id(self, entity_id: int) -> Optional[Theater]:
        return await self.get_by_id(entity_id)

    async def list_all(self, page_params: Dict[str, int]) -> List[Theater]:
        offset = page_params.get("offset", 0)
        limit = page_params.get("limit", 100)

        result = await self.session.execute(
            select(TheaterModel).offset(offset).limit(limit).order_by(TheaterModel.name)
        )

        return [TheaterModelMapper.to_domain(model) for model in result.scalars()]

    async def find_all(self, page_params: Dict[str, int]) -> List[Theater]:
        return await self.list_all(page_params)

    async def list_by_cinema(self, cinema_id: int) -> List[Theater]:
        result = await self.session.execute(
            select(TheaterModel).where(TheaterModel.cinema_id == cinema_id)
        )
        models = result.scalars().all()

        return [TheaterModelMapper.to_domain(model) for model in models]

    async def save(self, entity: Theater) -> Theater:
        model = TheaterModelMapper.from_domain(entity)

        try:
            if entity.id is None:
                self.session.add(model)
                await self.session.flush()
            else:
                model = await self.session.merge(model)

            await self.session.commit()

            if model in self.session:
                await self.session.refresh(model)

            return TheaterModelMapper.to_domain(model)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Failed to save theater: {str(e)}") from e

    async def delete(self, entity_id: int) -> None:
        await self.session.execute(
            delete(TheaterModel).where(TheaterModel.id == entity_id)
        )
        await self.session.commit()

    async def exists_by_id(self, entity_id: int) -> bool:
        result = await self.session.execute(
            select(TheaterModel.id).where(TheaterModel.id == entity_id).limit(1)
        )
        return bool(result.scalar())

    async def search(
        self, params: PaginationParams, filters: SearchTheaterFilters
    ) -> Page[Theater]:
        stmt = select(TheaterModel)
        count_stmt = select(func.count()).select_from(TheaterModel)

        conditions: List[Any] = []
        if filters.cinema_id is not None:
            conditions.app.d(TheaterModel.cinema_id == filters.cinema_id)
        if filters.name:
            conditions.app.d(TheaterModel.name.ilike(f"%{filters.name}%"))
        if filters.theater_type is not None:
            conditions.app.d(TheaterModel.theater_type == filters.theater_type)
        if filters.is_active is not None:
            conditions.app.d(TheaterModel.is_active == filters.is_active)
        if filters.maintenance_mode is not None:
            conditions.app.d(TheaterModel.maintenance_mode == filters.maintenance_mode)

        if conditions:
            stmt = stmt.where(and_(*conditions))
            count_stmt = count_stmt.where(and_(*conditions))

        total = (await self.session.execute(count_stmt)).scalar() or 0
        stmt = (
            stmt.order_by(TheaterModel.name).offset(params.offset).limit(params.limit)
        )

        rows = (await self.session.execute(stmt)).scalars().all()
        theaters = [TheaterModelMapper.to_domain(model) for model in rows]
        return Page.create(items=theaters, total=total, params=params)


class SQLAlchemyTheaterSeatRepository(TheaterSeatRepository):
    """
    SQLAlchemy implementation of the TheaterSeatRepository interface.
    Defines the contract for operations related to TheaterSeat entities.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, seat_id: int) -> Optional[Seat]:
        result = await self.session.execute(
            select(TheaterSeatModel).where(TheaterSeatModel.id == seat_id)
        )
        model = result.scalars().first()

        return TheaterSeatModelMapper.to_domain(model) if model else None

    async def get_by_theater(self, theater_id: int) -> List[Seat]:
        result = await self.session.execute(
            select(TheaterSeatModel)
            .where(TheaterSeatModel.theater_id == theater_id)
            .order_by(TheaterSeatModel.seat_row, TheaterSeatModel.seat_number)
        )
        models = result.scalars().all()

        return [TheaterSeatModelMapper.to_domain(model) for model in models]

    async def exists_by_theater(self, theater_id: int) -> bool:
        result = await self.session.execute(
            select(TheaterSeatModel.id)
            .where(TheaterSeatModel.theater_id == theater_id)
            .limit(1)
        )

        return bool(result.scalar())

    async def save(self, seat: Seat) -> Seat:
        model = TheaterSeatModelMapper.from_domain(seat)
        try:
            if seat.id is None:
                self.session.add(model)
                await self.session.flush()
            else:
                model = await self.session.merge(model)

            await self.session.commit()

            if model in self.session:
                await self.session.refresh(model)

            return TheaterSeatModelMapper.to_domain(model)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Failed to save seat: {str(e)}") from e

    async def delete(self, seat_id: int) -> None:
        await self.session.execute(
            delete(TheaterSeatModel).where(TheaterSeatModel.id == seat_id)
        )
        await self.session.commit()

    async def exist_by_theater_and_seat_values(
        self, theater_id: int, seat_row: str, seat_number: int
    ) -> bool:
        query = (
            select(TheaterSeatModel.id)
            .where(
                TheaterSeatModel.theater_id == theater_id,
                TheaterSeatModel.seat_row == seat_row,
                TheaterSeatModel.seat_number == seat_number,
            )
            .limit(1)
        )

        result = await self.session.execute(query)

        return bool(result.scalar())
