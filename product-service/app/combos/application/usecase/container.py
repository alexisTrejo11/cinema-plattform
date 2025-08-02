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
from app.combos.application.commands import ComboCreateCommand, ComboCommandResult
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import Page, PaginationQuery
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

    async def list_active_combos(
        self, query: PaginationQuery, include_items: bool
    ) -> Page[ComboResponse]:
        return await self.list_active.execute(query, include_items)

    async def get_combo_by_id(self, query: GetComboByIdQuery) -> ComboResponse:
        return await self.get_by_id.execute(query)

    async def get_combos_by_product(
        self, query: GetCombosByProductIdQuery
    ) -> Page[ComboResponse]:
        return await self.get_by_product.execute(query)

    async def create_combo(self, create_data: ComboCreateCommand) -> ComboCommandResult:
        return await self.create.execute(create_data)

    async def delete_combo(self, combo_id: ComboId) -> ComboCommandResult:
        return await self.delete.execute(combo_id)
