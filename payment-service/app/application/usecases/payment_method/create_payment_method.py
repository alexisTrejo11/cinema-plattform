from dataclasses import dataclass
from datetime import datetime
from app.application.dto.payment_method import PaymentMethodDTO
from app.application.interfaces.repository import IRepository
from app.domain.entities.payment_method import PaymentMethod
from app.domain.value_objects.id import ID
from app.domain.value_objects.card import Card

@dataclass
class CreatePaymentMethodCommand:
    user_id: str
    card_holder: str
    card_number: str
    cvv: str
    expiration_month: str
    expiration_year: str

class CreatePaymentMethodUseCase:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self, command: CreatePaymentMethodCommand) -> PaymentMethodDTO:
        
        card = Card(
            card_holder=command.card_holder,
            card_number=command.card_number,
            cvv=command.cvv,
            expiration_month=command.expiration_month,
            expiration_year=command.expiration_year
        )

        payment_method = PaymentMethod(
            id=ID.generate(),
            user_id=command.user_id,
            card=card,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.payment_method_repository.add(payment_method)
        
        return PaymentMethodDTO.from_entity(payment_method)

