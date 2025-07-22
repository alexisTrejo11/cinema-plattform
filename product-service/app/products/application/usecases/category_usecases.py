from app.products.domain.repositories import ProductCategoryRepository
from app.products.application.responses import (
    ProductCategoryResponse as CategoryResponse,
)
from app.products.application.commands import ProductCategoryInsertCommand
from app.products.domain.entities.product_category import ProductCategory
from app.products.domain.exceptions import (
    CategoryNameConflict,
    CategoryNotFoundError,
)
from typing import List


class GetCategoryByIdUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(self, category_id: int) -> CategoryResponse:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError("Product_Category", category_id)

        return CategoryResponse(**category.to_dict())


class ListCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(self) -> List[CategoryResponse]:
        category_list = self.category_repo.list()
        return [CategoryResponse(**category.to_dict()) for category in category_list]


class CreateCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(self, create_data: ProductCategoryInsertCommand) -> CategoryResponse:
        self._validate_name(create_data.name)

        new_category = ProductCategory(**create_data.model_dump())
        category_created = self.category_repo.save(new_category)

        return CategoryResponse(**category_created.to_dict())

    def _validate_name(self, name: str):
        if self.category_repo.exists_by_name(name.strip()):
            raise CategoryNameConflict(message="Category Name already Taken.")


class UpdateCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(
        self, category_id: int, update_data: ProductCategoryInsertCommand
    ) -> CategoryResponse:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError("Product_Category", category_id)

        if update_data.name and update_data.name != category.name:
            self._validate_name(update_data.name)

        self._update_fields(category, update_data)
        self.category_repo.save(category)

        return CategoryResponse(**category.to_dict())

    def _update_fields(
        self, category: ProductCategory, category_data: ProductCategoryInsertCommand
    ) -> None:
        update_data = category_data.model_dump()
        for k, v in update_data.items():
            setattr(category, k, v)

    def _validate_name(self, name: str) -> None:
        if self.category_repo.exists_by_name(name.strip()):
            raise CategoryNameConflict(message="Category Name already Taken.")


class SoftDeleteCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    def execute(self, category_id: int, is_soft_delete=True) -> bool:
        if is_soft_delete:
            category = self.category_repo.get_by_id(category_id)
            if not category:
                raise CategoryNotFoundError("Product_Category", category_id)

            category.soft_delete()
            self.category_repo.save(category)

            return True
        else:
            return self.category_repo.delete(category_id)
