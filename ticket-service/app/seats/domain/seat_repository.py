from abc import ABC, abstractmethod
from typing import List, Optional
from .showtime_seat import ShowtimeSeat

class SeatRepository:
    @abstractmethod
    async def get_by_id_and_showtime(self, showtime_id: int, id: int) -> Optional[ShowtimeSeat]:
        pass
    

    @abstractmethod
    async def list_by_id_in(self, id_list: List[int]) -> List[ShowtimeSeat]:
        pass
    
    @abstractmethod
    async def list_by_showtime_and_id_in(self, showtime_id: int, seat_id_in: List[int]) -> List[ShowtimeSeat]:
        pass
    
    @abstractmethod
    async def list_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        pass
    
    @abstractmethod
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        pass
    
    @abstractmethod
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        pass
    
    @abstractmethod
    async def bulk_update(self, seats: List[ShowtimeSeat]) -> None:
        pass