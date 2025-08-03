from fastapi import APIRouter, Depends, Path, status
from uuid import UUID
from typing import List
import logging

from app.shared.response import ApiResponse
from app.user.auth.auth_dependencies import get_logged_admin_user
from app.products.domain.entities.value_objects import ProductId
from app.products.application.commands import ProductUpdateCommand, ProductCreateCommand
from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery
from app.products.application.responses import ProductDetails
from app.products.application.usecases.container import ProductUseCases

from ..depedencies import get_product_use_cases
from ..requests_dto import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductSearchQuery,
)
from ..doc_data import (
    create_product_examples,
    create_update_examples,
    delete_product_examples,
    get_product_examples,
    search_products_examples,
)


logger = logging.getLogger("app")

router = APIRouter(prefix="/api/v2/products", tags=["Food Products"])


@router.get(
    "/{product_id}",
    response_model=ApiResponse[ProductDetails],
    summary="Get product by ID",
    description="Retrieve detailed information about a specific food product",
    responses={**get_product_examples},
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
        logger.error(f"Error retrieving product {product_id}: {e}")
        raise


@router.get(
    "/",
    response_model=ApiResponse[List[ProductDetails]],
    summary="Search food products",
    description="Search and filter food products with pagination",
    responses={**search_products_examples},
)
async def search_products(
    search_params: ProductSearchQuery = Depends(),
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
        logger.info(f"Searching products with params: {search_params.model_dump()}")

        params = SearchProductsQuery(**search_params.model_dump())
        products_response = await usecase.search_products(params)

        logger.info(f"Found {len(products_response.product_page)} products")
        return ApiResponse.success(
            data=products_response.product_page,
            message="Food products successfully retrieved",
            metadata={"page": products_response.metadata.model_dump()},
        )
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise


@router.post(
    "/",
    response_model=ApiResponse[ProductDetails],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food product",
    description="Creates a new food product with the provided details",
    responses={**create_product_examples},
)
async def create_product(
    product_data: CreateProductRequest,
    admin_user=Depends(get_logged_admin_user),
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
        logger.info(
            f"Admin {admin_user.get_id()} is attempting to create product: {product_data.model_dump()}"
        )

        command = ProductCreateCommand(**product_data.model_dump())
        product = await usecase.create_product(command)

        logger.info(f"Product created successfully: {product.id}")
        return ApiResponse.success(product)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise


@router.patch(
    "/{product_id}",
    response_model=ApiResponse[ProductDetails],
    summary="Update a food product",
    description="Update details of an existing food product",
    responses={**create_update_examples},
)
async def update_product(
    update_data: UpdateProductRequest,
    product_id: UUID = Path(..., description="ID of the product to update", example=1),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    admin_user=Depends(get_logged_admin_user),
):
    """
    Update an existing food product with new details.

    - **product_id**: The ID of the product to update
    - **update_data**: New values for the product (all fields optional)
    """
    try:
        logger.info(
            f"Admin {admin_user.get_id()} is attempting to update product {product_id} with data: {update_data.model_dump()}"
        )

        command = ProductUpdateCommand(
            product_id=ProductId(product_id), **update_data.model_dump()
        )

        product = await usecase.update_product(command)

        logger.info(f"Product {product_id} updated successfully")
        return ApiResponse.success(product)
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise


@router.delete(
    "/{product_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete a food product",
    description="Permanently remove a food product from the system",
    responses={**delete_product_examples},
)
async def delete_product(
    product_id: UUID = Path(..., description="ID of the product to delete", example=1),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    admin_user=Depends(get_logged_admin_user),
):
    """
    Delete a food product by its ID.

    - **product_id**: The ID of the product to delete
    """
    try:
        logger.info(
            f"Admin {admin_user.get_id()} is attempting to delete product {product_id}"
        )
        await usecase.soft_delete_product(ProductId(product_id))
        return ApiResponse.success(None, "Product successfully deleted")
    except Exception as e:
        raise
