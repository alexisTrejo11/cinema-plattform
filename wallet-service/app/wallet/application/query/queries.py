from pydantic import BaseModel
from app.wallet.domain.value_objects import WalletId
from app.user.domain.value_objects import UserId


class WalletQueryBase(BaseModel):
    include_transactions: bool = False
    offset: int = 0
    limit: int = 10


class GetWalletByIdQuery(WalletQueryBase):
    walletId: WalletId

    @staticmethod
    def from_request(wallet_uuid, include_transactions, limit, offset):
        return GetWalletByIdQuery(
            walletId=WalletId(wallet_uuid),
            include_transactions=include_transactions,
            limit=limit,
            offset=offset,
        )


class GetWalletByUserIdQuery(WalletQueryBase):
    userId: UserId

    @staticmethod
    def from_request(user_uuid, include_transactions, limit, offset):
        return GetWalletByUserIdQuery(
            userId=UserId(user_uuid),
            include_transactions=include_transactions,
            limit=limit,
            offset=offset,
        )
