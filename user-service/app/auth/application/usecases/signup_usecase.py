from app.users.domain.entities import User
from app.users.application.repositories import UserRepository
from app.users.application.dtos import UserResponse
from app.shared.response import Result
from ..services import PasswordService, AuthValidationService
from ..dtos import SignUpRequest


class SignUpUseCase:
    def __init__(
        self, 
        user_repository: UserRepository, 
        validation_service: AuthValidationService,
        password_service: PasswordService
    ):
        self.user_repository = user_repository
        self.validation_service = validation_service
        self.password_service = password_service

    async def execute(self, request: SignUpRequest) -> Result[UserResponse]:
        validation_result = await self.validation_service.validate_unique_fields(request.email, request.phone_number)
        if not validation_result.is_success():
            return validation_result
        
        new_user = self._create_user(request)
        created_user = await self.user_repository.save(new_user)
        
        user_response = UserResponse.from_domain(created_user)
        return Result.success(user_response)

    def _create_user(self, request: SignUpRequest) -> User:
        new_user = User(**request.model_dump())
        
        hashed_password = self.password_service.hash_password(request.password)
        new_user.password = hashed_password
        
        return new_user