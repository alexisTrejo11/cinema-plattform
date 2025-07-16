from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from app.user.domain.value_objects import UserId
from app.user.application.dtos import UserResponse
from pydantic import EmailStr
from .dependencies import get_user_by_id_uc, list_users_uc, get_user_by_email_uc
from .dependencies import GetUserByIdUseCase, ListUsersUseCase, GetUserByEmailUseCase
from app.shared.response import ApiResponse
from app.auth.auth_dependencies import get_logged_admin_user, User

router = APIRouter(prefix="/api/v2/admin/users", tags=["admin"])


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user_by_id(
    user_id: UUID, 
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_uc),
    admin_user: User = Depends(get_logged_admin_user),
):
    """
    Retrieve a user by their ID.
    """
    user = await use_case.execute(UserId(user_id))
    return ApiResponse.success(user, "User Successfully Retrieved")


@router.get("/email/{email}", response_model=ApiResponse[UserResponse])
async def get_user_by_email(
    email: EmailStr, 
    use_case: GetUserByEmailUseCase = Depends(get_user_by_email_uc),
    admin_user: User = Depends(get_logged_admin_user),
):
    """
    Retrieve a user by their email.
    """
    user = await use_case.execute(str(email))
    return ApiResponse.success(user, "User Successfully Retrieved")


@router.get("/", response_model=List[ApiResponse[UserResponse]])
async def list_users(
    use_case: ListUsersUseCase = Depends(list_users_uc),
    admin_user: User = Depends(get_logged_admin_user),
):
    """
    List all users.
    """
    users = await use_case.execute({})
    return ApiResponse.success(users, "User List Successfully Retrieved")
