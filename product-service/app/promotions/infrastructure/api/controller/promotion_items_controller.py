from uuid import UUID
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from http import HTTPStatus
import logging
from app.products.domain.entities.value_objects import ProductId
from app.shared.response import ApiResponse
from app.promotions.application.command.promotion_result import PromotionCommandResult
from app.promotions.application.queries.promotion_query import PromotionId
from app.promotions.application.usecase.promotions_usecases import PromotionsUseCases
from app.promotions.application.command.add_item_promotion_command import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
)
from ..dependecies import get_promotion_use_cases
from ..docs.examples import (
    create_promotion_examples,
    activate_promotion_examples,
    deactivate_promotion_examples,
    extend_promotion_examples,
)
from .dto.request import (
    PromotionCreateRequest,
    ExtendPromotionRequest,
    PromotionUpdateRequest,
)

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions Items"])


@router.post(
    "/products/",
    response_model=ApiResponse[PromotionId],
    summary="Create a new promotion",
    description="Create a new promotion for a product.",
)
async def add_products_to_promotion(
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    productId: list[UUID] = Body(..., description="ID of the product to add"),
    promotionId: UUID = Body(..., description="ID of the promotion to add products to"),
) -> ApiResponse[PromotionId]:
    command = AddProductsPromotionCommand(
        product_ids=[ProductId(pid) for pid in productId],
        promotion_id=PromotionId(promotionId),
    )

    result: PromotionCommandResult = await use_cases.add_products_to_promotion(command)
    if not result.is_success:
        logger.error(f"Failed to add products to promotion: {result.error}")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.model_dump(),
        )

    return ApiResponse.success(
        data=result.promotion_id, message="Products added to promotion successfully."
    )


@router.post(
    "/categories/",
    response_model=ApiResponse[PromotionId],
    summary="Create a new promotion",
    description="Create a new promotion for a product.",
)
async def add_category_to_promotion(
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    category_id: int = Body(..., description="ID of the category to add"),
    promotionId: UUID = Body(..., description="ID of the promotion to add products to"),
) -> ApiResponse[PromotionId]:
    command = AddCategoryPromotionCommand(
        category_id=category_id,
        promotion_id=PromotionId(promotionId),
    )

    result: PromotionCommandResult = await use_cases.add_category_to_promotion(command)
    if not result.is_success:
        logger.error(f"Failed to add category to promotion: {result.error}")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.model_dump(),
        )

    return ApiResponse.success(
        data=result.promotion_id, message="Category added to promotion successfully."
    )


@router.delete(
    "/categories/",
    response_model=ApiResponse[PromotionId],
    summary="Create a new promotion",
    description="Create a new promotion for a product.",
)
async def remove_category_from_promotion(
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    category_id: int = Body(..., description="ID of the category to remove"),
    promotionId: UUID = Body(
        ..., description="ID of the promotion to remove products from"
    ),
) -> ApiResponse[PromotionId]:
    command = AddCategoryPromotionCommand(
        category_id=category_id,
        promotion_id=PromotionId(promotionId),
    )

    result: PromotionCommandResult = await use_cases.remove_category_from_promotion(
        promotion_id=PromotionId(promotionId), category_id=category_id
    )
    if not result.is_success:
        logger.error(f"Failed to remove category from promotion: {result.error}")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.model_dump(),
        )

    return ApiResponse.success(
        data=result.promotion_id,
        message="Category removed from promotion successfully.",
    )


@router.delete(
    "/categories/",
    response_model=ApiResponse[PromotionId],
    summary="Create a new promotion",
    description="Create a new promotion for a product.",
)
async def remove_products_from_promotion(
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    product_ids: list[UUID] = Body(..., description="IDs of the products to remove"),
    promotionId: UUID = Body(
        ..., description="ID of the promotion to remove products from"
    ),
) -> ApiResponse[PromotionId]:

    result: PromotionCommandResult = await use_cases.remove_products_from_promotion(
        promotion_id=PromotionId(promotionId),
        product_ids=[ProductId(pid) for pid in product_ids],
    )
    if not result.is_success:
        logger.error(f"Failed to remove products from promotion: {result.error}")
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=result.model_dump(),
        )

    return ApiResponse.success(
        data=result.promotion_id,
        message="Category removed from promotion successfully.",
    )
