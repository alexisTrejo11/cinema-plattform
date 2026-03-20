from app.products.domain.repositories import ProductCategoryRepository
from app.products.application.responses import (
    ProductCategoryResponse as CategoryResponse,
)
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
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, category_id: int) -> CategoryResponse:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        return CategoryResponse(**category.to_dict())


class ListCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self) -> List[CategoryResponse]:
        category_list = await self.category_repo.list()
        return [CategoryResponse(**category.to_dict()) for category in category_list]


class CreateCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, create_data: CategoryCreateCommand) -> CategoryResponse:
        await self._validate_name(create_data.name)

        new_category = ProductCategory(**create_data.model_dump())
        category_created = await self.category_repo.save(new_category)

        return CategoryResponse(**category_created.to_dict())

    async def _validate_name(self, name: str):
        if await self.category_repo.exists_by_name(name.strip()):
            raise CategoryNameConflict(category_name=name.strip())


class UpdateCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(
        self, category_id: int, update_data: CategoryUpdateCommand
    ) -> CategoryResponse:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        if update_data.name and update_data.name != category.name:
            await self._validate_name(update_data.name)

        self._update_fields(category, update_data)
        await self.category_repo.save(category)

        return CategoryResponse(**category.to_dict())

    def _update_fields(
        self, category: ProductCategory, category_data: CategoryUpdateCommand
    ) -> None:
        update_data = category_data.model_dump()
        for k, v in update_data.items():
            setattr(category, k, v)

    async def _validate_name(self, name: str) -> None:
        if await self.category_repo.exists_by_name(name.strip()):
            raise CategoryNameConflict(message="Category Name already Taken.")


class SoftDeleteCategoryUseCase:
    def __init__(self, category_repo: ProductCategoryRepository) -> None:
        self.category_repo = category_repo

    async def execute(self, category_id: int, is_soft_delete=True) -> bool:
        if is_soft_delete:
            category = await self.category_repo.get_by_id(category_id)
            if not category:
                raise CategoryNotFoundError(category_id)

            category.soft_delete()
            await self.category_repo.save(category)

            return True
        else:
            return await self.category_repo.delete(category_id)
