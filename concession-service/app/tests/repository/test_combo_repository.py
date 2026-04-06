from decimal import Decimal

import pytest

from app.combos.domain.entities.combo import Combo, ComboItem
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.combos.infrastructure.persistence.sqlalchemy_combo_repo import (
    SQLAlchemyComboRepository,
)
from app.products.infrastructure.persistence.repositories.sqlalchemy_product_repo import (
    SqlAlchemyProductRepository,
)
from app.shared.pagination import PaginationQuery


class TestSQLAlchemyComboRepository:
    @pytest.mark.asyncio
    async def test_find_by_id_with_items(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=item["quantity"],
                )
                for item in sample_combo_data["items"]
            ],
        )
        await combo_repository.save(combo)

        retrieved_combo = await combo_repository.find_by_id(combo.id, include_items=True)

        assert retrieved_combo is not None
        assert retrieved_combo.id == combo.id
        assert retrieved_combo.name == sample_combo_data["name"]
        assert len(retrieved_combo.items) == 2
        assert retrieved_combo.items[0].product.id == sample_product.id

    @pytest.mark.asyncio
    async def test_find_by_id_ignores_include_items_flag_current_impl(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        """Repository always maps items when loading by id (include_items is not applied)."""
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=item["quantity"],
                )
                for item in sample_combo_data["items"]
            ],
        )
        await combo_repository.save(combo)

        retrieved_combo = await combo_repository.find_by_id(combo.id, include_items=False)

        assert retrieved_combo is not None
        assert len(retrieved_combo.items) == 2

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, combo_repository):
        non_existent_id = ComboId.generate()
        result = await combo_repository.find_by_id(non_existent_id, include_items=True)
        assert result is None

    @pytest.mark.asyncio
    async def test_find_by_product_with_items(
        self,
        combo_repository,
        session,
        sample_product,
        another_product,
        sample_combo_data,
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)
        await product_repo.save(another_product)

        combo1 = Combo(
            id=ComboId.generate(),
            name="Combo 1",
            description="Combo with sample product",
            price=Decimal("19.99"),
            discount_percentage=Decimal("10"),
            image_url="https://example.com/combo1.jpg",
            is_available=True,
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=2,
                )
            ],
        )

        combo2 = Combo(
            id=ComboId.generate(),
            name="Combo 2",
            description="Combo with another product",
            price=Decimal("29.99"),
            discount_percentage=Decimal("15"),
            image_url="https://example.com/combo2.jpg",
            is_available=True,
            items=[
                ComboItem(
                    product=another_product,
                    id=ComboItemId.generate(),
                    quantity=1,
                )
            ],
        )

        await combo_repository.save(combo1)
        await combo_repository.save(combo2)

        page = await combo_repository.find_by_product(
            sample_product.id,
            PaginationQuery(page=1, page_size=10),
            include_items=True,
        )

        assert len(page.items) == 1
        assert page.items[0].name == "Combo 1"
        assert page.items[0].items[0].product.id == sample_product.id

    @pytest.mark.asyncio
    async def test_find_by_product_without_items(
        self,
        combo_repository,
        session,
        sample_product,
        sample_combo_data,
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=item["quantity"],
                )
                for item in sample_combo_data["items"]
            ],
        )
        await combo_repository.save(combo)

        page = await combo_repository.find_by_product(
            sample_product.id,
            PaginationQuery(page=1, page_size=10),
            include_items=False,
        )

        assert len(page.items) == 1
        assert page.items[0].items == []

    @pytest.mark.asyncio
    async def test_find_active(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        for i in range(5):
            combo = Combo(
                id=ComboId.generate(),
                name=f"Combo {i}",
                description=f"Description {i}",
                price=Decimal(f"{10 + i}.99"),
                discount_percentage=Decimal("10"),
                image_url=f"https://example.com/combo{i}.jpg",
                is_available=True,
                items=[
                    ComboItem(
                        product=sample_product,
                        id=ComboItemId.generate(),
                        quantity=i + 1,
                    )
                ],
            )
            await combo_repository.save(combo)

        page = await combo_repository.find_active(
            PaginationQuery(page=2, page_size=3),
        )

        assert len(page.items) == 2
        assert page.items[0].name == "Combo 3"

    @pytest.mark.asyncio
    async def test_save_new_combo(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=item["quantity"],
                )
                for item in sample_combo_data["items"]
            ],
        )

        await combo_repository.save(combo)

        loaded = await combo_repository.find_by_id(combo.id, include_items=True)
        assert loaded is not None
        assert loaded.name == sample_combo_data["name"]
        assert len(loaded.items) == 2
        assert all(item.product.id == sample_product.id for item in loaded.items)

    @pytest.mark.asyncio
    async def test_save_update_combo(
        self,
        combo_repository,
        session,
        sample_product,
        another_product,
        sample_combo_data,
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)
        await product_repo.save(another_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=item["quantity"],
                )
                for item in sample_combo_data["items"]
            ],
        )
        await combo_repository.save(combo)

        updated_combo = Combo(
            id=combo.id,
            name="Updated Name",
            description="Updated Description",
            price=Decimal("39.99"),
            discount_percentage=Decimal("20"),
            image_url="https://example.com/updated.jpg",
            is_available=True,
            items=[
                ComboItem(
                    product=another_product,
                    id=ComboItemId.generate(),
                    quantity=3,
                )
            ],
        )
        await combo_repository.save(updated_combo)

        loaded = await combo_repository.find_by_id(combo.id, include_items=True)
        assert loaded is not None
        assert loaded.id == combo.id
        assert loaded.name == "Updated Name"
        assert loaded.price == Decimal("39.99")
        assert len(loaded.items) == 1
        assert loaded.items[0].product.id == another_product.id

    @pytest.mark.asyncio
    async def test_soft_delete(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        product_repo = SqlAlchemyProductRepository(session)
        await product_repo.save(sample_product)

        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=True,
            items=[
                ComboItem(
                    product=sample_product,
                    id=ComboItemId.generate(),
                    quantity=2,
                )
            ],
        )
        await combo_repository.save(combo)

        await combo_repository.delete(combo.id, soft_delete=True)

        assert await combo_repository.find_by_id(combo.id, include_items=False) is None

        deleted_combo = await combo_repository.find_deleted_by_id(combo.id)
        assert deleted_combo is not None
        assert deleted_combo.is_available is False
