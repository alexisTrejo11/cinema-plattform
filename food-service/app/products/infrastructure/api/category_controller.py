from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List
from app.utils.response import ApiResponse
from app.products.application.dtos import FoodCategoryResponse, FoodCategoryInsert
from app.products.application.category_usecases import CreateCategoryUseCase, DeleteCategoryUseCase, GetCategoryByIdUseCase, ListCategoryUseCase, UpdateCategoryUseCase
from .depedencies import  get_category_by_id_use_case, list_category_use_case, create_category_use_case, update_category_use_case, delete_category_use_case

router = APIRouter(
    prefix="/api/v2/categories",
    tags=["Food Categories"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid credentials"},
        status.HTTP_403_FORBIDDEN: {"description": "Not authorized to perform this action"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)

@router.post(
    "/",
    response_model=ApiResponse[FoodCategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food category",
    description="Creates a new food category with the provided details",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Category successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Pizzas",
                        "description": "Various types of pizzas",
                        "is_active": True
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {"detail": "Name must be between 1-100 characters"}
                }
            }
        }
    }
)
def create_category(
    category_data: FoodCategoryInsert,
    useCase: CreateCategoryUseCase = Depends(create_category_use_case)
):
    """
    Create a new food category with the following details:
    - **name**: Category name (1-100 characters)
    - **description**: Optional description
    - **is_active**: Active status (default: True)
    """
    try:
        category = useCase.execute(category_data)
        return ApiResponse.success(category, "Category succesfully created")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/{category_id}",
    response_model=ApiResponse[FoodCategoryResponse],
    summary="Get category by ID",
    description="Retrieve detailed information about a specific food category",
    responses={
        status.HTTP_200_OK: {
            "description": "Category details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Pizzas",
                        "description": "Various types of pizzas",
                        "is_active": True
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Category not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Category not found with ID 999"}
                }
            }
        }
    }
)
def get_category(
    category_id: int = Path(..., description="ID of the category to retrieve", example=1),
    useCase: GetCategoryByIdUseCase = Depends(get_category_by_id_use_case)
):
    """
    Retrieve a food category by its unique identifier.
    
    - **category_id**: The ID of the category to retrieve
    """
    try:
        category = useCase.execute(category_id)
        return ApiResponse.success(category,  "Category succesfully retrieved")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=ApiResponse[List[FoodCategoryResponse]],
    summary="List all food categories",
    description="Retrieve a list of all food categories",
    responses={
        status.HTTP_200_OK: {
            "description": "List of food categories",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Pizzas",
                        "is_active": True
                    }]
                }
            }
        }
    }
)
def list_categories(
    useCase: ListCategoryUseCase = Depends(list_category_use_case)
):
    """Retrieve all food categories in the system"""
    try:
        categories = useCase.execute()
        return ApiResponse.success(categories, "Categories succesfully retrieved")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put(
    "/{category_id}",
    response_model=ApiResponse[FoodCategoryResponse],
    summary="Update a food category",
    description="Update all details of an existing food category",
    responses={
        status.HTTP_200_OK: {
            "description": "Category updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Updated Category",
                        "description": "New description",
                        "is_active": False
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Category not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Category not found with ID 999"}
                }
            }
        }
    }
)
def update_category(
    update_data: FoodCategoryInsert,
    category_id: int = Path(..., description="ID of the category to update", example=1),
    useCase: UpdateCategoryUseCase = Depends(update_category_use_case)
):
    """
    Update an existing food category with new details.
    
    - **category_id**: The ID of the category to update
    - **update_data**: New values for the category
    """
    try:
        category = useCase.execute(category_id, update_data)
        return ApiResponse.success(category,  "Category succesfully updated")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a food category",
    description="Permanently remove a food category from the system",
    responses={
        status.HTTP_200_OK: {
            "description": "Category deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Category not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Category not found with ID 999"}
                }
            }
        }
    }
)
def delete_category(
    category_id: int = Path(..., description="ID of the category to delete", example=1),
    useCase: DeleteCategoryUseCase = Depends(delete_category_use_case)
):
    """
    Delete a food category by its ID.
    
    - **category_id**: The ID of the category to delete
    """
    try:
        useCase.execute(category_id)
        return ApiResponse.success(data=None, message="Category Successfully Deleted")    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )