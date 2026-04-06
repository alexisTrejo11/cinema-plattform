"""
HTTP integration tests for `/api/v2/promotions` item routes (promotion_items_controller).

These endpoints add/remove products and categories on promotions (no auth required).
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

PROMOTIONS = "/api/v2/promotions"


def _promotion_without_products(*, name: str) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "name": name,
        "promotion_type": "PERCENTAGE_DISCOUNT",
        "applicable_product_ids": None,
        "applicable_category_id": None,
        "rule": {
            "min_quantity": 1,
            "min_percentage_discount": "10",
        },
        "start_date": (now - timedelta(days=1)).isoformat(),
        "end_date": (now + timedelta(days=60)).isoformat(),
        "description": "E2E promotion items test",
        "is_active": True,
        "max_uses": 100,
    }


@pytest.mark.asyncio
class TestPromotionItemsProducts:
    async def test_add_products_to_promotion_204(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_without_products(name="E2E Items Add Products"),
            headers=admin_headers,
        )
        assert create_r.status_code == 201
        promo_id = UUID(str(create_r.json()))

        r = await async_client.post(
            f"{PROMOTIONS}/products/add",
            json={
                "product_ids": [str(sample_product.id.value)],
                "promotion_id": str(promo_id),
            },
        )
        assert r.status_code == 204

    async def test_remove_products_from_promotion(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_without_products(name="E2E Items Remove Products"),
            headers=admin_headers,
        )
        promo_id = UUID(str(create_r.json()))

        await async_client.post(
            f"{PROMOTIONS}/products/add",
            json={
                "product_ids": [str(sample_product.id.value)],
                "promotion_id": str(promo_id),
            },
        )

        r = await async_client.request(
            "DELETE",
            f"{PROMOTIONS}/products/remove",
            json={
                "product_ids": [str(sample_product.id.value)],
                "promotion_id": str(promo_id),
            },
        )
        assert r.status_code in (200, 204)


@pytest.mark.asyncio
class TestPromotionItemsCategories:
    async def test_add_and_remove_category(
        self, async_client, sample_category, admin_headers
    ):
        create_r = await async_client.post(
            f"{PROMOTIONS}/",
            json=_promotion_without_products(name="E2E Items Category"),
            headers=admin_headers,
        )
        promo_id = UUID(str(create_r.json()))

        add_r = await async_client.post(
            f"{PROMOTIONS}/categories/add",
            json={
                "category_id": sample_category.id,
                "promotionId": str(promo_id),
            },
        )
        assert add_r.status_code in (200, 204)

        rem_r = await async_client.request(
            "DELETE",
            f"{PROMOTIONS}/categories/remove",
            json={
                "category_id": sample_category.id,
                "promotionId": str(promo_id),
            },
        )
        assert rem_r.status_code in (200, 204)
