from fastapi import APIRouter, Depends, Path, Request, status
from uuid import UUID

from app.config.rate_limit import limiter
from app.config.security import require_roles, AuthUserContext
from app.products.domain.entities.value_objects import ProductId
from app.products.application.commands import ProductUpdateCommand, ProductCreateCommand
from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery
from app.shared.pagination import PaginationQuery, SortOrder as PaginationSortOrder
from app.products.infrastructure.api.dtos import (
    ProductResponse,
    ProductPaginatedResponse,
)
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


def _search_products_query_from_request(q: ProductSearchQuery) -> SearchProductsQuery:
    limit = max(1, q.limit)
    offset = max(0, q.offset)
    page_num = (offset // limit) + 1
    return SearchProductsQuery(
        page=PaginationQuery(
            page=page_num,
            page_size=limit,
            sort_by=q.sort_by.value,
            sort_order=PaginationSortOrder(q.sort_order.value),
        ),
        min_price=q.min_price,
        max_price=q.max_price,
        name=q.name_like,
        category=q.category_id,
        active_only=q.available_only,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
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
    product_id_obj = ProductId(value=product_id)
    query = GetProductByIdQuery(product_id=product_id_obj)

    product = await usecase.get_product_by_id(query)

    return ProductResponse.from_entity(product)


@router.get(
    "/",
    response_model=ProductPaginatedResponse,
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
    params = _search_products_query_from_request(search_params)
    return await usecase.search_products(params)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new food product",
    description="Creates a new food product with the provided details",
    responses={**create_product_examples},
)
@limiter.limit("10/minute")
async def create_product(
    request: Request,
    product_data: CreateProductRequest,
    perfomed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
    usecase: ProductUseCases = Depends(get_product_use_cases),
):
    command = ProductCreateCommand(**product_data.model_dump())
    product = await usecase.create_product(command)
    return ProductResponse.from_entity(product)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a food product",
    description="Update details of an existing food product",
    responses={**create_update_examples},
)
@limiter.limit("10/minute")
async def update_product(
    request: Request,
    update_data: UpdateProductRequest,
    product_id: UUID = Path(
        ..., description="ID of the product to update", examples=[1]
    ),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    perfomed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    product_id_obj = ProductId(value=product_id)
    command = ProductUpdateCommand(
        product_id=product_id_obj, **update_data.model_dump()
    )
    product = await usecase.update_product(command)
    return ProductResponse.from_entity(product)


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
    product_id: UUID = Path(
        ..., description="ID of the product to delete", examples=[1]
    ),
    usecase: ProductUseCases = Depends(get_product_use_cases),
    perfomed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    product_id_obj = ProductId(value=product_id)
    await usecase.delete_product(product_id_obj)
