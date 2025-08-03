import logging
from fastapi import APIRouter, Depends, status, Path
from typing import List
from app.shared.response import ApiResponse
from app.user.auth.auth_dependencies import get_logged_admin_user
from app.products.application.usecases.container import (
    ProductCategoryUseCases,
    CategoryCreateCommand,
    CategoryUpdateCommand,
)
from app.products.application.responses import ProductCategoryResponse
from ..requests_dto import CategoryRequest
from ..depedencies import get_category_use_cases
from ..doc_data import (
    create_category_examples,
    get_category_examples,
    list_categories_examples,
    update_category_examples,
    delete_category_examples,
)

logger = logging.getLogger("app")


router = APIRouter(
    prefix="/api/v2/categories",
    tags=["Product Categories"],
)


@router.post(
    "/",
    response_model=ApiResponse[ProductCategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product category",
    description="Creates a new product category with the provided details",
    responses={**create_category_examples},
)
async def create_category(
    category_data: CategoryRequest,
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
    admin_user=Depends(get_logged_admin_user),
):
    """
    Create a new product category with the following details:
    - **name**: Category name (1-100 characters)
    - **description**: Optional description
    - **is_active**: Active status (default: True)
    """
    try:
        logger.info(
            f"Admin {admin_user.get_id()} attempting to create category with data: {category_data.model_dump()}"
        )

        command = CategoryCreateCommand(**category_data.model_dump())
        category = await useCases.create_category(command)

        logger.info(f"Category Id {category.id} created successfully")
        return ApiResponse.success(category, "Category succesfully created")
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise


@router.get(
    "/{category_id}",
    response_model=ApiResponse[ProductCategoryResponse],
    summary="Get category by ID",
    description="Retrieve detailed information about a specific product category",
    responses={**get_category_examples},
)
async def get_category(
    category_id: int = Path(
        ..., description="ID of the category to retrieve", example=1
    ),
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Retrieve a product category by its unique identifier.

    - **category_id**: The ID of the category to retrieve
    """
    try:
        logger.info(f"Retrieving category with ID: {category_id}")
        category = await useCases.get_category_by_id(category_id)

        logger.info(f"Category {category_id} retrieved successfully")
        return ApiResponse.success(category, "Category succesfully retrieved")
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {e}")
        raise


@router.get(
    "/",
    response_model=ApiResponse[List[ProductCategoryResponse]],
    summary="List all product categories",
    description="Retrieve a list of all product categories",
    responses={**list_categories_examples},
)
async def list_categories(
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """Retrieve all product categories in the system"""
    try:
        logger.info("Listing all product categories")
        categories = await useCase.list_categories()

        logger.info(f"Retrieved {len(categories)} categories")
        return ApiResponse.success(categories, "Categories succesfully retrieved")
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        raise


@router.put(
    "/{category_id}",
    response_model=ApiResponse[ProductCategoryResponse],
    summary="Update a product category",
    description="Update all details of an existing product category",
    responses={**update_category_examples},
)
async def update_category(
    update_data: CategoryRequest,
    admin_user=Depends(get_logged_admin_user),
    category_id: int = Path(..., description="ID of the category to update", example=1),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Update an existing product category with new details.

    - **category_id**: The ID of the category to update
    - **update_data**: New values for the category
    """
    try:
        logger.info(
            f"Admin {admin_user.get_id()} updating is attempting to update category {category_id} with data: {update_data.model_dump()}"
        )
        command = CategoryUpdateCommand(id=category_id, **update_data.model_dump())
        category = await useCase.update_category(category_id, command)

        logger.info(f"Category {category_id} updated successfully")
        return ApiResponse.success(category, "Category succesfully updated")
    except Exception as e:
        logger.error(f"Error updating category {category_id}: {e}")
        raise


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft Delete a product category",
    description="Soft delete a product category from the system",
    responses={**delete_category_examples},
)
async def delete_category(
    category_id: int = Path(..., description="ID of the category to delete", example=1),
    admin_user=Depends(get_logged_admin_user),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    """
    Delete a product category by its ID.

    - **category_id**: The ID of the category to delete
    """
    try:
        logger.info(
            f"Admin {admin_user.get_id()} soft deleting category with ID: {category_id}"
        )
        await useCase.soft_delete_category(category_id)

        logger.info(f"Category {category_id} successfully deleted")
        return ApiResponse.success(message="Category Successfully Deleted")
    except Exception as e:
        logger.error(f"Error deleting category {category_id}: {e}")
        raise
