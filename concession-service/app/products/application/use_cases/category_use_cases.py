from app.products.domain.repositories import ProductCategoryRepository
from app.products.application.commands import (
    CategoryUpdateCommand,
    CategoryCreateCommand,
)
from app.products.domain.entities.product_category import ProductCategory
from app.products.domain.exceptions import (
    CategoryNameConflict,
    CategoryNotFoundError,
)
from typing import List


class GetCategoryByIdUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, category_id: int) -> ProductCategory:
        category = await self.category_repository.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        return category


class GetAllCategoriesUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self) -> List[ProductCategory]:
        return await self.category_repository.find_all()


class CreateCategoryUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, data: CategoryCreateCommand) -> ProductCategory:
        await self._validate_name(data.name)

        new_category = ProductCategory(**data.model_dump())
        created_category = await self.category_repository.save(new_category)

        return created_category

    async def _validate_name(self, name: str):
        if await self.category_repository.exists_by_name(name.strip()):
            raise CategoryNameConflict(category_name=name.strip())


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(
        self, category_id: int, update_data: CategoryUpdateCommand
    ) -> ProductCategory:
        category = await self.category_repository.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        if update_data.name and update_data.name != category.name:
            await self._validate_name(update_data.name)

        self._update_fields(category, update_data)

        updated_category = await self.category_repository.save(category)
        return updated_category

    def _update_fields(
        self, category: ProductCategory, category_data: CategoryUpdateCommand
    ) -> None:
        update_data = category_data.model_dump()
        for k, v in update_data.items():
            setattr(category, k, v)

    async def _validate_name(self, name: str) -> None:
        if await self.category_repository.exists_by_name(name.strip()):
            raise CategoryNameConflict(message="Category Name already Taken.")


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, category_id: int, is_soft_delete=True) -> None:
        if is_soft_delete:
            category = await self.category_repository.find_by_id(category_id)
            if not category:
                raise CategoryNotFoundError(category_id)

            category.soft_delete()
            await self.category_repository.save(category)
        else:
            await self.category_repository.delete(category_id)


class RestoreCategoryUseCase:
    def __init__(self, category_repository: ProductCategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, category_id: int) -> None:
        category = await self.category_repository.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        category.restore()
        await self.category_repository.save(category)
