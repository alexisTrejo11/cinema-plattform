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
    def __init__(self, food_repository: FoodRepository, product_repo: FoodCategoryRepository) -> None:
        self.food_repository = food_repository
        self.product_repo = product_repo
    
    def execute(self, create_data: FoodProductCreate) -> FoodProductResponse:
        self._validate_cateogry(create_data)
        
        new_product = FoodProduct(**create_data.model_dump())
        product_created = self.food_repository.save(new_product)
    
        return FoodProductResponse(**product_created.model_dump())

    def _validate_cateogry(self, create_data: FoodProductCreate):
        exists = self.product_repo.exists_by_id(create_data.category_id)
        if not exists:
            raise InvalidCategoryError("product_id", "cateogry must be valid")
    
    
class UpdateFoodUseCase:
    def __init__(self, food_repository: FoodRepository, product_repo: FoodCategoryRepository) -> None:
        self.food_repository = food_repository
        self.product_repo = product_repo

    
    def execute(self, product_id: int, update_data: FoodProductUpdate) -> FoodProductResponse:
        product = self.food_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError("Product", product_id)

        if update_data.category_id and update_data.category_id != product_id:
            self._validate_category(update_data.category_id)

        self._update_fields(product, update_data)
        self.food_repository.save(product)

        return FoodProductResponse(**product.model_dump())

    def _update_fields(self, product: FoodProduct, update_data: FoodProductUpdate):
          data = update_data.model_dump(exclude_unset=True)
          
          for k, v in data.items():
            setattr(product, k,v)

    def _validate_category(self, category_id: int):
        exists = self.product_repo.exists_by_id(category_id)
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