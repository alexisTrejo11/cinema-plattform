from typing import List
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete
from uuid import UUID
from sqlalchemy import select, asc, desc
from app.wallet.domain.value_objects import WalletId
from app.wallet.domain.entities.wallet import WalletTransaction as Transaction

from app.wallet.domain.repositories.transaction_repository import (
    WalletTransactionRepository,
)
from app.wallet.domain.entities.wallet_transaction import (
    WalletTransaction as DomainWalletTransaction,
)
from .sqlalchemy_models import (
    WalletTransactionSQLModel as TransactionSQLModel,
)
from app.wallet.application.query.queries import (
    TransactionByWalletQuery,
    SearchTransactionQuery,
)

logger = logging.getLogger("app")


class SqlAlchemyWalletTransactionRepository(WalletTransactionRepository):
    """SQLAlchemy implementation of the WalletTransactionRepository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, query: SearchTransactionQuery) -> List[Transaction]:
        stmt = select(TransactionSQLModel)
        filters = []

        # Apply filters based on query parameters
        # if query.userId:
        # filters.append(TransactionSQLModel.user_id == query.userId.value)
        if query.walletId:
            filters.append(TransactionSQLModel.wallet_id == query.walletId.value)
        if query.type:
            filters.append(TransactionSQLModel.transaction_type == query.type)

        if query.min_amount:
            try:
                min_amount_float = float(query.min_amount)
                filters.append(TransactionSQLModel.amount_value >= min_amount_float)
            except ValueError:
                logger.warning(
                    f"Warning: Invalid min_amount '{query.min_amount}'. Ignoring filter."
                )
        if query.max_amount:
            try:
                max_amount_float = float(query.max_amount)
                filters.append(TransactionSQLModel.amount_value <= max_amount_float)
            except ValueError:
                logger.warning(
                    f"Warning: Invalid max_amount '{query.max_amount}'. Ignoring filter."
                )

        if query.created_before:
            filters.append(TransactionSQLModel.timestamp <= query.created_before)
        if query.created_after:
            filters.append(TransactionSQLModel.timestamp >= query.created_after)

        if query.payment_method:
            filters.append(TransactionSQLModel.payment_method == query.payment_method)
        if query.payment_id:
            filters.append(TransactionSQLModel.payment_reference == query.payment_id)

        # Apply filters
        if filters:
            stmt = stmt.where(and_(*filters))

        # sorting
        sort_attr = getattr(TransactionSQLModel, query.sort_by, None)
        if sort_attr is not None:
            if query.sort_direction.lower() == "desc":
                stmt = stmt.order_by(desc(sort_attr))
            else:
                stmt = stmt.order_by(asc(sort_attr))
        else:
            logger.warning(
                f"Warning: Invalid sort_by parameter '{query.sort_by}'. Defaulting to 'created_at'."
            )
            stmt = stmt.order_by(asc(TransactionSQLModel.timestamp))

        # pagination
        stmt = stmt.offset(query.offset).limit(query.limit)

        result = await self.session.execute(stmt)
        sql_transactions = result.scalars().all()
        return [TransactionSQLModel.to_domain_transaction(t) for t in sql_transactions]

    async def list_by_wallet_id(self, query: TransactionByWalletQuery):
        stmt = select(TransactionSQLModel).where(
            TransactionSQLModel.wallet_id == query.walletId.value
        )

        sort_attr = getattr(TransactionSQLModel, query.sort_by, None)

        if sort_attr is not None:
            if query.sort_direction.lower() == "desc":
                stmt = stmt.order_by(desc(sort_attr))
            else:
                stmt = stmt.order_by(asc(sort_attr))
        else:
            logger.warning(
                f"Invalid sort_by parameter '{query.sort_by}'. Defaulting to 'created_at'."
            )
            stmt = stmt.order_by(asc(TransactionSQLModel.timestamp))

        stmt = stmt.offset(query.offset).limit(query.limit)

        result = await self.session.execute(stmt)
        sql_transactions = result.scalars().all()
        return [TransactionSQLModel.to_domain_transaction(t) for t in sql_transactions]

    async def create(
        self, transaction: DomainWalletTransaction
    ) -> DomainWalletTransaction:
        """
        Creates a new wallet transaction in the database.
        """
        transaction_sql_model = TransactionSQLModel.from_domain(transaction)

        self.session.add(transaction_sql_model)
        await self.session.flush()
        await self.session.commit()

        return transaction_sql_model.to_domain_transaction()

    async def delete(self, transaction_id: UUID) -> bool:
        """
        Deletes a wallet transaction by its ID from the database.
        """
        result = await self.session.execute(
            delete(TransactionSQLModel).where(
                TransactionSQLModel.transaction_id == transaction_id
            )
        )
        await self.session.commit()

        return result.rowcount > 0
