from typing import List
from abc import ABC, abstractmethod
from app.shared.repository.common_repository import CommonRepository
from ..domain.entities import Movie

class MovieRepository(CommonRepository[Movie], ABC):
    """
    Specific repository interface for Movie entities.
    Inherits common CRUD methods for Movie.
    """
    # @abstractmethod
    # async def find_movies_by_genre(self, genre: str) -> List[Movie]:
    #     pass
    @abstractmethod
    async def list_active(self) -> List[Movie]:
        pass
