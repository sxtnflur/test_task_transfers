from dataclasses import dataclass, field
import uuid
from transfers.domain.entities.base import Entity

from transfers.domain.enums import TransferStatus, TransferStatusResulted
from transfers.domain.value_objects.amount import Amount
from transfers.domain.value_objects.currency import Currency
from transfers.domain.value_objects.destination import Destination
from transfers.domain.value_objects.external_id import ExternalId
from transfers.domain.value_objects.transfer_id import TransferId


@dataclass
class Transfer(Entity):
    id: TransferId
    external_id: ExternalId
    currency: Currency
    amount: Amount
    destination: Destination
    comment: str | None = None
    status: TransferStatus = TransferStatus.pending

    def __post_init__(self):
        if not isinstance(self.id, TransferId):
            self.id = TransferId(self.id)

        if not isinstance(self.external_id, ExternalId):
            self.external_id = ExternalId(self.external_id)

        if not isinstance(self.currency, Currency):
            self.currency = Currency(self.currency)

        if not isinstance(self.amount, Amount):
            self.amount = Amount(self.amount)

        if not isinstance(self.destination, Destination):
            self.destination = Destination(self.destination)

    def complete(self) -> TransferStatusResulted:
        if self.status == TransferStatus.failed:
            raise ValueError("Failed transfer cannot be completed")

        self.status = TransferStatus.completed
        return TransferStatusResulted.completed

    def fail(self) -> TransferStatusResulted:
        if self.status == TransferStatus.completed:
            raise ValueError("Completed transfer cannot be failed")

        self.status = TransferStatus.failed
        return TransferStatusResulted.completed
