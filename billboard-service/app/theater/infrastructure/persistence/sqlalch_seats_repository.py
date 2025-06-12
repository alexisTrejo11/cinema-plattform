from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.theater.domain.seat import TheaterSeat as Seat
from app.theater.application.repositories import TheaterSeatRepository
from .models import TheaterSeatModel
from .model_mappers import TheaterSeatModelMapper

class SqlAlchemistTheaterSeatRepository(TheaterSeatRepository):
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

    async def exist_by_theater_and_seat_values(self, theater_id: int, seat_row: str, seat_number: int) -> bool:
        query = select(TheaterSeatModel.id).where(
            TheaterSeatModel.theater_id == theater_id,
            TheaterSeatModel.seat_row == seat_row,
            TheaterSeatModel.seat_number == seat_number,
        ).limit(1)

        result = await self.session.execute(query)
        
        return bool(result.scalar())
