import httpx
from pydantic import BaseModel

from .sign import WebhookSigner
from transfers.app.webhook.service import WebhookSender
from ...app.webhook.exceptions import ErrorSendWebhook, ErrorWebhookResponse


class HttpxWebhookSender(WebhookSender):
    def __init__(
        self,
        signer: WebhookSigner
    ):
        self.signer = signer

    async def send(
        self, payload: BaseModel, webhook_url: str
    ) -> None:
        body = payload.model_dump_json().encode('utf-8')
        signature = self.signer.sign(body)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    content=body,
                    headers={
                        "Content-Type": "application/json",
                        "X-signature": signature
                    }
                )
        except httpx.HTTPError as e:
            raise ErrorSendWebhook(e.__str__())

        if response.status_code >= 400:
            raise ErrorWebhookResponse(status=response.status_code, message=response.text)
