from abc import ABC, abstractmethod
from typing import List, Optional
from app.payment.domain.entities.payment import Payment, PaymentId

class PaymentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: PaymentId) -> Optional[Payment]:
        """Get a payment by its ID."""
        pass

    @abstractmethod
    async def list(self, **kwargs) -> List[Payment]:
        """List payments with filters."""
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        """Save a payment."""
        pass

    @abstractmethod
    async def soft_delete(self, payment_id: PaymentId) -> bool:
        """Delete a payment by its ID."""
        pass