"""
HTTP integration tests for `/api/v2/categories`.

Covers 2xx happy paths, 4xx validation/domain errors, and auth (401/403).
"""

import pytest

CATEGORIES = "/api/v2/categories"


@pytest.mark.asyncio
class TestCategoryControllerA_Read:
    async def test_get_category_200(self, async_client, sample_category):
        r = await async_client.get(f"{CATEGORIES}/{sample_category.id}")
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == sample_category.id
        assert body["name"] == sample_category.name

    async def test_get_category_404(self, async_client):
        r = await async_client.get(f"{CATEGORIES}/999999")
        assert r.status_code == 404

    async def test_list_categories_200(self, async_client, sample_category):
        r = await async_client.get(f"{CATEGORIES}/")
        assert r.status_code == 200
        body = r.json()
        assert isinstance(body, list)
        ids = {c["id"] for c in body}
        assert sample_category.id in ids


@pytest.mark.asyncio
class TestCategoryControllerB_Write:
    async def test_create_category_201(self, async_client, admin_headers):
        payload = {
            "name": "E2E Category Create",
            "description": "Created via API test",
            "is_active": True,
        }
        r = await async_client.post(
            f"{CATEGORIES}/", json=payload, headers=admin_headers
        )
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == payload["name"]
        assert "id" in body

    async def test_create_category_401(self, async_client):
        r = await async_client.post(
            f"{CATEGORIES}/",
            json={"name": "No Auth", "description": "x", "is_active": True},
        )
        assert r.status_code == 401

    async def test_create_category_403(self, async_client, customer_headers):
        r = await async_client.post(
            f"{CATEGORIES}/",
            json={"name": "Forbidden", "description": "x", "is_active": True},
            headers=customer_headers,
        )
        assert r.status_code == 403

    async def test_create_category_422_empty_name(self, async_client, admin_headers):
        r = await async_client.post(
            f"{CATEGORIES}/",
            json={"name": "", "description": "x", "is_active": True},
            headers=admin_headers,
        )
        assert r.status_code == 422

    async def test_create_category_409_duplicate_name(
        self, async_client, admin_headers
    ):
        name = "Unique E2E Category Name"
        payload = {"name": name, "description": "d", "is_active": True}
        r1 = await async_client.post(
            f"{CATEGORIES}/", json=payload, headers=admin_headers
        )
        assert r1.status_code == 201
        r2 = await async_client.post(
            f"{CATEGORIES}/", json=payload, headers=admin_headers
        )
        assert r2.status_code == 409

    async def test_update_category_200(self, async_client, sample_category, admin_headers):
        payload = {
            "name": "Updated Category Name",
            "description": sample_category.description or "desc",
            "is_active": True,
        }
        r = await async_client.put(
            f"{CATEGORIES}/{sample_category.id}",
            json=payload,
            headers=admin_headers,
        )
        assert r.status_code == 200
        assert r.json()["name"] == "Updated Category Name"

    async def test_update_category_401(self, async_client, sample_category):
        r = await async_client.put(
            f"{CATEGORIES}/{sample_category.id}",
            json={"name": "Nope", "description": "x", "is_active": True},
        )
        assert r.status_code == 401

    async def test_update_category_404(self, async_client, admin_headers):
        r = await async_client.put(
            f"{CATEGORIES}/999999",
            json={"name": "Ghost", "description": "x", "is_active": True},
            headers=admin_headers,
        )
        assert r.status_code == 404


@pytest.mark.asyncio
class TestCategoryControllerC_Delete:
    async def test_delete_category_204(self, async_client, session, admin_headers):
        from app.products.infrastructure.persistence.models.product_models import (
            ProductCategoryModel,
        )

        cat = ProductCategoryModel(
            name="E2E Delete Me Category",
            description="to delete",
            is_active=True,
        )
        session.add(cat)
        await session.commit()
        await session.refresh(cat)

        r = await async_client.delete(f"{CATEGORIES}/{cat.id}", headers=admin_headers)
        assert r.status_code == 204

        get_r = await async_client.get(f"{CATEGORIES}/{cat.id}")
        assert get_r.status_code == 200
        assert get_r.json()["is_active"] is False

    async def test_delete_category_401(self, async_client, sample_category):
        r = await async_client.delete(f"{CATEGORIES}/{sample_category.id}")
        assert r.status_code == 401
