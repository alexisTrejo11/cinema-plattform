import logging
from typing import cast
from collections.abc import Awaitable, Callable

import jwt
from fastapi import Request, status
from fastapi.responses import Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from jwt.types import Options

from app.config import settings
from app.config.security import AuthUserContext, _unauthorized


logger = logging.getLogger("app")


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

    if not settings.jwt_secret_key:
        logger.error(
            "JWT_SECRET_KEY is not configured; token validation cannot be performed."
        )
        return _unauthorized("Authentication is not properly configured.")

    options = cast(
        Options,
        {
            "verify_aud": settings.jwt_audience is not None,
            "verify_iss": settings.jwt_issuer is not None,
        },
    )

    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=settings.jwt_algorithms_list,
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options=options,
            leeway=settings.jwt_leeway_seconds,
        )
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
