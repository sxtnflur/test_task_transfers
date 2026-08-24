import pytest
import pytest_asyncio
from config.settings import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from transfers.infra.database import Base
from transfers.presentation.http.depends import (
    get_db_session, get_transfer_service, get_webhook_service,
    get_webhook_sender, get_webhook_signer
)


@pytest_asyncio.fixture
async def db_engine():
    assert settings.database_url.endswith('/test_transfers'), "Запуск только на тестовой БД!"

    engine = create_async_engine(settings.database_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    session_factory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with session_factory() as session:
        yield session


@pytest.fixture(scope='function')
def webhook_sender():
    return get_webhook_sender(signer=get_webhook_signer())


@pytest.fixture(scope='function')
def webhook_service(webhook_sender):
    return get_webhook_service(webhook_sender=webhook_sender)


@pytest.fixture(scope='function')
def transfer_service(db_session, webhook_service):
    return get_transfer_service(db_session, webhook_service=webhook_service)
