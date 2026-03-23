"""
End-to-end HTTP tests for the product API.

Covers happy paths (2xx), validation / domain errors (4xx), and auth (401/403).

Class names are ordered so read/update paths run before destructive delete tests.
"""

from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from app.products.infrastructure.persistence.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepository,
)

PRODUCTS = "/api/v2/products"


@pytest.mark.asyncio
class TestProductControllerA_Read:
    async def test_get_product_200(self, async_client, sample_product):
        pid = str(sample_product.id.value)
        r = await async_client.get(f"{PRODUCTS}/{pid}")

        assert r.status_code == 200
        body = r.json()

        assert body["name"] == sample_product.name
        assert UUID(body["id"]) == sample_product.id.value
        assert Decimal(str(body["price"])) == sample_product.price

    async def test_get_product_404(self, async_client):
        missing = uuid4()
        r = await async_client.get(f"{PRODUCTS}/{missing}")
        assert r.status_code == 404
        err = r.json()["error"]
        assert err["code"] == "PRODUCT_NOT_FOUND"

    async def test_get_product_invalid_uuid_422(self, async_client):
        r = await async_client.get(f"{PRODUCTS}/not-a-uuid")
        assert r.status_code == 422

    async def test_search_products_200(self, async_client, sample_product):
        r = await async_client.get(
            PRODUCTS + "/",
            params={
                "offset": 0,
                "limit": 10,
                "name_like": sample_product.name[:4],
            },
        )
        assert r.status_code == 200
        body = r.json()
        assert "product_page" in body
        assert "metadata" in body
        assert body["metadata"]["total_items"] >= 1
        ids = {p["id"] for p in body["product_page"]}
        assert str(sample_product.id.value) in ids

    async def test_search_invalid_limit_422(self, async_client):
        r = await async_client.get(PRODUCTS + "/", params={"limit": 0})
        assert r.status_code == 422


@pytest.mark.asyncio
class TestProductControllerB_Create:
    async def test_create_product_201(
        self, async_client, sample_category, admin_headers
    ):
        payload = {
            "name": "E2E Created Product",
            "description": "Created via API test",
            "price": 11.5,
            "image_url": "https://example.com/e2e.png",
            "is_available": True,
            "preparation_time_mins": 12,
            "calories": 400,
            "category_id": sample_category.id,
        }
        r = await async_client.post(PRODUCTS + "/", json=payload, headers=admin_headers)

        print(f"Response: {r.json()}")

        assert r.status_code == 201
        body = r.json()
        assert body["name"] == payload["name"]
        assert body["category_id"] == sample_category.id

    async def test_create_product_401_without_auth(self, async_client, sample_category):
        payload = {
            "name": "Unauthorized",
            "description": "x",
            "price": 9.99,
            "category_id": sample_category.id,
        }
        r = await async_client.post(PRODUCTS + "/", json=payload)
        assert r.status_code == 401

    async def test_create_product_403_wrong_role(
        self, async_client, sample_category, customer_headers
    ):
        payload = {
            "name": "Forbidden",
            "description": "x",
            "price": 9.99,
            "category_id": sample_category.id,
        }
        r = await async_client.post(
            PRODUCTS + "/", json=payload, headers=customer_headers
        )
        assert r.status_code == 403

    async def test_create_product_422_invalid_price(
        self, async_client, sample_category, admin_headers
    ):
        payload = {
            "name": "Bad price",
            "description": "x",
            "price": -1,
            "category_id": sample_category.id,
        }
        r = await async_client.post(PRODUCTS + "/", json=payload, headers=admin_headers)
        assert r.status_code == 422

    async def test_create_product_422_unknown_category(
        self, async_client, admin_headers
    ):
        payload = {
            "name": "No category",
            "description": "x",
            "price": 9.99,
            "category_id": 999999,
        }
        r = await async_client.post(PRODUCTS + "/", json=payload, headers=admin_headers)
        assert r.status_code == 422
        assert r.json()["error"]["code"] == "INVALID_CATEGORY_DATA"


@pytest.mark.asyncio
class TestProductControllerC_Update:
    async def test_update_product_200(
        self, async_client, sample_product, admin_headers
    ):
        pid = str(sample_product.id.value)
        payload = {
            "product_id": pid,
            "name": "Updated Via E2E",
            "description": sample_product.description,
        }
        r = await async_client.patch(
            f"{PRODUCTS}/{pid}",
            json=payload,
            headers=admin_headers,
        )
        assert r.status_code == 200
        assert r.json()["name"] == "Updated Via E2E"

    async def test_update_product_401(self, async_client, sample_product):
        pid = str(sample_product.id.value)
        r = await async_client.patch(
            f"{PRODUCTS}/{pid}",
            json={"product_id": pid, "name": "Nope"},
        )
        assert r.status_code == 401

    async def test_update_product_404(self, async_client, admin_headers):
        missing = uuid4()
        mid = str(missing)
        r = await async_client.patch(
            f"{PRODUCTS}/{missing}",
            json={"product_id": mid, "name": "Ghost"},
            headers=admin_headers,
        )
        assert r.status_code == 404


@pytest.mark.asyncio
class TestProductControllerD_Delete:
    async def test_delete_product_204_no_content(
        self, async_client, session, another_product, admin_headers
    ):
        repo = SQLAlchemyProductRepository(session)
        await repo.save(another_product)
        pid = str(another_product.id.value)

        r = await async_client.delete(f"{PRODUCTS}/{pid}", headers=admin_headers)
        assert r.status_code == 204
        assert r.content == b""

        get_r = await async_client.get(f"{PRODUCTS}/{pid}")
        assert get_r.status_code == 404

    async def test_delete_product_401(self, async_client, sample_product):
        pid = str(sample_product.id.value)
        r = await async_client.delete(f"{PRODUCTS}/{pid}")
        assert r.status_code == 401

    async def test_delete_product_404(self, async_client, admin_headers):
        missing = uuid4()
        r = await async_client.delete(f"{PRODUCTS}/{missing}", headers=admin_headers)
        assert r.status_code == 404


@pytest.mark.asyncio
class TestProductControllerE_AuthRoles:
    async def test_manager_can_create(
        self, async_client, sample_category, manager_headers
    ):
        payload = {
            "name": "Manager Created",
            "description": "mgr",
            "price": 8.0,
            "category_id": sample_category.id,
        }
        r = await async_client.post(
            PRODUCTS + "/", json=payload, headers=manager_headers
        )
        assert r.status_code == 201
