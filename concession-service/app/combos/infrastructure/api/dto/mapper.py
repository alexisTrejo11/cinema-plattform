from typing import Optional

from uuid import UUID
from app.combos.application.commands import ComboCreateCommand
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.combos.domain.entities.value_objects import ComboId
from .request import ComboCreateRequest
from app.shared.pagination import PaginationQuery
from app.products.domain.entities.value_objects import ProductId


class RequestDataMapper:
    """
    Maps request data to command objects for use cases.
    """

    @staticmethod
    def to_create_combo_command(
        request_data: ComboCreateRequest,
    ) -> ComboCreateCommand:
        """
        Maps ComboCreateRequest to ComboCreateCommand.
        """
        return ComboCreateCommand(**request_data.model_dump())

    @staticmethod
    def to_get_combo_by_id_query(
        combo_id: UUID,
        include_items: bool = False,
        pagination: Optional[PaginationQuery] = None,
    ) -> GetComboByIdQuery:
        """
        Maps parameters to a query object.
        """
        return GetComboByIdQuery(
            combo_id=ComboId(combo_id),
            include_items=include_items,
            pagination=pagination,
        )

    @staticmethod
    def to_get_combos_by_product_query(
        product_id: UUID,
        include_items: bool = False,
        pagination: Optional[PaginationQuery] = None,
    ) -> GetCombosByProductIdQuery:
        """
        Maps parameters to a query object for getting combos by product ID.
        """
        return GetCombosByProductIdQuery(
            product_id=ProductId(product_id),
            include_items=include_items,
            pagination=pagination,
        )
