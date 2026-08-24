from auth import VerifiedByToken
from transfers.app.transfers.dto import CreateTransferDTO
from fastapi import APIRouter, BackgroundTasks
from transfers.presentation.http.schemas import CreateTransferRequest, TransferResponse
from starlette import status

from .depends import TransfersService
from transfers.app.webhook.schemas import WebhookPayload

router = APIRouter(prefix='/transfer', tags=['Transfers'])


@router.post(
    '',
    response_model=TransferResponse,
    status_code=status.HTTP_200_OK
)
async def process_transfer(
    _: VerifiedByToken,
    request: CreateTransferRequest,
    service: TransfersService,
    bg_tasks: BackgroundTasks
):
    transfer_dto = CreateTransferDTO(
        external_id=request.external_id,
        amount=request.amount,
        currency=request.currency,
        destination=request.destination
    )
    transfer = await service.create(transfer_dto)
    bg_tasks.add_task(service.execute_transfer, transfer_id=transfer.id.value)
    return TransferResponse(
        id=transfer.id,
        external_id=transfer.external_id.value,
        currency=transfer.currency.value,
        amount=transfer.amount.value,
        destination=transfer.destination.value,
        status=transfer.status
    )


@router.post(
    '/test_webhook',
    response_model=WebhookPayload,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
async def example_client_webhook(
    request: WebhookPayload
):
    return request
