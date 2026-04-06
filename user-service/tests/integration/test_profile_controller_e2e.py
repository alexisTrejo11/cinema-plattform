"""Integration tests for `/api/v2/profiles/`."""

from __future__ import annotations

import pytest

from app.users.infrastructure.persistence.sqlalch_user_repo import SQLAlchemyUserRepository

from tests.integration.jwt_helpers import bearer_headers, encode_access_token
from tests.integration.stubs import make_domain_user

PROFILES = "/api/v2/profiles"


@pytest.mark.asyncio
class TestProfileController:
    async def test_get_profile_401_without_bearer(self, async_client):
        r = await async_client.get(f"{PROFILES}/")
        assert r.status_code == 401

    async def test_get_profile_401_invalid_token(self, async_client):
        r = await async_client.get(
            f"{PROFILES}/", headers=bearer_headers("not-a-jwt")
        )
        assert r.status_code == 401

    async def test_get_profile_200(self, async_client, session):
        repo = SQLAlchemyUserRepository(session)
        user = make_domain_user()
        saved = await repo.save(user)
        token = encode_access_token(user_id=saved.id)

        r = await async_client.get(f"{PROFILES}/", headers=bearer_headers(token))
        assert r.status_code == 200
        body = r.json()
        assert body["first_name"] == saved.first_name
