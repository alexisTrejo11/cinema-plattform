from uuid import UUID
from fastapi import APIRouter, Depends, Body, Request

from app.config.rate_limit import limiter
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.command.add_item_promotion_command import (
    AddProductsPromotionCommand,
    AddCategoryPromotionCommand,
    RemoveCategoryPromotionCommand,
    RemoveProductsPromotionCommand,
)
from app.promotions.application.queries.promotion_query import PromotionId
from app.promotions.application.use_cases.promotions_use_cases import PromotionsUseCases
from http import HTTPStatus

from ..dependencies import get_promotion_use_cases

router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions Items"])


@router.post(
    "/products/add",
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
    summary="Add products to a promotion",
    description="Add products to an existing promotion.",
)
@limiter.limit("10/minute")
async def add_products_to_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    product_ids: list[UUID] = Body(..., description="ID of the product to add"),
    promotion_id: UUID = Body(
        ..., description="ID of the promotion to add products to"
    ),
):

    command = AddProductsPromotionCommand(
        product_ids=[ProductId(value=pid) for pid in product_ids],
        promotion_id=PromotionId(value=promotion_id),
    )

    await use_cases.add_products_to_promotion(command)


@router.post(
    "/categories/add",
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
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
        promotion_id=PromotionId(value=promotionId),
    )
    await use_cases.add_category_to_promotion(command)


@router.delete(
    "/categories/remove",
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
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
        promotion_id=PromotionId(value=promotionId),
    )

    await use_cases.remove_category_from_promotion(command)


@router.delete(
    "/products/remove",
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
    summary="Remove products from a promotion",
    description="Remove products from an existing promotion.",
)
@limiter.limit("10/minute")
async def remove_products_from_promotion(
    request: Request,
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    product_ids: list[UUID] = Body(..., description="IDs of the products to remove"),
    promotion_id: UUID = Body(
        ..., description="ID of the promotion to remove products from"
    ),
):
    command = RemoveProductsPromotionCommand(
        product_ids=[ProductId(value=pid) for pid in product_ids],
        promotion_id=PromotionId(value=promotion_id),
    )

    await use_cases.remove_products_from_promotion(command)
