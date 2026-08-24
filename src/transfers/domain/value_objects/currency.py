from dataclasses import dataclass

from transfers.domain.exceptions import ValueDomainError
from transfers.domain.value_objects.base import ValueObject


@dataclass
class Currency(ValueObject):
    def __post_init__(self):
        value = self.value.upper()

        if len(value) != 3:
            raise ValueDomainError(
                input=self.value,
                field='currency',
                message="Length is more than 3"
            )

        self.value = value
