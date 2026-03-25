from app.wallet.application.event_publisher import (
    WalletEventPublisher,
    TransactionEvents,
    Wallet,
    WalletTransaction,
)
from app.config.queue.rabbit_producer import RabbitMQProducer
from app.config.app_config import settings
import logging

logger = logging.getLogger("app")


class WalletEventProducerImpl(WalletEventPublisher):
    def __init__(self, producer: RabbitMQProducer):
        self.producer = producer

    async def publish_event(
        self,
        user_wallet: Wallet,
        new_transaction: WalletTransaction,
        event_type: TransactionEvents,
    ):
        try:
            await self.producer.connect()
            # Build serializable dicts manually because wallet carries arbitrary types
            # (UserId) that Pydantic cannot auto-serialize to JSON.
            # transactions excluded — not needed by downstream consumers.
            wallet_dict = {
                "id": user_wallet.id.to_string(),
                "user_id": user_wallet.user_id.to_string(),
                "balance": str(user_wallet.balance.amount),
                "currency": user_wallet.balance.currency.value,
                "created_at": user_wallet.created_at.isoformat(),
                "updated_at": user_wallet.updated_at.isoformat(),
                "transactions": None,
            }
            transaction_dict = {
                "transaction_id": str(new_transaction.transaction_id),
                "wallet_id": new_transaction.wallet_id.to_string(),
                "amount": str(new_transaction.amount.amount),
                "currency": new_transaction.amount.currency.value,
                "transaction_type": new_transaction.transaction_type.value,
                "payment_method": new_transaction.payment_details.payment_method,
                "payment_id": str(new_transaction.payment_details.payment_id),
                "timestamp": new_transaction.timestamp.isoformat(),
            }
            event_dict = {
                "data": {
                    "wallet": wallet_dict,
                    "transaction": transaction_dict,
                    "event_type": event_type.value,
                }
            }
            await self.producer.publish_message(
                event_dict, routing_key="transaction.completed"
            )
        except Exception as e:
            logger.error(f"Failed to publish wallet event: {e}", exc_info=True)
            raise
