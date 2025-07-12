from uuid import UUID
from app.application.repositories.user_repository import UserRepository
from app.application.dtos.user_dtos import CreateUserResponse, UserResponse
from app.application.mappers.user_mapper import user_to_dto, create_user_dto_to_domain


class UserService:
    """Provides use cases for user operations."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, create_user_dto: CreateUserResponse) -> UserResponse:
        """Creates a new user."""
        new_user = create_user_dto_to_domain(create_user_dto)
        created_user = await self.user_repo.create(new_user)
        return user_to_dto(created_user)

    async def get_user_by_id(self, user_id: UUID) -> UserResponse | None:
        """Retrieves a user by their ID."""
        user = await self.user_repo.get_by_id(user_id)
        return user_to_dto(user) if user else None

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        """Retrieve a user by their email address."""
        user = await self.user_repo.get_by_email(email)
        return user_to_dto(user) if user else None

    async def get_all_users(self) -> list[UserResponse]:
        """Retrieves all users."""
        users = await self.user_repo.get_all()
        return [user_to_dto(user) for user in users]
