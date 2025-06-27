from abc import ABC, abstractmethod
from app.food.domain.entities import FoodCategory, FoodProduct
from typing import Optional, List
from .dtos import SearchFoodParams


class FoodCategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[FoodCategory]:
        pass
    
    @abstractmethod
    def list(self) -> List[FoodCategory]:
        pass
    
    @abstractmethod
    def save(self, category: FoodCategory) -> FoodCategory:
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> bool:
        pass
    
    @abstractmethod
    def exists_by_id(self, category_id: int) -> bool:
        pass
    
    
    @abstractmethod
    def exists_by_name(self, category_name: str) -> bool:
        pass
    

class FoodRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[FoodProduct]:
        """
        Retrieves a single food product by its ID, if it's active.
        """
        pass
    
    @abstractmethod
    def search(self, food_params: SearchFoodParams) -> List[FoodProduct]:
        """
        Searches for food products based on various criteria provided in SearchFoodParams.

        Args:
            food_params (SearchFoodParams): An object containing search parameters
                                            like price range, name, category,
                                            availability, offset, and limit.

        Returns:
            List[FoodProduct]: A list of FoodProduct domain entities that match
                               the search criteria.
        """
        pass
    
    @abstractmethod
    def save(self, product: FoodProduct) -> FoodProduct:
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass
    
    