from fastapi import APIRouter, Depends, status, Path
from typing import List
from app.shared.response import ApiResponse
from app.products.application.usecases.container import (
    ProductCategoryUseCases,
    ProductCategoryInsertCommand as CategoryInsertCommand,
)
from app.products.application.responses import ProductCategoryResponse
from ..requests_dto import InsertProductCategoryRequest
from ..depedencies import get_category_use_cases

router = APIRouter(
    prefix="/api/v2/categories",
    tags=["Food Categories"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid credentials"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authorized to perform this action"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)


@router.post(
    "/",
    response_model=ApiResponse[ProductCategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food category",
    description="Creates a new food category with the provided details",
)
def create_category(
    category_data: InsertProductCategoryRequest,
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Create a new food category with the following details:
    - **name**: Category name (1-100 characters)
    - **description**: Optional description
    - **is_active**: Active status (default: True)
    """
    try:
        command = CategoryInsertCommand(**category_data.model_dump())
        category = useCases.create_category(command)
        return ApiResponse.success(category, "Category succesfully created")
    except Exception as e:
        raise


@router.get(
    "/{category_id}",
    response_model=ApiResponse[ProductCategoryResponse],
    summary="Get category by ID",
    description="Retrieve detailed information about a specific food category",
)
def get_category(
    category_id: int = Path(
        ..., description="ID of the category to retrieve", example=1
    ),
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Retrieve a food category by its unique identifier.

    - **category_id**: The ID of the category to retrieve
    """
    category = useCases.get_category_by_id(category_id)
    return ApiResponse.success(category, "Category succesfully retrieved")


@router.get(
    "/",
    response_model=ApiResponse[List[ProductCategoryResponse]],
    summary="List all food categories",
    description="Retrieve a list of all food categories",
    responses={
        status.HTTP_200_OK: {
            "description": "List of food categories",
            "content": {
                "application/json": {
                    "example": [{"id": 1, "name": "Pizzas", "is_active": True}]
                }
            },
        }
    },
)
def list_categories(useCase: ProductCategoryUseCases = Depends(get_category_use_cases)):
    """Retrieve all food categories in the system"""
    try:
        categories = useCase.list_categories()
        return ApiResponse.success(categories, "Categories succesfully retrieved")
    except Exception as e:
        raise


@router.put(
    "/{category_id}",
    response_model=ApiResponse[ProductCategoryResponse],
    summary="Update a food category",
    description="Update all details of an existing food category",
)
def update_category(
    update_data: InsertProductCategoryRequest,
    category_id: int = Path(..., description="ID of the category to update", example=1),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Update an existing food category with new details.

    - **category_id**: The ID of the category to update
    - **update_data**: New values for the category
    """
    try:
        command = CategoryInsertCommand(**update_data.model_dump())
        category = useCase.update_category(category_id, command)
        return ApiResponse.success(category, "Category succesfully updated")
    except Exception as e:
        raise


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a food category",
    description="Permanently remove a food category from the system",
)
def delete_category(
    category_id: int = Path(..., description="ID of the category to delete", example=1),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Delete a food category by its ID.

    - **category_id**: The ID of the category to delete
    """
    try:
        useCase.soft_delete_category(category_id)
        return ApiResponse.success(message="Category Successfully Deleted")
    except Exception as e:
        raise
