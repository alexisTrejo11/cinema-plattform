from app.user.domain.repository import UserRepository
from typing import List, Optional, Dict, Any
from sqlalchemy import select, insert, update, delete, asc, desc
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .model import UserSQLModel
from app.user.domain.user import User, UserRole


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserSQLModel).where(UserSQLModel.id == UUID(user_id))
        result = await self.session.execute(stmt)
        sql_user = result.scalar_one_or_none()
        if sql_user:
            return sql_user.to_domain_user()
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserSQLModel).where(UserSQLModel.email == email)
        result = await self.session.execute(stmt)
        sql_user = result.scalar_one_or_none()
        if sql_user:
            return sql_user.to_domain_user()
        return None

    async def list(self, params: Dict[str, Any]) -> List[User]:
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
            # Use PostgreSQL array overlap operator
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

    async def save(self, user_data: Dict[str, Any]) -> User:
        # Convert domain objects to database-compatible values
        data_copy = user_data.copy()

        if "roles" in data_copy:
            data_copy["roles"] = [UserRole(role) for role in data_copy["roles"]]

        if "id" in data_copy and data_copy["id"]:
            user_id = (
                data_copy["id"].value
                if hasattr(data_copy["id"], "value")
                else data_copy["id"]
            )
            existing_user = await self.session.get(UserSQLModel, user_id)
            if existing_user:
                for key, value in data_copy.items():
                    if hasattr(existing_user, key):
                        # Convert value objects to their underlying values
                        if key == "id" and hasattr(value, "value"):
                            setattr(existing_user, key, value.value)
                        else:
                            setattr(existing_user, key, value)
                await self.session.flush()
                return existing_user.to_domain_user()

            # Convert the id to UUID for new user creation
            data_copy["id"] = user_id

        new_sql_user = UserSQLModel(**data_copy)
        self.session.add(new_sql_user)
        await self.session.flush()
        await self.session.refresh(new_sql_user)
        return new_sql_user.to_domain_user()

    async def delete(self, user_id: str) -> bool:
        stmt = delete(UserSQLModel).where(UserSQLModel.id == UUID(user_id))
        result = await self.session.execute(stmt)
        return result.rowcount > 0
