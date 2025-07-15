from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from app.wallet.domain.value_objects import Money, PaymentDetails, Currency
from app.wallet.domain.entities.wallet import Wallet, WalletTransaction

class WalletOperationRequest(BaseModel):
    """DTO for adding credit to a wallet."""
    wallet_id: UUID
    amount: Decimal
    currency: Currency
    payment_id: UUID
    payment_method: str
    
    
    model_config = ConfigDict(from_attributes=True)