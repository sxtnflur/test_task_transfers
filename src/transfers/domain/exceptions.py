from typing_extensions import Any


class DomainError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValueDomainError(DomainError, ValueError):
    def __init__(self, input: Any, field: str, message: str | None = None):
        _message = f'Invalid Value ({input!r}) for {field}'
        if message:
            _message += f' ({message})'

        super().__init__(_message)
