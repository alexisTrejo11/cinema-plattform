from typing import List, Optional
from app.showtime.domain.entities.theater import Theater
from abc import ABC, abstractmethod

class TheaterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, theater_id: int) -> Optional[Theater]:
        pass
    
    
    @abstractmethod
    async def create(self, theater: Theater) -> None:
        pass
    
    
    @abstractmethod
    async def update(self, theater: Theater) -> None:
        pass
    
    
    @abstractmethod
    async def delete(self, theater_id: int) -> None:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Theater]:
        pass