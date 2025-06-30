from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.combos.application.repository import ComboRepository
from app.combos.domain.combo import Combo
from .models import ComboModel, ComboItemModel

class SqlAlchemyComboRepository(ComboRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_by_id(self, combo_id: int, include_items: bool = True) -> Optional[Combo]:
        query = self.session.query(ComboModel)
        
        if include_items:
            query = query.options(
                joinedload(ComboModel.items)
                .joinedload(ComboItemModel.product)
            )
        
        combo_model = query.filter(ComboModel.id == combo_id).first()
        
        if not combo_model:
            return None
            
        return self._to_domain(combo_model)
    
    def list_by_product(self, product_id: int, include_items: bool = True) -> List[Combo]:
        query = self.session.query(ComboModel).join(ComboItemModel)
        
        if include_items:
            query = query.options(
                joinedload(ComboModel.items)
                .joinedload(ComboItemModel.product)
            )
        
        combo_models = query.filter(
            and_(
                ComboItemModel.product_id == product_id,
                ComboModel.is_available == True
            )
        ).all()
        
        return [self._to_domain(combo) for combo in combo_models]
    
    def list_all(self, active_only: bool = True) -> List[Combo]:
        query = self.session.query(ComboModel).options(
            joinedload(ComboModel.items)
            .joinedload(ComboItemModel.product)
        )
        
        if active_only:
            query = query.filter(ComboModel.is_available == True)
        
        combo_models = query.all()
        return [self._to_domain(combo) for combo in combo_models]
    
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
                is_available=combo.is_available
            )
            self.session.add(combo_model)
        
        # Add items
        for item in combo.items:
            item_model = ComboItemModel(
                combo=combo_model,
                product_id=item.product.id,
                quantity=item.quantity
            )
            self.session.add(item_model)
        
        self.session.flush()
        return self._to_domain(combo_model)
    
    def soft_delete(self, combo_id: int) -> None:
        combo = self.session.get(ComboModel, combo_id)
        if combo:
            combo.is_available = False
            self.session.add(combo)
    
    def _to_domain(self, combo_model: ComboModel) -> Combo:
        """Convert SQLAlchemy model to domain model"""
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
            items=[]
        )