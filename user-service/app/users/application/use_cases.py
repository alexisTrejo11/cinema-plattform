import logging
from typing import List

from app.auth.application.services import (
    AuthValidationService,
    PasswordService,
    TokenService,
)
from app.shared.pagination import PaginationParams as PageParams
from app.shared.response import Result
from app.token.domain.token import TokenType
from app.users.application.dtos import UserCreate, UserUpdate
from app.users.domain import User, UserNotFoundException, UserRepository

logger = logging.getLogger(__name__)


class ListUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def execute(self, page_params: PageParams) -> List[User]:
        return await self.repository.list_users(page_params.offset, page_params.limit)


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)
        return user


class CreateUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        password_service: PasswordService,
        validation_service: AuthValidationService,
    ) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service

    async def execute(self, user_data: UserCreate) -> Result[User]:
        result = await self.validation_service.validate_unique_fields(
            user_data.email, user_data.phone_number
        )
        if not result.is_success():
            return result

        User.validate_password_before_hash(user_data.password)
        user = user_data.to_domain()

        hashed_password = self.password_service.hash_password(user_data.password)
        user.password = hashed_password

        user_created = await self.repository.save(user)
        logger.info("user created id=%s", user_created.id)
        return Result.success(user_created)


class UpdateUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        validation_service: AuthValidationService,
        password_service: PasswordService,
    ) -> None:
        self.repository = repository
        self.password_service = password_service
        self.validation_service = validation_service

    async def execute(self, user_id: int, update_data: UserUpdate) -> Result[User]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)

        result = await self.validation_service.validate_unique_fields(
            update_data.email, update_data.phone_number
        )
        if not result.is_success():
            return result

        hashed_password = None
        if update_data.password:
            User.validate_password_before_hash(update_data.password)
            hashed_password = self.password_service.hash_password(update_data.password)

        user_updated = update_data.update_user_fields(user, hashed_password)

        user = await self.repository.save(user_updated)
        logger.info("user updated id=%s", user_id)
        return Result.success(user)


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def execute(self, user_id: int) -> bool:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)

        deleted = await self.repository.delete(user_id)
        if deleted:
            logger.info("user deleted id=%s", user_id)
        return deleted


class ActivateUser:
    def __init__(self, repository: UserRepository, token_service: TokenService) -> None:
        self.repository = repository
        self.token_service = token_service

    async def execute(self, user_id: int, activation_token: str) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)

        is_token_valid = self.token_service.verify_token(
            activation_token, TokenType.VERIFICATION, user_id
        )
        if not is_token_valid:
            raise ValueError("Invalid or Expired Token")

        user.activate()
        await self.repository.save(user)
        logger.info("user activated id=%s", user_id)


class BanUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def execute(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException("User", user_id)

        user.ban()
        await self.repository.save(user)
        logger.info("user banned id=%s", user_id)
