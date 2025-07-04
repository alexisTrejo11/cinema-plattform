from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentService(ABC):
    @abstractmethod
    async def request_payment(self, payment) -> Dict[str, Any]:
        pass