from fastapi import APIRouter, Depends, Path, Request, status
from typing import List

from app.config.rate_limit import limiter
from app.config.security import require_roles, AuthUserContext
from app.products.application.use_cases.container import (
    ProductCategoryUseCases,
    CategoryCreateCommand,
    CategoryUpdateCommand,
)
from app.products.infrastructure.api.dtos import ProductCategoryResponse
from ..requests_dto import CategoryRequest
from ..dependencies import get_category_use_cases
from ..doc_data import (
    create_category_examples,
    get_category_examples,
    list_categories_examples,
    update_category_examples,
    delete_category_examples,
)

router = APIRouter(
    prefix="/api/v2/categories",
    tags=["Product Categories"],
)


@router.post(
    "/",
    response_model=ProductCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product category",
    description="Creates a new product category with the provided details",
    responses={**create_category_examples},
)
@limiter.limit("10/minute")
async def create_category(
    request: Request,
    category_data: CategoryRequest,
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = CategoryCreateCommand(**category_data.model_dump())
    category = await useCases.create_category(command)
    return ProductCategoryResponse.model_validate(category)


@router.get(
    "/{category_id}",
    response_model=ProductCategoryResponse,
    summary="Get category by ID",
    description="Retrieve detailed information about a specific product category",
    responses={**get_category_examples},
)
@limiter.limit("60/minute")
async def get_category(
    request: Request,
    category_id: int = Path(
        ..., description="ID of the category to retrieve", examples=[1]
    ),
    useCases: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    category = await useCases.get_category_by_id(category_id)
    return ProductCategoryResponse.model_validate(category)


@router.get(
    "/",
    response_model=List[ProductCategoryResponse],
    summary="List all product categories",
    description="Retrieve a list of all product categories",
    responses={**list_categories_examples},
)
@limiter.limit("60/minute")
async def list_categories(
    request: Request,
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    categories = await useCase.list_categories()
    return [ProductCategoryResponse.model_validate(c) for c in categories]


@router.put(
    "/{category_id}",
    response_model=ProductCategoryResponse,
    summary="Update a product category",
    description="Update all details of an existing product category",
    responses={**update_category_examples},
)
@limiter.limit("10/minute")
async def update_category(
    request: Request,
    update_data: CategoryRequest,
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
    category_id: int = Path(
        ..., description="ID of the category to update", examples=[1]
    ),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    command = CategoryUpdateCommand(id=category_id, **update_data.model_dump())
    category = await useCase.update_category(category_id, command)
    return ProductCategoryResponse.model_validate(category)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft Delete a product category",
    description="Soft delete a product category from the system",
    responses={**delete_category_examples},
)
@limiter.limit("10/minute")
async def delete_category(
    request: Request,
    category_id: int = Path(
        ..., description="ID of the category to delete", examples=[1]
    ),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
    useCase: ProductCategoryUseCases = Depends(get_category_use_cases),
):
    await useCase.delete_category(category_id)
