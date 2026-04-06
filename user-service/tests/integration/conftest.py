"""Fixtures for HTTP integration tests."""

from __future__ import annotations

from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from app.config.postgres_config import get_db


@pytest.fixture(autouse=True)
def patch_startup_and_limits(monkeypatch: pytest.MonkeyPatch) -> None:
    async def noop(*_args: Any, **_kwargs: Any) -> None:
        return None

    monkeypatch.setattr("main.init_cache", noop)
    monkeypatch.setattr("main.close_cache", noop)
    monkeypatch.setattr("main.run_postgres_startup_check", noop)

    def fake_limit(*_a: Any, **_kw: Any):
        def decorator(func: Any):
            return func

        return decorator

    monkeypatch.setattr("main.limiter.limit", fake_limit)


@pytest.fixture
async def async_client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
