from typing import Optional

from app.wallet.domain.interfaces import UserInternalService
from app.wallet.domain.entities import User
from app.wallet.domain.value_objects import UserId


class UserGrpcService(UserInternalService):
    """
    gRPC implementation of the UserInternalService.

    This service calls to the user service to get user details.
    """

    def __init__(self) -> None:
        pass

    async def get_user_details(self, user_id: UserId) -> Optional[User]:
        """Resolve a user from the local `users` table or upstream user service."""
        pass
