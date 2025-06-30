from sqlalchemy.orm import Session
from config.postgres_config import get_db
from fastapi import Depends
from app.combos.application.repository import ComboRepository
from app.products.application.repositories import FoodRepository
from app.combos.application.usecases import (
    ListActiveComboUseCase,
    GetComboByIdUseCase,
    GetCombosByProductUseCase,
    CreateComboUseCase,
    UpdateComboUseCase,
    DeleteComboUseCase
)
from app.combos.infrastructure.persistence.sqlc_alch_como_repo import SqlAlchemyComboRepository
from app.products.infrastructure.persistence.sqlalch_food_repo import SqlAlchFoodRepository

def get_combo_repository(session: Session = Depends(get_db)) -> ComboRepository:
    return SqlAlchemyComboRepository(session)

def get_food_repository(session: Session = Depends(get_db)) -> FoodRepository:
    return SqlAlchFoodRepository(session)

# Combo Use Cases
def get_list_active_combo_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository)
) -> ListActiveComboUseCase:
    return ListActiveComboUseCase(combo_repo)

def get_combo_by_id_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository)
) -> GetComboByIdUseCase:
    return GetComboByIdUseCase(combo_repo)

def get_combos_by_product_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository),
    food_repo: FoodRepository = Depends(get_food_repository)
) -> GetCombosByProductUseCase:
    return GetCombosByProductUseCase(combo_repo, food_repo)

def create_combo_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository),
    food_repo: FoodRepository = Depends(get_food_repository)
) -> CreateComboUseCase:
    return CreateComboUseCase(combo_repo, food_repo)

def update_combo_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository),
    food_repo: FoodRepository = Depends(get_food_repository)
) -> UpdateComboUseCase:
    return UpdateComboUseCase(combo_repo, food_repo)

def delete_combo_use_case(
    combo_repo: ComboRepository = Depends(get_combo_repository)
) -> DeleteComboUseCase:
    return DeleteComboUseCase(combo_repo)