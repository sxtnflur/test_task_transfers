from abc import ABC
from dataclasses import asdict

from transfers.domain.entities.transfer import Transfer
from sqlalchemy import insert, text, select, update, exists, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from transfers.domain.repositories import BaseRepository, EntityT
from . import models
from .models import Base


class PostgresBaseRepository(BaseRepository[EntityT], ABC):
    model: type[Base]
    entity: type[EntityT]

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, model: Base | None) -> EntityT | None:
        if model is None:
            return

        data = model.__dict__
        del data['_sa_instance_state']
        print(f'{data=}')
        entity = self.entity(**data)
        return entity

    async def get_one(self, **filters) -> EntityT | None:
        obj = await self.session.scalar(
            select(self.model)
            .filter_by(**filters)
        )
        return self._to_domain(obj)

    async def save(self, obj: EntityT) -> None:
        await self.session.execute(
            insert(self.model)
            .values(obj.to_dict())
        )

    async def save_idempotent(self, obj: EntityT, on_conflict: list[str]) -> None:
        keys = list(asdict(obj).keys())
        fields = ', '.join(keys)
        vals_names = ', '.join(list(map(lambda k: f':{k}', keys)))
        on_conflict_ = ', '.join(on_conflict)
        stmt = text(f'''
            INSERT INTO {self.model.__tablename__} ({fields})
            VALUES ({vals_names})
            ON CONFLICT ({on_conflict_}) DO NOTHING
        ''').bindparams(**obj.to_dict())
        await self.session.execute(stmt)

    async def update(self, filters: dict, updates: dict) -> None:
        await self.session.execute(
            update(self.model)
            .filter_by(**filters)
            .values(**updates)
        )

    async def exists(self, **filters) -> bool:
        return await self.session.scalar(
            select(exists().where(
                *[getattr(self.model, f) == v for f, v in filters.items()]
            ))
        )

    async def count(self, **filters) -> int:
        return await self.session.scalar(
            select(func.count())
            .select_from(self.model)
            .filter_by(**filters)
        )

    async def delete(self, **filters) -> None:
        await self.session.execute(
            delete(self.model)
            .filter_by(**filters)
        )


class TransfersPostgresRepository(PostgresBaseRepository[Transfer]):
    model = models.Transfer
    entity = Transfer
