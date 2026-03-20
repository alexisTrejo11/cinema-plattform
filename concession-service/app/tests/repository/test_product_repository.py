import pytest
import pytest_asyncio
from app.products.domain.entities.value_objects import ProductId
from app.products.application.queries import SearchProductsQuery


# --- Test Cases ---
class TestSqlAlchProductRepository:
    @pytest.mark.asyncio
    async def test_get_by_id(
        self, product_repository: SqlAlchemyProductRepository, sample_product
    ):
        # Save the product first
        saved_product = await product_repository.save(sample_product)

        # Test get_by_id
        retrieved_product = await product_repository.get_by_id(saved_product.id)

        assert retrieved_product is not None
        assert retrieved_product.id.value == saved_product.id.value
        assert retrieved_product.name == sample_product.name
        assert retrieved_product.description == sample_product.description

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, product_repository: SqlAlchemyProductRepository
    ):
        non_existent_id = ProductId.generate()
        assert await product_repository.get_by_id(non_existent_id) is None

    @pytest.mark.asyncio
    async def test_get_by_id_in(
        self,
        product_repository: SqlAlchemyProductRepository,
        sample_product,
        another_product,
    ):
        # Save multiple products
        saved_product1 = await product_repository.save(sample_product)
        saved_product2 = await product_repository.save(another_product)

        # Test get_by_id_in
        product_map = await product_repository.get_by_id_in(
            [saved_product1.id, saved_product2.id]
        )

        assert len(product_map) == 2
        assert saved_product1.id in product_map
        assert saved_product2.id in product_map
        assert product_map[saved_product1.id].name == sample_product.name
        assert product_map[saved_product2.id].name == another_product.name

    @pytest.mark.asyncio
    async def test_get_by_id_in_empty_list(self, product_repository):
        assert await product_repository.get_by_id_in([]) == {}

    @pytest.mark.asyncio
    async def test_get_by_id_in_with_nonexistent_ids(self, product_repository):
        non_existent_ids = [ProductId.generate(), ProductId.generate()]
        assert await product_repository.get_by_id_in(non_existent_ids) == {}

    @pytest.mark.asyncio
    async def test_save_new_product(self, product_repository, sample_product_data):
        product = Product(**sample_product_data)
        saved_product = await product_repository.save(product)

        assert saved_product.id is not None
        assert saved_product.name == sample_product_data["name"]
        assert saved_product.description == sample_product_data["description"]

    @pytest.mark.asyncio
    async def test_save_existing_product(self, product_repository, sample_product):
        # First save
        saved_product = await product_repository.save(sample_product)

        # Update and save again
        updated_product = Product(
            id=saved_product.id,
            name="Updated Name",
            description=saved_product.description,
            price=saved_product.price,
            calories=saved_product.calories,
            category_id=saved_product.category_id,
            preparation_time_mins=saved_product.preparation_time_mins,
            image_url=saved_product.image_url,
            is_available=saved_product.is_available,
        )
        updated_saved_product = await product_repository.save(updated_product)

        assert updated_saved_product.id == saved_product.id
        assert updated_saved_product.name == "Updated Name"
        assert updated_saved_product.description == saved_product.description

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository, sample_product):
        # First save
        saved_product = await product_repository.save(sample_product)

        # Delete
        await product_repository.delete(saved_product.id)

        # Verify deletion
        assert await product_repository.get_by_id(saved_product.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_product(self, product_repository):
        non_existent_id = ProductId.generate()
        # Should not raise an exception
        await product_repository.delete(non_existent_id)

    @pytest.mark.asyncio
    async def test_search_products(
        self, product_repository, sample_product, another_product
    ):
        # Save multiple products
        await product_repository.save(sample_product)
        await product_repository.save(another_product)

        # Test search with no filters
        query = SearchProductsQuery()
        results = await product_repository.search(query)

        assert len(results) >= 2

        # Test search by name
        query = SearchProductsQuery(name="Another")
        results = await product_repository.search(query)
        assert len(results) == 1
        assert results[0].name == another_product.name

        # Test search by price range
        query = SearchProductsQuery(min_price=20.0, max_price=30.0)
        results = await product_repository.search(query)
        assert len(results) >= 1
        assert results[0].price == another_product.price

        # Test search by category
        query = SearchProductsQuery(category=sample_product.category_id)
        results = await product_repository.search(query)
        assert len(results) >= 2

        # Test search with limit and offset
        query = SearchProductsQuery(limit=1, offset=0)
        results = await product_repository.search(query)
        assert len(results) == 1

        query = SearchProductsQuery(limit=1, offset=1)
        results = await product_repository.search(query)
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_search_products_active_only(
        self, product_repository, sample_product_data
    ):
        # Create an inactive product
        inactive_product_data = sample_product_data.copy()
        inactive_product_data["id"] = ProductId.generate()
        inactive_product_data["is_available"] = False
        inactive_product = Product(**inactive_product_data)
        await product_repository.save(inactive_product)

        # Create an active product
        active_product = Product(**sample_product_data)
        await product_repository.save(active_product)

        # Test with active_only=True
        query = SearchProductsQuery(active_only=True)
        results = await product_repository.search(query)
        assert len(results) >= 1
        assert all(p.is_available for p in results)

        # Test with active_only=False
        query = SearchProductsQuery(active_only=False)
        results = await product_repository.search(query)
        assert len(results) >= 2
