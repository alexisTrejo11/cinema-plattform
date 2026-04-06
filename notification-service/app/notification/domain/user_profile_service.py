from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class UserContactProfile:
    """Minimal user contact data resolved from an external user directory."""

    user_id: str
    email: str | None = None
    phone_number: str | None = None


class UserProfileService(ABC):
    """Port to resolve contact channels for a user id."""

    @abstractmethod
    async def resolve_contact(self, user_id: str) -> UserContactProfile | None:
        raise NotImplementedError
