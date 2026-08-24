from abc import ABC, abstractmethod
from typing_extensions import Generic, TypeVar

from transfers.domain.entities.transfer import Transfer
from transfers.domain.entities.base import Entity

EntityT = TypeVar('EntityT', bound=Entity)


class BaseRepository(ABC, Generic[EntityT]):
    @abstractmethod
    async def get_one(self, **filters) -> EntityT:
        pass

    @abstractmethod
    async def save(self, obj: EntityT) -> None:
        pass

    @abstractmethod
    async def save_idempotent(self, obj: EntityT, on_conflict: list[str]) -> None:
        pass

    @abstractmethod
    async def update(self, filters: dict, updates: dict) -> None:
        pass

    @abstractmethod
    async def exists(self, **filters) -> bool:
        pass

    @abstractmethod
    async def count(self, **filters) -> int:
        pass

    @abstractmethod
    async def delete(self, **filters) -> None:
        pass


TransfersRepository = BaseRepository[Transfer]
