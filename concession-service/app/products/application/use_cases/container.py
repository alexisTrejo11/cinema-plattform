from typing import List
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
from app.products.application.commands import ProductCreateCommand, ProductUpdateCommand

from .product_use_cases import (
    GetProductByIdUseCase,
    UpdateProductUseCase,
    CreateProductUseCase,
    SearchProductUseCase,
    DeleteProductUseCase,
)
from .category_use_cases import (
    GetCategoryByIdUseCase,
    GetAllCategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
)
from ..commands import (
    ProductCreateCommand,
    ProductUpdateCommand,
    CategoryCreateCommand,
    CategoryUpdateCommand,
)
from app.products.domain.entities.value_objects import ProductId
from app.products.domain.entities.product_category import ProductCategory
from app.products.domain.entities.product import Product
from app.products.infrastructure.api.dtos import ProductPaginatedResponse


class ProductUseCases:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: ProductCategoryRepository,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.get_product_by_uc = GetProductByIdUseCase(product_repository)
        self.search_product_uc = SearchProductUseCase(product_repository)
        self.update_product_uc = UpdateProductUseCase(
            product_repository, category_repository
        )
        self.create_product_uc = CreateProductUseCase(
            product_repository, category_repository
        )
        self.delete_product_uc = DeleteProductUseCase(product_repository)

    """Use cases for managing food products"""

    async def get_product_by_id(self, query: GetProductByIdQuery) -> Product:
        """Get a product by its ID"""
        return await self.get_product_by_uc.execute(query)

    async def search_products(
        self, query: SearchProductsQuery
    ) -> ProductPaginatedResponse:
        """Search for products based on parameters"""
        return await self.search_product_uc.execute(query)

    async def create_product(self, create_data: ProductCreateCommand) -> Product:
        """Create a new product"""
        return await self.create_product_uc.execute(create_data)

    async def update_product(self, update_data: ProductUpdateCommand) -> Product:
        """Update an existing product"""
        return await self.update_product_uc.execute(update_data)

    async def delete_product(self, product_id: ProductId) -> None:
        """Soft delete a product by its ID"""
        return await self.delete_product_uc.execute(product_id)


class ProductCategoryUseCases:
    def __init__(self, category_repository: ProductCategoryRepository):
        self.category_repository = category_repository
        self.get_category_by_uc = GetCategoryByIdUseCase(category_repository)
        self.get_categories_uc = GetAllCategoriesUseCase(category_repository)
        self.create_category_uc = CreateCategoryUseCase(category_repository)
        self.update_category_uc = UpdateCategoryUseCase(category_repository)
        self.delete_category_uc = DeleteCategoryUseCase(category_repository)

    """Use cases for managing product categories"""

    async def get_category_by_id(self, category_id: int) -> ProductCategory:
        """Get a category by its ID"""
        return await self.get_category_by_uc.execute(category_id)

    async def list_categories(self) -> List[ProductCategory]:
        """List all product categories"""
        return await self.get_categories_uc.execute()

    async def create_category(
        self, create_data: CategoryCreateCommand
    ) -> ProductCategory:
        """Create a new product category"""
        return await self.create_category_uc.execute(create_data)

    async def update_category(
        self, category_id: int, update_data: CategoryUpdateCommand
    ) -> ProductCategory:
        """Update an existing product category"""
        return await self.update_category_uc.execute(category_id, update_data)

    async def delete_category(self, category_id: int) -> None:
        """Delete a product category by its ID"""
        await self.delete_category_uc.execute(category_id)
