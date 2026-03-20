from datetime import datetime, timedelta
from decimal import Decimal

import pytest
import pytest_asyncio

from app.products.domain.entities.product import ProductId
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository as PromotionRepo,
)
from app.promotions.domain.promotion import (
    Promotion,
    PromotionId,
    ProductId as PromotionProductId,
    PromotionRule,
    PromotionType,
)


@pytest_asyncio.fixture(scope="function")
async def sample_promotion() -> Promotion:
    """Create a Promotion entity from sample data"""
    return Promotion(
        name="Test Promotion",
        promotion_type=PromotionType.FIXED_DISCOUNT,
        discount_value=Decimal("10.00"),
        applicable_product_ids=[PromotionProductId.generate()],
        rule=PromotionRule(
            min_quantity=2,
            min_purchase_amount=Decimal("50.00"),
            applicable_categories=["Test Category"],
            required_products=[ProductId.generate()],
        ),
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        description="This is a test promotion",
        is_active=True,
        id=PromotionId.generate(),
        max_uses=100,
        current_uses=0,
    )


@pytest.fixture(scope="function")
def promotion_repository(session) -> PromotionRepo:
    """Fixture to provide a promotion repository instance"""
    return PromotionRepo(session)


@pytest.fixture
def sample_promotion_data():
    return {
        "name": "Test Promotion",
        "promotion_type": PromotionType.FIXED_DISCOUNT,
        "discount_value": Decimal("10.00"),
        "applicable_product_ids": [ProductId.generate()],
        "rule": PromotionRule(
            min_quantity=2,
            min_purchase_amount=Decimal("50.00"),
            applicable_categories=["Test Category"],
            required_products=[ProductId.generate()],
        ),
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "description": "Test description",
        "is_active": True,
        "max_uses": 100,
        "current_uses": 0,
    }
