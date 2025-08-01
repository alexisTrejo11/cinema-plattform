from datetime import datetime, timedelta
import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.postgres_config import Base
from app.combos.infrastructure.persistence.models import ComboModel, ComboItemModel
from app.products.infrastructure.persistence.db.sql.models import (
    ProductModel,
    ProductCategoryModel,
)

from typing import Any, Dict
from decimal import Decimal
from app.products.domain.entities.product import Product, ProductId
from app.products.infrastructure.persistence.db.repositories.sqlalchemy_product_repo import (
    SqlAlchemyProductRepository,
)
from app.combos.infrastructure.persistence.sqlalchemy_combo_repo import (
    SQLAlchemyComboRepository,
)


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/tests"


@pytest_asyncio.fixture(scope="function")
async def engine():

    engine = create_async_engine(TEST_DATABASE_URL, echo=False, connect_args={})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def sample_product_data(sample_category) -> Dict[str, Any]:
    """Create a sample product for testing"""
    return {
        "id": ProductId.generate(),
        "name": "Test Product",
        "description": "This is a test product",
        "price": Decimal("19.99"),
        "calories": 250,
        "category_id": sample_category.id,  # Use the actual category ID from the fixture
        "preparation_time_mins": 30,
        "image_url": "https://example.com/test-product.jpg",
        "is_available": True,
    }


@pytest_asyncio.fixture(scope="function")
async def sample_product(sample_product_data: Dict[str, Any], session) -> Product:
    """Create a Product entity from sample data"""
    product = Product(**sample_product_data)
    product_model = ProductModel(**product.to_dict())
    session.add(product_model)
    await session.commit()
    return product


@pytest_asyncio.fixture(scope="function")
async def another_product_data(sample_category) -> Dict[str, Any]:
    """Create another sample product for testing"""
    return {
        "id": ProductId.generate(),
        "name": "Another Test Product",
        "description": "This is another test product",
        "price": Decimal("29.99"),
        "calories": 300,
        "category_id": sample_category.id,
        "preparation_time_mins": 20,
        "image_url": "https://example.com/another-product.jpg",
        "is_available": True,
    }


@pytest_asyncio.fixture(scope="function")
async def another_product(another_product_data: Dict[str, Any]) -> Product:
    """Create another Product entity from sample data"""
    return Product(**another_product_data)


@pytest.fixture(scope="function")
def product_repository(session) -> SqlAlchemyProductRepository:
    """Fixture to provide a product repository instance"""
    return SqlAlchemyProductRepository(session)


@pytest_asyncio.fixture(scope="function")
async def sample_category(session):
    """Create a sample category for testing"""
    from app.products.infrastructure.persistence.db.sql.models import (
        ProductCategoryModel as CategoryModel,
    )

    category = CategoryModel(
        name="Test Category", description="Test Category Description"
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@pytest.fixture(scope="function")
def combo_repository(session) -> SQLAlchemyComboRepository:
    """Fixture to provide a combo repository instance"""
    return SQLAlchemyComboRepository(session)


@pytest.fixture(scope="function")
async def sample_combo_data(sample_product, sample_category) -> Dict[str, Any]:
    """Create a sample combo meal data"""
    return {
        "name": "Family Feast Bundle",
        "description": "Includes 2 large pizzas, garlic bread, and soda",
        "price": Decimal("29.99"),
        "discount_percentage": Decimal("15"),
        "image_url": "https://example.com/images/family-feast.jpg",
        "is_available": True,
        "items": [
            {"product_id": sample_product.id, "quantity": 2},
            {"product_id": sample_product.id, "quantity": 1},
        ],
    }


@pytest.fixture(scope="function")
async def sample_combo(sample_combo_data: Dict[str, Any]) -> ComboModel:
    """Create a ComboModel instance from sample data"""
    combo = ComboModel(
        name=sample_combo_data["name"],
        description=sample_combo_data["description"],
        price=sample_combo_data["price"],
        discount_percentage=sample_combo_data["discount_percentage"],
        image_url=sample_combo_data["image_url"],
        is_available=sample_combo_data["is_available"],
    )

    for item in sample_combo_data["items"]:
        combo_item = ComboItemModel(
            product_id=item["product_id"], quantity=item["quantity"]
        )
        combo.items.append(combo_item)

    return combo


# MOCK
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Provides an AsyncMock for the UserRepository."""
    return AsyncMock(spec=SqlAlchemyProductRepository)
