from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.ticket.domain.entities import ShowtimeSeat
from app.ticket.domain.exceptions import SeatNotFoundError
from app.ticket.domain.interfaces import SeatRepository
from app.ticket.infrastructure.persistence.mappers import ShowtimeSeatModelMapper
from app.ticket.infrastructure.persistence.models import ShowtimeSeatModel


class SqlAlchemySeatRepository(SeatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id.in_(id_list))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ShowtimeSeatModelMapper.to_domain(model) for model in models]

    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ShowtimeSeatModelMapper.to_domain(model) for model in models]

    async def list_by_showtime_and_id_in(
        self, showtime_id: int, showtime_seat_ids: List[int]
    ) -> List[ShowtimeSeat]:
        """Seat IDs are primary keys of `showtime_seats` (same IDs passed to take_seats)."""
        if not showtime_seat_ids:
            return []
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id,
            ShowtimeSeatModel.id.in_(showtime_seat_ids),
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ShowtimeSeatModelMapper.to_domain(model) for model in models]

    async def get_by_id_and_showtime(
        self, showtime_id: int, id: int
    ) -> Optional[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.showtime_id == showtime_id,
            ShowtimeSeatModel.id == id,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return ShowtimeSeatModelMapper.to_domain(model) if model else None

    async def get_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        return await self.list_by_id_in(id_list)

    async def get_by_showtime_and_id_in(
        self, showtime_id: int, seat_id_in: List[int]
    ) -> List[ShowtimeSeat]:
        return await self.list_by_showtime_and_id_in(showtime_id, seat_id_in)

    async def get_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        return await self.list_by_showtime(showtime_id)

    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        if seat.get_id() is None:
            seat_model = ShowtimeSeatModelMapper.from_domain(seat)
            self.session.add(seat_model)
            await self.session.flush()
            await self.session.refresh(seat_model)
        else:
            stmt = select(ShowtimeSeatModel).where(
                ShowtimeSeatModel.id == seat.get_id()
            )
            result = await self.session.execute(stmt)
            seat_model = result.scalar_one_or_none()

            if not seat_model:
                raise SeatNotFoundError("Seat", seat.get_id())

            seat_model.showtime_id = seat.get_showtime_id()
            seat_model.seat_id = seat.get_seat_id()
            seat_model.seat_name = seat.get_seat_name()
            seat_model.is_available = seat.get_is_available()
            taken_at = seat.get_taken_at()

            if taken_at is not None:
                seat_model.taken_at = taken_at
            ticket_id = seat.get_ticket_id()

            if ticket_id is not None:
                seat_model.ticket_id = ticket_id

            await self.session.flush()
            await self.session.refresh(seat_model)

        return ShowtimeSeatModelMapper.to_domain(seat_model)

    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        models_to_insert = [ShowtimeSeatModelMapper.from_domain(s) for s in seats]
        self.session.add_all(models_to_insert)
        await self.session.flush()

    async def bulk_update(self, seats: List[ShowtimeSeat]) -> None:
        for seat in seats:
            sid = seat.get_id()
            if sid is None:
                continue
            await self.session.execute(
                update(ShowtimeSeatModel)
                .where(ShowtimeSeatModel.id == sid)
                .values(
                    showtime_id=seat.get_showtime_id(),
                    seat_id=seat.get_seat_id(),
                    seat_name=seat.get_seat_name(),
                    is_available=seat.get_is_available(),
                    taken_at=seat.get_taken_at(),
                    ticket_id=seat.get_ticket_id(),
                )
            )
