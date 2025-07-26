from typing import List
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
from app.products.application.commands import ProductCreateCommand, ProductUpdateCommand
from app.products.application.responses import (
    ProductDetails,
    ProductCategoryResponse,
    ProductSearchResponse,
)
from .product_usecases import (
    GetProductByIdUseCase,
    UpdateProductUseCase,
    CreateProductUseCase,
    SearchProductUseCase,
    SoftDeleteProductUseCase,
)
from .category_usecases import (
    GetCategoryByIdUseCase,
    ListCategoryUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    SoftDeleteCategoryUseCase,
)
from ..commands import (
    ProductCreateCommand,
    ProductUpdateCommand,
    CategoryCreateCommand,
    CategoryUpdateCommand,
)
from app.products.domain.entities.value_objects import ProductId


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
        self.soft_delete_product_uc = SoftDeleteProductUseCase(product_repository)

    """Use cases for managing food products"""

    async def get_product_by_id(self, query: GetProductByIdQuery) -> ProductDetails:
        """Get a product by its ID"""
        return await self.get_product_by_uc.execute(query)

    async def search_products(
        self, query: SearchProductsQuery
    ) -> ProductSearchResponse:
        """Search for products based on parameters"""
        return await self.search_product_uc.execute(query)

    async def create_product(self, create_data: ProductCreateCommand) -> ProductDetails:
        """Create a new product"""
        return await self.create_product_uc.execute(create_data)

    async def update_product(self, update_data: ProductUpdateCommand) -> ProductDetails:
        """Update an existing product"""
        return await self.update_product_uc.execute(update_data)

    async def soft_delete_product(self, product_id: ProductId) -> None:
        """Soft delete a product by its ID"""
        return await self.soft_delete_product_uc.execute(product_id)


class ProductCategoryUseCases:
    def __init__(self, category_repository: ProductCategoryRepository):
        self.category_repository = category_repository
        self.get_category_by_uc = GetCategoryByIdUseCase(category_repository)
        self.list_category_uc = ListCategoryUseCase(category_repository)
        self.create_category_uc = CreateCategoryUseCase(category_repository)
        self.update_category_uc = UpdateCategoryUseCase(category_repository)
        self.soft_delete_category_uc = SoftDeleteCategoryUseCase(category_repository)

    """Use cases for managing product categories"""

    async def get_category_by_id(self, category_id: int) -> ProductCategoryResponse:
        """Get a category by its ID"""
        return await self.get_category_by_uc.execute(category_id)

    async def list_categories(self) -> List[ProductCategoryResponse]:
        """List all product categories"""
        return await self.list_category_uc.execute()

    async def create_category(
        self, create_data: CategoryCreateCommand
    ) -> ProductCategoryResponse:
        """Create a new product category"""
        return await self.create_category_uc.execute(create_data)

    async def update_category(
        self, category_id: int, update_data: CategoryUpdateCommand
    ) -> ProductCategoryResponse:
        """Update an existing product category"""
        return await self.update_category_uc.execute(category_id, update_data)

    async def soft_delete_category(self, category_id: int) -> None:
        """Soft delete a product category by its ID"""
        await self.soft_delete_category_uc.execute(category_id)
