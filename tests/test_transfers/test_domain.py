from contextlib import nullcontext
from decimal import Decimal

import pytest
import uuid
from transfers.domain.entities.transfer import Transfer
from transfers.domain.exceptions import ValueDomainError
from transfers.domain.value_objects.amount import Amount
from transfers.domain.value_objects.currency import Currency
from transfers.domain.value_objects.destination import Destination
from transfers.domain.value_objects.external_id import ExternalId
from transfers.domain.value_objects.transfer_id import TransferId


@pytest.mark.parametrize(
    'id,amount,currency,destination,external_id,raises',
    [
        ('550e8400-e29b-41d4-a716-4466554400000', 10, 'rub',
         'test', 'test', nullcontext()),
        ('550e8400-e29b-41d4-a716-4466554400000', Decimal(10.09), 'rub',
         'test', 'test', nullcontext()),
        (uuid.uuid4(), Decimal(10.09), 'aaa',
         'test', 'test', nullcontext()),
        (uuid.uuid4(), 10.09, 'bbb',
         'test', 'test', nullcontext()),

        ('550e8400-e29b-41d4-a716-4466554400000', 0, 'rub',
         'test', 'test', pytest.raises(ValueDomainError)),
        ('550e8400-e29b-41d4-a716-4466554400000', 10, 'ruble',
         'test', 'test', pytest.raises(ValueDomainError)),
        ('550e8400-e29b-41d4-a716-4466554400000', 'rub', 'rub',
         'test', 'test', pytest.raises(ValueDomainError)),
        ('550e8400-e29b-41d4-a716', 'rub', 'rub',
         'test', 'test', pytest.raises(ValueDomainError)),
    ]
)
def test_create_transfer(
        id: TransferId,
        amount: float | Amount,
        currency: str | Currency,
        destination: str | Destination,
        external_id: str | ExternalId,
        raises
):
    with raises:
        transfer = Transfer(
            id=id,
            amount=amount,
            currency=currency,
            destination=destination,
            external_id=external_id
        )

        assert isinstance(transfer.id, TransferId)
        assert isinstance(transfer.amount, Amount)
        assert isinstance(transfer.currency, Currency)
        assert isinstance(transfer.destination, Destination)
        assert isinstance(transfer.external_id, ExternalId)
