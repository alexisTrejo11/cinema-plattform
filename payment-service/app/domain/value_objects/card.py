from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    card_holder: str
    card_number: str
    cvv: str
    expiration_month: str
    expiration_year: str

