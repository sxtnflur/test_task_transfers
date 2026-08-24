from transfers.domain.exceptions import DomainError


class ErrorSendWebhook(DomainError):
    def __init__(self, message: str | None = None):
        self.message = f'Error during sending webhook'
        if message:
            self.message += f': {message}'


class ErrorWebhookResponse(ErrorSendWebhook):
    def __init__(self, status: int, message: str | None = None):
        self.status = status
        message_ = f'<{status} Response>'
        if message:
            message_ += ' ' + message

        super().__init__(message_)