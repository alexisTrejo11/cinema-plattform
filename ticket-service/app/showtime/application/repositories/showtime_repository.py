from app.showtime.domain.entities.showtime import Showtime
from abc import ABC, abstractmethod

class ShowtimeRepository(ABC):
    @abstractmethod
    def get_by_id(self, movie_id: int) -> Showtime:
        pass
    
    @abstractmethod
    def create(self, movie_id: int) -> None:
        pass
    
    
    @abstractmethod
    def update(self, movie_id: int) -> None:
        pass
    
    
    @abstractmethod
    def delete(self, movie_id: int) -> None:
        pass