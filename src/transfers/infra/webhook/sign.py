import hashlib
import hmac


class WebhookSigner:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _key(self) -> bytes:
        return hashlib.sha256(
            self.api_key.encode()
        ).digest()

    def sign(self, body: bytes) -> str:
        return hmac.new(
            self._key(),
            body,
            hashlib.sha256
        ).hexdigest()

    def verify(self, body: bytes, signature: str) -> bool:
        expected = self.sign(body)

        return hmac.compare_digest(
            expected,
            signature
        )
