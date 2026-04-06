from __future__ import annotations

from typing import Annotated, List
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, computed_field

from app.config.app_config import settings

_bearer = HTTPBearer(auto_error=False)


class AuthUserContext(BaseModel):
    """JWT claims available to wallet routes (minimal subset)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    sub: UUID
    email: str | None = None
    roles: List[str] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> UUID:
        """Alias for `sub` (resource owner / user id)."""
        return self.sub


# Roles that may access staff/management wallet endpoints (lowercase for comparison).
STAFF_ROLE_NAMES = frozenset({"admin", "manager", "employee"})


def is_staff_user(user: AuthUserContext) -> bool:
    return any(r.strip().lower() in STAFF_ROLE_NAMES for r in user.roles)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options={"verify_signature": True},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from exc


async def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> AuthUserContext:
    if creds is None or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
    payload = _decode_token(creds.credentials)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject.",
        )
    try:
        uid = UUID(sub) if isinstance(sub, str) else sub
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid subject in token.",
        ) from exc
    roles = payload.get("roles") or payload.get("role")
    if isinstance(roles, str):
        roles = [roles]
    if not isinstance(roles, list):
        roles = []
    return AuthUserContext(
        sub=uid,
        email=payload.get("email"),
        roles=[str(r) for r in roles],
    )


async def require_staff_user(
    user: AuthUserContext = Depends(get_current_user),
) -> AuthUserContext:
    if not is_staff_user(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires a staff role (admin, manager, or employee).",
        )
    return user
