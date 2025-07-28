from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Path, Query
from http import HTTPStatus
import logging
from app.promotions.application.queries.promotion_query import (
    PromotionId,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
    PaginationQuery,
    ProductId,
)
from app.promotions.application.queries.promotion_response import (
    PromotionResponse,
    PromotionSearchResponse,
)
from app.promotions.application.usecase.promotions_usecases import PromotionsUseCases
from app.shared.response import ApiResponse
from ..dependecies import get_promotion_use_cases

logger = logging.getLogger("app")
router = APIRouter(prefix="/promotions", tags=["Promotions"])


@router.get(
    "/active",
    status_code=HTTPStatus.OK,
    summary="Get all active promotions",
    description="Retrieves a paginated list of all active promotions.",
    response_model=ApiResponse[List[PromotionSearchResponse]],
    # responses={**get_active_promotions_examples},
)
async def get_active_promotions_endpoint(
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
    # responses={**get_promotion_by_id_examples},
)
async def get_promotion_by_id_endpoint(
    pagination_query: PaginationQuery = Depends(),
    promotion_id: PromotionId = Path(
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
            id=promotion_id,
            include_products=include_products,
            pagination=pagination_query,
        )

        logger.info(
            f"Received request to get promotion by ID: {promotion_id} (include_products: {include_products})"
        )
        response = await use_cases.get_promotion_by_id(query)

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
    # responses={**get_promotions_by_product_examples},
)
async def get_promotions_by_product_endpoint(
    product_id: UUID = Path(
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
            product_id=ProductId(product_id),
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
