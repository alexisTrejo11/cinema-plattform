import logging
from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.config.app_config import settings
from app.shared.core.jwt_security import (
    _unauthorized,
    decode_jwt_token,
    AuthUserContext,
)

logger = logging.getLogger(__name__)


async def jwt_auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request.state.current_user = None
    request.state.jwt_claims = None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        return await call_next(request)

    if not auth_header.lower().startswith("bearer "):
        logger.warning(
            "Authorization header format is invalid",
            extra={"props": {"path": request.url.path}},
        )
        return _unauthorized(
            "Invalid Authorization header format. Use: Bearer <token>."
        )

    token = auth_header[7:].strip()
    if not token:
        logger.warning(
            "Bearer token was empty",
            extra={"props": {"path": request.url.path}},
        )
        return _unauthorized("Bearer token is empty.")

    if not settings.JWT_SECRET_KEY:
        logger.error(
            "JWT_SECRET_KEY is not configured; token validation cannot be performed."
        )
        return _unauthorized("Authentication is not properly configured.")

    try:
        claims = decode_jwt_token(token)
        current_user = AuthUserContext.from_claims(claims)
        request.state.jwt_claims = claims
        request.state.current_user = current_user
    except ExpiredSignatureError:
        logger.info(
            "Expired JWT token",
            extra={"props": {"path": request.url.path}},
        )
        return _unauthorized("Token has expired.")
    except InvalidTokenError:
        logger.info(
            "Invalid JWT token",
            extra={"props": {"path": request.url.path}},
        )
        return _unauthorized("Token is invalid.")

    return await call_next(request)
