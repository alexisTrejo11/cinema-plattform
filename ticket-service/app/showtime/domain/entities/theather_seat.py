from datetime import datetime
from typing import Any, Dict, Optional
from ..enums.theather_enum import SeatType


class TheaterSeat:
    def __init__(
        self, 
        seat_id : int, 
        theater_id: int, 
        seat_row: str, 
        seat_number: int,
        seat_type: SeatType = SeatType.STANDARD, 
        is_active: bool = True,
        created_at: Optional[datetime] = None, 
        updated_at: Optional[datetime] = None
    ):    
        if not isinstance(theater_id, int) or theater_id <= 0:
            raise ValueError("Theater ID must be a positive integer.")
        
        if not isinstance(seat_id, int) or theater_id <= 0:
            raise ValueError("Seat ID must be a positive integer.")
        
        
        if not isinstance(seat_row, str) or not (1 <= len(seat_row) <= 5):
            raise ValueError("Seat row must be a string between 1 and 5 characters.")
        
        if not isinstance(seat_number, int) or seat_number <= 0:
            raise ValueError("Seat number must be a positive integer.")
        
        if not isinstance(seat_type, SeatType):
            raise ValueError(f"Seat type must be a valid SeatType enum value. Got: {seat_type}")
            
        if not isinstance(is_active, bool):
            raise ValueError("Is active must be a boolean.")
            
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object or None.")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise ValueError("Updated at must be a datetime object or None.")

        self.__seat_id = seat_id
        self.__theater_id = theater_id
        self.__seat_row = seat_row
        self.__seat_number = seat_number
        self.__seat_type = seat_type
        self.__is_active = is_active
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__updated_at = updated_at

    def get_theater_id(self) -> int:
        return self.__theater_id

    def get_seat_row(self) -> str:
        return self.__seat_row

    def get_seat_number(self) -> int:
        return self.__seat_number

    def get_seat_type(self) -> SeatType:
        return self.__seat_type

    def get_is_active(self) -> bool:
        return self.__is_active

    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    def __repr__(self):
        return (f"TheaterSeat(theater_id={self.__theater_id}, row='{self.__seat_row}', "
                f"number={self.__seat_number}, type={self.__seat_type.value}, "
                f"active={self.__is_active})")


    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "seat_id": self.__seat_id,
            "theater_id": self.__theater_id,
            "seat_row": self.__seat_row,
            "seat_number": self.__seat_number,
            "seat_type": self.__seat_type.value,
            "is_active": self.__is_active,
            "created_at": self.__created_at,
            "updated_at": self.__updated_at,
        }
