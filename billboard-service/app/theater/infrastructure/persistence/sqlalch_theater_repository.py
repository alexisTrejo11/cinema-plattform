from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.theater.domain.theater import Theater
from app.theater.application.repositories import TheaterRepository
from ..persistence.models import TheaterModel
from ..persistence.model_mappers import TheaterModelMapper

class SQLAlchemyTheaterRepository(TheaterRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: int) -> Optional[Theater]:
        result = await self.session.execute(select(TheaterModel).where(TheaterModel.id == entity_id))
        model = result.scalars().first()
        
        return TheaterModelMapper.to_domain(model) if model else None

    async def list_all(self, page_params: Dict[str, int]) -> List[Theater]:
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 100)
        
        result = await self.session.execute(
            select(TheaterModel)
            .offset(offset)
            .limit(limit)
            .order_by(TheaterModel.name)
        )
        
        return [TheaterModelMapper.to_domain(model) for model in result.scalars()]

    async def list_by_cinema(self, cinema_id: int) -> List[Theater]:
        result = await self.session.execute(select(TheaterModel).where(TheaterModel.cinema_id == cinema_id))
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
        await self.session.execute(delete(TheaterModel).where(TheaterModel.id == entity_id))
        await self.session.commit()
        



