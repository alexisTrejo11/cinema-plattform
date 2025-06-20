from typing import List, Dict
from app.shared.response import Result
from app.shared.pagintation import PaginationParams as PageParams
from app.users.application.dtos import UserResponse, UserCreate, UserUpdate
from app.auth.application.services import PasswordService, AuthValidationService, TokenService
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User
from app.users.domain.exceptions import UserNotFoundException

class ListUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, page_params: PageParams) -> List[UserResponse]:
        users = await self.repository.list_users(page_params.limit, page_params.offset)
        if not users or len == 0:
            return []
        
        return [UserResponse.from_domain(user) for user in users]


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        
    async def execute(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
        
        return UserResponse.from_domain(user)


class CreateUserUseCase:
    def __init__(self,  repository: UserRepository, password_service: PasswordService, validation_service: AuthValidationService) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service
        
    async def execute(self, user_data: UserCreate) -> Result[User]:
        result = await self.validation_service.validate_unique_fields(user_data.email, user_data.phone_number)
        if not result.is_success():
            return result
        
        User.validate_password_before_hash(user_data.password)
        user = user_data.to_domain() 
        
        hashed_password = self.password_service.hash_password(user_data.password)
        user.password = hashed_password

        user_created = await self.repository.save(user)
        
        return Result.success(UserResponse.from_domain(user_created)) 

    
class UpdateUserUseCase:
    def __init__(self, repository: UserRepository, validation_service: AuthValidationService, password_service: PasswordService) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service

    async def execute(self, user_id: int, update_data: UserUpdate) -> Result:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
        
        result = await self.validation_service.validate_unique_fields(update_data.email, update_data.phone_number)
        if not result.is_success():
            return result
        
        hashed_password = None
        if update_data.password:
            User.validate_password_before_hash(update_data.password)
            hashed_password =  self.password_service.hash_password(update_data.password)
        
        user_updated = update_data.update_user_fields(user, hashed_password)
        
        user = await self.repository.save(user_updated)
        
        return Result.success(UserResponse.from_domain(user))
    
    
class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
    
    async def execute(self, user_id: int) -> bool:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
        
        return await self.repository.delete(user_id)


class ActivateUser:
    def __init__(self, repository: UserRepository, token_service: TokenService) -> None:
        self.repository = repository
        self.token_service = token_service
        
    
    async def execute(self, user_id: int, activation_token: str) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
        
        self.token_service.verify_token(activation_token)
        
        user.activate()
        await self.repository.save(user)


class BanUser:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def execute(self, user_id: int, activation_token: str) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
                
        user.ban()
        await self.repository.save(user)
        
