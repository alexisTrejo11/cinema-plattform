from typing import List, Optional
from app.showtime.domain.entities.showtime import Showtime
from abc import ABC, abstractmethod

class ShowtimeRepository(ABC):
    @abstractmethod
    async def get_by_id(self, showtime_id: int, raise_exception=True) -> Showtime:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Showtime]:
        pass
    
    @abstractmethod
    async def create(self, showtime: Showtime) -> None:
        pass
    
    @abstractmethod
    async def update(self, showtime: Showtime) -> None:
        pass
    
    
    @abstractmethod
    async def delete(self, showtime_id: int) -> None:
        pass