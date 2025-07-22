from tests.contest import *
import pytest
from decimal import Decimal
from uuid import UUID
from app.combos.domain.entities.combo import Combo, ComboItem
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import PaginationQuery


class TestSqlAlchemyComboRepository:
    @pytest.mark.asyncio
    async def test_get_by_id_with_items(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        # First save a product and combo
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)

        # Create and save combo
        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(sample_product, ComboItemId.generate(), item["quantity"])
                for item in sample_combo_data["items"]
            ],
        )
        saved_combo = await combo_repository.save(combo)

        # Test get_by_id with items
        query = GetComboByIdQuery(combo_id=saved_combo.id, include_items=True)
        retrieved_combo = await combo_repository.get_by_id(query)

        assert retrieved_combo is not None
        assert retrieved_combo.id == saved_combo.id
        assert retrieved_combo.name == sample_combo_data["name"]
        assert len(retrieved_combo.items) == 2
        assert retrieved_combo.items[0].product.id == sample_product.id

    @pytest.mark.asyncio
    async def test_get_by_id_without_items(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        # Save product and combo
        product_repo = SqlAlchProductRepository(session)
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
                ComboItem(sample_product, ComboItemId.generate(), item["quantity"])
                for item in sample_combo_data["items"]
            ],
        )
        saved_combo = await combo_repository.save(combo)

        # Test get_by_id without items
        query = GetComboByIdQuery(combo_id=saved_combo.id, include_items=False)
        retrieved_combo = await combo_repository.get_by_id(query)

        assert retrieved_combo is not None
        assert retrieved_combo.id == saved_combo.id
        assert retrieved_combo.items == []

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, combo_repository):
        non_existent_id = ComboId.generate()
        query = GetComboByIdQuery(combo_id=non_existent_id, include_items=True)
        result = await combo_repository.get_by_id(query)
        assert result is None

    @pytest.mark.asyncio
    async def test_list_by_product(
        self,
        combo_repository,
        session,
        sample_product,
        another_product,
        sample_combo_data,
    ):
        # Save products
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)
        await product_repo.save(another_product)

        # Create combos - one with sample_product, one with another_product
        combo1 = Combo(
            id=ComboId.generate(),
            name="Combo 1",
            description="Combo with sample product",
            price=Decimal("19.99"),
            discount_percentage=Decimal("10"),
            image_url="https://example.com/combo1.jpg",
            is_available=True,
            items=[ComboItem(sample_product, None, 2)],
        )

        combo2 = Combo(
            id=ComboId.generate(),
            name="Combo 2",
            description="Combo with another product",
            price=Decimal("29.99"),
            discount_percentage=Decimal("15"),
            image_url="https://example.com/combo2.jpg",
            is_available=True,
            items=[ComboItem(another_product, None, 1)],
        )

        await combo_repository.save(combo1)
        await combo_repository.save(combo2)

        # Test list_by_product
        query = GetCombosByProductIdQuery(
            product_id=sample_product.id, include_items=True
        )
        combos = await combo_repository.list_by_product(query)

        assert len(combos) == 1
        assert combos[0].name == "Combo 1"
        assert combos[0].items[0].product.id == sample_product.id

    @pytest.mark.asyncio
    async def test_list(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        # Save product
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)

        # Create multiple combos
        for i in range(5):
            combo = Combo(
                id=ComboId.generate(),
                name=f"Combo {i}",
                description=f"Description {i}",
                price=Decimal(f"{10 + i}.99"),
                discount_percentage=Decimal("10"),
                image_url=f"https://example.com/combo{i}.jpg",
                is_available=True,
                items=[ComboItem(sample_product, None, i + 1)],
            )
            await combo_repository.save(combo)

        # Test list with pagination
        pagination = PaginationQuery(limit=3, offset=1)
        combos = await combo_repository.list(pagination)

        assert len(combos) == 3
        assert combos[0].name == "Combo 1"
        assert combos[0].items[0].quantity == 2

    @pytest.mark.asyncio
    async def test_save_new_combo(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        # Save product first
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)

        # Create new combo
        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(sample_product, None, item["quantity"])
                for item in sample_combo_data["items"]
            ],
        )

        saved_combo = await combo_repository.save(combo)

        assert saved_combo.id is not None
        assert saved_combo.name == sample_combo_data["name"]
        assert len(saved_combo.items) == 2
        assert all(item.product.id == sample_product.id for item in saved_combo.items)

    @pytest.mark.asyncio
    async def test_save_update_combo(
        self,
        combo_repository,
        session,
        sample_product,
        another_product,
        sample_combo_data,
    ):
        # Save products
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)
        await product_repo.save(another_product)

        # Create initial combo
        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=sample_combo_data["is_available"],
            items=[
                ComboItem(sample_product, None, item["quantity"])
                for item in sample_combo_data["items"]
            ],
        )
        saved_combo = await combo_repository.save(combo)

        # Update combo
        updated_combo = Combo(
            id=saved_combo.id,
            name="Updated Name",
            description="Updated Description",
            price=Decimal("39.99"),
            discount_percentage=Decimal("20"),
            image_url="https://example.com/updated.jpg",
            is_available=False,
            items=[ComboItem(another_product, None, 3)],
        )
        updated_saved_combo = await combo_repository.save(updated_combo)

        assert updated_saved_combo.id == saved_combo.id
        assert updated_saved_combo.name == "Updated Name"
        assert updated_saved_combo.price == Decimal("39.99")
        assert len(updated_saved_combo.items) == 1
        assert updated_saved_combo.items[0].product.id == another_product.id

    @pytest.mark.asyncio
    async def test_soft_delete(
        self, combo_repository, session, sample_product, sample_combo_data
    ):
        # Save product
        product_repo = SqlAlchProductRepository(session)
        await product_repo.save(sample_product)

        # Create and save combo
        combo = Combo(
            id=ComboId.generate(),
            name=sample_combo_data["name"],
            description=sample_combo_data["description"],
            price=sample_combo_data["price"],
            discount_percentage=sample_combo_data["discount_percentage"],
            image_url=sample_combo_data["image_url"],
            is_available=True,
            items=[ComboItem(sample_product, None, 2)],
        )
        saved_combo = await combo_repository.save(combo)

        # Soft delete
        await combo_repository.soft_delete(saved_combo.id)

        # Verify deletion
        query = GetComboByIdQuery(combo_id=saved_combo.id, include_items=False)
        deleted_combo = await combo_repository.get_by_id(query)

        assert deleted_combo is not None
        assert deleted_combo.is_available is False
