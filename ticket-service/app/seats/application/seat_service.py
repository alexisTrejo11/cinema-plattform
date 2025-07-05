from app.seats.domain.seat_repository import SeatRepository
from app.seats.domain.showtime_seat import ShowtimeSeat
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.application.repositories.theater_repository import TheaterRepository
from typing import List
from .exceptions import TheaterNotFound, SeatInvalidIdListError

class ShowtimeSeatService:
    def __init__(self, repository: SeatRepository, theater_repository: TheaterRepository) -> None:
        self.repository = repository
        self.theater_repository = theater_repository
    
    async def create_seats_from_showtime(self, showtime: Showtime):
        theater = await self.theater_repository.get_by_id(showtime.get_theater_id()) 
        if not theater:
            raise TheaterNotFound("Theater", showtime.get_theater_id())

        showtime_seats = []
        
        for theater_seat in theater.get_seats():
            seat_name = f"{theater_seat.get_seat_row()}-{theater_seat.get_seat_number()}"   
            showtime_seat = ShowtimeSeat(showtime.get_id(), theater_seat.get_seat_id(), seat_name, theater_seat.get_is_active())
            showtime_seats.append(showtime_seat)

        await self.repository.bulk_create(showtime_seats)

        print(f"Successfully create {len(showtime_seats)} seats for showtime")
    
    
    async def list_by_showtime_id_and_seat_id_list(self, showtime_id: int, seat_id_list: List[int]) -> List[ShowtimeSeat]:
        return await self.repository.list_by_showtime_and_id_in(showtime_id, seat_id_list)
        
    async def get_seats_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        return await self.repository.list_by_showtime(showtime_id)
    
    async def take_seats(self, seats_id_list: List[int]) -> None:
        seats = await self.repository.list_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Seat Ids", "Not all ids are valid")
        
        for seat in seats:
            seat.ocuppy()
        
        return await self.repository.bulk_update(seats)
        
        
    async def release_seats(self,  seats_id_list: List[int]):
        seats = await self.repository.list_by_id_in(seats_id_list)
        if len(seats) != len(seats_id_list):
            raise SeatInvalidIdListError("Invalid Seat", "Not all ids are valid")
        
        for seat in seats:
            seat.release()
        
        await self.repository.bulk_update(seats)
        