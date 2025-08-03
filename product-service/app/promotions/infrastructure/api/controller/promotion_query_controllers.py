from uuid import UUID
import logging
from typing import List
from fastapi import APIRouter, Depends, Path, Query
from http import HTTPStatus

from app.shared.pagination import PaginationQuery
from app.shared.response import ApiResponse

from app.promotions.application.queries.promotion_response import PromotionResponse
from app.promotions.application.usecase.promotions_usecases import PromotionsUseCases
from app.promotions.application.queries.promotion_query import (
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
)
from app.promotions.domain.entities.promotion import PromotionId
from app.products.domain.entities.value_objects import ProductId

from ..dependecies import get_promotion_use_cases
from ..docs.examples import get_promotion_by_id_examples, list_promotions_examples

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions"])


@router.get(
    "/active",
    status_code=HTTPStatus.OK,
    summary="Get all active promotions",
    description="Retrieves a paginated list of all active promotions.",
    response_model=ApiResponse[List[PromotionResponse]],
    responses={**list_promotions_examples},
)
async def get_active_promotions(
    pagination: PaginationQuery = Depends(),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Retrieves a list of active promotions with pagination.

    - **page**: The page number to retrieve.
    - **page_size**: The number of promotions per page.
    """
    try:
        logger.info(
            f"Received request to get active promotions with pagination: {pagination}"
        )
        response = await use_cases.get_active_promotions(pagination)

        logger.info(f"Retrieved {len(response.promotions)} active promotions.")
        return ApiResponse.success(
            data=response.promotions,
            message="Active promotions retrieved successfully.",
            metadata={"page": response.paginationMetadata},
        )
    except Exception as e:
        logger.error(f"Error getting active promotions: {e}", exc_info=True)
        raise


@router.get(
    "/{promotion_id}",
    status_code=HTTPStatus.OK,
    summary="Get promotion by ID",
    description="Retrieves a single promotion by its unique ID.",
    response_model=ApiResponse[PromotionResponse],
    responses={**get_promotion_by_id_examples},
)
async def get_promotion_by_id(
    pagination_query: PaginationQuery = Depends(),
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to retrieve", example="promo-123"
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Retrieves a promotion by its ID.

    - **promotion_id**: The ID of the promotion to retrieve.
    - **include_products**: If true, includes product details associated with the promotion.
    """
    try:
        query = GetPromotionByIdQuery(
            id=PromotionId(promotion_id),
            include_products=include_products,
            pagination=pagination_query,
        )

        logger.info(
            f"Received request to get promotion by ID: {promotion_id} (include_products: {include_products})"
        )
        response = await use_cases.get_promotion_by_id(query)

        print(f"Response: {response}")
        logger.info(f"Promotion {promotion_id} retrieved successfully.")
        return ApiResponse.success(
            data=response,
            message="Promotion retrieved successfully.",
        )

    except Exception as e:
        logger.error(f"Error getting promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.get(
    "/product/{product_id}",
    status_code=HTTPStatus.OK,
    summary="Get promotions by product ID",
    description="Retrieves a paginated list of promotions applicable to a specific product.",
    response_model=ApiResponse[List[PromotionResponse]],
    responses={**list_promotions_examples},
)
async def get_promotions_by_product(
    product_id: str = Path(
        ..., description="ID of the product to find promotions for", example="prod-456"
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    pagination_query: PaginationQuery = Depends(),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Retrieves promotions applicable to a specific product with pagination.

    - **product_id**: The ID of the product.
    - **page**: The page number to retrieve.
    - **page_size**: The number of promotions per page.
    """
    try:
        query = GetPromotionByProductIdQuery(
            product_id=ProductId.from_string(product_id),
            include_products=include_products,
            pagination=pagination_query,
        )

        logger.info(
            f"Received request to get promotions for product ID: {product_id} with pagination: {pagination_query}"
        )
        response = await use_cases.get_promotions_by_product(query)

        logger.info(
            f"Retrieved {len(response.promotions)} promotions for product {product_id}."
        )
        return ApiResponse.success(
            data=response.promotions,
            message="Active promotions retrieved successfully.",
            metadata={"page": response.paginationMetadata},
        )
    except Exception as e:
        logger.error(
            f"Error getting promotions for product {product_id}: {e}", exc_info=True
        )
        raise
