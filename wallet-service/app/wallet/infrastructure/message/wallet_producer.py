from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from kafka import KafkaProducer

from app.config.app_config import settings
from app.wallet.domain.entities import Wallet, WalletTransaction
from app.wallet.domain.interfaces import (
    TransactionEvents,
    WalletEventPublisher,
)

logger = logging.getLogger(__name__)


class _KafkaJsonProducer:
    """Thin sync Kafka client; async entry points use a thread executor."""

    def __init__(
        self,
        bootstrap_servers: str,
        client_id: str,
        topic: str,
    ) -> None:
        servers = [s.strip() for s in bootstrap_servers.split(",") if s.strip()]
        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=servers,
            client_id=client_id,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=5,
        )

    def send_json(self, payload: dict[str, Any], key: str | None = None) -> None:
        kb = key.encode("utf-8") if key else None
        fut = self._producer.send(self._topic, value=payload, key=kb)
        fut.get(timeout=15)
        self._producer.flush(timeout=10)

    def close(self) -> None:
        self._producer.flush(timeout=10)
        self._producer.close()


class WalletEventProducerImpl(WalletEventPublisher):
    def __init__(self, kafka: _KafkaJsonProducer) -> None:
        self._kafka = kafka

    async def publish_event(
        self,
        user_wallet: Wallet,
        new_transaction: WalletTransaction,
        event_type: TransactionEvents,
    ) -> None:
        try:
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
                "transaction_id": str(new_transaction.transaction_id.value),
                "wallet_id": new_transaction.wallet_id.to_string(),
                "amount": str(new_transaction.amount.amount),
                "currency": new_transaction.amount.currency.value,
                "transaction_type": new_transaction.transaction_type.value,
                "payment_method": new_transaction.payment_details.payment_method,
                "payment_id": str(new_transaction.payment_details.payment_id),
                "timestamp": new_transaction.timestamp.isoformat(),
            }
            event_dict: dict[str, Any] = {
                "data": {
                    "wallet": wallet_dict,
                    "transaction": transaction_dict,
                    "event_type": event_type.value,
                }
            }
            await asyncio.to_thread(
                self._kafka.send_json,
                event_dict,
                "transaction.completed",
            )
        except Exception as e:
            logger.error("Failed to publish wallet event: %s", e, exc_info=True)
            raise


def build_wallet_event_producer() -> WalletEventPublisher:
    kafka = _KafkaJsonProducer(
        settings.KAFKA_BOOTSTRAP_SERVERS,
        settings.KAFKA_CLIENT_ID,
        settings.KAFKA_WALLET_EVENTS_TOPIC,
    )
    return WalletEventProducerImpl(kafka)
