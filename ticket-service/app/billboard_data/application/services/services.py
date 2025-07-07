from typing import Optional, List
from app.billboard_data.domain.entities.cinema import Cinema, Theater
from app.billboard_data.domain.entities.theather_seat import TheaterSeat
from ..repositories.cinema_repository import CinemaRepository

class CinemaService:
    def __init__(self, repository: CinemaRepository) -> None:
        self.repository = repository
    
    async def get_by_id(self, cinema_id: int, raise_exception=True) -> Optional[Cinema]:
        cinema = await self.get_by_id(cinema_id)
        if cinema:
            return cinema   
    
        if raise_exception:
            raise ValueError("Cinema not Found")
    
        return None
    
    
    async def list(self) -> List[Cinema]:
        return await self.repository.get_all()
    
    
    async def save(self, cinema: Cinema) -> None:
        await self.repository.save(cinema)
    
    
    async def delete(self, cinema_id: int) -> None:
        await self.repository.delete(cinema_id) 
        
    
class TheaterService:
    def __init__(self, cinema_repository: CinemaRepository) -> None:
        self.cinema_repository = cinema_repository
    
    async def get_by_id(self, cinema_id: int, theather_id: int) -> Optional[Theater]:
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:            
            return None   

        return cinema.get_theater_by_id(theather_id)

    async def create_theater(self, cinema_id: int, theater: Theater) -> None:
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:            
            raise ValueError("Cinema not Found")
        
        cinema.add_theater(theater)        
        await self.cinema_repository.save(cinema)
        
        
    async def update_theater(self, cinema_id: int, theater: Theater) -> None:
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:            
            raise ValueError("Cinema not Found")
        
        cinema.add_theater(theater)        
        await self.cinema_repository.save(cinema)


    async def delete_theater(self, cinema_id: int, theather_id: int) -> bool:
        cinema = await self.cinema_repository.get_by_id(cinema_id)
        if not cinema:            
            raise ValueError("cinema not found")   

        is_deleted = cinema.remove_theater(theather_id)
        if not is_deleted:
            return False
        
        await self.cinema_repository.save(cinema)
        
        return True  


class TheaterSeatService:
    def __init__(self, theater_service: TheaterService) -> None:
        self.theater_service = theater_service
    
    async def get_seats_by_ids(self, cinema_id: int, theater_id: int, seat_id: int) -> Optional[TheaterSeat]:
        theater = await self.theater_service.get_by_id(cinema_id, theater_id)
        if not theater:            
            return None   

        return theater.get_seat_by_id(seat_id)

    
    async def save_seat_list(self, cinema_id: int, theater_id: int, seats: List[TheaterSeat]) -> None:
        theater = await self.theater_service.get_by_id(cinema_id, theater_id)
        if not theater:            
            raise ValueError("theater not found")
        
        theater.save_seats(seats)        
        await self.theater_service.update_theater(cinema_id, theater)
        
        
