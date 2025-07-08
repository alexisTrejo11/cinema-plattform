from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.application.service.user_service import UserService
from app.application.dtos.user_dtos import UserResponse
from config.dependency_injection import get_user_service, UserService

router = APIRouter(prefix="api/v2/wallet/users")


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID in wallet service, to manually check if some user was create here",
    description="Retrieves a user by their ID.",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    },
)
def get_user(user_id: UUID, user_use_cases: UserService = Depends(get_user_service)):
    """
    Retrieves a user by their ID.
    - **user_id**: The ID of the user to retrieve.
    """
    user = user_use_cases.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
