from uuid import UUID
from fastapi import APIRouter, Depends, Path, Query, Request, status
from typing import List

from app.config.rate_limit import limiter
from app.shared.pagination import PaginationQuery
from app.combos.application.response import ComboResponse, ComboListResponse
from app.combos.application.use_cases.container import ComboUseCases
from app.combos.domain.entities.value_objects import ComboId
from app.config.security import AuthUserContext, require_roles

from .dto.request import ComboCreateRequest
from .dto.mapper import RequestDataMapper
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
    response_model=ComboResponse,
    summary="Get combo by ID",
    description="Retrieve detailed information about a specific combo",
    responses={**get_combo_examples},
)
@limiter.limit("60/minute")
async def get_combo_by_id(
    request: Request,
    combo_id: UUID = Path(..., description="ID of the combo to retrieve", examples=[1]),
    pagination: PaginationQuery = Depends(),
    include_items: bool = Query(
        False,
        description="Whether to include combo items in the response",
        examples=[True],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    query = RequestDataMapper.to_get_combo_by_id_query(
        combo_id, include_items, pagination
    )
    return await usecase.get_combo_by_id(query)


@router.get(
    "/",
    response_model=ComboListResponse,
    summary="List all active combos",
    description="Retrieve a list of all currently available combos",
    responses={**list_combos_examples},
)
@limiter.limit("60/minute")
async def list_active_combos(
    request: Request,
    pagination: PaginationQuery = Depends(),
    include_items: bool = Query(
        False,
        description="Whether to include combo items in the response",
        examples=[True],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    combo_page = await usecase.list_active_combos(pagination, include_items)
    return ComboListResponse(items=combo_page.items, metadata=combo_page.metadata)


@router.get(
    "/by-product/{product_id}",
    response_model=ComboListResponse,
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
    query = RequestDataMapper.to_get_combos_by_product_query(
        product_id, include_items, pagination
    )
    combo_page = await usecase.get_combos_by_product(query)
    return ComboListResponse(items=combo_page.items, metadata=combo_page.metadata)


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
    staff_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    command = RequestDataMapper.to_create_combo_command(request_data)
    result = await usecase.create_combo(command)
    return UUID(result.combo_id)


@router.delete(
    "/{combo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a combo",
    description="Soft remove a combo from the system",
    responses={**delete_combo_examples},
)
@limiter.limit("10/minute")
async def soft_delete_combo(
    request: Request,
    combo_id: UUID = Path(
        ...,
        description="ID of the combo to delete",
        examples=["c7cdc31d-6682-418a-b9ca-df13a3e85da5"],
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
    staff_user: AuthUserContext = Depends(require_roles("admin", "manager")),
):
    await usecase.delete_combo(ComboId(combo_id))
