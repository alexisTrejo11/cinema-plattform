from dataclasses import dataclass
from datetime import datetime
from app.application.dto.payment_method import PaymentMethodDTO
from app.application.interfaces.repository import IRepository

@dataclass
class SoftDeletePaymentMethodCommand:
    id: str

class SoftDeletePaymentMethodUseCase:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self, command: SoftDeletePaymentMethodCommand):
        payment_method = self.payment_method_repository.find_by_id(command.id)
        
        if not payment_method:
            raise Exception("Payment method not found")
        
        payment_method.deleted_at = datetime.now()
        payment_method.updated_at = datetime.now()
        
        self.payment_method_repository.update(payment_method)

