from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateTransferDTO:
    external_id: str
    currency: str
    amount: Decimal
    destination: str
    comment: str | None = None
