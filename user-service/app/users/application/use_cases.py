from app.users.application.dtos import UserResponse, UserCreate, UserUpdate
from app.auth.application.services import PasswordService, AuthValidationService
from typing import List, Dict
from app.users.application.repositories import UserRepository
from app.shared.exceptions import NotFoundException
from app.shared.response import Result

class ListUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, page_params :Dict[str, int]) -> List[UserResponse]:
        users = await self.repository.list_users(page_params.get("size", 10), page_params.get("number", 0))
        if not users or len == 0:
            return []
        
        return [UserResponse.from_domain(user) for user in users]


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        
    async def execute(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        return UserResponse.from_domain(user)


class CreateUserUseCase:
    def __init__(self, repository: UserRepository, password_service: PasswordService, validation_service: AuthValidationService) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service
        
    async def execute(self, user_data: UserCreate) -> Result:
        result = await self.validation_service.validate_unique_fields(user_data.email, user_data.phone_number)
        if not result.is_success():
            return result
        
        hashed_password = self.password_service.hash_password(user_data.password)
        user = user_data.to_domain(hashed_password) 

        user_created = await self.repository.create(user)
        
        return Result.success(UserResponse.from_domain(user_created)) 

    
class UpdateUserUseCase:
    def __init__(self, repository: UserRepository, validation_service: AuthValidationService,  password_service: PasswordService) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service

    async def execute(self, user_id: int, update_data: UserUpdate) -> Result:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        result = await self.validation_service.validate_unique_fields(update_data.email, update_data.phone_number)
        if not result.is_success():
            return result
        
        hashed_password =  self.password_service.hash_password(update_data.password) if update_data.password else None
        user_updated = update_data.update_user_fields(user, hashed_password)
        
        user = await self.repository.update(user_updated)
        
        return Result.success(UserResponse.from_domain(user))
    
    
class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, user_id: int) -> bool:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        return await self.repository.delete(user_id)