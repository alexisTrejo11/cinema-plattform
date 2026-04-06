"""
HTTP integration tests for `/api/v2/combos`.

Covers 2xx happy paths, 4xx validation/domain errors, and auth (401/403).
"""

from uuid import UUID, uuid4

import pytest

COMBOS = "/api/v2/combos"


def _combo_create_payload(sample_product):
    pid = str(sample_product.id.value)
    return {
        "name": "E2E Combo Bundle",
        "description": "integration test combo",
        "price": 29.99,
        "discount_percentage": 15,
        "image_url": "https://example.com/combo-e2e.jpg",
        "is_available": True,
        "items": [
            {"product_id": pid, "quantity": 2},
            {"product_id": pid, "quantity": 1},
        ],
    }


@pytest.mark.asyncio
class TestComboControllerA_Read:
    async def test_get_combo_404(self, async_client):
        r = await async_client.get(f"{COMBOS}/{uuid4()}")
        assert r.status_code == 404

    async def test_get_combo_200(self, async_client, sample_product, admin_headers):
        create_r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )
        assert create_r.status_code == 201
        combo_id = create_r.json()
        if isinstance(combo_id, str):
            combo_id = UUID(combo_id)

        r = await async_client.get(f"{COMBOS}/{combo_id}")

        assert r.status_code == 200
        body = r.json()
        assert body["name"] == "E2E Combo Bundle"
        assert "items" in body

    async def test_list_active_combos_200(
        self, async_client, sample_product, admin_headers
    ):
        await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )
        r = await async_client.get(
            f"{COMBOS}/",
            params={"page": 1, "page_size": 10},
        )
        assert r.status_code == 200
        body = r.json()
        assert "items" in body
        assert "metadata" in body

    async def test_get_combos_by_product_200(
        self, async_client, sample_product, admin_headers
    ):
        await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )
        pid = str(sample_product.id.value)
        r = await async_client.get(
            f"{COMBOS}/by-product/{pid}",
            params={"page": 1, "page_size": 10, "include_items": "false"},
        )
        assert r.status_code == 200
        assert r.json()["metadata"]["total_items"] >= 1

    async def test_get_combos_by_product_unknown_product_422(self, async_client):
        r = await async_client.get(
            f"{COMBOS}/by-product/{uuid4()}",
            params={"page": 1, "page_size": 10},
        )
        assert r.status_code == 422


@pytest.mark.asyncio
class TestComboControllerB_Write:
    async def test_create_combo_201(self, async_client, sample_product, admin_headers):
        r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )
        assert r.status_code == 201
        assert r.json() is not None

    async def test_create_combo_401(self, async_client, sample_product):
        r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
        )
        assert r.status_code == 401

    async def test_create_combo_403(
        self, async_client, sample_product, customer_headers
    ):
        r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=customer_headers,
        )
        assert r.status_code == 403

    async def test_create_combo_422_invalid_items(
        self, async_client, sample_product, admin_headers
    ):
        p = _combo_create_payload(sample_product)
        p["items"] = []
        r = await async_client.post(f"{COMBOS}/", json=p, headers=admin_headers)
        assert r.status_code == 422


@pytest.mark.asyncio
class TestComboControllerC_DeleteRestore:
    async def test_delete_combo_204_and_restore(
        self, async_client, sample_product, admin_headers
    ):
        create_r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )
        assert create_r.status_code == 201
        combo_id = (
            UUID(create_r.json())
            if isinstance(create_r.json(), str)
            else create_r.json()
        )

        del_r = await async_client.delete(f"{COMBOS}/{combo_id}", headers=admin_headers)
        assert del_r.status_code == 204

        get_inactive = await async_client.get(f"{COMBOS}/{combo_id}")
        assert get_inactive.status_code == 404

        restore_r = await async_client.post(
            f"{COMBOS}/{combo_id}/restore",
            headers=admin_headers,
        )
        assert restore_r.status_code == 204

        get_active = await async_client.get(f"{COMBOS}/{combo_id}")

        assert get_active.status_code == 200
        assert get_active.json()["is_available"] is True

    async def test_delete_combo_401(self, async_client, sample_product, admin_headers):
        create_r = await async_client.post(
            f"{COMBOS}/",
            json=_combo_create_payload(sample_product),
            headers=admin_headers,
        )

        combo_id = (
            UUID(create_r.json())
            if isinstance(create_r.json(), str)
            else create_r.json()
        )

        r = await async_client.delete(f"{COMBOS}/{combo_id}")
        assert r.status_code == 401
