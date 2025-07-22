from app.products.domain.repositories import ProductRepository
from app.products.domain.entities.product import Product, ProductId
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from .models import ProductModel
from app.products.application.queries import SearchProductsQuery


class SqlAlchProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, product_id: ProductId) -> Optional[Product]:
        model = (
            self.session.query(ProductModel)
            .filter(
                ProductModel.id == product_id.value,
                ProductModel.is_available == True,
            )
            .first()
        )

        return model.to_domain() if model else None

    def get_by_id_in(
        self, product_id_list: List[ProductId]
    ) -> Dict[ProductId, Product]:
        if not product_id_list:
            return {}

        models = (
            self.session.query(ProductModel)
            .filter(
                ProductModel.id.in_(product_id_list),
                ProductModel.is_available == True,
            )
            .all()
        )

        return {ProductId(model.id): model.to_domain() for model in models}

    def search(self, food_params: SearchProductsQuery) -> List[Product]:

        query = self.session.query(ProductModel)

        if food_params.min_price is not None:
            query = query.filter(ProductModel.price >= food_params.min_price)

        if food_params.max_price is not None:
            query = query.filter(ProductModel.price <= food_params.max_price)

        if food_params.name:
            query = query.filter(ProductModel.name.ilike(f"%{food_params.name}%"))

        if food_params.category is not None:
            query = query.filter(ProductModel.category_id == food_params.category)

        if food_params.active_only:
            query = query.filter(ProductModel.is_available == True)

        query = query.order_by(ProductModel.name)

        if food_params.offset is not None and food_params.offset >= 0:
            query = query.offset(food_params.offset)

        if food_params.limit is not None and food_params.limit > 0:
            query = query.limit(food_params.limit)

        product_models = query.all()

        return [model.to_domain() for model in product_models]

    def save(self, product: Product) -> Product:
        model = ProductModel(**product.to_dict())
        if product.id == 0:
            model.id = None  # type: ignore
            self.session.add(model)
            self.session.flush()
        else:
            self.session.merge(model)

        self.session.commit()

        if model in self.session:
            self.session.refresh(model)

        return model.to_domain()

    def delete(self, product_id: ProductId) -> None:
        model = (
            self.session.query(ProductModel)
            .filter(ProductModel.id == product_id.value)
            .first()
        )
        if not model:
            return

        self.session.delete(model)
        self.session.commit()
