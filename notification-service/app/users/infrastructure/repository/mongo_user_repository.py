from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


from app.users.domain.entities.user import (
    User,
    UserRole,
)
from app.users.domain.repository import UserRepository
from app.users.domain.exceptions import *


class MongoUserRepository(UserRepository):
    """
    MongoDB implementation of the UserRepository.
    """

    def __init__(self, database):
        """
        Initializes MongoUserRepository with a MongoDB database instance.
        """
        self.collection = database["users"]

    async def _create_indexes(self):
        """Helper to create necessary indexes."""
        try:
            await self.collection.create_index("email", unique=True)
            await self.collection.create_index(
                "phone",
                unique=True,
                partialFilterExpression={"phone": {"$exists": True, "$ne": None}},
            )
            print("MongoDB indexes for users created/ensured.")
        except Exception as e:
            print(f"Error creating MongoDB indexes: {e}")

    def _doc_to_user(self, doc: Optional[Dict[str, Any]]) -> Optional[User]:
        if doc:
            return User.from_mongo_dict(doc)
        return None

    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            return None

        doc = await self.collection.find_one({"_id": uuid_id, "deleted_at": None})
        return self._doc_to_user(doc)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        doc = await self.collection.find_one({"email": email, "deleted_at": None})
        return self._doc_to_user(doc)

    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone."""
        doc = await self.collection.find_one({"phone": phone, "deleted_at": None})
        return self._doc_to_user(doc)

    async def create(self, user: User) -> User:
        """Create a new user."""
        if await self.exists_by_email(user.email):
            raise UserAlreadyExistsException(
                f"User with email '{user.email}' already exists."
            )
        if user.phone and await self.exists_by_phone(user.phone):
            raise UserAlreadyExistsException(
                f"User with phone '{user.phone}' already exists."
            )

        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        await self.collection.insert_one(user.to_mongo_dict())
        return user

    async def update(self, user: User) -> User:
        """Update an existing user."""
        user.updated_at = datetime.now()
        result = await self.collection.update_one(
            {"_id": user.id},
            {"$set": user.to_mongo_dict()},
            upsert=False,
        )
        if result.matched_count == 0:
            raise UserNotFoundException(
                f"User with ID '{user.id}' not found for update."
            )
        return user

    async def delete(self, user_id: str) -> bool:
        """Hard delete a user."""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            return False

        result = await self.collection.delete_one({"_id": uuid_id})
        return result.deleted_count > 0

    async def soft_delete(self, user_id: str) -> bool:
        """Soft delete a user by setting deleted_at timestamp."""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            return False

        result = await self.collection.update_one(
            {
                "_id": uuid_id,
                "deleted_at": None,
            },
            {"$set": {"deleted_at": datetime.now(), "updated_at": datetime.now()}},
        )
        return result.matched_count > 0

    async def restore(self, user_id: str) -> bool:
        """Restore a soft-deleted user."""
        try:
            uuid_id = UUID(user_id)
        except ValueError:
            return False

        result = await self.collection.update_one(
            {
                "_id": uuid_id,
                "deleted_at": {"$ne": None},
            },
            {"$set": {"deleted_at": None, "updated_at": datetime.now()}},
        )
        return result.matched_count > 0

    async def get_active_users(self) -> List[User]:
        """Get all active users (not soft-deleted)."""
        cursor = self.collection.find({"deleted_at": None})
        return [
            user
            for doc in await cursor.to_list(length=None)
            if (user := self._doc_to_user(doc)) is not None
        ]

    async def get_users_by_role(self, role: UserRole) -> List[User]:
        """Get users by role."""
        cursor = self.collection.find({"roles": role.value, "deleted_at": None})
        return [
            user
            for doc in await cursor.to_list(length=None)
            if (user := self._doc_to_user(doc)) is not None
        ]

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email (active or soft-deleted)."""
        count = await self.collection.count_documents({"email": email})
        return count > 0

    async def exists_by_phone(self, phone: str) -> bool:
        """Check if user exists by phone (active or soft-deleted)."""
        if phone is None:
            return False
        count = await self.collection.count_documents({"phone": phone})
        return count > 0
