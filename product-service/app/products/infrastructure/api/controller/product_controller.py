from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import List, Optional
from decimal import Decimal
from app.shared.response import ApiResponse
from ..requests_dto import CreateProductRequest, UpdateProductRequest

from app.products.domain.entities.value_objects import ProductId
from app.products.application.commands import ProductUpdateCommand, ProductCreateCommand
from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery
from app.products.application.responses import ProductDetails
from app.products.application.usecases.container import ProductUseCases
from ..depedencies import get_product_use_cases


router = APIRouter(
    prefix="/api/v2/products",
    tags=["Food Products"],
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
    response_model=ApiResponse[ProductDetails],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food product",
    description="Creates a new food product with the provided details",
)
async def create_product(
    product_data: CreateProductRequest,
    usecase: ProductUseCases = Depends(get_product_use_cases),
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
        command = ProductCreateCommand(**product_data.model_dump())
        product = await usecase.create_product(command)
        return ApiResponse.success(product)
    except Exception as e:
        raise


@router.get(
    "/{product_id}",
    response_model=ApiResponse[ProductDetails],
    summary="Get product by ID",
    description="Retrieve detailed information about a specific food product",
)
async def get_product_by_id(
    product_id: UUID = Path(
        ...,
        description="ID of the product to retrieve",
        example="75bb2bef-953f-47b2-8e48-6f3101515ebe",
    ),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    """
    Retrieve a food product by its unique identifier.

    - **product_id**: The ID of the product to retrieve
    """
    try:
        query = GetProductByIdQuery(product_id=ProductId(product_id))
        product = await usecase.get_product_by_id(query)
        return ApiResponse.success(product, "Food product successfully retrieved")
    except Exception as e:
        raise


@router.get(
    "/",
    response_model=ApiResponse[List[ProductDetails]],
    summary="Search food products",
    description="Search and filter food products with pagination",
)
async def search_products(
    offset: int = Query(default=0, ge=0, description="Pagination offset", example=0),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return (1-100)",
        example=10,
    ),
    category_id: Optional[int] = Query(
        None, ge=1, description="Filter by category ID", example=1
    ),
    min_price: Optional[Decimal] = Query(
        None, description="Minimum price filter", example=5.00
    ),
    max_price: Optional[Decimal] = Query(
        None, description="Maximum price filter", example=20.00
    ),
    name_like: Optional[str] = Query(
        None, description="Filter by product name (partial match)", example="pizza"
    ),
    available_only: bool = Query(
        True, description="Only include available products", example=True
    ),
    usecase: ProductUseCases = Depends(get_product_use_cases),
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
        params = SearchProductsQuery(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            category=category_id,
            name=name_like,
            active_only=available_only,
        )
        products = await usecase.search_products(params)
        return ApiResponse.success(products, "Food products successfully retrieved")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/{product_id}",
    response_model=ApiResponse[ProductDetails],
    summary="Update a food product",
    description="Update details of an existing food product",
)
async def update_product(
    update_data: UpdateProductRequest,
    product_id: UUID = Path(..., description="ID of the product to update", example=1),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    """
    Update an existing food product with new details.

    - **product_id**: The ID of the product to update
    - **update_data**: New values for the product (all fields optional)
    """
    try:
        command = ProductUpdateCommand(
            product_id=ProductId(product_id), **update_data.model_dump()
        )
        product = await usecase.update_product(command)
        return ApiResponse.success(product)
    except Exception as e:
        raise


@router.delete(
    "/{product_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete a food product",
    description="Permanently remove a food product from the system",
)
async def delete_product(
    product_id: UUID = Path(..., description="ID of the product to delete", example=1),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    """
    Delete a food product by its ID.

    - **product_id**: The ID of the product to delete
    """
    try:
        await usecase.soft_delete_product(ProductId(product_id))
        return ApiResponse.success(None, "Product successfully deleted")
    except Exception as e:
        raise
