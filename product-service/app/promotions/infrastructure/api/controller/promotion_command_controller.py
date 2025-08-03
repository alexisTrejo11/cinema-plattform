import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from http import HTTPStatus

from app.shared.response import ApiResponse
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.usecase.promotions_usecases import PromotionsUseCases
from app.promotions.domain.entities.promotion import PromotionId

from ..dependecies import get_promotion_use_cases
from ..docs.examples import (
    create_promotion_examples,
    activate_promotion_examples,
    deactivate_promotion_examples,
    extend_promotion_examples,
)
from .dto.mapper import RequestMapper
from .dto.request import (
    PromotionCreateRequest,
    ExtendPromotionRequest,
)

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions"])


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    summary="Create a new promotion",
    description="Creates a new promotion in the system.",
    response_model=ApiResponse[UUID],
    responses={**create_promotion_examples},
)
async def create_promotion(
    request: PromotionCreateRequest = Body(
        ..., description="Details for the new promotion"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Creates a new promotion.

    - **command**: The data required to create the promotion.
    """
    try:
        logger.info(f"Received request to create promotion: {request.name}")
        command = RequestMapper.create_request_to_command(request)

        result = await use_cases.create_promotion(command)
        if not result.is_success:
            logger.error(f"Failed to create promotion: {result.message}")
            raise_response_error(result)

        logger.info(f"Promotion '{command.name}' created successfully.")
        return ApiResponse.success(message=result.message, data=result.promotion_id)
    except Exception as e:
        logger.error(f"Error creating promotion: {e}", exc_info=True)
        raise


@router.patch(
    "/{promotion_id}/activate",
    status_code=HTTPStatus.OK,
    summary="Activate a promotion",
    description="Activates an existing promotion by its ID.",
    response_model=ApiResponse[None],
    responses={**activate_promotion_examples},
)
async def activate_promotion(
    promotion_id: UUID = Path(
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

        result = await use_cases.activate_promotion(PromotionId(promotion_id))
        if not result.is_success:
            logger.error(
                f"Failed to activate promotion {promotion_id}: {result.message}"
            )
            raise_response_error(result)

        logger.info(f"Promotion {promotion_id} activated successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error activating promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.patch(
    "/{promotion_id}/deactivate",
    status_code=HTTPStatus.OK,
    summary="Deactivate a promotion",
    description="Deactivates an existing promotion by its ID.",
    response_model=ApiResponse[None],
    responses={**deactivate_promotion_examples},
)
async def deactivate_promotion(
    promotion_id: str = Path(
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

        result = await use_cases.deactivate_promotion(
            PromotionId.from_string(promotion_id)
        )

        if not result.is_success:
            logger.error(
                f"Failed to deactivate promotion {promotion_id}: {result.message}"
            )
            raise_response_error(result)

        logger.info(f"Promotion {promotion_id} deactivated successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error deactivating promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.patch(
    "/extend",
    status_code=HTTPStatus.OK,
    summary="Extend a promotion's end date",
    description="Extends the end date of an existing promotion.",
    response_model=ApiResponse[None],
    responses={**extend_promotion_examples},
)
async def extend_promotion(
    request: ExtendPromotionRequest = Body(
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
        command = RequestMapper.extend_request_to_command(request)

        result = await use_cases.extend_promotion(command)
        if not result.is_success:
            logger.error(f"Failed to extend promotion {promotion_id}: {result.message}")
            raise_response_error(result)

        logger.info(f"Promotion {result.promotion_id} extended successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error extending promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.patch(
    "/{promotion_id}/apply",
    status_code=HTTPStatus.OK,
    summary="Apply a promotion to products",
    description="Applies a promotion to specified products.",
    response_model=ApiResponse[None],
)
async def apply_promotion(
    promotion_id: str = Path(
        ..., description="ID of the promotion to apply", example="promo-123"
    ),
    product_ids: list[str] = Body(
        ..., description="List of product IDs to apply the promotion to"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """Applies a promotion to specified products.
    - **promotion_id**: The ID of the promotion to apply.
    - **product_ids**: List of product IDs to which the promotion will be applied.
    """
    try:
        logger.info(
            f"Received request to apply promotion {promotion_id} to products: {product_ids}"
        )

        result = await use_cases.apply_promotion(
            PromotionId.from_string(promotion_id),
            [ProductId.from_string(pid) for pid in product_ids],
        )

        if not result.is_success:
            logger.error(f"Failed to apply promotion {promotion_id}: {result.message}")
            raise_response_error(result)

        logger.info(f"Promotion {promotion_id} applied successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error applying promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.delete(
    "/{promotion_id}",
    status_code=HTTPStatus.OK,
    summary="Delete a promotion",
    description="Deletes an existing promotion by its ID.",
    responses={HTTPStatus.OK: {"description": "Promotion deleted successfully"}},
)
async def delete_promotion(
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to delete", example="promo-123"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    """
    Deletes a promotion by its ID.

    - **promotion_id**: The ID of the promotion to delete.
    """
    try:
        logger.info(f"Received request to delete promotion ID: {promotion_id}")
        result = await use_cases.delete_promotion(PromotionId(promotion_id))
        if not result.is_success:
            logger.error(f"Failed to delete promotion {promotion_id}: {result.message}")
            raise_response_error(result)

        logger.info(f"Promotion {promotion_id} deleted successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error deleting promotion {promotion_id}: {e}", exc_info=True)
        raise


@router.patch(
    "{promotion_id}/clear",
    status_code=HTTPStatus.OK,
    summary="Clear all promotions",
    description="Clears all promotions from the system.",
)
async def clear_promotions(
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to clear", example="promo-123"
    ),
):
    """Clears all promotions from the system."""
    try:
        logger.info("Received request to clear all promotions.")
        result = await use_cases.clear_promotions(PromotionId(promotion_id))
        if not result.is_success:
            logger.error(f"Failed to clear promotions: {result.message}")
            raise_response_error(result)

        logger.info("All promotions cleared successfully.")
        return ApiResponse.success(message=result.message)
    except Exception as e:
        logger.error(f"Error clearing promotions: {e}", exc_info=True)
        raise


def raise_response_error(result) -> None:
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=ApiResponse.failure(
            error=result.to_error_response(), message="Promotion operation failed"
        ).model_dump(),
    )
