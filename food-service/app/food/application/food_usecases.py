from typing import List
from .repositories import FoodRepository
from .dtos import FoodProductResponse, FoodProductCreate, FoodProductUpdate, SearchFoodParams
from app.food.domain.entities import FoodProduct

class GetFoodByIdUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, id: int) -> FoodProductResponse:
        food = self.food_repository.get_by_id(id)
        if not food:
            raise ValueError("Product Not Found")

        return FoodProductResponse(**food.model_dump())    
    
    
class SearchFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, food_params: SearchFoodParams) -> List[FoodProductResponse]:
        food_product_list = self.food_repository.search(food_params)
        return [FoodProductResponse(**product.model_dump()) for product in food_product_list]


class CreateFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, create_data: FoodProductCreate) -> FoodProductResponse:
        new_category = FoodProduct(**create_data.model_dump())
        category_created = self.food_repository.save(new_category)
    
        return FoodProductResponse(**category_created.model_dump())

    
class UpdateFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, category_id: int, update_data: FoodProductUpdate) -> FoodProductResponse:
        category = self.food_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category Not Found")

        self._update_fields(update_data, update_data)
        self.food_repository.save(category)

        return FoodProductResponse(**category.model_dump())

    def _update_fields(self, category: FoodProductUpdate, category_data: FoodProductUpdate):
          update_data = category_data.model_dump(exclude_unset=True)
          
          for k, v in update_data.items():
            setattr(category, k,v)

class DeleteFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, id: int) -> None:
        food = self.food_repository.get_by_id(id)
        if not food:
            raise ValueError("Product Not Found")

        self.food_repository.delete(id)