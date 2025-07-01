from app.showtime.domain.entities.theater import Theater
from abc import ABC, abstractmethod

class TheaterRepository(ABC):
    @abstractmethod
    def get_by_id(self, movie_id: int) -> Theater:
        pass
    
    @abstractmethod
    def create(self, theather: Theater) -> None:
        pass
    
    @abstractmethod
    def update(self, movie_id: int) -> None:
        pass
    
    
    @abstractmethod
    def delete(self, movie_id: int) -> None:
        pass
    