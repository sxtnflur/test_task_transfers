from dataclasses import dataclass

from transfers.domain.value_objects.base import ValueObject


@dataclass
class ExternalId(ValueObject):
    value: str
