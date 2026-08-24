from decimal import Decimal

import pytest

from transfers.app.transfers.dto import CreateTransferDTO
from transfers.app.webhook.exceptions import ErrorSendWebhook
from transfers.domain.enums import TransferStatus
from transfers.domain.value_objects.amount import Amount
from transfers.domain.value_objects.currency import Currency
from transfers.domain.value_objects.destination import Destination
from transfers.domain.value_objects.external_id import ExternalId
from transfers.domain.value_objects.transfer_id import TransferId
from transfers.domain.entities.transfer import Transfer


@pytest.mark.parametrize(
    'transfer_dto',
    [
        CreateTransferDTO(
            external_id='test',
            currency='usd',
            amount=Decimal(10),
            destination='test',
            comment='test comment'
        )
    ]
)
async def test_transfer_service_create(
        transfer_service, transfer_dto: CreateTransferDTO
):
    transfer = await transfer_service.create(
        transfer_dto=transfer_dto
    )

    print(transfer)
    assert transfer is not None
    assert isinstance(transfer, Transfer)

    assert isinstance(transfer.id, TransferId)
    assert isinstance(transfer.amount, Amount)
    assert isinstance(transfer.currency, Currency)
    assert isinstance(transfer.destination, Destination)
    assert isinstance(transfer.external_id, ExternalId)

    assert transfer.amount.value == transfer_dto.amount
    assert transfer.currency.value == transfer_dto.currency.upper()
    assert transfer.destination.value == transfer_dto.destination
    assert transfer.external_id.value == transfer_dto.external_id
    assert transfer.comment == transfer_dto.comment

    assert transfer.status == TransferStatus.pending

    added_transfer = await transfer_service.transfers_repo.get_one(id=transfer.id.value)

    assert added_transfer == transfer

    transfer_dupl = await transfer_service.create(transfer_dto)

    assert transfer_dupl == added_transfer == transfer

    assert await transfer_service.transfers_repo.count(external_id=transfer.external_id.value) == 1


@pytest.mark.parametrize(
    'transfer_dto',
    [
        CreateTransferDTO(
            external_id='test',
            currency='usd',
            amount=Decimal(10),
            destination='test',
            comment='test comment'
        ),
    ]
)
async def test_execute_transfer(
        transfer_service, transfer_dto: CreateTransferDTO
):
    assert isinstance(transfer_dto, CreateTransferDTO)

    transfer = await transfer_service.create(
        transfer_dto=transfer_dto
    )

    try:
        await transfer_service.execute_transfer(transfer_id=transfer.id.value)
    except ErrorSendWebhook:
        pass

    transfer_from_db = await transfer_service.transfers_repo.get_one(id=transfer.id.value)

    assert transfer_from_db.id == transfer.id
    assert transfer_from_db.amount == transfer.amount
    assert transfer_from_db.currency == transfer.currency
    assert transfer_from_db.currency == transfer.currency
    assert transfer_from_db.external_id == transfer.external_id

    assert transfer_from_db.status == TransferStatus.completed
    assert transfer.status == TransferStatus.pending
