from typing import Optional
from datetime import datetime, timezone
from ..domain.repository import UserRepository
from ..domain.entities.user import User, UserRole
from exceptions import AuthenticationError, AuthorizationError


class AuthUseCases:
    """Use cases for authentication and authorization operations"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str) -> User:
        """
        Authenticate a user by email

        Args:
            email: User's email address

        Returns:
            User: Authenticated user

        Raises:
            AuthenticationError: If user not found or inactive
        """
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise AuthenticationError(f"User with email {email} not found")

        if not user.is_active():
            raise AuthenticationError(f"User with email {email} is inactive")

        return user

    async def authenticate_user_by_phone(self, phone: str) -> User:
        """
        Authenticate a user by phone

        Args:
            phone: User's phone number

        Returns:
            User: Authenticated user

        Raises:
            AuthenticationError: If user not found or inactive
        """
        user = await self.user_repository.get_by_phone(phone)

        if not user:
            raise AuthenticationError(f"User with phone {phone} not found")

        if not user.is_active():
            raise AuthenticationError(f"User with phone {phone} is inactive")

        return user

    async def validate_user_role(self, user_id: str, required_role: UserRole) -> bool:
        """
        Validate if a user has the required role

        Args:
            user_id: User's ID
            required_role: Required role for the operation

        Returns:
            bool: True if user has the required role

        Raises:
            AuthenticationError: If user not found or inactive
            AuthorizationError: If user doesn't have the required role
        """
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise AuthenticationError(f"User with ID {user_id} not found")

        if not user.is_active():
            raise AuthenticationError(f"User with ID {user_id} is inactive")

        if not user.has_role(required_role):
            raise AuthorizationError(
                f"User {user_id} does not have required role: {required_role.value}"
            )

        return True

    async def validate_admin_access(self, user_id: str) -> bool:
        """
        Validate if a user has admin access

        Args:
            user_id: User's ID

        Returns:
            bool: True if user has admin access

        Raises:
            AuthenticationError: If user not found or inactive
            AuthorizationError: If user is not an admin
        """
        return await self.validate_user_role(user_id, UserRole.ADMIN)

    async def get_user_profile(self, user_id: str) -> User:
        """
        Get user profile for authenticated user

        Args:
            user_id: User's ID

        Returns:
            User: User profile

        Raises:
            AuthenticationError: If user not found or inactive
        """
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise AuthenticationError(f"User with ID {user_id} not found")

        if not user.is_active():
            raise AuthenticationError(f"User with ID {user_id} is inactive")

        return user

    async def check_user_exists(self, email: str, phone: str) -> bool:
        """
        Check if a user already exists with the given email or phone

        Args:
            email: User's email
            phone: User's phone

        Returns:
            bool: True if user exists
        """
        email_exists = await self.user_repository.exists_by_email(email)
        phone_exists = await self.user_repository.exists_by_phone(phone)

        return email_exists or phone_exists

    async def create_user(
        self, user_id: str, email: str, phone: str, roles: Optional[list] = None
    ) -> User:
        """
        Create a new user

        Args:
            user_id: User's ID
            email: User's email
            phone: User's phone
            roles: List of user roles (optional)

        Returns:
            User: Created user

        Raises:
            AuthenticationError: If user already exists
        """
        if await self.check_user_exists(email, phone):
            raise AuthenticationError("User already exists with this email or phone")

        now = datetime.now(timezone.utc)
        user_roles = roles if roles else [UserRole.CUSTOMER]

        user = User(
            id=user_id,
            email=email,
            phone=phone,
            created_at=now,
            updated_at=now,
            roles=user_roles,
        )

        return await self.user_repository.create(user)

    async def update_user_roles(self, user_id: str, roles: list) -> User:
        """
        Update user roles

        Args:
            user_id: User's ID
            roles: New list of roles

        Returns:
            User: Updated user

        Raises:
            AuthenticationError: If user not found or inactive
        """
        user = await self.get_user_profile(user_id)
        user.roles = roles
        user.updated_at = datetime.now(timezone.utc)

        return await self.user_repository.update(user)
