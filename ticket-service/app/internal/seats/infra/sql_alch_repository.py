from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.seats.application.exceptions import SeatNotFoundError
from app.internal.seats.domain.seat_repository import SeatRepository
from app.internal.seats.domain.showtime_seat import ShowtimeSeat

from .mapper import ModelMapper
from .model import ShowtimeSeatModel


class SqlAlchemySeatRepository(SeatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id_and_showtime(
        self, showtime_id: int, id: int
    ) -> Optional[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id,
            ShowtimeSeatModel.id == id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return ModelMapper.to_domain(model) if model else None

    async def list_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id.in_(id_list))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ModelMapper.to_domain(model) for model in models]

    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ModelMapper.to_domain(model) for model in models]

    async def list_by_showtime_and_id_in(
        self, showtime_id: int, seat_id_in: List[int]
    ) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id,
            ShowtimeSeatModel.id.in_(seat_id_in),
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ModelMapper.to_domain(model) for model in models]

    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        if seat.id is None:
            seat_model = ModelMapper.from_domain(seat)
            self.session.add(seat_model)
            await self.session.flush()
            await self.session.refresh(seat_model)
        else:
            stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id == seat.id)
            result = await self.session.execute(stmt)
            seat_model = result.scalar_one_or_none()

            if not seat_model:
                raise SeatNotFoundError("Seat", seat.id)

            seat_model.showtime_id = seat.showtime_id
            seat_model.seat_id = seat.seat_id
            seat_model.seat_name = seat.seat_name
            seat_model.is_available = seat.is_available
            if seat.taken_at is not None:
                seat_model.taken_at = seat.taken_at
            if seat.ticket_id is not None:
                seat_model.ticket_id = seat.ticket_id

            await self.session.flush()
            await self.session.refresh(seat_model)

        return ModelMapper.to_domain(seat_model)

    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        models_to_insert = [ModelMapper.from_domain(s) for s in seats]
        self.session.add_all(models_to_insert)
        await self.session.flush()

    async def bulk_update(self, seats: List[ShowtimeSeat]) -> None:
        for seat in seats:
            if seat.id is None:
                continue
            stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id == seat.id)
            result = await self.session.execute(stmt)
            row = result.scalar_one_or_none()
            if not row:
                continue
            row.showtime_id = seat.showtime_id
            row.seat_id = seat.seat_id
            row.seat_name = seat.seat_name
            row.is_available = seat.is_available
            row.taken_at = seat.taken_at
            row.ticket_id = seat.ticket_id
        await self.session.flush()
