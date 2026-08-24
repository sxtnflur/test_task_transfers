from dataclasses import dataclass

from .base import ValueObject
from ..exceptions import ValueDomainError


@dataclass
class Destination(ValueObject):
    def __post_init__(self):
        if len(self.value) > 1_000:
            raise ValueDomainError(
                input=str(self.value),
                field='destination',
                message=f'Too Length destination. Max length is 1.000. Your value\'s length is {len(self.value)}'
            )
