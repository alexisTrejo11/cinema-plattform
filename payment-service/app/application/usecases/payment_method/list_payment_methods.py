from typing import List
from app.application.dto.payment_method import PaymentMethodDTO
from app.application.interfaces.repository import IRepository

class ListPaymentMethodsQuery:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self) -> List[PaymentMethodDTO]:
        payment_methods = self.payment_method_repository.find_all()
        return [PaymentMethodDTO.from_entity(pm) for pm in payment_methods]

