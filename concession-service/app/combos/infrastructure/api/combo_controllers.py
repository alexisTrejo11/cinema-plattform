from uuid import UUID
from fastapi import APIRouter, Depends, Path, Query, Request, status

from app.config.rate_limit import limiter
from app.shared.pagination import PaginationQuery
from app.combos.application.use_cases.container import ComboUseCases
from app.combos.application.commands import ComboCreateCommand
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.combos.domain.entities.value_objects import ComboId
from app.products.domain.entities.value_objects import ProductId
from app.config.security import AuthUserContext, require_roles

from .dtos import (
    ComboCreateRequest,
    ComboDetailResponse,
    ComboPaginatedResponse,
)
from .dependencies import get_combos_uc
from .docs_examples import (
    create_combo_examples,
    get_combo_examples,
    list_combos_examples,
    delete_combo_examples,
)

router = APIRouter(prefix="/api/v2/combos", tags=["Combos"])


@router.get(
    "/{combo_id}",
    response_model=ComboDetailResponse,
    summary="Get combo by ID",
    description="Retrieve detailed information about a specific combo",
    responses={**get_combo_examples},
)
@limiter.limit("60/minute")
async def get_combo_by_id(
    request: Request,
    combo_id: UUID = Path(..., description="ID of the combo to retrieve", examples=[1]),
    include_items: bool = Query(
        True,
        description="Whether to include combo items in the response",
        examples=[True],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    query = GetComboByIdQuery(
        combo_id=ComboId(value=combo_id),
        include_items=include_items,
    )
    combo = await usecase.get_combo_by_id(query)
    return ComboDetailResponse.from_domain(combo)


@router.get(
    "/",
    response_model=ComboPaginatedResponse,
    summary="Get active combos",
    description="Retrieve a list of currently available combos",
    responses={**list_combos_examples},
)
@limiter.limit("60/minute")
async def get_active_combos(
    request: Request,
    pagination: PaginationQuery = Depends(),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    combo_page = await usecase.get_active_combos(pagination)

    return ComboPaginatedResponse.from_domain(combo_page)


@router.get(
    "/by-product/{product_id}",
    response_model=ComboPaginatedResponse,
    summary="Get combos containing a product",
    description="Find all combos that include the specified product",
    responses={**list_combos_examples},
)
@limiter.limit("60/minute")
async def get_combos_by_product(
    request: Request,
    product_id: UUID = Path(
        ..., description="ID of the product to search for", examples=[1]
    ),
    include_items: bool = Query(
        False,
        description="Whether to include combo items in the response",
        examples=[True],
    ),
    pagination: PaginationQuery = Depends(),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    query = GetCombosByProductIdQuery(
        product_id=ProductId(value=product_id),
        include_items=include_items,
        pagination=pagination,
    )
    combos_page = await usecase.get_combos_by_product(query)

    return ComboPaginatedResponse.from_domain(combos_page)


@router.post(
    "/",
    response_model=UUID,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new combo",
    description="Creates a new combo meal with the provided details",
    responses={**create_combo_examples},
)
@limiter.limit("10/minute")
async def create_combo(
    request: Request,
    request_data: ComboCreateRequest,
    usecase: ComboUseCases = Depends(get_combos_uc),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = ComboCreateCommand(**request_data.model_dump())
    combo = await usecase.create_combo(command)
    return combo.id.value


# Restore
@router.post(
    "/{combo_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Restore a deleted combo",
    description="Restore a deleted combo",
)
@limiter.limit("10/minute")
async def restore_combo(
    request: Request,
    combo_id: UUID = Path(
        ...,
        description="ID of the combo to restore",
        examples=["c7cdc31d-6682-418a-b9ca-df13a3e85da5"],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    combo_id_obj = ComboId(value=combo_id)
    await usecase.restore_combo(combo_id_obj)


@router.delete(
    "/{combo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a combo",
    description="Remove a combo from the system",
    responses={**delete_combo_examples},
)
@limiter.limit("10/minute")
async def delete_combo(
    request: Request,
    combo_id: UUID = Path(
        ...,
        description="ID of the combo to delete",
        examples=["c7cdc31d-6682-418a-b9ca-df13a3e85da5"],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
    performed_by: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    combo_id_obj = ComboId(value=combo_id)
    await usecase.delete_combo(combo_id_obj)
