from .repositories import FoodCategoryRepository
from app.food.application.dtos import FoodCategoryResponse as CategoryResponse, FoodCategoryInsert
from app.food.domain.entities import FoodCategory
from typing import List

class GetCategoryByIdUseCase:
    def __init__(self, category_repo: FoodCategoryRepository) -> None:
        self.category_repo = category_repo
    
    def execute(self, category_id: int) -> CategoryResponse:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category Not Found")

        return CategoryResponse(**category.model_dump())
    
class ListCategoryUseCase:
    def __init__(self, category_repo: FoodCategoryRepository) -> None:
        self.category_repo = category_repo
    
    def execute(self) -> List[CategoryResponse]:
        category_list = self.category_repo.list()
        return [CategoryResponse(**category.model_dump()) for category in category_list]
    
    
class CreateCategoryUseCase:
    def __init__(self, category_repo: FoodCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(self, create_data: FoodCategoryInsert) -> CategoryResponse:
        new_category = FoodCategory(**create_data.model_dump())
        category_created = self.category_repo.save(new_category)
    
        return CategoryResponse(**category_created.model_dump())


class UpdateCategoryUseCase:
    def __init__(self, category_repo: FoodCategoryRepository) -> None:
        self.category_repo = category_repo
    
    def execute(self, category_id: int, update_data: FoodCategoryInsert) -> CategoryResponse:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category Not Found")

        self._update_fields(category, update_data)
        self.category_repo.save(category)

        return CategoryResponse(**category.model_dump())

    def _update_fields(self, category: FoodCategory, category_data: FoodCategoryInsert):
          update_data = category_data.model_dump()
          
          for k, v in update_data.items():
            setattr(category, k,v)


class DeleteCategoryUseCase:
    def __init__(self, category_repo: FoodCategoryRepository) -> None:
        self.category_repo = category_repo
    
    def execute(self, category_id: int, is_soft_delete=True) -> bool:
        if is_soft_delete:
            category = self.category_repo.get_by_id(category_id)
            if not category:
                return False
            
            category.soft_delete()
            self.category_repo.save(category)
            
            return True
        else:
            return self.category_repo.delete(category_id)