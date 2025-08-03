import json
from uuid import UUID
from typing import Dict, Any
from app.user.domain.value_objects import UserId
from app.user.application.usecases import (
    CreateUserUseCase,
    UpdateUserUseCase,
    SoftDeleteUserUseCase,
    UserCreateCommand,
    UserUpdateCommand,
)
from app.user.domain.repository import UserRepository
from app.user.infrastructure.sql_user_respository import SqlAlchemyUserRepository
from config.db.postgres_config import get_db as get_db_session

import logging  # queue log?

logger = logging.getLogger("name")


class UserEventProcessor:
    def __init__(self):
        pass

    async def process_user_event(self, payload: Dict[str, Any]):
        event_type = payload.get("type")
        user_data: Dict[str, Any] = payload.get("data")

        self._validate(event_type, user_data, payload)
        self.map_str_id_to_uiid(user_data)

        async for session in get_db_session():
            user_repo: UserRepository = SqlAlchemyUserRepository(session)
            try:
                match event_type:
                    case "user.created":
                        await self._proccess_user_create_event(user_data, user_repo)
                    case "user.updated":
                        await self._proccess_user_update_event(
                            user_data, user_repo, payload
                        )
                    case "user.deleted":
                        await self._proccess_user_delete_event(
                            user_data, user_repo, payload
                        )
                    case _:
                        logger.info(f"Unknown event type: {event_type}")
            except Exception as e:
                logger.info(f"Error processing user event '{event_type}': {e}")
                # re-raise or log more extensively???.

    async def _proccess_user_create_event(self, user_data: Dict[str, Any], user_repo):
        use_case = CreateUserUseCase(user_repo)
        command = UserCreateCommand(
            user_id=user_data["user_id"],
            email=user_data["email"],
            roles=user_data["roles"],
            is_active=user_data["is_active"],
        )

        await use_case.execute(command)
        logger.info(f"User created: {user_data.get('email')}")

    async def _proccess_user_update_event(
        self, user_data: Dict[str, Any], user_repo, payload
    ):
        user_id_str = str(user_data.get("id"))
        if user_id_str:
            use_case = UpdateUserUseCase(user_repo)
            command = UserUpdateCommand(
                email=user_data["email"],
                roles=user_data["roles"],
                is_active=user_data["is_active"],
            )

            await use_case.execute(UserId.from_string(user_id_str), command)
            logger.info(f"User updated: {user_id_str}")
        else:
            logger.info(f"Update event missing user ID: {payload}")

    async def _proccess_user_delete_event(
        self, user_data: Dict[str, Any], user_repo, payload
    ):
        user_id_str = str(user_data.get("id"))
        if user_id_str:
            use_case = SoftDeleteUserUseCase(user_repo)

            await use_case.execute(UserId.from_string(user_id_str))
            logger.info(f"User deleted: {user_id_str}")
        else:
            logger.info(f"Delete event missing user ID: {payload}")

    def map_str_id_to_uiid(self, user_data: Dict[str, Any]):
        if "id" in user_data and isinstance(user_data["id"], str):
            try:
                user_data["id"] = UUID(user_data["id"])
            except ValueError:
                logger.error(f"Invalid UUID format for user_id: {user_data['id']}")
                return

    def _validate(self, event_type, user_data, payload):
        if not event_type or not user_data:
            logger.error(f"Invalid message format: {payload}")
            return
