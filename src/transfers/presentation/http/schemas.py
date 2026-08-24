from decimal import Decimal

from transfers.domain.enums import TransferStatus
from uuid import UUID

from pydantic import BaseModel


class CreateTransferRequest(BaseModel):
    external_id: str
    currency: str
    amount: Decimal
    destination: str
    comment: str | None = None


class TransferResponse(BaseModel):
    id: UUID
    external_id: str
    currency: str
    amount: Decimal
    destination: str
    status: TransferStatus
