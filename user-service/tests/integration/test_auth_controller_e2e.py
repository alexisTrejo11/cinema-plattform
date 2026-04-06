"""Integration tests for `/api/v2/auth/*`."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from main import app
from app.auth.infrastructure.api.dependencies import get_auth_use_cases
from app.shared.response import Result


@pytest.mark.asyncio
class TestAuthController:
    async def test_signup_422_empty_body(self, async_client):
        r = await async_client.post("/api/v2/auth/signup", json={})
        assert r.status_code == 422

    async def test_login_422_empty_body(self, async_client):
        r = await async_client.post("/api/v2/auth/login", json={})
        assert r.status_code == 422

    async def test_signup_400_when_use_case_fails(self, async_client, monkeypatch):
        fake = MagicMock()
        fake.execute = AsyncMock(return_value=Result.error("email taken"))
        container = MagicMock()
        container.signup = fake

        app.dependency_overrides[get_auth_use_cases] = lambda: container
        try:
            r = await async_client.post(
                "/api/v2/auth/signup",
                json={
                    "email": "new@example.com",
                    "password": "Str0ng!Pass",
                    "phone_number": "1234567890",
                    "gender": "MALE",
                    "first_name": "New",
                    "last_name": "User",
                    "date_of_birth": "1995-06-01",
                },
            )
            assert r.status_code == 400
        finally:
            app.dependency_overrides.pop(get_auth_use_cases, None)

    async def test_logout_401_without_token(self, async_client):
        r = await async_client.post(
            "/api/v2/auth/logout",
            json={"refresh_token": "dummy"},
        )
        assert r.status_code == 401
