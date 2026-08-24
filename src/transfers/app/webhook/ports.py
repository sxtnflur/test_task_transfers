from abc import ABC, abstractmethod

from pydantic import BaseModel


class WebhookSender(ABC):

    @abstractmethod
    async def send(
        self, payload: BaseModel, webhook_url: str
    ) -> None:
        """
        :raise ErrorSendWebhook
        """
