from sqlalchemy import inspect
from .models import ComboModel, ComboItemModel
from app.combos.domain.entities.combo import Combo, ComboItem, ComboItemId, ComboId
from app.products.infrastructure.persistence.repositories.mapper import (
    ModelMapper as ProductMapper,
)


class ModelMapper:
    @classmethod
    def to_domain(cls, combo_model: ComboModel, include_items: bool) -> Combo:
        """Convert SQLAlchemy model to domain model"""
        items = []
        if include_items:
            state = inspect(combo_model)
            if "items" in state.unloaded:
                pass
            else:
                for item in combo_model.items:
                    items.append(
                        ComboItem(
                            ProductMapper.to_domain(item.product),
                            ComboItemId(item.id),
                            item.quantity,
                        )
                    )

        return Combo(
            id=ComboId(combo_model.id),
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
