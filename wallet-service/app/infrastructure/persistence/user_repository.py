from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.application.repositories.user_repository import UserRepository
from app.domain.models import User
from app.infrastructure.persistence.sqlalchemy_models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy async implementation of the User repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalars().first()
        return User.model_validate(user_model) if user_model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalars().first()
        return User.model_validate(user_model) if user_model else None

    async def create(self, user: User) -> User:
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return User.model_validate(user_model)

    async def update(self, User: User) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == User.id)
        )
        user_model = result.scalars().first()

        if user_model:
            for field, value in User.model_dump().items():
                setattr(user_model, field, value)
            await self.session.commit()
            await self.session.refresh(user_model)

        return User.model_validate(user_model)

    async def delete(self, User_id: UUID) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == User_id)
        )
        user_model = result.scalars().first()

        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()
            return True
        return False
