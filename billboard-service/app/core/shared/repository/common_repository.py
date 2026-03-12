from typing import Generic, TypeVar, Optional, List, Dict
from abc import ABC, abstractmethod

T = TypeVar("T")


class CommonRepository(ABC, Generic[T]):
    """
    Generic abstract base class for common CRUD repository operations.
    T represents the specific Domain Entity type (e.g., Cinema, Movie).
    """

    @abstractmethod
    async def find_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieves a single entity by its ID.
        """
        pass

    @abstractmethod
    async def find_all(self, page_params: Dict[str, int]) -> List[T]:
        """
        Retrieves a list of entities with pagination parameters.
        page_params should contain 'offset' and 'limit'.
        """
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """
        Saves a new entity or updates an existing one.
        If the entity has no ID, it's typically considered new.
        Returns the saved/updated entity, often with its assigned ID.
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.
        """
        pass

    @abstractmethod
    async def exists_by_id(self, entity_id: int) -> bool:
        """
        Checks if an entity exists by its ID.
        """
        pass
