from sqlalchemy.orm import Session
from config.postgres_config import get_db
from fastapi import Depends
from app.food.application.repositories import FoodCategoryRepository, FoodRepository
from app.food.application.category_usecases import CreateCategoryUseCase, UpdateCategoryUseCase, DeleteCategoryUseCase, ListCategoryUseCase, GetCategoryByIdUseCase 
from app.food.infrastructure.persistence.sqlach_category_repo import SQLAlchemyCategoryRepository 
from app.food.infrastructure.persistence.sqlalch_food_repo import SqlAlchFoodRepository 
from app.food.application.food_usecases import GetFoodByIdUseCase, SearchFoodUseCase, CreateFoodUseCase, UpdateFoodUseCase, DeleteFoodUseCase

def get_category_repository(session: Session = Depends(get_db)) -> FoodCategoryRepository:
    return SQLAlchemyCategoryRepository(session)

def get_food_repository(session: Session = Depends(get_db)) -> FoodRepository:
    return SqlAlchFoodRepository(session)

# Category
def list_category_use_case(category_repo : FoodCategoryRepository = Depends(get_category_repository)) -> ListCategoryUseCase:
    return ListCategoryUseCase(category_repo)

def get_category_by_id_use_case(category_repo : FoodCategoryRepository = Depends(get_category_repository)) -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase(category_repo)

def create_category_use_case(category_repo : FoodCategoryRepository = Depends(get_category_repository)) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(category_repo)

def update_category_use_case(category_repo : FoodCategoryRepository = Depends(get_category_repository)) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(category_repo)

def delete_category_use_case(category_repo : FoodCategoryRepository = Depends(get_category_repository)) -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(category_repo)


# Food

def search_food_use_case(food_repo : FoodRepository = Depends(get_food_repository)) -> SearchFoodUseCase:
    return SearchFoodUseCase(food_repo)

def get_food_by_id_use_case(food_repo : FoodRepository = Depends(get_food_repository)) -> GetFoodByIdUseCase:
    return GetFoodByIdUseCase(food_repo)

def create_food_use_case(food_repo : FoodRepository = Depends(get_food_repository)) -> CreateFoodUseCase:
    return CreateFoodUseCase(food_repo)

def update_food_use_case(food_repo : FoodRepository = Depends(get_food_repository)) -> UpdateFoodUseCase:
    return UpdateFoodUseCase(food_repo)

def delete_food_use_case(food_repo : FoodRepository = Depends(get_food_repository)) -> DeleteFoodUseCase:
    return DeleteFoodUseCase(food_repo)
