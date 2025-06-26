from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.food.application.dtos import FoodCategoryResponse, FoodCategoryInsert
from app.food.application.category_usecases import CreateCategoryUseCase, DeleteCategoryUseCase, GetCategoryByIdUseCase, ListCategoryUseCase, UpdateCategoryUseCase
from depedencies import get_category_by_id_use_case, list_category_use_case, create_category_use_case, update_category_use_case, delete_category_use_case

category_router = APIRouter(prefix="/categories", tags=["Food Categories"])

@category_router.post("/", response_model=FoodCategoryResponse, status_code=201)
def create_category(
    category_data: FoodCategoryInsert,
    useCase: CreateCategoryUseCase = Depends(create_category_use_case)
):
    return useCase.execute(category_data)

@category_router.get("/{category_id}", response_model=FoodCategoryResponse)
def get_category(
    category_id: int,
    useCase: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case)
):
    category = useCase.execute(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@category_router.get("/", response_model=List[FoodCategoryResponse])
def list_categories(
    useCase: ListCategoryUseCase = Depends(list_category_use_case)
):
    return useCase.execute()

@category_router.put("/{category_id}", response_model=FoodCategoryResponse)
def update_category(
    category_id: int,
    update_data: FoodCategoryInsert,
    useCase: UpdateCategoryUseCase = Depends(update_category_use_case)
):
    category = useCase.execute(category_id, update_data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@category_router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    useCase: DeleteCategoryUseCase = Depends(delete_category_use_case)
):
    if not useCase.execute(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
