from pydantic import BaseModel, Field


class CreatePaymentMethodCommand(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    card_holder: str = Field(..., description="The name of the card holder")
    card_number: str = Field(..., description="The number of the card")
    cvv: str = Field(..., description="The CVV of the card")
    expiration_month: str = Field(..., description="The month of the expiration date")
    expiration_year: str = Field(..., description="The year of the expiration date")


class SoftDeletePaymentMethodCommand(BaseModel):
    id: str = Field(..., description="The ID of the payment method")
