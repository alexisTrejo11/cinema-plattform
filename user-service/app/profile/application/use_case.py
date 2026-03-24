from .dtos import Profile, ProfileUpdate
from app.users.application.repositories import UserRepository
from app.users.domain import User

class GetProfileUseCase:    
    def execute(self, user: User) -> Profile:
        return Profile(joined_date=user.created_at, **user.model_dump())
    
    
class UpdateProfileUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, user: User, update_data: ProfileUpdate) -> Profile:
        user.update_profile(**update_data.model_dump(exclude_unset=True)) 
        user_update = await self.repository.save(user)
        return Profile(joined_date=user.created_at, **user_update.model_dump())