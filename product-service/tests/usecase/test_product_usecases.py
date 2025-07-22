from tests.contest import *
import pytest
from unittest.mock import MagicMock, AsyncMock
from decimal import Decimal
from uuid import UUID
from app.products.domain.exceptions import ProductNotFoundError, InvalidCategoryError
from app.products.application.queries import GetProductByIdQuery, SearchProductsQuery
from app.products.application.responses import ProductDetails
from app.products.application.commands import ProductCreateCommand, ProductUpdateCommand
from app.products.domain.entities.product import Product, ProductId
from app.products.application.usecases.container import (
    GetProductByIdUseCase,
    SearchProductUseCase,
    CreateProductUseCase,
    UpdateProductUseCase,
    SoftDeleteProductUseCase,
)

# MOCK
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Provides an AsyncMock for the UserRepository."""
    return AsyncMock(spec=SqlAlchProductRepository)


# UseCases Fixtures
@pytest.fixture
def product_domain_mock(sample_product_data: Dict[str, Any]) -> Product:
    """Fixture to provide a Product domain entity for testing"""
    product = MagicMock(spec=Product)

    # Mock the ProductId to return a specific value
    mock_product_id = MagicMock(spec=ProductId)
    mock_product_id.value = sample_product_data["id"].value
    mock_product_id.to_string.return_value = str(sample_product_data["id"].value)

    # Set properties/attributes instead of methods
    product.id = mock_product_id
    product.name = sample_product_data["name"]
    product.description = sample_product_data["description"]
    product.price = sample_product_data["price"]
    product.calories = sample_product_data["calories"]
    product.category_id = sample_product_data["category_id"]
    product.preparation_time_mins = sample_product_data[
        "preparation_time_mins"
    ]
    product.image_url = sample_product_data["image_url"]
    product.is_available = sample_product_data["is_available"]
    product.to_dict.return_value = {
        "id": sample_product_data["id"].value,
        "name": sample_product_data["name"],
        "description": sample_product_data["description"],
        "price": str(sample_product_data["price"]),
        "calories": sample_product_data["calories"],
        "category_id": sample_product_data["category_id"],
        "preparation_time_mins": sample_product_data["preparation_time_mins"],
        "image_url": sample_product_data["image_url"],
        "is_available": sample_product_data["is_available"],
    }
    return product


@pytest.fixture
def another_domain_product() -> Product:
    product = MagicMock(spec=Product)
    new_id = ProductId.generate()
    product.id = new_id
    product.name = "Another Test Product"
    product.description = "This is another test product"
    product.price = Decimal("29.99")
    product.calories = 300
    product.preparation_time_mins = 20
    product.image_url = "https://example.com/another-product.jpg"
    product.is_available = True
    product.category_id = 1
    product.to_dict.return_value = {
        "id": new_id.value,
        "name": "Another Test Product",
        "description": "This is another test product",
        "price": "29.99",
        "calories": 300,
        "preparation_time_mins": 20,
        "image_url": "https://example.com/another-product.jpg",
        "is_available": True,
        "category_id": 1,
    }
    return product


@pytest.mark.asyncio
class TestGetProductByIdUseCase:
    async def test_execute_success(self, product_domain_mock):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = product_domain_mock

        use_case = GetProductByIdUseCase(mock_repo)
        query = GetProductByIdQuery(product_id=product_domain_mock.id)

        # Execute
        result = await use_case.execute(query)

        # Verify
        mock_repo.get_by_id.assert_called_once_with(query.product_id)
        assert isinstance(result, ProductDetails)
        assert str(result.id) == str(product_domain_mock.id.value)
        assert result.name == product_domain_mock.name

    async def test_execute_product_not_found(self, product_domain_mock):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        use_case = GetProductByIdUseCase(mock_repo)
        query = GetProductByIdQuery(product_id=product_domain_mock.id)

        # Execute & Verify
        with pytest.raises(ProductNotFoundError):
            await use_case.execute(query)


@pytest.mark.asyncio
class TestSearchProductUseCase:
    async def test_execute_success(self, product_domain_mock, another_domain_product):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.search.return_value = [product_domain_mock, another_domain_product]

        use_case = SearchProductUseCase(mock_repo)
        query = SearchProductsQuery(name="Test")

        # Execute
        results = await use_case.execute(query)

        # Verify
        mock_repo.search.assert_awaited_once_with(query)
        assert len(results) == 2
        assert isinstance(results[0], ProductDetails)
        assert results[0].name == product_domain_mock.name
        assert results[1].name == another_domain_product.name

    async def test_execute_empty_results(self):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.search.return_value = []

        use_case = SearchProductUseCase(mock_repo)
        query = SearchProductsQuery(name="Nonexistent")

        # Execute
        results = await use_case.execute(query)

        # Verify
        assert len(results) == 0


@pytest.mark.asyncio
class TestCreateProductUseCase:
    async def test_execute_success(self, sample_product_data):
        # Setup
        mock_product_repo = AsyncMock()
        mock_category_repo = MagicMock()
        mock_category_repo.exists_by_id.return_value = True

        create_data = ProductCreateCommand(
            name=sample_product_data["name"],
            description=sample_product_data["description"],
            price=float(sample_product_data["price"]),  # Convert to float for schema compatibility
            calories=sample_product_data["calories"],
            category_id=sample_product_data["category_id"],
            preparation_time_mins=sample_product_data["preparation_time_mins"],
            image_url=sample_product_data["image_url"],
            is_available=sample_product_data["is_available"],
        )

        # Mock the saved product
        saved_product = MagicMock(spec=Product)
        saved_product_id = ProductId.generate()
        saved_product.id = saved_product_id
        saved_product.to_dict.return_value = {
            "name": sample_product_data["name"],
            "description": sample_product_data["description"],
            "price": str(sample_product_data["price"]),
            "calories": sample_product_data["calories"],
            "category_id": sample_product_data["category_id"],
            "preparation_time_mins": sample_product_data["preparation_time_mins"],
            "image_url": sample_product_data["image_url"],
            "is_available": sample_product_data["is_available"],
        }
        mock_product_repo.save.return_value = saved_product

        use_case = CreateProductUseCase(mock_product_repo, mock_category_repo)

        # Execute
        result = await use_case.execute(create_data)

        # Verify
        mock_category_repo.exists_by_id.assert_called_once_with(create_data.category_id)
        mock_product_repo.save.assert_awaited_once()
        assert isinstance(result, ProductDetails)

    async def test_execute_invalid_category(self, sample_product_data):
        # Setup
        mock_product_repo = AsyncMock()
        mock_category_repo = MagicMock()
        mock_category_repo.exists_by_id.return_value = False

        create_data = ProductCreateCommand(
            category_id=999,  # Invalid category
            name=sample_product_data["name"],
            description=sample_product_data["description"],
            price=float(sample_product_data["price"]),  # Convert to float for schema compatibility
            calories=sample_product_data["calories"],
            preparation_time_mins=sample_product_data["preparation_time_mins"],
            image_url=sample_product_data["image_url"],
            is_available=sample_product_data["is_available"],
        )

        use_case = CreateProductUseCase(mock_product_repo, mock_category_repo)

        # Execute & Verify
        with pytest.raises(InvalidCategoryError):
            await use_case.execute(create_data)

        mock_product_repo.save.assert_not_awaited()


@pytest.mark.asyncio
class TestUpdateProductUseCase:
    async def test_execute_success(self, product_domain_mock, sample_product_data):
        # Setup
        mock_product_repo = AsyncMock()
        mock_category_repo = MagicMock()
        mock_category_repo.exists_by_id.return_value = True
        mock_product_repo.get_by_id.return_value = product_domain_mock

        update_data = ProductUpdateCommand(
            product_id=product_domain_mock.id,
            name="Updated Name",
            price=39.99,  # Use float for schema compatibility
            is_available=False,
        )

        use_case = UpdateProductUseCase(mock_product_repo, mock_category_repo)

        # Mock updating the product details and returning
        product_domain_mock.name = "Updated Name"
        product_domain_mock.to_dict.return_value["name"] = "Updated Name"

        # Execute
        result = await use_case.execute(update_data)

        # Verify
        mock_product_repo.get_by_id.assert_awaited_once_with(update_data.product_id)
        mock_product_repo.save.assert_awaited_once_with(product_domain_mock)
        assert isinstance(result, ProductDetails)
        assert result.name == "Updated Name"

    async def test_execute_product_not_found(self, product_domain_mock):
        # Setup
        mock_product_repo = AsyncMock()
        mock_category_repo = MagicMock()
        mock_product_repo.get_by_id.return_value = None

        update_data = ProductUpdateCommand(
            product_id=product_domain_mock.id, name="Updated Name"
        )

        use_case = UpdateProductUseCase(mock_product_repo, mock_category_repo)

        # Execute & Verify
        with pytest.raises(ProductNotFoundError):
            await use_case.execute(update_data)

        mock_product_repo.save.assert_not_awaited()

    async def test_execute_invalid_category(self, product_domain_mock):
        # Setup
        mock_product_repo = AsyncMock()
        mock_category_repo = MagicMock()
        mock_category_repo.exists_by_id.return_value = False
        mock_product_repo.get_by_id.return_value = product_domain_mock

        update_data = ProductUpdateCommand(
            product_id=product_domain_mock.id, category_id=999  # Invalid category
        )

        use_case = UpdateProductUseCase(mock_product_repo, mock_category_repo)

        # Execute & Verify
        with pytest.raises(InvalidCategoryError):
            await use_case.execute(update_data)

        mock_product_repo.save.assert_not_awaited()


@pytest.mark.asyncio
class TestSoftDeleteProductUseCase:
    async def test_execute_success(self, product_domain_mock):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = product_domain_mock

        use_case = SoftDeleteProductUseCase(mock_repo)

        # Execute
        await use_case.execute(product_domain_mock.id)

        # Verify
        mock_repo.get_by_id.assert_awaited_once_with(product_domain_mock.id)
        mock_repo.delete.assert_awaited_once_with(product_domain_mock.id)

    async def test_execute_product_not_found(self, product_domain_mock):
        # Setup
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        use_case = SoftDeleteProductUseCase(mock_repo)

        # Execute & Verify
        with pytest.raises(ProductNotFoundError):
            await use_case.execute(product_domain_mock.id)

        mock_repo.delete.assert_not_awaited()
