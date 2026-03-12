from datetime import datetime, timezone
from app.core.cinema.domain.entities import Cinema
from app.core.cinema.domain.enums import CinemaFeatures
from app.core.cinema.domain.value_objects import (
    CinemaAmenities,
    ContactInfo,
    SocialMedia,
    Location,
)
from app.core.cinema.infrastructure.persistence.cinema_model import CinemaModel


class CinemaModelMapper:

    @staticmethod
    def from_domain(entity: Cinema) -> CinemaModel:
        """
        Converts a Cinema domain entity to a CinemaModel ORM model.

        Args:
            entity: Cinema domain entity

        Returns:
            CinemaModel: ORM model instance

        Raises:
            ValueError: If entity is not a Cinema instance
        """
        if not isinstance(entity, Cinema):
            raise ValueError("Entity must be a Cinema instance")

        amenities_data = entity.amenities.model_dump() if entity.amenities else {}
        contact_info_data = (
            entity.contact_info.model_dump() if entity.contact_info else {}
        )
        location_data = (
            entity.contact_info.location.model_dump()
            if entity.contact_info.location.model_dump()
            else {}
        )
        social_media_data = (
            entity.social_media.model_dump() if entity.social_media else {}
        )
        features_list = (
            [feature for feature in entity.features] if entity.features else []
        )

        orm_data = {
            "id": entity.id,
            "image": entity.image,
            "name": entity.name,
            "tax_number": entity.tax_number,
            "is_active": entity.is_active,
            "description": entity.description,
            "screens": entity.screens,
            "last_renovation": entity.last_renovation,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            # Enums
            "type": entity.type,
            "status": entity.status,
            "region": entity.region,
            # Amenities (flattened)
            "has_parking": amenities_data.get("parking", False),
            "has_food_court": amenities_data.get("food_court", False),
            "has_coffee_station": amenities_data.get("coffee_station", False),
            "has_disabled_access": amenities_data.get("disabled_access", False),
            # Contact info (flattened)
            "address": contact_info_data.get("address", ""),
            "phone": contact_info_data.get("phone", ""),
            "email_contact": contact_info_data.get("email_contact", ""),
            "latitude": location_data.get("lat", 0.0),
            "longitude": location_data.get("lng", 0.0),
            # Social media (flattened)
            "facebook_url": social_media_data.get("facebook"),
            "instagram_url": social_media_data.get("instagram"),
            "x_url": social_media_data.get("x"),
            "tik_tok_url": social_media_data.get("tik_tok"),
            # Features as string list
            "features": features_list,
        }

        return CinemaModel(**orm_data)

    @staticmethod
    def to_domain(model: CinemaModel) -> Cinema:
        """
        Converts a CinemaModel ORM model to a Cinema domain entity.

        Args:
            model: CinemaModel ORM instance

        Returns:
            Cinema: Domain entity instance

        Raises:
            ValueError: If model is not a CinemaModel instance
        """
        if not isinstance(model, CinemaModel):
            raise ValueError("Model must be a CinemaModel instance")

        features_list = [
            CinemaFeatures(feature_str) for feature_str in (model.features or [])
        ]

        amenities = CinemaAmenities(
            parking=model.has_parking,
            food_court=model.has_food_court,
            coffee_station=model.has_coffee_station,
            disabled_access=model.has_disabled_access,
        )

        contact_info = ContactInfo(
            address=model.address,
            phone=model.phone,
            email_contact=model.email_contact,
            location=Location(lat=model.latitude, lng=model.longitude),
        )

        social_media = SocialMedia(
            facebook=model.facebook_url,
            instagram=model.instagram_url,
            x=model.x_url,
            tik_tok=model.tik_tok_url,
        )

        return Cinema(
            id=model.id,
            image=model.image,
            name=model.name,
            tax_number=model.tax_number,
            is_active=model.is_active,
            description=model.description,
            screens=model.screens,
            last_renovation=model.last_renovation,
            # Enums
            type=model.type,
            status=model.status,
            region=model.region,
            # Value objects
            amenities=amenities,
            contact_info=contact_info,
            social_media=social_media,
            # Features
            features=features_list,
        )
