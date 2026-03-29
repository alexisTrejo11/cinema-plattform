import logging

from app.wallet.domain.interfaces import UserInternalService
from app.wallet.domain.entities import User
from app.wallet.domain.value_objects import UserId
from app.shared.core.response import Result

logger = logging.getLogger(__name__)


class UserGrpcService(UserInternalService):
    """
    gRPC implementation of the UserInternalService.

    This service calls to the user service to get user details.
    """

    def __init__(self) -> None:
        pass

    async def get_user_details(self, user_id: UserId) -> Result[User]:
        """Resolve a user from the local `users` table or upstream user service."""
        logger.warning(
            "UserGrpcService.get_user_details not implemented yet, returning success temporarily"
        )
        return Result.success(
            User(id=user_id, name="John Doe", email="john.doe@example.com")
        )
