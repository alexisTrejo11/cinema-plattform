from http import HTTPStatus
from fastapi import APIRouter, Depends, Body, Request

from app.config.rate_limit import limiter
from ..dependencies import (
    get_promotion_use_cases,
    PromotionsUseCasesContainer as UseCasesContainer,
)
from .dto import (
    AddProductsToPromotionRequest,
    AddCategoryToPromotionRequest,
    RemoveCategoryFromPromotionRequest,
    RemoveProductsFromPromotionRequest,
)

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
    use_cases: UseCasesContainer = Depends(get_promotion_use_cases),
    request_data: AddProductsToPromotionRequest = Body(
        ..., description="Promotion and product IDs to add"
    ),
):
    command = request_data.to_command()
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
    use_cases: UseCasesContainer = Depends(get_promotion_use_cases),
    body: AddCategoryToPromotionRequest = Body(
        ..., description="Promotion and category to add"
    ),
):
    command = body.to_command()
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
    use_cases: UseCasesContainer = Depends(get_promotion_use_cases),
    request_data: RemoveCategoryFromPromotionRequest = Body(
        ..., description="Promotion and category to remove"
    ),
):
    command = request_data.to_command()
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
    use_cases: UseCasesContainer = Depends(get_promotion_use_cases),
    body: RemoveProductsFromPromotionRequest = Body(
        ..., description="Promotion and product IDs to remove"
    ),
):
    command = body.to_command()
    await use_cases.remove_products_from_promotion(command)
