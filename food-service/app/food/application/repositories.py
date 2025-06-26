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
    
    

class FoodRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[FoodProduct]:
        pass
    
    @abstractmethod
    def search(self, food_params: SearchFoodParams) -> List[FoodProduct]:
        pass
    
    @abstractmethod
    def save(self, category: FoodProduct) -> FoodProduct:
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> bool:
        pass
    
    