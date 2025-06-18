from fastapi import APIRouter, Depends, Request
from app.users.domain.entities import User
from app.profile.application.dtos import Profile, ProfileUpdate
from .dependencies import GetProfileUseCase, UpdateProfileUseCase
from .dependencies import get_profile_use_case, update_profile_use_case
from app.auth.infrastructure.api.dependencies import get_logged_user
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])

@router.get("/", response_model=Profile)
async def get_my_profile(
    request: Request,
    user: User = Depends(get_logged_user), 
    usecase: GetProfileUseCase = Depends(get_profile_use_case)
):
    logger.info(f"GET profile started | user_id:{user.id} | client:{request.client.host if request.client else None}")
    try:
        profile = usecase.execute(user)
        logger.info(f"GET profile success | user_id:{user.id}")
        return profile
    except Exception as e:
        logger.error(f"GET profile failed | user_id:{user.id} | error:{str(e)}")
        raise

@router.patch("/", response_model=Profile)
async def update_my_profile(
    request: Request,
    update_data: ProfileUpdate,
    user: User = Depends(get_logged_user), 
    usecase: UpdateProfileUseCase = Depends(update_profile_use_case)
):
    logger.info(f"PATCH profile started | user_id:{user.id} | client:{request.client.host if request.client else None}")
    try:
        profile_updated = await usecase.execute(user, update_data)
        logger.info(f"PATCH profile success | user_id:{user.id}")
        return profile_updated
    except Exception as e:
        logger.error(f"PATCH profile failed | user_id:{user.id} | error:{str(e)}")
        raise