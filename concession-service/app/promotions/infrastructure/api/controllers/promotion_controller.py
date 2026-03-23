from uuid import UUID
from fastapi import APIRouter, Depends, Body, Path, Request, Query

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
from http import HTTPStatus

from app.config.rate_limit import limiter
from app.shared.base_exceptions import DomainException
from app.config.security import require_roles, AuthUserContext
from app.products.domain.entities.value_objects import ProductId
from app.promotions.application.command.promotion_command import (
    ExtendPromotionCommand,
    PromotionCreateCommand,
)
from ..dependencies import get_promotion_use_cases
from ..docs.examples import (
    get_promotion_by_id_examples,
    list_promotions_examples,
    create_promotion_examples,
    activate_promotion_examples,
    deactivate_promotion_examples,
    extend_promotion_examples,
)
from app.promotions.application.use_cases.promotions_use_cases import PromotionsUseCases
from app.promotions.domain.entities.promotion import PromotionId
from .dto.request import (
    PromotionCreateRequest,
    ExtendPromotionRequest,
)

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
    product_id: UUID = Path(
        ...,
        description="ID of the product to find promotions for",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    ),
    include_products: bool = Query(
        False, description="Whether to include associated product details"
    ),
    pagination_query: PaginationQuery = Depends(),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    query = GetPromotionByProductIdQuery(
        product_id=ProductId(value=product_id),
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
        id=PromotionId(value=promotion_id),
        include_products=include_products,
        pagination=pagination_query,
    )

    return await use_cases.get_promotion_by_id(query)


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
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = request_data.to_command()
    promotion = await use_cases.create_promotion(command)

    return promotion.id.value


@router.patch(
    "/{promotion_id}/activate",
    status_code=HTTPStatus.NO_CONTENT,
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
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):

    promotion_id_obj = PromotionId(value=promotion_id)
    await use_cases.activate_promotion(promotion_id_obj)


@router.patch(
    "/{promotion_id}/deactivate",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Deactivate a promotion",
    description="Deactivates an existing promotion by its ID.",
    responses={**deactivate_promotion_examples},
)
@limiter.limit("10/minute")
async def deactivate_promotion(
    request: Request,
    promotion_id: UUID = Path(
        ...,
        description="ID of the promotion to deactivate",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    promotion_id_obj = PromotionId(value=promotion_id)
    await use_cases.deactivate_promotion(promotion_id_obj)


@router.patch(
    "/{promotion_id}/extend",
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
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to extend", examples=["promo-123"]
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    extend_command = request_data.to_command(promotion_id)
    await use_cases.extend_promotion(extend_command)


@router.patch(
    "/{promotion_id}/apply",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Apply a promotion to products",
    description="Applies a promotion to specified products.",
)
@limiter.limit("10/minute")
async def apply_promotion(
    request: Request,
    promotion_id: UUID = Path(
        ..., description="ID of the promotion to apply", examples=["promo-123"]
    ),
    product_ids: list[UUID] = Body(
        ..., description="List of product IDs to apply the promotion to"
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
):
    promotion_id_obj = PromotionId(value=promotion_id)
    product_ids_obj = [ProductId(value=pid) for pid in product_ids]

    await use_cases.apply_promotion(promotion_id_obj, product_ids_obj)


@router.delete(
    "/{promotion_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Delete a promotion",
    description="Deletes an existing promotion by its ID.",
    response_model=None,
)
@limiter.limit("10/minute")
async def delete_promotion(
    request: Request,
    promotion_id: UUID = Path(
        ...,
        description="ID of the promotion to delete",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    ),
    use_cases: PromotionsUseCases = Depends(get_promotion_use_cases),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    promotion_id_obj = PromotionId(value=promotion_id)
    await use_cases.delete_promotion(promotion_id_obj)


@router.patch(
    "/{promotion_id}/clear",
    status_code=HTTPStatus.NO_CONTENT,
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
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    promotion_id_obj = PromotionId(value=promotion_id)
    await use_cases.clear_promotions(promotion_id_obj)
