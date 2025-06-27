from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from decimal import Decimal
from app.food.application.dtos import FoodProductCreate, FoodProductUpdate, FoodProductResponse, SearchFoodParams
from app.food.application.food_usecases import GetFoodByIdUseCase, SearchFoodUseCase, CreateFoodUseCase, UpdateFoodUseCase, DeleteFoodUseCase
from .depedencies import get_food_by_id_use_case, search_food_use_case, create_food_use_case, update_food_use_case, delete_food_use_case

router = APIRouter(prefix="/products", tags=["Food Products"])

@router.post("/", response_model=FoodProductResponse, status_code=201)
def create_product(
    product_data: FoodProductCreate,
    usecase: CreateFoodUseCase = Depends(create_food_use_case)
):
    product = usecase.execute(product_data)
    return product

@router.get("/{product_id}", response_model=FoodProductResponse)
def get_product_by_id(
    product_id: int,
    usecase: GetFoodByIdUseCase = Depends(get_food_by_id_use_case)
):
    product = usecase.execute(product_id)
    return product

@router.get("/", response_model=List[FoodProductResponse])
def search_products(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = Query(None, ge=1),
    min_price: Optional[Decimal] = Query(None),
    max_price: Optional[Decimal] = Query(None),
    name_like: Optional[str] = Query(None),
    available_only: bool = Query(True),
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
    
    print(params)
    
    return usecase.execute(params)

@router.patch("/{product_id}", response_model=FoodProductResponse)
def update_product(
    product_id: int,
    update_data: FoodProductUpdate,
    usecase: UpdateFoodUseCase = Depends(update_food_use_case)
):
    product = usecase.execute(product_id, update_data)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    usecase: DeleteFoodUseCase = Depends(delete_food_use_case)
):
    usecase.execute(product_id)
