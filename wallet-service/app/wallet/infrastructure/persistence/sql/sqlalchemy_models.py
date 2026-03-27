import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.postgres_config import Base

from app.wallet.domain.enums import Currency, TransactionType
from app.wallet.domain.value_objects import (
    Money,
    PaymentDetails,
    WalletId,
    UserId,
    WalletTransactionId,
)
from app.wallet.domain.entities import WalletTransaction, Wallet


class WalletTransactionSQLModel(Base):
    __tablename__ = "wallet_transactions"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    wallet_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("cinema_wallets.id"),
        nullable=False,
        index=True,
    )
    amount_value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    amount_currency: Mapped[Currency] = mapped_column(
        Enum(Currency, name="currency_enum"), nullable=False
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum"), nullable=False
    )
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    wallet: Mapped["WalletSQLModel"] = relationship(
        "WalletSQLModel", back_populates="transactions"
    )

    def __repr__(self) -> str:
        return (
            f"<WalletTransactionSQLModel(id={self.transaction_id}, "
            f"wallet_id={self.wallet_id}, "
            f"amount={self.amount_value} {self.amount_currency.value}, "
            f"type={self.transaction_type.value})>"
        )

    def to_domain(self) -> WalletTransaction:
        ref = self.payment_reference
        if not ref:
            raise ValueError("payment_reference is required to map transaction")
        pid = uuid.UUID(ref) if isinstance(ref, str) else ref
        return WalletTransaction(
            transaction_id=WalletTransactionId(value=self.transaction_id),
            wallet_id=WalletId(value=self.wallet_id),
            amount=Money(amount=self.amount_value, currency=self.amount_currency),
            transaction_type=self.transaction_type,
            payment_details=PaymentDetails(
                payment_method=self.payment_method,
                payment_id=pid,
            ),
            timestamp=self.timestamp,
        )

    def to_domain_transaction(self) -> WalletTransaction:
        return self.to_domain()

    @classmethod
    def from_domain(
        cls, domain_transaction: WalletTransaction
    ) -> "WalletTransactionSQLModel":
        tid = domain_transaction.transaction_id.value
        return cls(
            transaction_id=tid,
            wallet_id=domain_transaction.wallet_id.value,
            amount_value=domain_transaction.amount.amount,
            amount_currency=domain_transaction.amount.currency,
            transaction_type=domain_transaction.transaction_type,
            payment_method=(
                domain_transaction.payment_details.payment_method
                if domain_transaction.payment_details
                else ""
            ),
            payment_reference=(
                str(domain_transaction.payment_details.payment_id)
                if domain_transaction.payment_details
                else None
            ),
            timestamp=domain_transaction.timestamp,
        )


class WalletSQLModel(Base):
    """SQLAlchemy model for the wallets table."""

    __tablename__ = "cinema_wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, index=True
    )
    balance_amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    balance_currency: Mapped[Currency] = mapped_column(
        Enum(Currency, name="currency_enum"), nullable=False, default=Currency.USD
    )

    transactions: Mapped[List["WalletTransactionSQLModel"]] = relationship(
        "WalletTransactionSQLModel",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<WalletSQLModel(id={self.id}, user_id={self.user_id}, "
            f"balance={self.balance_amount} {self.balance_currency.value})>"
        )

    def to_domain_wallet(self) -> Wallet:
        domain_wallet = Wallet(
            id=WalletId(value=self.id),
            user_id=UserId(self.user_id),
            balance=Money(amount=self.balance_amount, currency=self.balance_currency),
        )
        if self.transactions:
            domain_wallet.set_transactions([tx.to_domain() for tx in self.transactions])
        return domain_wallet

    @classmethod
    def from_domain(cls, domain_wallet: Wallet) -> "WalletSQLModel":
        return cls(
            id=domain_wallet.id.value,
            user_id=domain_wallet.user_id.value,
            balance_amount=domain_wallet.balance.amount,
            balance_currency=domain_wallet.balance.currency,
        )
