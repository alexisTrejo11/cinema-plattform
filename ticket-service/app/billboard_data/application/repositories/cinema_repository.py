from typing import List, Optional
from app.billboard_data.domain.entities.cinema import Cinema
from abc import ABC, abstractmethod

class CinemaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, cinema_id: int) -> Optional[Cinema]:
        pass
    
    @abstractmethod
    async def save(self, cinema: Cinema) -> None:
        pass
    
    @abstractmethod
    async def delete(self, cinema_id: int) -> None:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Cinema]:
        pass