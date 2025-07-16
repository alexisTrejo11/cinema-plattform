from app.wallet.domain.entities.wallet import WalletTransaction, Wallet
from abc import ABC, abstractmethod
from enum import Enum

class TransactionEvents(Enum):
    CHARGE_CREDIT = "CHARGE_CREDIT"
    BUY_PRODUCT = "BUY_PRODUCT"

class WalletEventPublisher(ABC):
    @abstractmethod
    async def publish_event(self, user_wallet: Wallet, new_transaction: WalletTransaction, event_type: TransactionEvents):
        pass
    