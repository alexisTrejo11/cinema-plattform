from fastapi import APIRouter, Depends, Request, status, HTTPException
from app.shared.response import ApiResponse, ErrorResponse
from app.auth.infrastructure.api.dependencies import get_logged_user
from app.users.domain.entities import User
from app.profile.application.dtos import ProfileResponse, ProfileUpdate
from .dependencies import GetProfileUseCase, UpdateProfileUseCase
from .dependencies import get_profile_use_case, update_profile_use_case
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/profiles", tags=["User Profiles"]) 

common_profile_error_responses = {
400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid input or business rule violation."},
401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Authentication required or failed (e.g., missing or invalid token)."},
403: {"model": ApiResponse[ErrorResponse], "description": "Forbidden - User does not have the necessary permissions."},
404: {"model": ApiResponse[ErrorResponse], "description": "Not Found - The requested resource was not found."},
500: {"model": ApiResponse[ErrorResponse], "description": "Internal Server Error - An unexpected server error occurred."}
}

@router.get(
    "/",
    response_model=ApiResponse[ProfileResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve the authenticated user's profile",
    description="Fetches the detailed profile information for the currently authenticated user.",
    responses={
        200: {"model": ApiResponse[ProfileResponse], "description": "Successfully retrieved user profile."},
        **common_profile_error_responses
    }
)
async def get_my_profile(
    request: Request,
    user: User = Depends(get_logged_user), 
    usecase: GetProfileUseCase = Depends(get_profile_use_case)
):
    """
    Retrieves the profile of the currently authenticated user.
    """
    logger.info(f"GET profile started | user_id:{user.id} | client:{request.client.host if request.client else None}")
    try:
        profile = usecase.execute(user)
        logger.info(f"GET profile success | user_id:{user.id}")
        return ApiResponse.success(profile, "User profile retrieved successfully.")
    except Exception as e:
        logger.error(f"GET profile failed | user_id:{user.id} | error:{str(e)}")
        raise
    
    
@router.patch(
    "/",
    response_model=ApiResponse[ProfileResponse],
    status_code=status.HTTP_200_OK,
    summary="Update the authenticated user's profile",
    description="Updates specific fields of the currently authenticated user's profile. Partial updates are supported.",
    responses={
        200: {"model": ApiResponse[ProfileResponse], "description": "User profile successfully updated."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid profile data provided."},
        **common_profile_error_responses
    }
)
async def update_my_profile(
    request: Request,
    update_data: ProfileUpdate,
    user: User = Depends(get_logged_user), 
    usecase: UpdateProfileUseCase = Depends(update_profile_use_case)
):
    """
    Updates the profile of the currently authenticated user.
    """
    logger.info(f"PATCH profile started | user_id:{user.id} | client:{request.client.host if request.client else None}")
    try:
        profile_updated = await usecase.execute(user, update_data)
        logger.info(f"PATCH profile success | user_id:{user.id}")
        return ApiResponse.success(profile_updated, "User profile updated successfully.")
    except Exception as e:
        logger.error(f"PATCH profile failed | user_id:{user.id} | error:{str(e)}")
        raise