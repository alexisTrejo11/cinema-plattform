from typing import List
from .usecases import (
    ListActiveComboUseCase,
    GetComboByIdUseCase,
    GetCombosByProductUseCase,
    CreateComboUseCase,
    DeleteComboUseCase,
)
from app.combos.domain.repository import ComboRepository
from app.products.domain.repositories import ProductRepository
from app.combos.application.response import ComboResponse
from app.combos.application.commands import ComboCreateComand
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import PaginationQuery
from app.combos.domain.entities.value_objects import ComboId


class ComboUseCases:
    def __init__(
        self, combo_repository: ComboRepository, product_repository: ProductRepository
    ) -> None:
        self.list_active = ListActiveComboUseCase(combo_repository)
        self.get_by_id = GetComboByIdUseCase(combo_repository)
        self.get_by_product = GetCombosByProductUseCase(
            combo_repository, product_repository
        )
        self.create = CreateComboUseCase(combo_repository, product_repository)
        self.delete = DeleteComboUseCase(combo_repository)

    def list_active_combos(self, query: PaginationQuery) -> List[ComboResponse]:
        return self.list_active.execute(query)

    def get_combo_by_id(self, query: GetComboByIdQuery) -> ComboResponse:
        return self.get_by_id.execute(query)

    def get_combos_by_product(
        self, query: GetCombosByProductIdQuery
    ) -> List[ComboResponse]:
        return self.get_by_product.execute(query)

    def create_combo(self, create_data: ComboCreateComand) -> ComboResponse:
        return self.create.execute(create_data)

    def delete_combo(self, combo_id: ComboId) -> None:
        return self.delete.execute(combo_id)
