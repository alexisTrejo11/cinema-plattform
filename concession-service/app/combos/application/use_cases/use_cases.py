from typing import List
from app.shared.pagination import Page, PaginationQuery
from app.products.domain.repositories import ProductRepository
from app.combos.domain.repository import ComboRepository
from app.combos.application.commands import (
    ComboCreateCommand,
    ComboItemCreateCommand,
)
from app.combos.domain.entities.combo import Combo, ComboItem
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.combos.domain.exceptions import (
    ComboNotFoundError,
    ComboItemValidationError,
    ProductValidationError,
)
from app.products.domain.entities.value_objects import ProductId
from ..queries import GetCombosByProductIdQuery, GetComboByIdQuery


class GetActiveComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, pagination: PaginationQuery) -> Page[Combo]:
        return await self.combo_repository.find_active(pagination)


class GetComboByIdUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, query: GetComboByIdQuery) -> Combo:
        combo = await self.combo_repository.find_by_id(
            query.combo_id, query.include_items
        )
        if not combo:
            raise ComboNotFoundError(query.combo_id)

        return combo


class GetCombosByProductUseCase:
    def __init__(
        self, combo_repository: ComboRepository, product_repository: ProductRepository
    ) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository

    async def execute(self, query: GetCombosByProductIdQuery) -> Page[Combo]:
        product = await self.product_repository.find_by_id(query.product_id)
        if not product:
            raise ProductValidationError()

        return await self.combo_repository.find_by_product(
            query.product_id,
            query.pagination,
            query.include_items,
        )


class CreateComboUseCase:
    def __init__(
        self, combo_repository: ComboRepository, product_repository: ProductRepository
    ) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository

    async def execute(self, create_data: ComboCreateCommand) -> Combo:
        new_combo = Combo.model_validate(
            {
                "id": ComboId.generate(),
                **create_data.model_dump(exclude={"items"}),
                "items": [],
            }
        )

        items = await self._generate_products(create_data)
        new_combo.items = items

        new_combo.validate_business_logic()

        await self.combo_repository.save(new_combo)
        return new_combo

    async def _generate_products(
        self, create_data: ComboCreateCommand
    ) -> List[ComboItem]:
        self.validate_items(create_data.items)
        products_map = await self.product_repository.find_by_id_in(
            [ProductId(item.product_id) for item in create_data.items]
        )

        items = []
        for item in create_data.items:
            combo_items = ComboItem(
                id=ComboItemId.generate(),
                quantity=item.quantity,
                product=products_map[ProductId(item.product_id)],
            )
            items.append(combo_items)

        return items

    # TODO: delete???
    def validate_items(self, required_items: List["ComboItemCreateCommand"]):
        if len(required_items) <= 0:
            raise ComboItemValidationError(
                "at least one product is require to create a combo"
            )
        elif len(required_items) == 1:
            if required_items[0].quantity <= 1:
                raise ComboItemValidationError(
                    "at least one item and two quantity are required to create a combo "
                )
        elif len(required_items) > 20:
            raise ComboItemValidationError("too much items")


class DeleteComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, combo_id: ComboId, soft_delete: bool = True) -> None:
        if soft_delete:
            combo = await self.combo_repository.find_by_id(
                combo_id, include_items=False
            )
            if not combo:
                raise ComboNotFoundError(combo_id)

            combo.mark_as_deleted()
            await self.combo_repository.save(combo)
        else:
            await self.combo_repository.delete(combo_id, soft_delete=False)


class RestoreComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, combo_id: ComboId) -> Combo:
        combo = await self.combo_repository.find_deleted_by_id(combo_id)
        if not combo:
            raise ComboNotFoundError(combo_id)

        combo.restore()
        await self.combo_repository.save(combo)
        return combo
