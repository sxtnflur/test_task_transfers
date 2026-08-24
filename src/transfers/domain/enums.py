from enum import StrEnum, auto


class TransferStatusResulted(StrEnum):
    failed = auto()
    completed = auto()


class TransferStatus(StrEnum):
    failed = auto()
    completed = auto()
    pending = auto()
