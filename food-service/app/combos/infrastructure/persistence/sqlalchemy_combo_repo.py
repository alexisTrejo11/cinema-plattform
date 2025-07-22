from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.combos.domain.repository import ComboRepository
from app.combos.domain.entities.combo import Combo, ComboItem
from .models import ComboModel, ComboItemModel
from app.combos.domain.entities.value_objects import ComboId
from app.combos.application.queries import GetComboByIdQuery, GetCombosByProductIdQuery
from app.shared.pagination import PaginationQuery


class SqlAlchemyComboRepository(ComboRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, search_query: GetComboByIdQuery) -> Optional[Combo]:
        query = self.session.query(ComboModel)

        if search_query.include_items:
            query = query.options(
                joinedload(ComboModel.items).joinedload(ComboItemModel.product)
            )

        combo_model = query.filter(ComboModel.id == search_query.combo_id.value).first()

        if not combo_model:
            return None

        return self._to_domain(
            combo_model,
            search_query.include_items if search_query.include_items else False,
        )

    def list_by_product(self, search_query: GetCombosByProductIdQuery) -> List[Combo]:
        query = self.session.query(ComboModel).join(ComboItemModel)

        if search_query.include_items:
            query = query.options(
                joinedload(ComboModel.items).joinedload(ComboItemModel.product)
            )

        combo_models = query.filter(
            and_(
                ComboItemModel.product_id == search_query.product_id.value,
                ComboModel.is_available == True,
            )
        ).all()

        return [
            self._to_domain(
                combo,
                search_query.include_items if search_query.include_items else False,
            )
            for combo in combo_models
        ]

    def list_all(self, pagination: PaginationQuery) -> List[Combo]:
        query = self.session.query(ComboModel).options(
            joinedload(ComboModel.items).joinedload(ComboItemModel.product)
        )

        combo_models = query.all()
        return [self._to_domain(combo, True) for combo in combo_models]

    def save(self, combo: Combo) -> Combo:
        if combo.id:
            # Update existing combo
            combo_model = self.session.get(ComboModel, combo.id)
            if not combo_model:
                raise ValueError(f"Combo with id {combo.id} not found")

            # Update combo fields
            combo_model.name = combo.name
            combo_model.description = combo.description
            combo_model.price = combo.price
            combo_model.discount_percentage = combo.discount_percentage
            combo_model.image_url = combo.image_url
            combo_model.is_available = combo.is_available

            # Clear existing items
            self.session.query(ComboItemModel).filter(
                ComboItemModel.combo_id == combo.id
            ).delete()
        else:
            # Create new combo
            combo_model = ComboModel(
                name=combo.name,
                description=combo.description,
                price=combo.price,
                discount_percentage=combo.discount_percentage,
                image_url=combo.image_url,
                is_available=combo.is_available,
            )
            self.session.add(combo_model)

        # Add items
        for item in combo.items:
            item_model = ComboItemModel(
                combo=combo_model, product_id=item.product.id, quantity=item.quantity
            )
            self.session.add(item_model)

        self.session.commit()
        return self._to_domain(combo_model, True)

    def soft_delete(self, combo_id: ComboId) -> None:
        combo = self.session.get(ComboModel, combo_id.value)
        if combo:
            combo.is_available = False
            self.session.add(combo)

    def _to_domain(self, combo_model: ComboModel, include_items: bool) -> Combo:
        """Convert SQLAlchemy model to domain model"""
        items = []
        if include_items:
            items = [
                ComboItem(item.product.to_domain(), item.id, item.quantity)
                for item in combo_model.items
                if combo_model.items
            ]

        return Combo(
            id=combo_model.id,
            name=combo_model.name,
            description=combo_model.description,
            price=combo_model.price,
            discount_percentage=combo_model.discount_percentage,
            image_url=combo_model.image_url,
            is_available=combo_model.is_available,
            created_at=combo_model.created_at,
            updated_at=combo_model.updated_at,
            items=items,
        )
