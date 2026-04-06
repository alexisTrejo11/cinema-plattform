from dataclasses import dataclass
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.app_config import settings

_bearer = HTTPBearer(auto_error=True)


@dataclass
class AuthUserContext:
    user_id: int
    email: str
    roles: list[str]

    def has_role(self, *roles: str) -> bool:
        return any(r in self.roles for r in roles)


def _decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"verify_aud": bool(settings.JWT_AUDIENCE)},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {exc}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> AuthUserContext:
    payload = _decode_token(credentials.credentials)
    return AuthUserContext(
        user_id=int(payload.get("sub", 0)),
        email=payload.get("email", ""),
        roles=payload.get("roles", []),
    )


def require_roles(*required_roles: str):
    """Dependency factory that enforces role-based access."""

    async def _check(user: AuthUserContext = Depends(get_current_user)) -> AuthUserContext:
        if not user.has_role(*required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {list(required_roles)}",
            )
        return user

    return _check
