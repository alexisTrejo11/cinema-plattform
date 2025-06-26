from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from decimal import Decimal
from app.food.application.dtos import FoodProductCreate, FoodProductUpdate, FoodProductResponse, SearchFoodParams
from app.food.application.food_usecases import GetFoodByIdUseCase, SearchFoodUseCase, CreateFoodUseCase, UpdateFoodUseCase, DeleteFoodUseCase
from .depedencies import get_food_by_id_use_case, search_food_use_case, create_category_use_case, update_category_use_case, delete_category_use_case

router = APIRouter(prefix="/products", tags=["Food Products"])

@router.post("/", response_model=FoodProductResponse, status_code=201)
def create_product(
    product_data: FoodProductCreate,
    usecase: CreateFoodUseCase = Depends(create_category_use_case)
):
    product = usecase.execute(product_data)
    if not product:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    return product

@router.get("/{product_id}", response_model=FoodProductResponse)
def search_product(
    product_id: int,
    usecase: GetFoodByIdUseCase = Depends(get_food_by_id_use_case)
):
    product = usecase.execute(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=List[FoodProductResponse])
def search_products(
    offset: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: int = Query(1, ge=1),
    min_price: Decimal = Query(),
    max_price: Decimal = Query(),
    name_like: str = Query(),
    available_only: bool = Query(False),
    usecase: SearchFoodUseCase = Depends(search_food_use_case)
):
    params = SearchFoodParams(
        offset=offset, 
        limit=limit, 
        min_price=min_price, 
        max_price=max_price, 
        category=category_id, 
        name=name_like, 
        active_only=available_only
    )
    
    return usecase.execute(params)

@router.patch("/{product_id}", response_model=FoodProductResponse)
def update_product(
    product_id: int,
    update_data: FoodProductUpdate,
    usecase: UpdateFoodUseCase = Depends(update_category_use_case)
):
    product = usecase.execute(product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or invalid category_id")
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    usecase: DeleteFoodUseCase = Depends(delete_category_use_case)
):
    if not usecase.execute(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
