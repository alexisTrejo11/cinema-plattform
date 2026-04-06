from pydantic import BaseModel, ConfigDict, Field

from app.products.domain.entities.product import Product

from ..exceptions import *
from .value_objects import ComboItemId


class ComboItem(BaseModel):
    """Represents an individual food product within a combo."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ComboItemId = Field(default_factory=ComboItemId.generate)
    product: Product
    quantity: int = Field(default=1, ge=1, le=10)

    def validate_quantity_range(self):
        """Validates that quantity is within allowed range (1-10)."""
        min_quantity = 1
        max_quantity = 10
        if not (min_quantity <= self.quantity <= max_quantity):
            raise QuantityRangeException(self.product.id, min_quantity, max_quantity)
