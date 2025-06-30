from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List
from app.utils.response import ApiResponse
from app.combos.application.dtos import ComboCreate, ComboResponse
from app.combos.application.usecases import (
    ListActiveComboUseCase,
    GetComboByIdUseCase,
    GetCombosByProductUseCase,
    CreateComboUseCase,
    UpdateComboUseCase,
    DeleteComboUseCase
)
from .depedencies import (
    get_list_active_combo_use_case,
    get_combo_by_id_use_case,
    get_combos_by_product_use_case,
    create_combo_use_case,
    update_combo_use_case,
    delete_combo_use_case
)

router = APIRouter(
    prefix="/api/v2/combos",
    tags=["Combos"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid credentials"},
        status.HTTP_403_FORBIDDEN: {"description": "Not authorized to perform this action"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)

@router.post(
    "/",
    response_model=ApiResponse[ComboResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new combo",
    description="Creates a new combo meal with the provided details",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Combo successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Family Feast",
                        "price": 49.99,
                        "items": [
                            {"product_id": 1, "quantity": 2}
                        ]
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {"detail": "Price must be greater than 0"}
                }
            }
        }
    }
)
def create_combo(
    combo_data: ComboCreate,
    usecase: CreateComboUseCase = Depends(create_combo_use_case)
):
    """
    Create a new combo with the following details:
    - **name**: Unique name for the combo (1-200 chars)
    - **price**: Total price (must be positive)
    - **items**: List of products in the combo (1-10 items)
    - **discount_percentage**: Optional discount (0-100)
    """
    try:
        combo = usecase.execute(combo_data)
        return ApiResponse.success(
            data=combo,
            message="Combo created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{combo_id}",
    response_model=ApiResponse[ComboResponse],
    summary="Get combo by ID",
    description="Retrieve detailed information about a specific combo",
    responses={
        status.HTTP_200_OK: {
            "description": "Combo details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Family Feast",
                        "price": 49.99,
                        "items": [
                            {"id": 1, "product_id": 1, "quantity": 2}
                        ]
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Combo not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Combo not found with ID 999"}
                }
            }
        }
    }
)
def get_combo_by_id(
    combo_id: int = Path(..., description="ID of the combo to retrieve", example=1),
    include_items: bool = Query(
        True,
        description="Whether to include combo items in the response",
        example=True
    ),
    usecase: GetComboByIdUseCase = Depends(get_combo_by_id_use_case)
):
    """
    Retrieve a combo by its unique identifier.
    
    - **combo_id**: The ID of the combo to retrieve
    - **include_items**: Set to false to exclude item details
    """
    try:
        combo = usecase.execute(combo_id, include_items)
        return ApiResponse.success(data=combo, message="Combo successfully retrieved")        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=ApiResponse[List[ComboResponse]],
    summary="List all active combos",
    description="Retrieve a list of all currently available combos",
    responses={
        status.HTTP_200_OK: {
            "description": "List of active combos",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Family Feast",
                        "price": 49.99
                    }]
                }
            }
        }
    }
)
def list_active_combos(
    usecase: ListActiveComboUseCase = Depends(get_list_active_combo_use_case)
):
    """Retrieve all combos that are currently marked as available"""
    try:
        combo_list = usecase.execute()
        return ApiResponse.success(data=combo_list, message="Active Combos successfully retrieved")        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/by-product/{product_id}",
    response_model=ApiResponse[List[ComboResponse]],
    summary="Get combos containing a product",
    description="Find all combos that include the specified product",
    responses={
        status.HTTP_200_OK: {
            "description": "List of combos containing the product",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Family Feast",
                        "price": 49.99
                    }]
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid product ID",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid product ID"}
                }
            }
        }
    }
)
def get_combos_by_product(
    product_id: int = Path(..., description="ID of the product to search for", example=1),
    include_items: bool = Query(
        True,
        description="Whether to include combo items in the response",
        example=True
    ),
    usecase: GetCombosByProductUseCase = Depends(get_combos_by_product_use_case)
):
    """
    Find all combos that contain a specific product.
    
    - **product_id**: The ID of the product to search for
    - **include_items**: Set to false to exclude item details
    """
    try:
        return usecase.execute(product_id, include_items)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        

@router.delete(
    "/{combo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a combo",
    description="Permanently remove a combo from the system",
    response_model=ApiResponse[None],
    responses={
        status.HTTP_200_OK: {
            "description": "Combo deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Combo not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Combo not found with ID 999"}
                }
            }
        }
    }
)
def delete_combo(
    combo_id: int = Path(..., description="ID of the combo to delete", example=1),
    usecase: DeleteComboUseCase = Depends(delete_combo_use_case)
):
    """
    Delete a combo by its ID.
    
    - **combo_id**: The ID of the combo to delete
    """
    try:
        usecase.execute(combo_id)
        ApiResponse.success(data=None, message="combo successfuly deleted")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )