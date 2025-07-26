from typing import List
from app.combos.domain.repository import ComboRepository
from ..response import ComboResponse, ComboItemResponse
from app.combos.application.commands import ComboCreateCommand, ComboItemCreateCommand
from app.combos.domain.exceptions import (
    ComboNotFoundError,
    ComboItemValidationError,
    ProductValidationError,
)
from app.products.domain.repositories import ProductRepository
from app.combos.domain.entities.combo import Combo, ComboItem
from app.shared.pagination import PaginationQuery
from app.combos.domain.entities.value_objects import ComboId, ComboItemId
from app.products.domain.entities.value_objects import ProductId
from ..queries import GetCombosByProductIdQuery, GetComboByIdQuery


class ListActiveComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, pagination: PaginationQuery) -> List[ComboResponse]:
        combos = await self.combo_repository.list(pagination)
        return [ComboResponse.from_domain(combo) for combo in combos]


class GetComboByIdUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository

    async def execute(self, query: GetComboByIdQuery) -> ComboResponse:
        combo = await self.combo_repository.get_by_id(query)
        if not combo:
            raise ComboNotFoundError(query.combo_id.to_string())

        return ComboResponse.from_domain(combo)


class GetCombosByProductUseCase:
    def __init__(
        self, combo_repository: ComboRepository, product_repository: ProductRepository
    ) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository

    async def execute(self, query: GetCombosByProductIdQuery) -> List[ComboResponse]:
        product = await self.product_repository.get_by_id(query.product_id)
        if not product:
            raise ProductValidationError()

        combos = await self.combo_repository.list_by_product(query)
        return [ComboResponse.from_domain(combo) for combo in combos]


class CreateComboUseCase:
    def __init__(
        self, combo_repository: ComboRepository, product_repository: ProductRepository
    ) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository

    async def execute(self, create_data: ComboCreateCommand) -> ComboResponse:
        new_combo = Combo(id=ComboId.generate(), **create_data.model_dump())

        items = await self._generate_products(create_data)
        new_combo.items = items

        new_combo.validate_business_logic()

        combo_created = await self.combo_repository.save(new_combo)
        return ComboResponse.from_domain(combo_created)

    async def _generate_products(
        self, create_data: ComboCreateCommand
    ) -> List[ComboItem]:
        self.validate_items(create_data.items)
        products_map = await self.product_repository.get_by_id_in(
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

    async def execute(self, combo_id: ComboId) -> None:
        combo = await self.combo_repository.get_by_id(
            GetComboByIdQuery(combo_id=combo_id)
        )
        if not combo:
            raise ComboNotFoundError(combo_id.to_string())

        print(f"Deleting combo with ID: {combo}")
        await self.combo_repository.soft_delete(combo_id)
