from uuid import UUID
from fastapi import APIRouter, Depends, Body, Request

from app.config.rate_limit import limiter
from app.shared.base_exceptions import DomainException
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.command.add_item_promotion_command import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)
from app.promotions.application.queries.promotion_query import PromotionId
from app.promotions.application.use_cases.promotions_use_cases import PromotionsUseCases

from ..dependencies import get_promotion_use_cases

router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions Items"])


@router.post(
    "/products/add",
    response_model=UUID,
    summary="Add products to a promotion",
    description="Add products to an existing promotion.",
)
@limiter.limit("10/minute")
async def add_products_to_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    productId: list[UUID] = Body(..., description="ID of the product to add"),
    promotionId: UUID = Body(..., description="ID of the promotion to add products to"),
):
    command = AddProductsPromotionCommand(
        product_ids=[ProductId(pid) for pid in productId],
        promotion_id=PromotionId(promotionId),
    )
    result = await use_cases.add_products_to_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_ADD_PRODUCTS_ERROR"
        )
    return UUID(result.promotion_id)


@router.post(
    "/categories/add",
    response_model=UUID,
    summary="Add category to a promotion",
    description="Add a category to an existing promotion.",
)
@limiter.limit("10/minute")
async def add_category_to_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    category_id: int = Body(..., description="ID of the category to add"),
    promotionId: UUID = Body(..., description="ID of the promotion to add products to"),
):
    command = AddCategoryPromotionCommand(
        category_id=category_id,
        promotion_id=PromotionId(promotionId),
    )
    result = await use_cases.add_category_to_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_ADD_CATEGORY_ERROR"
        )
    return UUID(result.promotion_id)


@router.delete(
    "/categories/remove",
    response_model=UUID,
    summary="Remove category from a promotion",
    description="Remove a category from an existing promotion.",
)
@limiter.limit("10/minute")
async def remove_category_from_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    category_id: int = Body(..., description="ID of the category to remove"),
    promotionId: UUID = Body(
        ..., description="ID of the promotion to remove products from"
    ),
):
    command = RemoveCategoryPromotionCommand(
        category_id=category_id,
        promotion_id=PromotionId(promotionId),
    )
    result = await use_cases.remove_category_from_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_REMOVE_CATEGORY_ERROR"
        )
    return UUID(result.promotion_id)


@router.delete(
    "/products/remove",
    response_model=UUID,
    summary="Remove products from a promotion",
    description="Remove products from an existing promotion.",
)
@limiter.limit("10/minute")
async def remove_products_from_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    product_ids: list[UUID] = Body(..., description="IDs of the products to remove"),
    promotionId: UUID = Body(
        ..., description="ID of the promotion to remove products from"
    ),
):
    command = RemoveProductsPromotionCommand(
        product_ids=[ProductId(pid) for pid in product_ids],
        promotion_id=PromotionId(promotionId),
    )
    result = await use_cases.remove_products_from_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_REMOVE_PRODUCTS_ERROR"
        )
    return UUID(result.promotion_id)
