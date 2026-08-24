from dataclasses import dataclass, fields
from enum import Enum

from transfers.domain.value_objects.base import ValueObject


@dataclass
class Entity:
    def to_dict(self):
        """
        Returns dict with ValueObject.value
        """
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, ValueObject):
                value = value.value
            if isinstance(value, Enum):
                value = value.value
            result[field.name] = value
        return result
