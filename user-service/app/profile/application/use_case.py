from .dtos import Profile, ProfileUpdate
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User

class GetProfileUseCase:    
    def execute(self, user: User) -> Profile:
        return Profile(**user.model_dump())
    
    
class UpdateProfileUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, user: User, update_data: ProfileUpdate) -> Profile:
        user.update_profile(**update_data.model_dump(exclude_unset=True)) 
        user_update = await self.repository.save(user)
        return Profile(**user_update.model_dump())