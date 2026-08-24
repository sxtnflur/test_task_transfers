from dataclasses import dataclass, field

import uuid
from transfers.domain.value_objects.base import ValueObject


@dataclass
class TransferId(ValueObject):
    value: uuid.UUID = field(default_factory=uuid.uuid4)
