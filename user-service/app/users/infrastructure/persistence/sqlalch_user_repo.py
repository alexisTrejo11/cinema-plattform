import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain import User, UserRepository
from app.users.domain.exceptions import *
from .models import UserModel

logger = logging.getLogger(__name__)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None

    async def get_by_phone(self, phone: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.phone_number == phone)
        )
        user_model = result.scalar_one_or_none()
        return user_model.to_domain() if user_model else None

    async def save(self, user: User) -> User:
        model = UserModel.from_domain(user)
        try:
            if user.id == 0:
                self.session.add(model)
                await self.session.flush()
            else:
                model = await self.session.merge(model)

            await self.session.commit()

            if model in self.session:
                await self.session.refresh(model)

            return model.to_domain()
        except Exception as e:
            await self.session.rollback()
            logger.exception("user persist failed")
            raise RuntimeError(f"Failed to save user: {str(e)}") from e

    async def update(self, user: User) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )

        user_model = result.scalar_one_or_none()
        if not user_model:
            raise UserNotFoundException("User", user.id)

        user_model.update_from_domain(user)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model.to_domain()

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )

        user_model = result.scalar_one_or_none()
        if not user_model:
            return False

        await self.session.delete(user_model)
        await self.session.commit()
        logger.info("user row removed id=%s", user_id)
        return True

    async def list_users(self, offset: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(
            select(UserModel).offset(offset).limit(limit)
        )
        user_models = result.scalars().all()

        return [user_model.to_domain() for user_model in user_models]
