from app.user.domain.user import User, UserId
from typing import Any, Dict, List, Optional
from app.user.domain.exceptions import UserNotFoundException
from app.user.domain.repository import UserRepository
from app.user.application.dtos import UserCreateCommand, UserResponse
from datetime import datetime
from typing import List, Optional
from app.user.domain.user import User, UserId


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> UserResponse:
        """
        Retrieves a user by their Email.

        :param email: The email of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        user = await self.user_repository.get_by_id(user_id.to_string())
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        return UserResponse(**user.to_dict())


class GetUserByEmailUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str) -> UserResponse:
        """
        Retrieves a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(f"User with email {email} not found.")

        return UserResponse(**user.to_dict())


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, params: Dict[str, Any]) -> List[UserResponse]:
        """
        Lists all users.

        :return: A list of User objects.
        """
        users = await self.user_repository.list(params)
        return [UserResponse(**user.to_dict()) for user in users]


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: UserCreateCommand) -> UserResponse:
        """
        Creates a new user.

        :param user: The User object to create.
        :return: The created User object.
        """
        user_created = await self.user_repository.save(**command.model_dump())

        return UserResponse(**user_created.to_dict())


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self, user_id: UserId, command: UserCreateCommand
    ) -> UserResponse:
        """
        Creates a new user.

        :param user: The User object to create.
        :return: The created User object.
        """
        user = await self.user_repository.get_by_id(user_id.to_string())
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        user_created = await self.user_repository.save(
            **command.model_dump(exclude_unset=True)
        )

        return UserResponse(**user_created.to_dict())


class SoftDeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UserId) -> None:
        """
        Soft Delete a new user.

        :param user: The User object to create.
        :return: The created User object.
        """
        user = await self.user_repository.get_by_id(user_id.to_string())
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        await self.user_repository.delete(user_id.to_string())
