from uuid import UUID
from fastapi import APIRouter, Depends, Body, Path, Request
from http import HTTPStatus

from app.config.rate_limit import limiter
from app.shared.base_exceptions import DomainException
from app.config.security import require_roles, AuthUserContext
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.use_cases.promotions_use_cases import PromotionsUseCases
from app.promotions.domain.entities.promotion import PromotionId

from ..dependencies import get_promotion_use_cases
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

router = APIRouter(prefix="/api/v2/promotions", tags=["Promotions"])


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    summary="Create a new promotion",
    description="Creates a new promotion in the system.",
    response_model=UUID,
    responses={**create_promotion_examples},
)
@limiter.limit("10/minute")
async def create_promotion(
    request: Request,
    request_data: PromotionCreateRequest = Body(
        ..., description="Details for the new promotion"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = RequestMapper.create_request_to_command(request_data)
    result = await use_cases.create_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_CREATE_ERROR"
        )
    return UUID(result.promotion_id)


@router.patch(
    "/{promotion_id}/activate",
    status_code=HTTPStatus.OK,
    summary="Activate a promotion",
    description="Activates an existing promotion by its ID.",
    responses={**activate_promotion_examples},
)
@limiter.limit("10/minute")
async def activate_promotion(
    request: Request,
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to activate", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    result = await use_cases.activate_promotion(PromotionId(promotion_id))
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_ACTIVATE_ERROR"
        )


@router.patch(
    "/{promotion_id}/deactivate",
    status_code=HTTPStatus.OK,
    summary="Deactivate a promotion",
    description="Deactivates an existing promotion by its ID.",
    responses={**deactivate_promotion_examples},
)
@limiter.limit("10/minute")
async def deactivate_promotion(
    request: Request,
    promotion_id: str = Path(
        ..., description="ID of the promotion to deactivate", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    result = await use_cases.deactivate_promotion(PromotionId.from_string(promotion_id))
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_DEACTIVATE_ERROR"
        )


@router.patch(
    "/extend",
    status_code=HTTPStatus.OK,
    summary="Extend a promotion's end date",
    description="Extends the end date of an existing promotion.",
    responses={**extend_promotion_examples},
)
@limiter.limit("10/minute")
async def extend_promotion(
    request: Request,
    request_data: ExtendPromotionRequest = Body(
        ..., description="Details for extending the promotion"
    ),
    promotion_id: str = Path(
        ..., description="ID of the promotion to extend", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = RequestMapper.extend_request_to_command(request_data)
    result = await use_cases.extend_promotion(command)
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_EXTEND_ERROR"
        )


@router.patch(
    "/{promotion_id}/apply",
    status_code=HTTPStatus.OK,
    summary="Apply a promotion to products",
    description="Applies a promotion to specified products.",
)
@limiter.limit("10/minute")
async def apply_promotion(
    request: Request,
    promotion_id: str = Path(
        ..., description="ID of the promotion to apply", examples=["promo-123"]
    ),
    product_ids: list[str] = Body(
        ..., description="List of product IDs to apply the promotion to"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    result = await use_cases.apply_promotion(
        PromotionId.from_string(promotion_id),
        [ProductId.from_string(pid) for pid in product_ids],
    )
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_APPLY_ERROR"
        )


@router.delete(
    "/{promotion_id}",
    status_code=HTTPStatus.OK,
    summary="Delete a promotion",
    description="Deletes an existing promotion by its ID.",
    responses={HTTPStatus.OK: {"description": "Promotion deleted successfully"}},
)
@limiter.limit("10/minute")
async def delete_promotion(
    request: Request,
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to delete", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    result = await use_cases.delete_promotion(PromotionId(promotion_id))
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_DELETE_ERROR"
        )


@router.patch(
    "/{promotion_id}/clear",
    status_code=HTTPStatus.OK,
    summary="Clear all promotions",
    description="Clears all promotions from the system.",
)
@limiter.limit("10/minute")
async def clear_promotions(
    request: Request,
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to clear", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    admin_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    result = await use_cases.clear_promotions(PromotionId(promotion_id))
    if not result.is_success:
        raise DomainException(
            message=result.message, error_code="PROMOTION_CLEAR_ERROR"
        )
