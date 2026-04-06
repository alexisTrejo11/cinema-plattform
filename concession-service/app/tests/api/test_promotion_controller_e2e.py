"""
HTTP integration tests for `/api/v2/promotions` (promotion_controller).

Covers 2xx happy paths, 4xx validation/domain errors, and auth (401/403).
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest

PROMOTIONS = "/api/v2/promotions"


def _promotion_create_payload(sample_product, *, name: str = "E2E Promo Test") -> dict:
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "promotion_type": "PERCENTAGE_DISCOUNT",
        "applicable_product_ids": [str(sample_product.id.value)],
        "applicable_category_id": None,
        "rule": {
            "min_quantity": 1,
            "min_percentage_discount": "10",
        },
        "start_date": (now - timedelta(days=1)).isoformat(),
        "end_date": (now + timedelta(days=60)).isoformat(),
        "description": "E2E integration test promotion",
        "is_active": True,
        "max_uses": 100,
    }


@pytest.mark.asyncio
class TestPromotionControllerA_Read:
    async def test_get_active_promotions_200(self, async_client):
        r = await async_client.get(
            f"{PROMOTIONS}/active",
            params={"page": 1, "page_size": 10},
        )
        assert r.status_code == 200
        body = r.json()
        assert "promotions" in body
        assert "paginationMetadata" in body

    async def test_get_promotion_by_id_404(self, async_client):
        r = await async_client.get(f"{PROMOTIONS}/{uuid4()}")
        assert r.status_code == 404

    async def test_get_promotions_by_product_200(self, async_client, sample_product):
        r = await async_client.get(
            f"{PROMOTIONS}/product/{sample_product.id.value}",
            params={"page": 1, "page_size": 10, "include_products": "false"},
        )
        assert r.status_code == 200


@pytest.mark.asyncio
class TestPromotionControllerB_Write:
    async def test_create_promotion_201(
        self, async_client, sample_product, admin_headers
    ):
        r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(sample_product),
            headers=admin_headers,
        )
        assert r.status_code == 201
        raw = r.json()
        assert raw is not None
        UUID(str(raw))

    async def test_create_promotion_401(self, async_client, sample_product):
        r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(sample_product),
        )
        assert r.status_code == 401

    async def test_create_promotion_403(
        self, async_client, sample_product, customer_headers
    ):
        r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(sample_product),
            headers=customer_headers,
        )
        assert r.status_code == 403

    async def test_create_promotion_422_short_name(
        self, async_client, sample_product, admin_headers
    ):
        p = _promotion_create_payload(sample_product, name="bad")
        r = await async_client.post(f"{PROMOTIONS}/", json=p, headers=admin_headers)
        assert r.status_code == 422

    async def test_get_promotion_by_id_200(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(
                sample_product, name="E2E Get By Id Promotion"
            ),
            headers=admin_headers,
        )
        assert create_r.status_code == 201
        pid = UUID(str(create_r.json()))

        r = await async_client.get(f"{PROMOTIONS}/{pid}")
        assert r.status_code == 200
        assert r.json()["name"] == "E2E Get By Id Promotion"

    async def test_deactivate_promotion_204(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(
                sample_product, name="E2E Deactivate Promotion"
            ),
            headers=admin_headers,
        )
        pid = UUID(str(create_r.json()))

        r = await async_client.patch(
            f"{PROMOTIONS}/{pid}/deactivate",
            headers=admin_headers,
        )
        assert r.status_code == 204

    async def test_deactivate_promotion_401(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(
                sample_product, name="E2E Deactivate Auth Promotion"
            ),
            headers=admin_headers,
        )
        pid = UUID(str(create_r.json()))

        r = await async_client.patch(f"{PROMOTIONS}/{pid}/deactivate")
        assert r.status_code == 401

    async def test_delete_promotion_204(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(sample_product, name="E2E Delete Promotion"),
            headers=admin_headers,
        )
        pid = UUID(str(create_r.json()))

        r = await async_client.delete(f"{PROMOTIONS}/{pid}", headers=admin_headers)
        assert r.status_code == 204

    async def test_delete_promotion_401(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(
                sample_product, name="E2E Delete Auth Promotion"
            ),
            headers=admin_headers,
        )
        pid = UUID(str(create_r.json()))

        r = await async_client.delete(f"{PROMOTIONS}/{pid}")
        assert r.status_code == 401


@pytest.mark.asyncio
class TestPromotionControllerC_ApplyPatch:
    async def test_apply_promotion_204(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_create_payload(sample_product, name="E2E Apply Promotion"),
            headers=admin_headers,
        )
        pid = UUID(str(create_r.json()))

        r = await async_client.patch(
            f"{PROMOTIONS}/{pid}/apply",
            json={"product_ids": [str(sample_product.id.value)]},
        )
        assert r.status_code == 204
