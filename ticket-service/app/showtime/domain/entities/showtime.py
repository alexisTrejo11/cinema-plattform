from datetime import datetime
from decimal import Decimal
from typing import Optional
from ..enums.showtime_enum import ShowtimeLanguage, ShowtimeType

class Showtime:
    def __init__(
        self, 
        id: int, 
        movie_id: int, 
        cinema_id: int, 
        theater_id: int,
        price: Decimal, 
        start_time: datetime, 
        type: ShowtimeType,
        language: ShowtimeLanguage, 
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID must be a positive integer.")
        
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("Movie ID must be a positive integer.")
        
        if not isinstance(cinema_id, int) or cinema_id <= 0:
            raise ValueError("Cinema ID must be a positive integer.")
        
        if not isinstance(theater_id, int) or theater_id <= 0:
            raise ValueError("Theater ID must be a positive integer.")
        
        if not isinstance(price, Decimal) or price <= 0:
            raise ValueError("Price must be a positive Decimal.")
        
        exponent = price.as_tuple().exponent
        if isinstance(exponent, int) and exponent < -2:  # Check if more than 2 decimal places
            raise ValueError("Price can have at most 2 decimal places.")

        if not isinstance(start_time, datetime):
            raise ValueError("Start time must be a datetime object.")
        
        if not isinstance(type, ShowtimeType):
            raise ValueError(f"Type must be a valid ShowtimeType enum value. Got: {type}")
        
        if not isinstance(language, ShowtimeLanguage):
            raise ValueError(f"Language must be a valid ShowtimeLanguage enum value. Got: {language}")
        
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object or None.")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise ValueError("Updated at must be a datetime object or None.")

        self.__id = id
        self.__movie_id = movie_id
        self.__cinema_id = cinema_id
        self.__theater_id = theater_id
        self.__price = price
        self.__start_time = start_time
        self.__type = type
        self.__language = language
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__updated_at = updated_at

    def get_id(self) -> int:
        return self.__id

    def get_movie_id(self) -> int:
        return self.__movie_id

    def get_cinema_id(self) -> int:
        return self.__cinema_id

    def get_theater_id(self) -> int:
        return self.__theater_id

    def get_price(self) -> Decimal:
        return self.__price

    def get_start_time(self) -> datetime:
        return self.__start_time

    def get_type(self) -> ShowtimeType:
        return self.__type

    def get_language(self) -> ShowtimeLanguage:
        return self.__language

    def get_created_at(self) -> datetime:
        return self.__created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    def __repr__(self):
        return (f"Showtime(id={self.__id}, movie_id={self.__movie_id}, "
                f"cinema_id={self.__cinema_id}, start_time={self.__start_time.strftime('%Y-%m-%d %H:%M')}, "
                f"type={self.__type.value}, language={self.__language.value})")