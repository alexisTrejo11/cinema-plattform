import logging
from decimal import Decimal
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.products.domain.exceptions import ProductNotFoundError, InvalidCategoryError
from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
from app.products.domain.entities.product import Product, ProductId
from app.products.infrastructure.api.dtos import (
    ProductPaginatedResponse,
    ProductResponse,
)
from ..commands import ProductCreateCommand, ProductUpdateCommand

logger = logging.getLogger(__name__)


class GetProductByIdUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, query: GetProductByIdQuery) -> Product:
        product = await self.product_repository.find_by_id(query.product_id)
        if not product:
            raise ProductNotFoundError(query.product_id)

        return product


class SearchProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(
        self, product_params: SearchProductsQuery
    ) -> ProductPaginatedResponse:
        products, metadata = await self.product_repository.search(product_params)
        return ProductPaginatedResponse(
            product_page=[ProductResponse.from_entity(p) for p in products],
            metadata=metadata,
        )


class CreateProductUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ) -> None:
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, create_data: ProductCreateCommand) -> Product:
        logger.info(f"Creating product: {create_data}")
        await self._validate_category(create_data)

        new_product = Product.create(create_data.model_dump())
        new_product.validate_business_rules()

        logger.info(f"Saving product: {new_product}")
        saved_product = await self.product_repository.save(new_product)

        logger.info(f"Product saved: {saved_product}")
        return saved_product

    async def _validate_category(self, create_data: ProductCreateCommand):
        exists = await self.category_repository.exists_by_id(create_data.category_id)
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

    async def execute(self, update_data: ProductUpdateCommand) -> Product:
        logger.info(f"Updating product: {update_data}")
        product = await self.product_repository.find_by_id(update_data.product_id)
        if not product:
            raise ProductNotFoundError(update_data.product_id)

        logger.info(f"Validating category: {update_data.category_id}")
        if (
            update_data.category_id is not None
            and update_data.category_id != product.category_id
        ):
            await self._validate_category(update_data.category_id)

        self._update_fields(product, update_data)
        product.validate_business_rules()

        await self.product_repository.save(product)

        return product

    def _update_fields(self, product: Product, update_data: ProductUpdateCommand):
        data = update_data.model_dump(
            exclude_unset=True, exclude_none=True, exclude={"product_id"}
        )
        for k, v in data.items():
            print(f"Updating field: {k} with value: {v}")
            setattr(product, k, v)

    async def _validate_category(self, category_id: int):
        exists = await self.category_repository.exists_by_id(category_id)
        if not exists:
            raise InvalidCategoryError("category_id", "category must be valid")


class RestoreProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, id: ProductId) -> None:
        product = await self.product_repository.find_deleted_by_id(id)
        if not product:
            raise ProductNotFoundError(id)

        product.restore()
        await self.product_repository.save(product)


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, id: ProductId) -> None:
        product = await self.product_repository.find_by_id(id)
        if not product:
            raise ProductNotFoundError(id)

        await self.product_repository.delete(id)
