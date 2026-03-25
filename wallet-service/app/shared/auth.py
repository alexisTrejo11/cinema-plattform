import logging
from typing import Any, Optional, cast

import jwt
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from jwt.types import Options

from config.app_config import settings


logger = logging.getLogger(__name__)


def build_jwt_decode_options() -> Options:
    """PyJWT options aligned with optional audience / issuer validation."""
    return cast(
        Options,
        {
            "verify_aud": settings.JWT_AUDIENCE is not None,
            "verify_iss": settings.JWT_ISSUER is not None,
        },
    )


def decode_jwt_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT using the same rules as the auth middleware.
    Issued tokens must include matching aud/iss claims when those settings are set.
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
        options=build_jwt_decode_options(),
        leeway=settings.JWT_LEEWAY_SECONDS,
    )


class AuthUserContext(BaseModel):
    user_id: Optional[str] = None
    subject: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    roles: list[str] = Field(default_factory=list)
    claims: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_claims(cls, claims: dict[str, Any]) -> "AuthUserContext":
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


def _first_text_claim(claims: dict[str, Any], *keys: str) -> Optional[str]:
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


def get_current_user(request: Request) -> Optional[AuthUserContext]:
    return getattr(request.state, "current_user", None)


def require_authenticated_user(request: Request) -> AuthUserContext:
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

    def dependency(request: Request) -> AuthUserContext:
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


def get_jwt_claims(request: Request) -> Optional[dict[str, Any]]:
    return getattr(request.state, "jwt_claims", None)
