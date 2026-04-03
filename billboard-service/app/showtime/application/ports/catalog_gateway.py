from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogTheaterSeat:
    id: int
    theater_id: int
    seat_row: str
    seat_number: int


class CatalogGateway(ABC):
    """Port used by showtime use cases to read catalog data."""

    @abstractmethod
    async def is_movie_active(self, movie_id: int) -> bool:
        pass

    @abstractmethod
    async def is_cinema_active(self, cinema_id: int) -> bool:
        pass

    @abstractmethod
    async def theater_has_seats(self, theater_id: int) -> bool:
        pass

    @abstractmethod
    async def list_theater_seats(self, theater_id: int) -> list[CatalogTheaterSeat]:
        pass
