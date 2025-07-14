from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from uuid import UUID

from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from app.wallet.domain.entities.wallet_transaction import (
    WalletTransaction as DomainWalletTransaction,
)
from app.wallet.infrastructure.persistence.sqlalchemy_models import (
    WalletTransactionSQLModel,
)


class SqlAlchemyWalletTransactionRepository(WalletTransactionRepository):
    """SQLAlchemy implementation of the WalletTransactionRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, transaction: DomainWalletTransaction
    ) -> DomainWalletTransaction:
        """
        Creates a new wallet transaction in the database.
        """
        transaction_sql_model = WalletTransactionSQLModel.from_domain(transaction)

        self.session.add(transaction_sql_model)
        await self.session.flush()
        await self.session.commit()

        return transaction_sql_model.to_domain_transaction()

    async def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a wallet transaction by its ID from the database.
        """
        result = await self.session.execute(
            delete(WalletTransactionSQLModel).where(
                WalletTransactionSQLModel.transaction_id == transaction_id
            )
        )
        await self.session.commit()

        return result.rowcount > 0
