import logging

from app.shared.events.builders import two_factor_disabled, two_factor_enabled
from app.shared.events.protocols import EventPublisher
from app.shared.token.core import TokenProvider, TokenType
from app.users.domain import (
    InvalidTokenError,
    TwoFaAlreadyConfiguredError,
    User,
    User2FaAuthError,
    UserRepository,
)

logger = logging.getLogger(__name__)


class Enable2FAUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenProvider,
        event_publisher: EventPublisher,
    ) -> None:
        self.user_repo = user_repo
        self.token_service = token_service
        self._event_publisher = event_publisher

    async def execute(self, user: User) -> tuple:
        await self._validate_user(user)

        totp_secret_token = self.token_service.create(
            TokenType.TWO_FACTOR_SECRET, **user.model_dump()
        )
        user.add_2FA_config(totp_secret_token.code)
        qr_code = "TODO"

        await self.user_repo.save(user)
        logger.info("2fa enabled user_id=%s", user.id)
        await self._event_publisher.publish(
            two_factor_enabled(user.id, str(user.email))
        )

        return qr_code, totp_secret_token.code

    async def _validate_user(self, user: User):
        if user.is_2fa_enabled:
            raise TwoFaAlreadyConfiguredError(message="2FA auth already configured")


class Disable2FaUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenProvider,
        event_publisher: EventPublisher,
    ) -> None:
        self.user_repo = user_repo
        self.token_service = token_service
        self._event_publisher = event_publisher

    async def execute(self, user: User, token: str) -> None:
        await self._validate_user(user)

        is_valid = self.token_service.revoke(
            str(user.id), TokenType.VERIFICATION, token
        )
        if not is_valid:
            raise InvalidTokenError()

        user.disable_2FA_config()

        await self.user_repo.save(user)
        logger.info("2fa disabled user_id=%s", user.id)
        await self._event_publisher.publish(
            two_factor_disabled(user.id, str(user.email))
        )

    async def _validate_user(self, user: User):
        if not user.is_2fa_enabled:
            raise User2FaAuthError(message="User don't have 2FA enable")
