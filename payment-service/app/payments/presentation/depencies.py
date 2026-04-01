from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.app_config import settings
from app.config.postgres_config import get_db
from app.payments.application.usecases.admin_usecases import AdminPaymentUseCases
from app.payments.application.usecases.customer_usecases import CustomerPaymentUseCases
from app.payments.application.usecases.payment_method_usecases import PaymentMethodUseCases
from app.payments.application.usecases.staff_usecases import StaffPaymentUseCases
from app.payments.domain.interfaces import (
    PaymentEventsPublisher,
    PaymentMethodRepository,
    PaymentRepository,
    PurchaseAssertionClient,
    StoredPaymentMethodRepository,
)
from app.payments.infrastructure.persistence.sql_alchemy_repository import (
    SqlAlchemyPaymentMethodRepository,
    SqlAlchemyPaymentRepository,
    SqlAlchemyStoredPaymentMethodRepository,
)
from app.payments.infrastructure.grpc.purchase_assertion_grpc_client import (
    PurchaseAssertionGrpcClient,
)
from app.payments.infrastructure.messaging.kafka_payment_events import (
    build_payment_events_publisher,
)


class NoopPurchaseAssertionClient(PurchaseAssertionClient):
    async def assert_ticket_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {"asserted": True, "kind": "ticket", "user_id": user_id, "payload": payload}

    async def assert_concessions_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "asserted": True,
            "kind": "concessions",
            "user_id": user_id,
            "payload": payload,
        }

    async def assert_merchandise_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "asserted": True,
            "kind": "merchandise",
            "user_id": user_id,
            "payload": payload,
        }

    async def assert_subscription_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "asserted": True,
            "kind": "subscription",
            "user_id": user_id,
            "payload": payload,
        }

    async def assert_wallet_credit(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "asserted": True,
            "kind": "wallet_credit",
            "user_id": user_id,
            "payload": payload,
        }


class NoopPaymentEventsPublisher(PaymentEventsPublisher):
    async def publish(
        self, event_name: str, payload: dict[str, Any], key: str | None = None
    ) -> None:
        # Intentionally no-op; will be replaced by Kafka implementation.
        return None


def get_payment_repository(
    db: AsyncSession = Depends(get_db),
) -> PaymentRepository:
    return SqlAlchemyPaymentRepository(db)


def get_payment_method_repository(
    db: AsyncSession = Depends(get_db),
) -> PaymentMethodRepository:
    return SqlAlchemyPaymentMethodRepository(db)


def get_stored_payment_method_repository(
    db: AsyncSession = Depends(get_db),
) -> StoredPaymentMethodRepository:
    return SqlAlchemyStoredPaymentMethodRepository(db)


def get_purchase_assertion_client() -> PurchaseAssertionClient:
    if settings.GRPC_BILLBOARD_TARGET.strip() or settings.GRPC_PAYMENT_TARGET.strip():
        return PurchaseAssertionGrpcClient()
    return NoopPurchaseAssertionClient()


def get_payment_events_publisher() -> PaymentEventsPublisher:
    return build_payment_events_publisher()


def get_payment_method_use_cases(
    payment_method_repository: PaymentMethodRepository = Depends(
        get_payment_method_repository
    ),
) -> PaymentMethodUseCases:
    return PaymentMethodUseCases(payment_method_repository)


def get_customer_payment_use_cases(
    payment_repository: PaymentRepository = Depends(get_payment_repository),
    purchase_assertion_client: PurchaseAssertionClient = Depends(
        get_purchase_assertion_client
    ),
    events_publisher: PaymentEventsPublisher = Depends(get_payment_events_publisher),
    stored_payment_method_repository: StoredPaymentMethodRepository = Depends(
        get_stored_payment_method_repository
    ),
) -> CustomerPaymentUseCases:
    return CustomerPaymentUseCases(
        payment_repository=payment_repository,
        purchase_assertion_client=purchase_assertion_client,
        events_publisher=events_publisher,
        stored_payment_method_repository=stored_payment_method_repository,
    )


def get_staff_payment_use_cases(
    payment_repository: PaymentRepository = Depends(get_payment_repository),
    events_publisher: PaymentEventsPublisher = Depends(get_payment_events_publisher),
) -> StaffPaymentUseCases:
    return StaffPaymentUseCases(
        payment_repository=payment_repository,
        events_publisher=events_publisher,
    )


def get_admin_payment_use_cases(
    payment_repository: PaymentRepository = Depends(get_payment_repository),
    events_publisher: PaymentEventsPublisher = Depends(get_payment_events_publisher),
) -> AdminPaymentUseCases:
    return AdminPaymentUseCases(
        payment_repository=payment_repository,
        events_publisher=events_publisher,
    )
