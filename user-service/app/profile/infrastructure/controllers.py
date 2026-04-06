from fastapi import APIRouter, Depends, status

from app.auth.infrastructure.api.dependencies import get_logged_user
from app.shared.response import ErrorResponse
from app.users.domain import User
from app.profile.application.dtos import ProfileResponse, ProfileUpdate
from .dependencies import GetProfileUseCase, UpdateProfileUseCase
from .dependencies import get_profile_use_case, update_profile_use_case

router = APIRouter(prefix="/api/v2/profiles", tags=["User Profiles"])

common_profile_error_responses = {
    400: {
        "model": ErrorResponse,
        "description": "Bad Request - Invalid input or business rule violation.",
    },
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized - Authentication required or failed (e.g., missing or invalid token).",
    },
    403: {
        "model": ErrorResponse,
        "description": "Forbidden - User does not have the necessary permissions.",
    },
    404: {
        "model": ErrorResponse,
        "description": "Not Found - The requested resource was not found.",
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal Server Error - An unexpected server error occurred.",
    },
}


@router.get(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve the authenticated user's profile",
    description="Fetches the detailed profile information for the currently authenticated user.",
    responses={
        200: {
            "model": ProfileResponse,
            "description": "Successfully retrieved user profile.",
        },
        **common_profile_error_responses,
    },
)
async def get_my_profile(
    user: User = Depends(get_logged_user),
    usecase: GetProfileUseCase = Depends(get_profile_use_case),
) -> ProfileResponse:
    """Retrieves the profile of the currently authenticated user."""
    return usecase.execute(user)


@router.patch(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update the authenticated user's profile",
    description="Updates specific fields of the currently authenticated user's profile. Partial updates are supported.",
    responses={
        200: {
            "model": ProfileResponse,
            "description": "User profile successfully updated.",
        },
        400: {
            "model": ErrorResponse,
            "description": "Bad Request - Invalid profile data provided.",
        },
        **common_profile_error_responses,
    },
)
async def update_my_profile(
    update_data: ProfileUpdate,
    user: User = Depends(get_logged_user),
    usecase: UpdateProfileUseCase = Depends(update_profile_use_case),
) -> ProfileResponse:
    """Updates the profile of the currently authenticated user."""
    return await usecase.execute(user, update_data)
