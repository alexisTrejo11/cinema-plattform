from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.seats.domain.showtime_seat import ShowtimeSeat
from app.seats.domain.seat_repository import SeatRepository
from .mapper import ModelMapper
from .model import ShowtimeSeatModel

class SqlAlchemySeatRepository(SeatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def list_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id.in_(id_list))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ModelMapper.to_domain(model) for model in models]
    
    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:

        stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.showtime_id == showtime_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [ModelMapper.to_domain(model) for model in models]
    
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        if seat.get_id() is None:
            # New seat - create new model
            seat_model = ModelMapper.from_domain(seat)
            self.session.add(seat_model)
            await self.session.flush()
            await self.session.refresh(seat_model)
        else:
            # Existing seat - find and update
            stmt = select(ShowtimeSeatModel).where(ShowtimeSeatModel.id == seat.get_id())
            result = await self.session.execute(stmt)
            seat_model = result.scalar_one_or_none()
            
            if not seat_model:
                raise ValueError(f"Seat with ID {seat.get_id()} not found")
            
            # Update existing model with new values
            seat_model.showtime_id = seat.get_showtime_id()
            seat_model.seat_id = seat.get_seat_id()
            seat_model.seat_name = seat.get_seat_name()
            seat_model.is_available = seat.get_is_available()
            seat_model.taken_at = seat.get_taken_at()
            seat_model.ticket_id = seat.get_ticket_id()
            
            await self.session.flush()
            await self.session.refresh(seat_model)

        return ModelMapper.to_domain(seat_model)

    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        models_to_insert = [ModelMapper.from_domain(s) for s in seats]
        self.session.add_all(models_to_insert)
        await self.session.flush()

    async def bulk_update(self, seats: List[ShowtimeSeat]) -> None:
        updates = []
        for seat in seats:
            if not seat.get_seat_id():
                continue

            update_data = seat.to_dict()
            update_data.pop("seat_id", None)
            update_data.pop("created_at", None)
            update_data["updated_at"] = datetime.now()

            updates.append({
                "seat_id": seat.get_seat_id(),
                **update_data
            })
        
        if updates:

            await self.session.execute(
                update(ShowtimeSeatModel),
                updates
            )
        