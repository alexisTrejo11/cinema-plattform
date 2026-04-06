from sqlalchemy import inspect

from app.combos.domain.entities.combo import Combo, ComboItem
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.products.infrastructure.persistence.repositories.mapper import (
    ModelMapper as ProductMapper,
)
from .models import ComboModel


def combo_model_to_domain(combo_model: ComboModel, include_items: bool) -> Combo:
    """Convert SQLAlchemy model to domain model."""
    items = []
    if include_items:
        state = inspect(combo_model)
        if "items" not in state.unloaded:
            for item in combo_model.items:
                items.append(
                    ComboItem(
                        product=ProductMapper.to_domain(item.product),
                        id=ComboItemId(value=item.id),
                        quantity=item.quantity,
                    )
                )

    return Combo(
        id=ComboId(value=combo_model.id),
        name=combo_model.name,
        description=combo_model.description,
        price=combo_model.price,
        discount_percentage=combo_model.discount_percentage,
        image_url=combo_model.image_url,
        is_available=combo_model.is_available,
        created_at=combo_model.created_at,
        updated_at=combo_model.updated_at,
        items=items,
    )


def combo_model_from_domain(combo: Combo) -> ComboModel:
    """Create a persistence model from a domain entity (without items; items are saved separately)."""
    return ComboModel(
        id=combo.id.value,
        name=combo.name,
        description=combo.description,
        price=combo.price,
        discount_percentage=combo.discount_percentage,
        image_url=combo.image_url,
        is_available=combo.is_available,
        created_at=combo.created_at,
        updated_at=combo.updated_at,
    )
