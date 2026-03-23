"""Shared fixtures for HTTP / API integration tests."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from app.config.app_config import settings
from app.config.db.postgres_config import get_db


def _encode_test_jwt(roles: list[str]) -> str:
    """HS256 token signed with app JWT_SECRET_KEY; matches jwt_auth_middleware validation."""
    now = datetime.now(timezone.utc)
    payload: dict = {
        "sub": "e2e-test-user",
        "roles": roles,
        "iat": now,
        "exp": now + timedelta(hours=1),
    }
    if settings.JWT_AUDIENCE:
        payload["aud"] = settings.JWT_AUDIENCE
    if settings.JWT_ISSUER:
        payload["iss"] = settings.JWT_ISSUER
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


@pytest.fixture(autouse=True)
def patch_redis_lifecycle(monkeypatch):
    async def noop():
        return None

    monkeypatch.setattr("main.init_cache", noop)
    monkeypatch.setattr("main.close_cache", noop)


@pytest.fixture(autouse=True)
def disable_route_rate_limits(monkeypatch):
    def fake_limit(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    for mod in (
        "app.products.infrastructure.api.controllers.product_controller",
        "app.products.infrastructure.api.controllers.category_controller",
        "app.combos.infrastructure.api.combo_controllers",
        "app.promotions.infrastructure.api.controllers.promotion_controller",
        "app.promotions.infrastructure.api.controllers.promotion_items_controller",
    ):
        monkeypatch.setattr(f"{mod}.limiter.limit", fake_limit)


@pytest.fixture
async def async_client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_headers():
    return {"Authorization": f"Bearer {_encode_test_jwt(['admin'])}"}


@pytest.fixture
def manager_headers():
    return {"Authorization": f"Bearer {_encode_test_jwt(['manager'])}"}


@pytest.fixture
def customer_headers():
    return {"Authorization": f"Bearer {_encode_test_jwt(['customer'])}"}
