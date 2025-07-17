from app.user.domain.repository import UserRepository
from typing import List, Optional, Dict, Any
from sqlalchemy import select, insert, update, delete, asc, desc
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from .model import UserSQLModel
from app.user.domain.user import User, UserRole, UserId
from app.user.domain.exceptions import UserNotFoundException


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UserId, raise_exception=True) -> User:
        stmt = select(UserSQLModel).where(UserSQLModel.id == user_id.value)
        result = await self.session.execute(stmt)
        sql_user = result.scalar_one_or_none()

        if sql_user:
            return sql_user.to_domain_user()

        if not raise_exception:
            return None

        raise UserNotFoundException(user_id.to_string())

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserSQLModel).where(UserSQLModel.email == email)
        result = await self.session.execute(stmt)
        sql_user = result.scalar_one_or_none()

        if sql_user:
            return sql_user.to_domain_user()

        return None

    async def search(self, params: Dict[str, Any]) -> List[User]:
        stmt = select(UserSQLModel)

        if "is_active" in params:
            stmt = stmt.where(UserSQLModel.is_active == params["is_active"])
        if "email_contains" in params:
            stmt = stmt.where(UserSQLModel.email.ilike(f"%{params['email_contains']}%"))
        if "role" in params:
            if isinstance(params["role"], str):
                role_enum = UserRole(params["role"])
            else:
                role_enum = params["role"]
            # array overlap operator
            stmt = stmt.where(UserSQLModel.roles.op("&&")([role_enum]))

        if "sort_by" in params:
            sort_column_name = params["sort_by"]
            sort_direction = params.get("sort_direction", "asc").lower()

            sort_attr = getattr(UserSQLModel, sort_column_name, None)

            if sort_attr is not None:
                if sort_direction == "desc":
                    stmt = stmt.order_by(desc(sort_attr))
                else:
                    stmt = stmt.order_by(asc(sort_attr))

        if "offset" in params:
            stmt = stmt.offset(params["offset"])

        if "limit" in params:
            stmt = stmt.limit(params["limit"])

        result = await self.session.execute(stmt)
        sql_users = result.scalars().all()
        return [sql_user.to_domain_user() for sql_user in sql_users]

    async def create(self, user: User) -> None:
        new_sql_user = UserSQLModel.from_domain(user)

        self.session.add(new_sql_user)
        await self.session.flush()

    async def update(self, user: User) -> None:
        existing_user = await self.session.get(UserSQLModel, user.get_id().value)

        if not existing_user:
            raise UserNotFoundException(user.get_id().to_string())

        existing_user.update_from_domain(user)

        self.session.add(existing_user)
        await self.session.commit()

    async def delete(self, user_id: UserId) -> bool:
        stmt = delete(UserSQLModel).where(UserSQLModel.id == user_id.value)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
