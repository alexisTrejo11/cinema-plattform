from typing import List

from app.shared.core.pagination import Page
from app.wallet.domain.entities import WalletTransaction
from app.wallet.domain.value_objects import WalletTransactionId
from app.wallet.domain.interfaces import WalletTransactionRepository
from ..queries import SearchTransactionQuery


class SearchTransactionUseCase:
    def __init__(self, repository: WalletTransactionRepository) -> None:
        self.repository = repository

    async def execute(self, query: SearchTransactionQuery) -> Page[WalletTransaction]:
        return await self.repository.search(query)


class GetTransactionByIdUseCase:
    def __init__(self, repository: WalletTransactionRepository) -> None:
        self.repository = repository

    async def execute(self, transaction_id: WalletTransactionId) -> WalletTransaction:
        return await self.repository.find_by_id(transaction_id)
