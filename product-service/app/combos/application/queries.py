from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.shared.pagination import PaginationQuery
from app.products.domain.entities.value_objects import ProductId
from app.combos.domain.entities.value_objects import ComboId


class GetCombosByProductIdQuery(BaseModel):
    product_id: ProductId
    include_items: Optional[bool] = False
    pagination: Optional[PaginationQuery] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetComboByIdQuery(BaseModel):
    combo_id: ComboId
    include_items: Optional[bool] = False
    pagination: Optional[PaginationQuery] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
