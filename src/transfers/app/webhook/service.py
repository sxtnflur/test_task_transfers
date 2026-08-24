from transfers.app.webhook.ports import WebhookSender
from .dto import WebhookPayloadDTO
from .schemas import WebhookPayload, WebhookDetails


class WebhookService:
    def __init__(
            self,
            from_address: str,
            webhook_url: str,
            webhook_sender: WebhookSender
    ):
        self.webhook_sender = webhook_sender
        self.from_address = from_address
        self.webhook_url = webhook_url

    async def send(self, payload_dto: WebhookPayloadDTO) -> None:
        """
        :raise ErrorSendWebhook
        """
        payload = WebhookPayload(
            id=payload_dto.id,
            external_id=payload_dto.external_id,
            amount=payload_dto.amount,
            status=payload_dto.status,
            details=WebhookDetails(
                from_address=self.from_address,
                to_address=payload_dto.destination,
                tx_hash=payload_dto.tx_hash
            )
        )
        await self.webhook_sender.send(
            payload=payload, webhook_url=self.webhook_url
        )
