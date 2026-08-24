import pytest
from transfers.domain.entities.transfer import Transfer
from transfers.domain.enums import TransferStatus
from transfers.domain.value_objects.transfer_id import TransferId
from transfers.infra.database import TransfersPostgresRepository


@pytest.mark.parametrize(
    'transfer',
    [
        Transfer(
            id=TransferId(),
            amount=10,
            currency='usd',
            destination='asdsa',
            external_id='asdsad',
            comment='asdsadsadsa'
        )
    ]
)
async def test_transfers_repo(db_session, transfer):
    repo = TransfersPostgresRepository(db_session)

    # CREATE
    await repo.save(transfer)

    transfer_from_db = await repo.get_one(id=transfer.id.value)

    assert transfer_from_db == transfer
    assert transfer_from_db.status == TransferStatus.pending

    # UPDATE

    await repo.update(
        filters=dict(id=transfer.id.value),
        updates=dict(status=TransferStatus.completed)
    )

    transfer_from_db_2 = await repo.get_one(id=transfer.id.value)

    assert transfer_from_db_2.status == TransferStatus.completed

    transfer_from_db_2.status = TransferStatus.pending

    assert transfer_from_db_2 == transfer_from_db

    # DELETE

    await repo.delete(id=transfer.id.value)

    assert await repo.get_one(id=transfer.id.value) is None
