from decimal import Decimal

import uuid
from pydantic import BaseModel
from transfers.domain.enums import TransferStatusResulted


class WebhookDetails(BaseModel):
    from_address: str
    to_address: str
    tx_hash: str | None = None


class WebhookPayload(BaseModel):
    id: uuid.UUID
    external_id: str
    amount: Decimal
    status: TransferStatusResulted
    details: WebhookDetails
