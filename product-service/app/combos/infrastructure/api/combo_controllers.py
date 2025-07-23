from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List
from app.shared.response import ApiResponse
from app.combos.application.response import ComboResponse
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.combos.application.usecase.container import ComboUseCases
from .depedencies import get_combos_uc
from app.combos.application.commands import ComboCreateComand
from app.combos.domain.entities.value_objects import ComboId
from app.shared.pagination import PaginationQuery
from app.products.domain.entities.value_objects import ProductId

router = APIRouter(
    prefix="/api/v2/combos",
    tags=["Combos"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid credentials"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authorized to perform this action"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)


@router.post(
    "/",
    response_model=ApiResponse[ComboResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new combo",
    description="Creates a new combo meal with the provided details",
)
async def create_combo(
    combo_data: ComboCreateComand,
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Create a new combo with the following details:
    - **name**: Unique name for the combo (1-200 chars)
    - **price**: Total price (must be positive)
    - **items**: List of products in the combo (1-10 items)
    - **discount_percentage**: Optional discount (0-100)
    """
    try:
        combo = await usecase.create_combo(combo_data)
        return ApiResponse.success(data=combo, message="Combo created successfully")
    except Exception as e:

        raise


# TODO: ADD PAGINATION AND FILTERING
@router.get(
    "/{combo_id}",
    response_model=ApiResponse[ComboResponse],
    summary="Get combo by ID",
    description="Retrieve detailed information about a specific combo",
)
async def get_combo_by_id(
    combo_id: UUID = Path(..., description="ID of the combo to retrieve", example=1),
    pagination: PaginationQuery = Depends(),  # TODO: Implement pagination,
    include_items: bool = Query(
        True, description="Whether to include combo items in the response", example=True
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Retrieve a combo by its unique identifier.

    - **combo_id**: The ID of the combo to retrieve
    - **include_items**: Set to false to exclude item details
    """
    try:
        query = GetComboByIdQuery(
            combo_id=ComboId(combo_id),
            include_items=include_items,
            pagination=pagination,
        )
        combo = await usecase.get_combo_by_id(query)
        return ApiResponse.success(data=combo, message="Combo successfully retrieved")
    except Exception as e:
        raise


@router.get(
    "/",
    response_model=ApiResponse[List[ComboResponse]],
    summary="List all active combos",
    description="Retrieve a list of all currently available combos",
)
async def list_active_combos(
    pagination: PaginationQuery = Depends(),  # TODO: Implement pagination
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """Retrieve all combos that are currently marked as available"""
    try:

        combo_list = await usecase.list_active_combos(pagination)
        return ApiResponse.success(
            data=combo_list, message="Active Combos successfully retrieved"
        )
    except Exception as e:
        raise


@router.get(
    "/by-product/{product_id}",
    response_model=ApiResponse[List[ComboResponse]],
    summary="Get combos containing a product",
    description="Find all combos that include the specified product",
)
async def get_combos_by_product(
    product_id: UUID = Path(
        ..., description="ID of the product to search for", example=1
    ),
    include_items: bool = Query(
        True, description="Whether to include combo items in the response", example=True
    ),
    pagination: PaginationQuery = Depends(),  # TODO: Implement pagination
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Find all combos that contain a specific product.

    - **product_id**: The ID of the product to search for
    - **include_items**: Set to false to exclude item details
    """
    try:
        query = GetCombosByProductIdQuery(
            product_id=ProductId(product_id),
            include_items=include_items,
            pagination=pagination,
        )
        return usecase.get_combos_by_product(query)
    except Exception as e:
        raise


@router.delete(
    "/{combo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a combo",
    description="Permanently remove a combo from the system",
    response_model=ApiResponse[None],
)
async def soft_delete_combo(
    combo_id: UUID = Path(..., description="ID of the combo to delete", example=1),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Soft delete a combo by its ID.

    - **combo_id**: The ID of the combo to delete
    """
    try:
        await usecase.delete_combo(ComboId(combo_id))
        ApiResponse.success(data=None, message="combo successfuly soft deleted")
    except Exception as e:
        raise
