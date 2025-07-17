from app.user.domain.user import UserId
from typing import Any, Dict, List
from app.user.domain.exceptions import UserNotFoundException
from app.user.domain.repository import UserRepository
from app.user.application.commands import UserCreateCommand, UserUpdateCommand
from app.user.application.dtos import UserResponse
from app.user.domain.user import UserId
from .mapper import UserMapper


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id.to_string())

        return UserResponse(**user.to_dict())


class GetUserByEmailUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str) -> UserResponse:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(email)

        return UserResponse(**user.to_dict())


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, params: Dict[str, Any]) -> List[UserResponse]:
        users = await self.user_repository.search(params)
        return [UserResponse(**user.to_dict()) for user in users]


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: UserCreateCommand) -> UserResponse:
        new_user = UserMapper.from_create_command(command)

        user_created = await self.user_repository.create(new_user)

        return UserResponse(**user_created.to_dict())


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self, user_id: UserId, command: UserUpdateCommand
    ) -> UserResponse:
        existing_user = await self.user_repository.get_by_id(
            user_id, raise_exception=True
        )

        update_user = UserMapper.from_update_command(command, existing_user)
        user_created = await self.user_repository.update(update_user)

        return UserResponse(**user_created.to_dict())


class SoftDeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> None:
        await self.user_repository.get_by_id(user_id, raise_exception=True)
        await self.user_repository.delete(user_id, soft_delete=True)
