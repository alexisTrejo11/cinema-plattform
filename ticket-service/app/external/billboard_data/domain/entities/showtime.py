from datetime import datetime
from decimal import Decimal
from typing import Optional
from ..enums.showtime_enum import ShowtimeLanguage, ShowtimeType
from app.external.billboard_data.domain.entities.movie import Movie
from app.external.billboard_data.domain.entities.theater import Theater
from app.external.billboard_data.domain.entities.cinema import Cinema

class Showtime:
    def __init__(
        self, 
        id: int, 
        movie: Movie, 
        cinema: Cinema, 
        theater: Theater,
        price: Decimal, 
        start_time: datetime, 
        type: ShowtimeType,
        language: ShowtimeLanguage, 
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID must be a positive integer.")
        
        if not isinstance(movie, Movie):
            raise ValueError("Movie must be an instance of movie domain")
        
        if not isinstance(cinema, Cinema):
            raise ValueError("Cinema must be an instance of cinema domain")
        
        if not isinstance(theater, Theater):
            raise ValueError("Theater must be an instance of theater domain")
        
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
        self.__movie = movie
        self.__cinema= cinema
        self.__theater = theater
        self.__price = price
        self.__start_time = start_time
        self.__type = type
        self.__language = language
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__updated_at = updated_at

    def get_id(self) -> int:
        return self.__id

    def get_movie(self) -> Movie:
        return self.__movie

    def get_cinema(self) -> Cinema:
        return self.__cinema

    def get_theater(self) -> Theater:
        return self.__theater

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
        return (f"Showtime(id={self.__id}, movie_id={self.__movie.get_id()}, "
                f"cinema_id={self.__cinema.id}, start_time={self.__start_time.strftime('%Y-%m-%d %H:%M')}, "
                f"type={self.__type.value}, language={self.__language.value})")
        
    #TODO: Map 
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            
            "movie": self.__movie,
            "cinema": self.__cinema,
            "theater": self.__theater,
            
            "price": str(self.__price),
            "start_time": self.__start_time.isoformat(),
            "type": self.__type.value,
            "language": self.__language.value,
            "created_at": self.__created_at.isoformat(),
            "updated_at": self.__updated_at.isoformat() if self.__updated_at else None
        }