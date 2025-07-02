from app.showtime.domain.enums.theather_enum import TheaterType, SeatType
from pymongo.database import Database
from app.showtime.domain.entities.theater import TheaterSeat, Theater
from app.showtime.domain.entities.showtime import Showtime
from typing import Any, Dict

class TheaterMongoMapper:
    @staticmethod
    def doc_to_domain(data: Dict[str, Any]) -> Theater:
        seat_data = data.get("seats", [])
        
        seats = []
        for seat in seats:
            seat = TheaterSeat(
                seat_id=seat_data['seat_id'],
                theater_id=seat_data['seat_id'],
                seat_row=seat_data['seat_row'],
                seat_number=seat_data['seat_number'],
                seat_type=SeatType(seat_data['seat_type']),
                is_active=data.get("is_active", True)
            )
            seats.append(seat)
        
        return Theater(
            theater_id=data["theater_id"],
            cinema_id=data["cinema_id"],
            name=data["name"],
            capacity=data["capacity"],
            theater_type=TheaterType(data["theater_type"]),
            seats=seats,
            is_active=data.get("is_active", True),
            maintenance_mode=data.get("maintenance_mode", False),  
            )
        
    @staticmethod
    def domain_to_doc(theater: Theater) -> Dict[str, Any]:
        doc = {
            "id": theater.get_theater_id(),
            "cinema_id": theater.get_cinema_id(),
            "name": theater.get_name(),
            "capacity": theater.get_capacity(),
            "theater_type": theater.get_theater_type().value,
            "seats": [seat.to_dict() for seat in theater.get_seats()],
            "is_active": theater.get_is_active(),
            "maintenance_mode": theater.get_maintenance_mode(),
            "created_at": theater.get_created_at(),
            "updated_at": theater.get_updated_at(),
        }
      
        return doc



class ShowtimeDocMapper:
    @staticmethod
    def doc_to_domain(data: Dict[str, Any]) -> Showtime: 
        return Showtime(
            id=data["id"],
            movie_id=data["movie_id"],
            cinema_id=data["cinema_id"],
            theater_id=data["theater_id"],
            price=data["price"],
            start_time=data["start_time"],
            type=data["type"],
            language=data["language"],
        )
        
    @staticmethod
    def domain_to_doc(showtime: Showtime) -> Dict[str, Any]:
        return showtime.to_dict()



