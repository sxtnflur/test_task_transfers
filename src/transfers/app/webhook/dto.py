from decimal import Decimal

import uuid
from dataclasses import dataclass
from transfers.domain.enums import TransferStatusResulted


@dataclass
class WebhookPayloadDTO:
    id: uuid.UUID
    external_id: str
    amount: Decimal
    destination: str
    status: TransferStatusResulted
    tx_hash: str | None = None
