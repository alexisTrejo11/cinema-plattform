"""Integration tests for `/api/v2/users/*` (admin)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from main import app
from app.auth.infrastructure.api.dependencies import get_logged_admin_user
from app.users.domain import UserRole
from app.users.domain.exceptions import UserNotFoundException
from app.users.infrastructure.controller.dependencies import get_user_use_cases

from tests.integration.stubs import make_domain_user

USERS = "/api/v2/users"


@pytest.mark.asyncio
class TestUserManagementController:
    async def test_list_users_401_without_token(self, async_client):
        r = await async_client.get(f"{USERS}/")
        assert r.status_code == 401

    async def test_list_users_200_with_overrides(self, async_client):
        admin = make_domain_user(user_id=1, role=UserRole.ADMIN)
        listed = make_domain_user(user_id=2, email="other@example.com")

        async def fake_admin() -> object:
            return admin

        fake_uc = MagicMock()
        fake_uc.list_users = MagicMock()
        fake_uc.list_users.execute = AsyncMock(return_value=[listed])

        app.dependency_overrides[get_logged_admin_user] = fake_admin
        app.dependency_overrides[get_user_use_cases] = lambda: fake_uc
        try:
            r = await async_client.get(f"{USERS}/")
            assert r.status_code == 200
            data = r.json()
            assert len(data) == 1
            assert data[0]["email"] == "other@example.com"
        finally:
            app.dependency_overrides.pop(get_logged_admin_user, None)
            app.dependency_overrides.pop(get_user_use_cases, None)

    async def test_get_user_404(self, async_client):
        admin = make_domain_user(user_id=1, role=UserRole.ADMIN)

        async def fake_admin() -> object:
            return admin

        fake_uc = MagicMock()
        fake_uc.get_user = MagicMock()
        fake_uc.get_user.execute = AsyncMock(
            side_effect=UserNotFoundException("User", 999)
        )

        app.dependency_overrides[get_logged_admin_user] = fake_admin
        app.dependency_overrides[get_user_use_cases] = lambda: fake_uc
        try:
            r = await async_client.get(f"{USERS}/999")
            assert r.status_code == 404
        finally:
            app.dependency_overrides.pop(get_logged_admin_user, None)
            app.dependency_overrides.pop(get_user_use_cases, None)
