from app.external.billboard_data.domain.enums.theather_enum import TheaterType, SeatType
from pymongo.database import Database
from app.external.billboard_data.domain.entities.theater import TheaterSeat, Theater
from app.external.billboard_data.domain.entities.showtime import Showtime
from app.external.billboard_data.domain.entities.cinema import Cinema
from typing import Any, Dict
from datetime import datetime

class CinemaMongoMapper:
    @staticmethod
    def doc_to_domain(data: Dict[str, Any]) -> Cinema:
        theaters_doc = data.get("theaters", [])
        
        theaters = []
        for theater_doc in theaters_doc: 
            theather = TheaterMongoMapper.doc_to_domain(theater_doc)
            theaters.append(theather)
        
        return Cinema(
            cinema_id =data["cinema_id"],
            address=data["address"],
            name=data["name"],
            theaters=theaters,
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.now()),
            updated_at=data.get("updated_at", datetime.now()),
            )
        
    @staticmethod
    def domain_to_doc(cinema: Cinema) -> Dict[str, Any]:
        doc = {
            "cinema_id": cinema.cinema_id,
            "name": cinema.name,
            "theathers": [theater.to_dict() for theater in cinema.theaters],
            "is_active": cinema.is_active,
            "created_at": cinema.created_at,
            "updated_at": cinema.updated_at,
        }
        return doc


class TheaterMongoMapper:
    @staticmethod
    def doc_to_domain(data: Dict[str, Any]) -> Theater:
        seat_data = data.get("seats", [])
        theater_id = data["theater_id"]

        seats = []
        for s in seat_data:
            seats.append(
                TheaterSeat(
                    seat_id=s["seat_id"],
                    theater_id=s.get("theater_id", theater_id),
                    seat_row=s["seat_row"],
                    seat_number=s["seat_number"],
                    seat_type=SeatType(s["seat_type"]),
                    is_active=s.get("is_active", True),
                )
            )
        
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
            "id": theater.theater_id,
            "cinema_id": theater.cinema_id,
            "name": theater.name,
            "capacity": theater.capacity,
            "theater_type": theater.theater_type.value,
            "seats": [seat.to_dict() for seat in theater.seats],
            "is_active": theater.is_active,
            "maintenance_mode": theater.maintenance_mode,
            "created_at": theater.created_at,
            "updated_at": theater.updated_at,
        }
      
        return doc



class ShowtimeDocMapper:
    @staticmethod
    def doc_to_domain(data: Dict[str, Any]) -> Showtime: 
        return Showtime(
            id=data["id"],
            movie=data["movie"],
            cinema=data["cinema"],
            theater=data["theater"],
            price=data["price"],
            start_time=data["start_time"],
            type=data["type"],
            language=data["language"],
        )
        
    @staticmethod
    def domain_to_doc(showtime: Showtime) -> Dict[str, Any]:
        return showtime.to_dict()



