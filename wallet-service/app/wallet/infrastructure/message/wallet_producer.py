from app.wallet.application.event_publisher import WalletEventPublisher, TransactionEvents, Wallet, WalletTransaction
from config.queue.rabbit_producer import RabbitMQProducer
from config.app_config import settings
import logging

logger = logging.getLogger("app")

class WalletEventProducerImpl(WalletEventPublisher):
    def __init__(self, producer: RabbitMQProducer):
        self.producer = producer

    async def publish_event(
        self,
        user_wallet: Wallet,
        new_transaction: WalletTransaction,
        event_type: TransactionEvents
    ):
        try:
            await self.producer.connect()
            wallet_dict = user_wallet.to_dict()
            wallet_dict["transactions"] = None
            event_dict = {
                "data" : {
                    "wallet" : wallet_dict,
                    "transaction" : new_transaction.to_dict(),
                    "event_type" : event_type.value
                }
            }
            await self.producer.publish_message(event_dict, routing_key="transaction.completed")
        except Exception as e:
            logger.error(f"Failed to publish wallet event: {e}", exc_info=True)
            raise