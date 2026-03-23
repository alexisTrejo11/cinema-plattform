"""Shared fixtures for HTTP / API integration tests."""

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from app.config.db.postgres_config import get_db
from app.config.security import AuthUserContext


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


@pytest.fixture(autouse=True)
def inject_test_auth_from_bearer_header(monkeypatch):
    """Map Authorization header to roles without real JWT (main app has no JWT middleware)."""

    def _get_current_user(request):
        auth = request.headers.get("authorization", "")
        if auth == "Bearer test-admin-token":
            return AuthUserContext(roles=["admin"])
        if auth == "Bearer test-manager-token":
            return AuthUserContext(roles=["manager"])
        if auth == "Bearer test-customer-token":
            return AuthUserContext(roles=["customer"])
        return None

    monkeypatch.setattr("app.config.security.get_current_user", _get_current_user)


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
    return {"Authorization": "Bearer test-admin-token"}


@pytest.fixture
def manager_headers():
    return {"Authorization": "Bearer test-manager-token"}


@pytest.fixture
def customer_headers():
    return {"Authorization": "Bearer test-customer-token"}
