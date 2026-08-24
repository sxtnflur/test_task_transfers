from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse
from transfers.domain.exceptions import DomainError, ValueDomainError


def register_errors(app: FastAPI) -> FastAPI:

    @app.exception_handler(ValueDomainError)
    async def value_domain_exception_handler(
        request,
        exc: ValueDomainError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": exc.message,
            }
        )

    @app.exception_handler(DomainError)
    async def domain_exception_handler(
        request,
        exc: DomainError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
            }
        )

    return app
