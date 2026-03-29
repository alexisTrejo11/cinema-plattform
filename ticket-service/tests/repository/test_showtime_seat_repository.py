from typing import List

from sqlalchemy import select

from app.internal.seats.domain.showtime_seat import ShowtimeSeat
from app.internal.seats.infra.model import ShowtimeSeatModel

from .conftest import *


class TestSqlAlchemySeatRepository:
    async def test_list_by_id_in(self, seat_repository, multiple_seat_models):
        id_list = [seat.id for seat in multiple_seat_models[:3]]
        seats = await seat_repository.list_by_id_in(id_list)

        assert len(seats) == 3
        assert all(seat.id in id_list for seat in seats)
        assert all(isinstance(seat, ShowtimeSeat) for seat in seats)

    async def test_list_by_id_in_empty(self, seat_repository):
        seats = await seat_repository.list_by_id_in([])
        assert len(seats) == 0

    async def test_list_by_showtime(self, seat_repository, multiple_seat_models):
        showtime_id: int = multiple_seat_models[0].showtime_id
        seats: List[ShowtimeSeat] = await seat_repository.list_by_showtime(
            showtime_id
        )

        assert len(seats) == len(multiple_seat_models)
        assert all(seat.showtime_id == showtime_id for seat in seats)
        assert all(isinstance(seat, ShowtimeSeat) for seat in seats)

    async def test_save_new_seat(self, seat_repository, sample_seat_entity, async_session):
        saved_seat: ShowtimeSeat = await seat_repository.save(sample_seat_entity)

        assert saved_seat.id is not None
        assert sample_seat_entity.id is None

        assert saved_seat.showtime_id == sample_seat_entity.showtime_id
        assert saved_seat.seat_id == sample_seat_entity.seat_id
        assert saved_seat.seat_name == sample_seat_entity.seat_name
        assert saved_seat.is_available == sample_seat_entity.is_available
        assert saved_seat.ticket_id == sample_seat_entity.ticket_id

        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.seat_id == saved_seat.seat_id
        )
        result = await async_session.execute(stmt)
        db_seat = result.scalar_one()
        assert db_seat is not None

    async def test_save_existing_seat(self, seat_repository, sample_seat_model, async_session):
        existing_seat = ShowtimeSeat(
            id=sample_seat_model.id,
            showtime_id=sample_seat_model.showtime_id,
            seat_id=sample_seat_model.seat_id,
            seat_name=sample_seat_model.seat_name,
            is_available=False,
            ticket_id=1,
            created_at=sample_seat_model.created_at,
        )

        updated_seat: ShowtimeSeat = await seat_repository.save(existing_seat)

        assert updated_seat.seat_id == sample_seat_model.seat_id
        assert updated_seat.is_available is False
        assert updated_seat.ticket_id == 1

        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.seat_id == sample_seat_model.seat_id
        )
        result = await async_session.execute(stmt)
        db_seat = result.scalar_one()
        assert db_seat.is_available is False
        assert db_seat.ticket_id == 1

    async def test_bulk_create(self, seat_repository, async_session):
        seats = [
            ShowtimeSeat(
                showtime_id=3,
                seat_id=300 + i,
                seat_name=f"C{i+1}",
                is_available=True,
            )
            for i in range(3)
        ]

        await seat_repository.bulk_create(seats)

        stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.showtime_id == 3)
        result = await async_session.execute(stmt)
        db_seats = result.scalars().all()

        assert len(db_seats) == 3
        assert all(seat.showtime_id == 3 for seat in db_seats)

    async def test_bulk_update(self, seat_repository, multiple_seat_models, async_session):
        seats_to_update = [
            ShowtimeSeat(
                id=seat.id,
                showtime_id=seat.showtime_id,
                seat_id=seat.seat_id,
                seat_name=seat.seat_name,
                is_available=False,
                ticket_id=1,
                created_at=seat.created_at,
            )
            for seat in multiple_seat_models[:3]
        ]

        await seat_repository.bulk_update(seats_to_update)

        stmt = select(ShowtimeSeatModel).where(
            ShowtimeSeatModel.id.in_([s.id for s in seats_to_update])
        )
        result = await async_session.execute(stmt)
        updated_seats = result.scalars().all()

        assert len(updated_seats) == 3
        assert all(seat.is_available is False for seat in updated_seats)
        assert all(seat.ticket_id == 1 for seat in updated_seats)

    async def test_bulk_update_empty(self, seat_repository):
        await seat_repository.bulk_update([])
