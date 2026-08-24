import uuid

from transfers.domain.value_objects.amount import Amount
from transfers.domain.value_objects.currency import Currency
from transfers.domain.value_objects.external_id import ExternalId

from .dto import CreateTransferDTO
from transfers.domain.repositories import TransfersRepository
from transfers.domain.entities.transfer import Transfer
from ..webhook.dto import WebhookPayloadDTO
from ..webhook.service import WebhookService
from ...domain.value_objects.destination import Destination
from ...domain.value_objects.transfer_id import TransferId


class TransfersService:
    def __init__(
            self,
            transfers_repo: TransfersRepository,
            webhook_service: WebhookService
    ):
        self.transfers_repo = transfers_repo
        self.webhook_service = webhook_service

    async def create(self, transfer_dto: CreateTransferDTO) -> Transfer:
        external_id = ExternalId(transfer_dto.external_id)

        if await self.transfers_repo.exists(external_id=external_id.value):
            transfer = await self.transfers_repo.get_one(external_id=external_id.value)
        else:
            transfer = Transfer(
                id=TransferId(),
                external_id=external_id,
                currency=Currency(transfer_dto.currency),
                amount=Amount(transfer_dto.amount),
                destination=Destination(transfer_dto.destination),
                comment=transfer_dto.comment
            )
            await self.transfers_repo.save(transfer)

        return transfer

    async def execute_transfer(self, transfer_id: uuid.UUID) -> None:
        transfer_id = TransferId(transfer_id).value

        transfer: Transfer = await self.transfers_repo.get_one(
            id=transfer_id
        )

        try:
            ...  # Какая-то логика
        except:
            result_status = transfer.fail()
        else:
            result_status = transfer.complete()

        await self.transfers_repo.update(
            filters=dict(id=transfer_id),
            updates=dict(status=result_status.value)
        )

        try:
            await self.webhook_service.send(
                payload_dto=WebhookPayloadDTO(
                    id=transfer.id.value,
                    external_id=transfer.external_id.value,
                    amount=transfer.amount.value,
                    destination=transfer.destination.value,
                    status=result_status,
                    tx_hash=None
                )
            )
        except Exception:
            # TODO: Можно реализовать логику retry
            pass
