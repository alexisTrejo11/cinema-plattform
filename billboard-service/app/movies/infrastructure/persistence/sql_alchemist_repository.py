from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.movies.application.repositories import MovieRepository
from app.movies.domain.entities import Movie
from .models import MovieModel
from .mappers import MovieMapper

class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_active(self) -> List[Movie]:        
        stmt = select(MovieModel).where(MovieModel.is_active == True)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [MovieMapper.to_entity(model) for model in models]

    async def get_by_id(self, entity_id: int) -> Optional[Movie]:
        model = await self.session.get(MovieModel, entity_id)

        return MovieMapper.to_entity(model) if model else None

    async def list_all(self, page_params: Dict[str, int]) -> List[Movie]:
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 10)
        
        stmt = select(MovieModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [MovieMapper.to_entity(model) for model in models]

    async def save(self, entity: Movie) -> Movie:
        model = MovieMapper.to_model(entity)
        
        if entity.id is None:
            self.session.add(model)
        else:
            model = await self.session.merge(model)
            
        await self.session.commit()
        await self.session.refresh(model)
        
        return MovieMapper.to_entity(model)

    
    async def delete(self, entity_id: int) -> None:
        stmt = delete(MovieModel).where(MovieModel.id == entity_id)
        await self.session.execute(stmt)
        await self.session.commit()


