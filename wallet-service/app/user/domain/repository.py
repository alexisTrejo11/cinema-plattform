from abc import ABC, abstractmethod
from typing import List, Optional
from typing import Dict, Any
from app.user.domain.user import User, UserId


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UserId, raise_exception=True) -> User:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        pass

    @abstractmethod
    async def search(self, params: Dict[str, Any]) -> List[User]:
        """
        Searches for users based on provided filters, sorting, and pagination parameters.

        Args:
            params (Dict[str, Any]): A dictionary of parameters to filter, sort, and paginate the query.
                Possible keys include:
                - "is_active" (bool, optional): Filters users by their active status.
                - "email_contains" (str, optional): Filters users whose email addresses contain the given string (case-insensitive).
                - "role" (Union[str, UserRole], optional): Filters users who have the specified role.
                  Can be a string (e.g., "admin", "member") which will be converted to `UserRole` enum,
                  or directly a `UserRole` enum member.
                - "sort_by" (str, optional): The name of the column to sort by (e.g., "email", "created_at").
                  Must be an attribute of `UserSQLModel`.
                - "sort_direction" (str, optional): The direction of sorting. Can be "asc" (default) or "desc".
                  Only considered if "sort_by" is provided.
                - "offset" (int, optional): The number of records to skip from the beginning.
                - "limit" (int, optional): The maximum number of records to return.

        Returns:
            List[User]: A list of User domain models matching the search criteria.
        """
        pass

    @abstractmethod
    async def create(self, user: User) -> None:
        """Create a new user."""
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        """Update an existing user."""
        pass

    @abstractmethod
    async def delete(self, user_id: UserId) -> bool:
        """Delete a user by their ID."""
        pass
