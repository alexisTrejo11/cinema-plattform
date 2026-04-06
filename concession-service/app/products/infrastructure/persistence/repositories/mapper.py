from app.products.domain.entities.product_category import ProductCategory
from ..models.product_models import ProductModel, ProductCategoryModel
from app.products.domain.entities.product import Product, ProductId
from decimal import Decimal


class ModelMapper:
    @staticmethod
    def to_domain(model: "ProductModel") -> "Product":
        return Product(
            id=ProductId(value=model.id),
            name=model.name,
            image_url=model.image_url,
            description=model.description,
            price=Decimal(f"{model.price}"),
            is_available=model.is_available,
            preparation_time_mins=model.preparation_time_mins,
            calories=model.calories,
            category_id=model.category_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def from_domain(product: "Product") -> "ProductModel":
        dumped_data = product.model_dump(exclude={"id"})
        return ProductModel(
            id=product.id.value,
            **dumped_data,
        )

    @staticmethod
    def to_category_domain(model: "ProductCategoryModel") -> "ProductCategory":
        return ProductCategory(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
