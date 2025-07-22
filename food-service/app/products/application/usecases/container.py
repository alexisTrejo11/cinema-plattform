from typing import List
from app.products.domain.repositories import (
    ProductRepository,
    ProductCategoryRepository,
)
from app.products.application.queries import SearchProductsQuery, GetProductByIdQuery
from app.products.application.commands import ProductCreateCommand, ProductUpdateCommand
from app.products.application.responses import ProductDetails, ProductCategoryResponse
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
    ProductCategoryInsertCommand,
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

    def get_product_by_id(self, query: GetProductByIdQuery) -> ProductDetails:
        """Get a product by its ID"""
        return self.get_product_by_uc.execute(query)

    def search_products(self, query: SearchProductsQuery) -> List[ProductDetails]:
        """Search for products based on parameters"""
        return self.search_product_uc.execute(query)

    def create_product(self, create_data: ProductCreateCommand) -> ProductDetails:
        """Create a new product"""
        return self.create_product_uc.execute(create_data)

    def update_product(self, update_data: ProductUpdateCommand) -> ProductDetails:
        """Update an existing product"""
        return self.update_product_uc.execute(update_data)

    def soft_delete_product(self, product_id: ProductId) -> None:
        """Soft delete a product by its ID"""
        return self.soft_delete_product_uc.execute(product_id)


class ProductCategoryUseCases:
    def __init__(self, category_repository: ProductCategoryRepository):
        self.category_repository = category_repository
        self.get_category_by_uc = GetCategoryByIdUseCase(category_repository)
        self.list_category_uc = ListCategoryUseCase(category_repository)
        self.create_category_uc = CreateCategoryUseCase(category_repository)
        self.update_category_uc = UpdateCategoryUseCase(category_repository)
        self.soft_delete_category_uc = SoftDeleteCategoryUseCase(category_repository)

    """Use cases for managing product categories"""

    def get_category_by_id(self, category_id: int) -> ProductCategoryResponse:
        """Get a category by its ID"""
        return self.get_category_by_uc.execute(category_id)

    def list_categories(self) -> List[ProductCategoryResponse]:
        """List all product categories"""
        return self.list_category_uc.execute()

    def create_category(
        self, create_data: ProductCategoryInsertCommand
    ) -> ProductCategoryResponse:
        """Create a new product category"""
        return self.create_category_uc.execute(create_data)

    def update_category(
        self, category_id: int, update_data: ProductCategoryInsertCommand
    ) -> ProductCategoryResponse:
        """Update an existing product category"""
        return self.update_category_uc.execute(category_id, update_data)

    def soft_delete_category(self, category_id: int) -> None:
        """Soft delete a product category by its ID"""
        self.soft_delete_category_uc.execute(category_id)
