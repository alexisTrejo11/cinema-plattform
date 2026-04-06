from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
import pytest_asyncio

from app.products.domain.entities.value_objects import ProductId
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository as PromotionRepo,
)
from app.promotions.domain.entities.promotion import Promotion
from app.promotions.domain.entities.value_objects import (
    PromotionId,
    PromotionType,
    ProductId as PromotionProductId,
)


@pytest_asyncio.fixture(scope="function")
async def sample_promotion() -> Promotion:
    return Promotion(
        name="Test Promotion",
        promotion_type=PromotionType.PERCENTAGE_DISCOUNT,
        rule={"min_discount": "10.00", "max_discount": "50.00"},
        applicable_product_ids=[PromotionProductId.generate()],
        applicable_categories_ids=[],
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=30),
        description="This is a test promotion",
        is_active=True,
        id=PromotionId.generate(),
        max_uses=100,
        current_uses=0,
    )


@pytest.fixture(scope="function")
def promotion_repository(session) -> PromotionRepo:
    return PromotionRepo(session)


@pytest.fixture
def sample_promotion_data():
    return {
        "name": "Test Promotion",
        "promotion_type": PromotionType.PERCENTAGE_DISCOUNT,
        "rule": {"min_discount": "10.00", "max_discount": "50.00"},
        "applicable_product_ids": [PromotionProductId.generate()],
        "applicable_categories_ids": [],
        "start_date": datetime.now(timezone.utc),
        "end_date": datetime.now(timezone.utc) + timedelta(days=30),
        "description": "Test description",
        "is_active": True,
        "max_uses": 100,
        "current_uses": 0,
    }
