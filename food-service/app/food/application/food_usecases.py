from typing import List
from .exceptions import ProductNotFoundError, InvalidCategoryError
from .repositories import FoodRepository, FoodCategoryRepository
from .dtos import FoodProductResponse, FoodProductCreate, FoodProductUpdate, SearchFoodParams
from app.food.domain.entities import FoodProduct

class GetFoodByIdUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, id: int) -> FoodProductResponse:
        food = self.food_repository.get_by_id(id)
        if not food:
            raise ProductNotFoundError("Product", id)

        return FoodProductResponse(**food.model_dump())    
    
    
class SearchFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, food_params: SearchFoodParams) -> List[FoodProductResponse]:
        food_product_list = self.food_repository.search(food_params)
        return [FoodProductResponse(**product.model_dump()) for product in food_product_list]


class CreateFoodUseCase:
    def __init__(self, food_repository: FoodRepository, category_repo: FoodCategoryRepository) -> None:
        self.food_repository = food_repository
        self.category_repo = category_repo
    
    def execute(self, create_data: FoodProductCreate) -> FoodProductResponse:
        new_category = FoodProduct(**create_data.model_dump())
        category_created = self.food_repository.save(new_category)
    
        return FoodProductResponse(**category_created.model_dump())

    def _validate_category(self, create_data: FoodProductCreate):
        exists = self.category_repo.exists_by_id(create_data.category_id)
        if not exists:
            raise InvalidCategoryError("category_id", "cateogry must be valid")
    
    
class UpdateFoodUseCase:
    def __init__(self, food_repository: FoodRepository, category_repo: FoodCategoryRepository) -> None:
        self.food_repository = food_repository
        self.category_repo = category_repo

    
    def execute(self, category_id: int, update_data: FoodProductUpdate) -> FoodProductResponse:
        category = self.food_repository.get_by_id(category_id)
        if not category:
            raise ProductNotFoundError("Product", category_id)

        if update_data.category_id and update_data.category_id != category_id:
            self._validate_category(update_data.category_id)

        self._update_fields(update_data, update_data)
        self.food_repository.save(category)

        return FoodProductResponse(**category.model_dump())

    def _update_fields(self, category: FoodProductUpdate, category_data: FoodProductUpdate):
          update_data = category_data.model_dump(exclude_unset=True)
          
          for k, v in update_data.items():
            setattr(category, k,v)

    def _validate_category(self, category_id: int):
        exists = self.category_repo.exists_by_id(category_id)
        if not exists:
            raise InvalidCategoryError("category_id", "cateogry must be valid")

class DeleteFoodUseCase:
    def __init__(self, food_repository: FoodRepository) -> None:
        self.food_repository = food_repository
    
    def execute(self, id: int) -> None:
        food = self.food_repository.get_by_id(id)
        if not food:
            raise ProductNotFoundError("Product", id)

        self.food_repository.delete(id)