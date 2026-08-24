from config.settings import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from transfers.app.transfers.service import TransfersService
from transfers.infra.database import (
    TransfersPostgresRepository
)
from transfers.app.webhook.service import WebhookSender, WebhookService
from transfers.infra.database.engine import AsyncSessionLocal
from transfers.infra.webhook.sign import WebhookSigner
from transfers.infra.webhook.client import HttpxWebhookSender
from typing_extensions import Annotated


async def get_db_session():
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    else:
        await session.commit()
    finally:
        await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_webhook_signer() -> WebhookSigner:
    return WebhookSigner(settings.api_token)


WebhookSigner = Annotated[WebhookSigner, Depends(get_webhook_signer)]


def get_webhook_sender(
        signer: WebhookSigner
) -> WebhookSender:
    return HttpxWebhookSender(signer=signer)


WebhookSender = Annotated[WebhookSender, Depends(get_webhook_sender)]


def get_webhook_service(
    webhook_sender: WebhookSender
):
    return WebhookService(
        from_address=settings.tx_from_address,
        webhook_url=settings.webhook_url,
        webhook_sender=webhook_sender
    )


WebhookService = Annotated[WebhookService, Depends(get_webhook_service)]


def get_transfer_service(
        db_session: DbSession,
        webhook_service: WebhookService
) -> TransfersService:
    repository = TransfersPostgresRepository(db_session)

    return TransfersService(
        transfers_repo=repository,
        webhook_service=webhook_service
    )


TransfersService = Annotated[TransfersService, Depends(get_transfer_service)]
