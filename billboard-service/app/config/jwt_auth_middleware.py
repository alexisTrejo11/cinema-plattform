import logging
from typing import Any
from typing import cast
from collections.abc import Awaitable, Callable

import jwt
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from jwt.types import Options
from pydantic import BaseModel, Field

from app.config.app_config import settings

logger = logging.getLogger("app")


class AuthenticatedUserDTO(BaseModel):
    user_id: str | None = None
    subject: str | None = None
    email: str | None = None
    username: str | None = None
    roles: list[str] = Field(default_factory=list)
    claims: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: dict[str, Any]) -> "AuthenticatedUserDTO":
        roles_raw = claims.get("roles") or claims.get("role") or []

        if isinstance(roles_raw, str):
            roles = [roles_raw]
        elif isinstance(roles_raw, list):
            roles = [str(role) for role in roles_raw]
        else:
            roles = []

        return cls(
            user_id=_first_text_claim(claims, "user_id", "uid", "id", "sub"),
            subject=_first_text_claim(claims, "sub"),
            email=_first_text_claim(claims, "email"),
            username=_first_text_claim(
                claims, "username", "preferred_username", "name"
            ),
            roles=roles,
            claims=claims,
        )


def _first_text_claim(claims: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = claims.get(key)
        if value is None:
            continue
        return str(value)
    return None


def _unauthorized(message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": {"code": "UNAUTHORIZED", "message": message}},
        headers={"WWW-Authenticate": "Bearer"},
    )


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
        current_user = AuthenticatedUserDTO.from_claims(claims)
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


def get_current_user(request: Request) -> AuthenticatedUserDTO | None:
    return getattr(request.state, "current_user", None)


def require_authenticated_user(request: Request) -> AuthenticatedUserDTO:
    user = get_current_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: str):
    normalized_allowed = {
        role.strip().lower() for role in allowed_roles if role.strip()
    }

    def dependency(request: Request) -> AuthenticatedUserDTO:
        user = require_authenticated_user(request)

        user_roles = {role.strip().lower() for role in user.roles if role.strip()}
        if normalized_allowed and not (user_roles & normalized_allowed):
            logger.warning(
                "User is authenticated but does not have required role",
                extra={
                    "props": {
                        "path": request.url.path,
                        "required_roles": sorted(normalized_allowed),
                        "user_roles": sorted(user_roles),
                        "user_id": user.user_id,
                    }
                },
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return dependency


def get_jwt_claims(request: Request) -> dict[str, Any] | None:
    return getattr(request.state, "jwt_claims", None)
