from typing import Any, Dict
from tests.conftest import *
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.cinema.domain.entities import Cinema
from app.cinema.domain.value_objects import (
    CinemaAmenities,
    ContactInfo,
    Location,
    SocialMedia,
)
from app.cinema.infrastructure.persistence.sql_alch_repository import (
    SQLAlchemyCinemaRepository as CinemaRepository,
)
from app.cinema.domain.enums import (
    CinemaType,
    CinemaStatus,
    LocationRegion,
    CinemaFeatures,
)


@pytest_asyncio.fixture(scope="function")
async def cinema_repo(session: AsyncSession) -> CinemaRepository:
    return CinemaRepository(session)


@pytest.fixture
def sample_cinema():
    return Cinema(
        id=None,
        name="Sample Cinema",
        tax_number="1234567890",
        is_active=True,
        description="A test cinema",
        screens=5,
        last_renovation=date(2020, 1, 1),
        type=CinemaType.TRADITIONAL,
        status=CinemaStatus.CLOSED,
        region=LocationRegion.CDMX_CENTER,
        image="www.test-image.com",
        features=[CinemaFeatures.DOBLY_ATMOS, CinemaFeatures.IMAX],
        amenities=CinemaAmenities(parking=True),
        contact_info=ContactInfo(
            phone="+1234567890",
            email_contact="test-email@email.com",
            address="123 Sample Street",
            location=Location(lat=19.4326, lng=-99.1332),
        ),
        social_media=SocialMedia(
            facebook="https://facebook.com/samplecinema",
            instagram="https://instagram.com/samplecinema",
            x="https://x.com/samplecinema",
            tik_tok="https://tiktok.com/@samplecinema",
        ),
    )


@pytest.fixture
def updated_cinema_data() -> Dict[str, Any]:
    return {
        "name": "Updated Cinema Name",
        "description": "An updated cinema description",
        "is_active": False,
        "tax_number": "9876543210",
    }
