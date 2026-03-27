from typing import List

from app.wallet.application.queries import SearchTransactionQuery
from app.wallet.domain.entities import WalletTransaction
from app.wallet.domain.interfaces import WalletTransactionRepository as TransactionRepository


class SearchTransactionUseCase:
    def __init__(self, repository: TransactionRepository) -> None:
        self.repository = repository

    # TODO: Return page metadata
    async def execute(
        self, query: SearchTransactionQuery
    ) -> List[WalletTransaction]:
        return await self.repository.search(query)
