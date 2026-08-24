from fastapi import FastAPI

from transfers.presentation.http import (
    router as transfer_router,
    register_errors as transfer_register_errors
)


class FastAPIServer:
    def __init__(self, app: FastAPI):
        self._register_routers(app)
        self._register_errors(app)
        self.app = app

    @staticmethod
    def _register_routers(app: FastAPI):
        app.include_router(transfer_router)

    @staticmethod
    def _register_errors(app: FastAPI):
        transfer_register_errors(app)

    def get_app(self) -> FastAPI:
        return self.app
