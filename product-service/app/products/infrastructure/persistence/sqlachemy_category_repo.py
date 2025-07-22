from app.products.domain.repositories import ProductCategoryRepository
from app.products.domain.entities.product_category import ProductCategory
from typing import Optional, List
from .models import ProductCategoryModel
from sqlalchemy.orm import Session


class SQLAlchemyCategoryRepository(ProductCategoryRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, category_id: int) -> Optional[ProductCategory]:
        category_model = (
            self.session.query(ProductCategoryModel)
            .filter(
                ProductCategoryModel.id == category_id,
                ProductCategoryModel.is_active == True,
            )
            .first()
        )

        if category_model:
            return category_model.to_domain()

    def list(self) -> List[ProductCategory]:
        categories = (
            self.session.query(ProductCategoryModel)
            .filter(ProductCategoryModel.is_active == True)
            .all()
        )

        return [category.to_domain() for category in categories]

    def save(self, category: ProductCategory) -> ProductCategory:
        model = ProductCategoryModel(**category.to_dict())
        if category.id == 0:
            model.id = None
            self.session.add(model)
            self.session.flush()
        else:
            self.session.merge(model)

        self.session.commit()

        if model in self.session:
            self.session.refresh(model)

        return model.to_domain()

    def delete(self, category_id: int) -> bool:
        category_model = (
            self.session.query(ProductCategoryModel)
            .filter(ProductCategoryModel.id == category_id)
            .first()
        )
        if not category_model:
            return False

        self.session.delete(category_model)
        self.session.commit()

        return True

    def exists_by_id(self, category_id: int) -> bool:
        return (
            self.session.query(ProductCategoryModel)
            .filter(ProductCategoryModel.id == category_id)
            .first()
            is not None
        )

    def exists_by_name(self, category_name: str) -> bool:
        return (
            self.session.query(ProductCategoryModel)
            .filter(ProductCategoryModel.name == category_name)
            .first()
            is not None
        )
