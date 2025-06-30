from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import List, Optional
from decimal import Decimal
from app.utils.response import ApiResponse
from app.products.application.dtos import FoodProductCreate, FoodProductUpdate, FoodProductResponse, SearchFoodParams
from app.products.application.food_usecases import GetFoodByIdUseCase, SearchFoodUseCase, CreateFoodUseCase, UpdateFoodUseCase, DeleteFoodUseCase
from .depedencies import get_food_by_id_use_case, search_food_use_case, create_food_use_case, update_food_use_case, delete_food_use_case

router = APIRouter(
    prefix="/api/v2/products",
    tags=["Food Products"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid credentials"},
        status.HTTP_403_FORBIDDEN: {"description": "Not authorized to perform this action"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)

@router.post(
    "/",
    response_model=ApiResponse[FoodProductResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food product",
    description="Creates a new food product with the provided details",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Product successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Margherita Pizza",
                        "price": 12.99,
                        "category_id": 1,
                        "is_available": True
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {"detail": "Price must be greater than 0"}
                }
            }
        }
    }
)
def create_product(
    product_data: FoodProductCreate,
    usecase: CreateFoodUseCase = Depends(create_food_use_case)
):
    """
    Create a new food product with the following details:
    - **name**: Product name (1-200 characters)
    - **price**: Product price (must be positive)
    - **category_id**: ID of the product category
    - **description**: Optional description
    - **image_url**: Optional product image URL
    - **preparation_time**: Optional prep time in minutes
    - **calories**: Optional calorie count
    """
    try:
        product = usecase.execute(product_data)
        return ApiResponse.success(product) 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/{product_id}",
    response_model=ApiResponse[FoodProductResponse],
    summary="Get product by ID",
    description="Retrieve detailed information about a specific food product",
    responses={
        status.HTTP_200_OK: {
            "description": "Product details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Margherita Pizza",
                        "price": 12.99,
                        "category_id": 1,
                        "is_available": True
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Product not found with ID 999"}
                }
            }
        }
    }
)
def get_product_by_id(
    product_id: int = Path(..., description="ID of the product to retrieve", example=1),
    usecase: GetFoodByIdUseCase = Depends(get_food_by_id_use_case)
):
    """
    Retrieve a food product by its unique identifier.
    
    - **product_id**: The ID of the product to retrieve
    """
    try:
        product = usecase.execute(product_id)
        return ApiResponse.success(product, "Food product successfully retrieved")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=ApiResponse[List[FoodProductResponse]],
    summary="Search food products",
    description="Search and filter food products with pagination",
    responses={
        status.HTTP_200_OK: {
            "description": "List of matching food products",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Margherita Pizza",
                        "price": 12.99,
                        "category_id": 1
                    }]
                }
            }
        }
    }
)
def search_products(
    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination offset",
        example=0
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)",
        example=10
    ),
    category_id: Optional[int] = Query(
        None,
        ge=1,
        description="Filter by category ID",
        example=1
    ),
    min_price: Optional[Decimal] = Query(
        None,
        description="Minimum price filter",
        example=5.00
    ),
    max_price: Optional[Decimal] = Query(
        None,
        description="Maximum price filter",
        example=20.00
    ),
    name_like: Optional[str] = Query(
        None,
        description="Filter by product name (partial match)",
        example="pizza"
    ),
    available_only: bool = Query(
        True,
        description="Only include available products",
        example=True
    ),
    usecase: SearchFoodUseCase = Depends(search_food_use_case)
):
    """
    Search food products with various filters:
    
    - **offset**: Pagination starting point
    - **limit**: Number of items per page (1-100)
    - **category_id**: Filter by category
    - **min_price/max_price**: Price range filter
    - **name_like**: Name search (partial match)
    - **available_only**: Show only available products
    """
    try:
        params = SearchFoodParams(
            offset=offset, 
            limit=limit, 
            min_price=min_price, 
            max_price=max_price, 
            category=category_id, 
            name=name_like, 
            active_only=available_only
        )
        products = usecase.execute(params)
        return ApiResponse.success(products, "Food products successfully retrieved")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.patch(
    "/{product_id}",
    response_model=ApiResponse[FoodProductResponse],
    summary="Update a food product",
    description="Update details of an existing food product",
    responses={
        status.HTTP_200_OK: {
            "description": "Product updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Updated Pizza",
                        "price": 14.99
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Product not found with ID 999"}
                }
            }
        }
    }
)
def update_product(
    update_data: FoodProductUpdate,
    product_id: int = Path(..., description="ID of the product to update", example=1),
    usecase: UpdateFoodUseCase = Depends(update_food_use_case)
):
    """
    Update an existing food product with new details.
    
    - **product_id**: The ID of the product to update
    - **update_data**: New values for the product (all fields optional)
    """
    try:
        product = usecase.execute(product_id, update_data)
        return ApiResponse.success(product) 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete(
    "/{product_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete a food product",
    description="Permanently remove a food product from the system",
    responses={
        status.HTTP_200_OK: {
            "description": "Product deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Product not found with ID 999"}
                }
            }
        }
    }
)
def delete_product(
    product_id: int = Path(..., description="ID of the product to delete", example=1),
    usecase: DeleteFoodUseCase = Depends(delete_food_use_case)
):
    """
    Delete a food product by its ID.
    
    - **product_id**: The ID of the product to delete
    """
    try:
        usecase.execute(product_id)
        return ApiResponse.success(None, "Product successfully deleted")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )