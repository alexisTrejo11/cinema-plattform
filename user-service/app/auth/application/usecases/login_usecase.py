import logging
from typing import Any

from app.shared.events.builders import two_factor_challenge_issued
from app.shared.events.protocols import EventPublisher
from app.shared.qr import generate_qr
from app.shared.response import Result
from app.shared.token.core import TokenProvider, TokenType
from app.users.domain import User

from ..dtos import LoginRequest, RefreshTokenRequest, SessionResponse
from ..services import AuthValidationService, SessionService

logger = logging.getLogger(__name__)


class LoginUseCase:
    def __init__(
        self,
        session_service: SessionService,
        validation_service: AuthValidationService,
        token_service: TokenProvider,
        event_publisher: EventPublisher,
    ):
        self.session_service = session_service
        self.token_service = token_service
        self.validation_service = validation_service
        self._event_publisher = event_publisher

    async def execute(self, request: LoginRequest) -> Result[Any]:
        user = await self.validation_service.authenticate_user(
            request.identifier_field, request.password
        )
        if not user:
            logger.info("login failed: invalid credentials")
            return Result.error("User not found with given credentials")

        if user.is_2fa_enabled:
            qr_code = await self._request_2fa_access(request, user)
            return Result.success({"QR": qr_code})

        session = await self._process_login(user)
        return Result.success(session)

    async def _process_login(self, user: User):
        self.validation_service.validate_account_status_for_login(user)
        session = await self.session_service.create_session(user)
        logger.info("session created user_id=%s", user.id)
        return session

    async def _request_2fa_access(self, request: LoginRequest, user: User):
        if not user.totp_secret:
            raise ValueError("User dont have 2FA secret")

        token = self.token_service.create(
            TokenType.TWO_FA, **{"email": user.email, "totp_secret": user.totp_secret}
        )

        await self._event_publisher.publish(
            two_factor_challenge_issued(user, reason="login_step_up")
        )
        return generate_qr(token.code)


class TwoFALoginUseCase:
    def __init__(
        self,
        token_service: TokenProvider,
        validation_service: AuthValidationService,
        session_service: SessionService,
        event_publisher: EventPublisher,
    ) -> None:
        self.session_service = session_service
        self.token_service = token_service
        self.validation_service = validation_service
        self._event_publisher = event_publisher

    async def execute(self, request: LoginRequest) -> Result:
        user = await self.validation_service.authenticate_user(
            request.identifier_field, request.password
        )
        if not user:
            logger.info("login failed: invalid credentials")
            return Result.error("User not found with given credentials")

        if not request.twoFACode:
            return await self._request_2fa_access(user)

        self.validation_service.validate_2FA_Access(user, request.twoFACode)
        session = await self.session_service.create_session(user)
        logger.info("session created after 2fa user_id=%s", user.id)
        return Result.success(session)

    async def _request_2fa_access(self, user: User):
        if not user.totp_secret:
            raise ValueError("User dont have 2FA secret")

        token = self.token_service.create(
            TokenType.TWO_FA, **{"email": user.email, "totp_secret": user.totp_secret}
        )

        await self._event_publisher.publish(
            two_factor_challenge_issued(user, reason="two_fa_access_endpoint")
        )
        qr = generate_qr(token.code)
        return Result.success(qr)


class RefreshTokenUseCase:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service

    async def execute(
        self, request: RefreshTokenRequest, user: User
    ) -> SessionResponse:
        token_response = await self.session_service.refresh_session(request, user)
        logger.info("token refreshed user_id=%s", user.id)
        return token_response
