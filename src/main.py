import logging
from fastapi import FastAPI
from server import FastAPIServer


logging.basicConfig(
    level=logging.ERROR,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
)


def create_app(*args, **kwargs) -> FastAPI:
    return FastAPIServer(FastAPI(
        root_path='/api/v1',
        title='Transfers API',
        version='0.1.0'
    )).get_app()

