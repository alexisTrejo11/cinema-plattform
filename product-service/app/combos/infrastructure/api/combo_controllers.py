from uuid import UUID
from fastapi import APIRouter, Depends, Path, Query, status
from typing import List
import logging

from app.shared.pagination import PaginationQuery
from app.shared.response import ApiResponse
from app.combos.application.response import ComboResponse
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.combos.application.usecase.container import ComboUseCases
from app.combos.domain.entities.value_objects import ComboId
from app.products.domain.entities.value_objects import ProductId


from .dto.request import ComboCreateRequest
from .dto.mapper import RequestDataMapper
from .depedencies import get_combos_uc
from .docs_examples import (
    create_combo_examples,
    get_combo_examples,
    list_combos_examples,
    delete_combo_examples,
)

logger = logging.getLogger("app")

router = APIRouter(prefix="/api/v2/combos", tags=["Combos"])


@router.post(
    "/",
    response_model=ApiResponse[ComboResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new combo",
    description="Creates a new combo meal with the provided details",
    responses={**create_combo_examples},
)
async def create_combo(
    request_data: ComboCreateRequest,
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
        logger.info(f"Creating combo with data: {request_data}")
        command = RequestDataMapper.to_create_combo_command(request_data)

        combo = await usecase.create_combo(command)
        logger.info(f"Combo created successfully: ID{combo.id}")

        return ApiResponse.success(data=combo, message="Combo created successfully")
    except Exception as e:
        logger.error(f"Error creating combo: {e}")
        raise


@router.get(
    "/{combo_id}",
    response_model=ApiResponse[ComboResponse],
    summary="Get combo by ID",
    description="Retrieve detailed information about a specific combo",
    responses={**get_combo_examples},
)
async def get_combo_by_id(
    combo_id: UUID = Path(..., description="ID of the combo to retrieve", example=1),
    pagination: PaginationQuery = Depends(),
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
        logger.info(f"Retrieving combo with ID: {combo_id}")
        query = RequestDataMapper.to_get_combo_by_id_query(
            combo_id, include_items, pagination
        )

        combo = await usecase.get_combo_by_id(query)
        logger.info(f"Combo retrieved successfully: ID{combo.id}")

        return ApiResponse.success(data=combo, message="Combo successfully retrieved")
    except Exception as e:
        logger.error(f"Error retrieving combo: {e}")
        raise


@router.get(
    "/",
    response_model=ApiResponse[List[ComboResponse]],
    summary="List all active combos",
    description="Retrieve a list of all currently available combos",
    responses={**list_combos_examples},
)
async def list_active_combos(
    pagination: PaginationQuery = Depends(),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """Retrieve all combos that are currently marked as available"""
    try:
        logger.info("Listing all active combos")

        combo_list = await usecase.list_active_combos(pagination)
        logger.info(f"Active combos retrieved: {len(combo_list)} found")

        return ApiResponse.success(combo_list, "Active Combos successfully retrieved")
    except Exception as e:
        logger.error(f"Error listing active combos: {e}")
        raise


@router.get(
    "/by-product/{product_id}",
    response_model=ApiResponse[List[ComboResponse]],
    summary="Get combos containing a product",
    description="Find all combos that include the specified product",
    responses={**list_combos_examples},
)
async def get_combos_by_product(
    product_id: UUID = Path(
        ..., description="ID of the product to search for", example=1
    ),
    include_items: bool = Query(
        True, description="Whether to include combo items in the response", example=True
    ),
    pagination: PaginationQuery = Depends(),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Find all combos that contain a specific product.

    - **product_id**: The ID of the product to search for
    - **include_items**: Set to false to exclude item details
    """
    try:
        query = RequestDataMapper.to_get_combos_by_product_query(
            product_id, include_items, pagination
        )
        logger.info(f"Retrieving combos for product ID: {product_id}")

        combo_response = await usecase.get_combos_by_product(query)
        logger.info(f"Combos retrieved successfully for product ID: {product_id}")

        return ApiResponse.success(
            combo_response, "Combos successfully retrieved by product"
        )
    except Exception as e:
        logger.error(f"Error retrieving combos by product: {e}")
        raise


@router.delete(
    "/{combo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a combo",
    description="Soft remove a combo from the system",
    response_model=ApiResponse[None],
    responses={**delete_combo_examples},
)
async def soft_delete_combo(
    combo_id: UUID = Path(
        ...,
        description="ID of the combo to delete",
        example="c7cdc31d-6682-418a-b9ca-df13a3e85da5",
    ),
    usecase: ComboUseCases = Depends(get_combos_uc),
):
    """
    Soft delete a combo by its ID.

    - **combo_id**: The ID of the combo to delete
    """
    try:
        logger.info(f"Soft deleting combo with ID: {combo_id}")

        await usecase.delete_combo(ComboId(combo_id))
        logger.info(f"Combo successfully soft deleted: ID{combo_id}")

        return ApiResponse.success(message="Combo successfully soft deleted")
    except Exception as e:
        logger.error(f"Error deleting combo: {e}")
        raise
