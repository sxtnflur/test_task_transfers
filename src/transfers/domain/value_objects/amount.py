from dataclasses import dataclass
from decimal import Decimal

from transfers.domain.exceptions import ValueDomainError
from transfers.domain.value_objects.base import ValueObject


@dataclass
class Amount(ValueObject):
    value: Decimal

    def __post_init__(self):
        if not isinstance(self.value, Decimal):
            try:
                self.value = Decimal(self.value)
            except:
                raise ValueDomainError(
                    input=self.value, field='amount', message='Amount must be Decimal'
                )

        if self.value <= 0:
            raise ValueDomainError(
                input=self.value, field='amount', message='Amount must be greater than zero'
            )
