from abc import ABC, abstractmethod
from typing import Optional, List

from app.external.billboard.core.entities.theater import Theater
from app.external.billboard.core.entities.cinema import Cinema
from app.external.billboard.core.entities.showtime import Showtime


class TheaterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, theater_id: int) -> Optional[Theater]:
        pass

    @abstractmethod
    async def save(self, theater: Theater) -> None:
        """Insert or replace the theater aggregate in the read store."""

    @abstractmethod
    async def delete(self, theater_id: int) -> None:
        """Remove the theater from the read store."""


class CinemaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, cinema_id: int) -> Optional[Cinema]:
        pass

    @abstractmethod
    async def save(self, cinema: Cinema) -> None:
        pass

    @abstractmethod
    async def delete(self, cinema_id: int) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[Cinema]:
        pass


class ShowtimeRepository(ABC):
    @abstractmethod
    async def get_by_id(
        self, showtime_id: int, raise_exception: bool = True
    ) -> Optional[Showtime]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Showtime]:
        pass

    @abstractmethod
    async def create(self, showtime: Showtime) -> None:
        pass

    @abstractmethod
    async def update(self, showtime: Showtime) -> None:
        pass

    @abstractmethod
    async def delete(self, showtime_id: int) -> None:
        pass
