from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Path, Query, Request
from http import HTTPStatus

from app.config.rate_limit import limiter
from app.shared.pagination import PaginationQuery
from app.promotions.application.queries.promotion_response import (
    PromotionResponse,
    PromotionSearchResponse,
)
from app.promotions.application.use_cases.promotions_use_cases import PromotionsUseCases
from app.promotions.application.queries.promotion_query import (
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
)
from app.promotions.domain.entities.promotion import PromotionId
from app.products.domain.entities.value_objects import ProductId

from ..dependencies import get_promotion_use_cases
from ..docs.examples import get_promotion_by_id_examples, list_promotions_examples

router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions"])


@router.get(
    "/active",
    status_code=HTTPStatus.OK,
    summary="Get all active promotions",
    description="Retrieves a paginated list of all active promotions.",
    response_model=PromotionSearchResponse,
    responses={**list_promotions_examples},
)
@limiter.limit("60/minute")
async def get_active_promotions(
    request: Request,
    pagination: PaginationQuery = Depends(),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    return await use_cases.get_active_promotions(pagination)


@router.get(
    "/product/{product_id}",
    status_code=HTTPStatus.OK,
    summary="Get promotions by product ID",
    description="Retrieves a paginated list of promotions applicable to a specific product.",
    response_model=PromotionSearchResponse,
    responses={**list_promotions_examples},
)
@limiter.limit("60/minute")
async def get_promotions_by_product(
    request: Request,
    product_id: str = Path(
        ..., description="ID of the product to find promotions for", examples=["prod-456"]
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    pagination_query: PaginationQuery = Depends(),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    query = GetPromotionByProductIdQuery(
        product_id=ProductId.from_string(product_id),
        include_products=include_products,
        pagination=pagination_query,
    )
    return await use_cases.get_promotions_by_product(query)


@router.get(
    "/{promotion_id}",
    status_code=HTTPStatus.OK,
    summary="Get promotion by ID",
    description="Retrieves a single promotion by its unique ID.",
    response_model=PromotionResponse,
    responses={**get_promotion_by_id_examples},
)
@limiter.limit("60/minute")
async def get_promotion_by_id(
    request: Request,
    pagination_query: PaginationQuery = Depends(),
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to retrieve", examples=["promo-123"]
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    query = GetPromotionByIdQuery(
        id=PromotionId(promotion_id),
        include_products=include_products,
        pagination=pagination_query,
    )
    return await use_cases.get_promotion_by_id(query)
