from unittest import result
from uuid import UUID
from fastapi import APIRouter, Depends, Body, HTTPException, Path, Query
from http import HTTPStatus
import logging
from app.shared.response import ApiResponse, ErrorResponse
from app.promotions.app.command.promotion_command import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
)
from app.promotions.app.queries.promotion_query import (
    PromotionId,
    GetPromotionByIdQuery,
    GetPromotionByProductIdQuery,
    PaginationQuery,
    ProductId,
)
from app.promotions.app.queries.promotion_response import (
    PromotionResponse,
    PromotionSearchResponse,
)
from app.promotions.app.usecase.promotions_usecases import PromotionsUseCases
from ..dependecies import get_promotion_use_cases

logger = logging.getLogger("app")
router = APIRouter(prefix="/promotions", tags=["Promotions"])


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    summary="Create a new promotion",
    description="Creates a new promotion in the system.",
    # responses={**create_promotion_examples}, # Descomentar y definir tus ejemplos
)
async def create_promotion_endpoint(
    command: PromotionCreateCommand = Body(
        ..., description="Details for the new promotion"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Creates a new promotion.

    - **command**: The data required to create the promotion.
    """
    try:
        logger.info(f"Received request to create promotion: {command.name}")

        result = await use_cases.create_promotion(command)
        if not result.success:
            logger.error(f"Failed to create promotion: {result.message}")
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ApiResponse.failure(result.error_details()),
            )

        logger.info(f"Promotion '{command.name}' created successfully.")
        return ApiResponse.success(
            message=result.message, data={"id": result.promotion_id}
        )
    except Exception as e:
        logger.error(f"Error creating promotion: {e}", exc_info=True)
        raise


@router.put(
    "/{promotion_id}/activate",
    status_code=HTTPStatus.OK,
    summary="Activate a promotion",
    description="Activates an existing promotion by its ID.",
    # responses={**activate_promotion_examples},
)
async def activate_promotion_endpoint(
    promotion_id: PromotionId = Path(
        ..., description="ID of the promotion to activate", example="promo-123"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Activates a promotion by its ID.

    - **promotion_id**: The ID of the promotion to activate.
    """
    try:
        logger.info(f"Received request to activate promotion ID: {promotion_id}")
        result = await use_cases.activate_promotion(promotion_id)
        if not result.success:
            logger.error(
                f"Failed to activate promotion {promotion_id}: {result.message}"
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ApiResponse.failure(result.error_details()),
            )

        logger.info(f"Promotion {promotion_id} activated successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error activating promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.put(
    "/{promotion_id}/deactivate",
    status_code=HTTPStatus.OK,
    summary="Deactivate a promotion",
    description="Deactivates an existing promotion by its ID.",
    # responses={**deactivate_promotion_examples},
)
async def deactivate_promotion_endpoint(
    promotion_id: PromotionId = Path(
        ..., description="ID of the promotion to deactivate", example="promo-123"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Deactivates a promotion by its ID.

    - **promotion_id**: The ID of the promotion to deactivate.
    """
    try:
        logger.info(f"Received request to deactivate promotion ID: {promotion_id}")

        result = await use_cases.deactivate_promotion(promotion_id)
        if not result.success:
            logger.error(
                f"Failed to deactivate promotion {promotion_id}: {result.message}"
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ApiResponse.failure(result.error_details()),
            )

        logger.info(f"Promotion {promotion_id} deactivated successfully.")
        return ApiResponse.success(message=result.message)

    except Exception as e:
        logger.error(f"Error deactivating promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.put(
    "/extend",
    status_code=HTTPStatus.OK,
    summary="Extend a promotion's end date",
    description="Extends the end date of an existing promotion.",
    # responses={**extend_promotion_examples},
)
async def extend_promotion_endpoint(
    command: ExtendPromotionCommand = Body(
        ..., description="Details for extending the promotion"
    ),
    promotion_id: str = Path(
        ..., description="ID of the promotion to extend", example="promo-123"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Extends a promotion's end date.

    - **command**: The data required to extend the promotion.
    """
    try:
        logger.info(f"Received request to extend promotion ID: {promotion_id}")
        command.id = PromotionId.from_string(promotion_id)

        result = await use_cases.extend_promotion(command)
        if not result.success:
            logger.error(f"Failed to extend promotion {promotion_id}: {result.message}")
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ApiResponse.failure(result.error_details()),
            )

        logger.info(f"Promotion {result.promotion_id} extended successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error extending promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.get(
    "/active",
    status_code=HTTPStatus.OK,
    summary="Get all active promotions",
    description="Retrieves a paginated list of all active promotions.",
    # responses={**get_active_promotions_examples},
)
async def get_active_promotions_endpoint(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
) -> PromotionSearchResponse:
    """
    Retrieves a list of active promotions with pagination.

    - **page**: The page number to retrieve.
    - **page_size**: The number of promotions per page.
    """
    try:
        pagination_query = PaginationQuery(page=page, page_size=page_size)
        logger.info(
            f"Received request to get active promotions with pagination: {pagination_query}"
        )
        response = await use_cases.get_active_promotions(pagination_query)

        logger.info(f"Retrieved {len(response.promotions)} active promotions.")
        return response
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
    promotion_id: PromotionId = Path(
        ..., description="ID of the promotion to retrieve", example="promo-123"
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
) -> PromotionResponse:
    """
    Retrieves a promotion by its ID.

    - **promotion_id**: The ID of the promotion to retrieve.
    - **include_products**: If true, includes product details associated with the promotion.
    """
    try:
        query = GetPromotionByIdQuery(
            id=promotion_id, include_products=include_products
        )
        logger.info(
            f"Received request to get promotion by ID: {promotion_id} (include_products: {include_products})"
        )
        response = await use_cases.get_promotion_by_id(query)

        logger.info(f"Promotion {promotion_id} retrieved successfully.")
        return response

    except Exception as e:
        logger.error(f"Error getting promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.get(
    "/product/{product_id}",
    status_code=HTTPStatus.OK,
    summary="Get promotions by product ID",
    description="Retrieves a paginated list of promotions applicable to a specific product.",
    # responses={**get_promotions_by_product_examples},
)
async def get_promotions_by_product_endpoint(
    product_id: ProductId = Path(
        ..., description="ID of the product to find promotions for", example="prod-456"
    ),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
) -> PromotionSearchResponse:
    """
    Retrieves promotions applicable to a specific product with pagination.

    - **product_id**: The ID of the product.
    - **page**: The page number to retrieve.
    - **page_size**: The number of promotions per page.
    """
    try:
        pagination_query = PaginationQuery(
            offset=page,
            limit=page_size,
        )
        query = GetPromotionByProductIdQuery(
            product_id=product_id, pagination=pagination_query
        )

        logger.info(
            f"Received request to get promotions for product ID: {product_id} with pagination: {pagination_query}"
        )
        response = await use_cases.get_promotions_by_product(query)

        logger.info(
            f"Retrieved {len(response.promotions)} promotions for product {product_id}."
        )
        return response
    except Exception as e:
        logger.error(
            f"Error getting promotions for product {product_id}: {e}", exc_info=True
        )
        raise
