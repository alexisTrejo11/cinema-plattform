from fastapi import APIRouter, Depends
from app.users.domain.entities import User
from app.users.application.dtos import Profile, ProfileUpdate
from .dependecies import GetProfileUseCase, UpdateProfileUseCase
from .dependecies import get_profile_use_case, update_profile_use_case
from app.auth.infrastructure.api.dependencies import get_logged_user


router = APIRouter(prefix="/api/v1/profiles")

@router.get("/", response_model=Profile)
def get_my_profile(
    user: User = Depends(get_logged_user), 
    usecase: GetProfileUseCase = Depends(get_profile_use_case)
):
    profile = usecase.execute(user)
    return profile

@router.patch("/", response_model=Profile)
async def update_my_profile(
    update_data: ProfileUpdate,
    user: User = Depends(get_logged_user), 
    usecase: UpdateProfileUseCase = Depends(update_profile_use_case)
):
    profile_updated = await usecase.execute(user, update_data)
    return profile_updated

