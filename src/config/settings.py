from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    api_token: str
    webhook_url: str
    tx_from_address: str
    database_url: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
