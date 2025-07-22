from typing import List
from decimal import Decimal
from app.products.domain.exceptions import ProductNotFoundError, InvalidCategoryError
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
from app.products.application.responses import ProductDetails
from ..commands import (
    ProductCreateCommand,
    ProductUpdateCommand,
)
from app.products.domain.entities.product import Product, ProductId


class GetProductByIdUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, query: GetProductByIdQuery) -> ProductDetails:

        product = await self.product_repository.get_by_id(query.product_id)

        if not product:
            raise ProductNotFoundError(query.product_id.to_string())

        return ProductDetails.from_entity(product)


class SearchProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(
        self, product_params: SearchProductsQuery
    ) -> List[ProductDetails]:
        product_list = await self.product_repository.search(product_params)
        return [ProductDetails.from_entity(product) for product in product_list]


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ) -> None:
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, create_data: ProductCreateCommand) -> ProductDetails:
        self._validate_category(create_data)

        product_data = create_data.model_dump()
        product_data["id"] = ProductId.generate()
        product_data["price"] = Decimal(str(product_data["price"]))

        new_product = Product(**product_data)
        product_created = await self.product_repository.save(new_product)

        return ProductDetails.from_entity(product_created)

    def _validate_category(self, create_data: ProductCreateCommand):
        exists = self.category_repository.exists_by_id(create_data.category_id)
        if not exists:
            raise InvalidCategoryError("product_id", "category must be valid")


class UpdateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ) -> None:
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, update_data: ProductUpdateCommand) -> ProductDetails:
        product = await self.product_repository.get_by_id(update_data.product_id)
        if not product:
            raise ProductNotFoundError(update_data.product_id)

        if (
            update_data.category_id
            and update_data.category_id != update_data.product_id
        ):
            self._validate_category(update_data.category_id)

        self._update_fields(product, update_data)
        await self.product_repository.save(product)

        return ProductDetails.from_entity(product)

    def _update_fields(self, product: Product, update_data: ProductUpdateCommand):
        data = update_data.model_dump(exclude_unset=True)

        for k, v in data.items():
            if k == "price" and v is not None:
                v = Decimal(str(v))
            setattr(product, k, v)

    def _validate_category(self, category_id: int):
        exists = self.category_repository.exists_by_id(category_id)
        if not exists:
            raise InvalidCategoryError("category_id", "category must be valid")


class SoftDeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, id: ProductId) -> None:
        product = await self.product_repository.get_by_id(id)
        if not product:
            raise ProductNotFoundError(id.to_string())

        await self.product_repository.delete(id)
