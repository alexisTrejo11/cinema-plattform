from datetime import timezone, datetime
from typing import List
from app.theater.application.repositories import TheaterSeatRepository
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.theater.domain.seat import TheaterSeat
from ..repositories import ShowtimeSeatRepository

class ShowTimeSeatService:
    def __init__(self, theater_seat_repo: TheaterSeatRepository, showtime_seat_repo: ShowtimeSeatRepository):
        self.theater_seat_repo = theater_seat_repo
        self.showtime_seat_repo = showtime_seat_repo

    async def create_showtimes_seats(self, showtime: Showtime):
        theater_seats = await self.theater_seat_repo.get_by_theater(showtime.theater_id)
        showtimes_seats = self._generate_showtimes_seats(theater_seats, showtime)
        await self.showtime_seat_repo.bulk_create(showtimes_seats)

    def _generate_showtimes_seats(self, theater_seats: List[TheaterSeat], showtime: Showtime) -> List[ShowtimeSeat]:
        showtimes_seats: List[ShowtimeSeat] = []
        
        for theater_seat in theater_seats:
            if showtime.id is None or theater_seat.id is None:
                raise ValueError("Showtime id and theater_seat cannot be None when creating showtime seats.")
            
            showtime_seat = ShowtimeSeat(
                showtime_id=showtime.id,
                theater_seat_id=theater_seat.id,
                id=None,
                taken_at=None,
                user_id=None,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            showtimes_seats.append(showtime_seat)    
                
        return showtimes_seats