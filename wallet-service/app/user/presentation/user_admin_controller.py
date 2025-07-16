from uuid import UUID
from typing import List
from pydantic import EmailStr

from fastapi import APIRouter, Depends, status

from app.user.domain.value_objects import UserId
from app.auth.auth_dependencies import get_logged_admin_user, User
from app.user.application.dtos import UserResponse

from .dependencies import get_user_by_id_uc, list_users_uc, get_user_by_email_uc
from .dependencies import GetUserByIdUseCase, ListUsersUseCase, GetUserByEmailUseCase

from app.shared.response import ApiResponse
from app.shared.documentation import common_error_responses

router = APIRouter(prefix="/api/v2/admin/users", tags=["admin"])


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
    summary="Retrieve User by ID (Admin Only)",
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "User successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful User Retrieval",
                            "value": {
                                "message": "User Successfully Retrieved",
                                "data": {
                                    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                                    "email": "testuser@example.com",
                                    "roles": ["user", "admin"],
                                    "is_active": True,
                                    "created_at": "2024-07-15T10:30:00.123456Z",
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def get_user_by_id(
    user_id: UUID,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_uc),
    admin_user: User = Depends(get_logged_admin_user),
):
    """
    Retrieves a single user's detailed information by their unique identifier (UUID).

    This endpoint is restricted to users with administrative privileges.
    The response includes the user's ID, email address, assigned roles,
    account active status, and the timestamp of account creation.

    **Authentication:** A valid Bearer Token from an authenticated admin user is required.
    """
    user = await use_case.execute(UserId(user_id))
    return ApiResponse.success(user, "User Successfully Retrieved")


@router.get(
    "/by-email/{email}",
    response_model=ApiResponse[UserResponse],
    summary="Retrieve User by Email (Admin Only)",
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "User successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful User Retrieval by Email",
                            "value": {
                                "message": "User Successfully Retrieved",
                                "data": {
                                    "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
                                    "email": "anotheruser@example.com",
                                    "roles": ["user", "guest"],
                                    "is_active": False,
                                    "created_at": "2024-07-10T09:15:00.000000Z",
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def get_user_by_email(
    email: EmailStr,
    use_case: GetUserByEmailUseCase = Depends(get_user_by_email_uc),
    admin_user: User = Depends(get_logged_admin_user),
):
    """
    Retrieves a single user's detailed information by their email address.

    This endpoint is restricted to users with administrative privileges.
    The response includes the user's ID, email address, assigned roles,
    account active status, and the timestamp of account creation.

    **Authentication:** A valid Bearer Token from an authenticated admin user is required.
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
