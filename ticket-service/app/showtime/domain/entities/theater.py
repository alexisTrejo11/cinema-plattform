from datetime import datetime
from typing import List, Optional
from ..enums.theather_enum import TheaterType
from .theather_seat import TheaterSeat

class Theater:
    def __init__(
        self, id: int, 
        cinema_id: int, 
        name: str, 
        capacity: int,
        theater_type: TheaterType,
        seats: List[TheaterSeat],
        is_active: bool = True,
        maintenance_mode: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):    
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID must be a positive integer.")
        
        if not isinstance(cinema_id, int) or cinema_id <= 0:
            raise ValueError("Cinema ID must be a positive integer.")
            
        if not isinstance(name, str) or not (1 <= len(name) <= 50):
            raise ValueError("Name must be a string between 1 and 50 characters.")
            
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
            
        if not isinstance(theater_type, TheaterType):
            raise ValueError(f"Theater type must be a valid TheaterType enum value. Got: {theater_type}")
            
        if not isinstance(is_active, bool):
            raise ValueError("Is active must be a boolean.")
            
        if not isinstance(maintenance_mode, bool):
            raise ValueError("Maintenance mode must be a boolean.")
        
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object or None.")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise ValueError("Updated at must be a datetime object or None.")

        self.__id = id
        self.__cinema_id = cinema_id
        self.__name = name
        self.__capacity = capacity
        self.__theater_type = theater_type
        self.__is_active = is_active
        self.__maintenance_mode = maintenance_mode
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__updated_at = updated_at
        self.__seats = seats
        
    def get_id(self) -> int:
        return self.__id

    def get_cinema_id(self) -> int:
        return self.__cinema_id

    def get_name(self) -> str:
        return self.__name

    def get_capacity(self) -> int:
        return self.__capacity

    def get_theater_type(self) -> TheaterType:
        return self.__theater_type

    def get_is_active(self) -> bool:
        return self.__is_active

    def get_maintenance_mode(self) -> bool:
        return self.__maintenance_mode
    
    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    def get_seats(self) -> List[TheaterSeat]:
        return self.__seats

    def __repr__(self):
        return (f"Theater(id={self.__id}, name='{self.__name}', cinema_id={self.__cinema_id}, "
                f"capacity={self.__capacity}, type={self.__theater_type.value}, "
                f"active={self.__is_active}, maintenance={self.__maintenance_mode})")