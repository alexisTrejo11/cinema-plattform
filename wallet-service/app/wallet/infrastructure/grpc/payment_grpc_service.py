import logging
from typing import Any


from app.wallet.domain.interfaces import PaymentInternalService
from app.shared.core.response import Result

logger = logging.getLogger(__name__)


class PaymentGrpcService(PaymentInternalService):
    def __init__(self) -> None:
        pass

    async def create_payment(
        self, payment_details: dict[str, Any]
    ) -> Result[dict[str, Any]]:
        logger.warning(
            "PaymentGrpcService.create_payment not implemented yet, returning success temporarily"
        )
        return Result.success(payment_details)
