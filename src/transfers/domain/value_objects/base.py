from dataclasses import dataclass

from typing_extensions import Any


@dataclass
class ValueObject:
    value: Any

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
