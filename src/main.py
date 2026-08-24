from fastapi import FastAPI
from server import FastAPIServer


def create_app(*args, **kwargs) -> FastAPI:
    return FastAPIServer(FastAPI(
        root_path='/api/v1',
        title='Transfers API',
        version='0.1.0'
    )).get_app()

