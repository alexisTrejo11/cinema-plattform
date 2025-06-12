from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.showtime.application.repositories import ShowtimeSeatRepository
from app.showtime.domain.entities.showtime_seat import ShowtimeSeat
from .model_mappers import ShowtimeSeatModelMapper
from .models import ShowtimeSeatModel

class SqlAlchShowtimeSeatRepository(ShowtimeSeatRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_showtime_and_seat(self, showtime_id: int, seat_id: int) -> Optional[ShowtimeSeat]:
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
            select(ShowtimeSeatModel).where(ShowtimeSeatModel.showtime_id == showtime_id)
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
