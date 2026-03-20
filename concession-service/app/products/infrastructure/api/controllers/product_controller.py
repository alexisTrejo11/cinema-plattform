from fastapi import APIRouter, Depends, Path, Request, status
from uuid import UUID
from typing import List

from app.config.rate_limit import limiter
from app.config.security import require_roles, AuthUserContext
from app.products.domain.entities.value_objects import ProductId
from app.products.application.commands import ProductUpdateCommand, ProductCreateCommand
from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery
from app.products.application.responses import ProductDetails, ProductSearchResponse
from app.products.application.use_cases.container import ProductUseCases

from ..dependencies import get_product_use_cases
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

router = APIRouter(prefix="/api/v2/products", tags=["Food Products"])


@router.get(
    "/{product_id}",
    response_model=ProductDetails,
    summary="Get product by ID",
    description="Retrieve detailed information about a specific food product",
    responses={**get_product_examples},
)
@limiter.limit("60/minute")
async def get_product_by_id(
    request: Request,
    product_id: UUID = Path(
        ...,
        description="ID of the product to retrieve",
        examples=["75bb2bef-953f-47b2-8e48-6f3101515ebe"],
    ),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    query = GetProductByIdQuery(product_id=ProductId(product_id))
    return await usecase.get_product_by_id(query)


@router.get(
    "/",
    response_model=ProductSearchResponse,
    summary="Search food products",
    description="Search and filter food products with pagination",
    responses={**search_products_examples},
)
@limiter.limit("60/minute")
async def search_products(
    request: Request,
    search_params: ProductSearchQuery = Depends(),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    params = SearchProductsQuery(**search_params.model_dump())
    response = await usecase.search_products(params)
    return ProductSearchResponse(
        product_page=response.product_page,
        metadata=response.metadata,
    )


@router.post(
    "/",
    response_model=ProductDetails,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food product",
    description="Creates a new food product with the provided details",
    responses={**create_product_examples},
)
@limiter.limit("10/minute")
async def create_product(
    request: Request,
    product_data: CreateProductRequest,
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    command = ProductCreateCommand(**product_data.model_dump())
    return await usecase.create_product(command)


@router.patch(
    "/{product_id}",
    response_model=ProductDetails,
    summary="Update a food product",
    description="Update details of an existing food product",
    responses={**create_update_examples},
)
@limiter.limit("10/minute")
async def update_product(
    request: Request,
    update_data: UpdateProductRequest,
    product_id: UUID = Path(..., description="ID of the product to update", examples=[1]),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = ProductUpdateCommand(
        product_id=ProductId(product_id), **update_data.model_dump()
    )
    return await usecase.update_product(command)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a food product",
    description="Permanently remove a food product from the system",
    responses={**delete_product_examples},
)
@limiter.limit("10/minute")
async def delete_product(
    request: Request,
    product_id: UUID = Path(..., description="ID of the product to delete", examples=[1]),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    await usecase.soft_delete_product(ProductId(product_id))
