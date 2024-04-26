import pytest
from popol import context
from fastapi import FastAPI
from tests.settings import init_settings

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    init_settings(app)
    context.setup(app)
    return app
