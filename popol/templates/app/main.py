from fastapi import FastAPI

from app.extensions import init_extensions
from app.middleware import init_middleware
from app.routers import init_routers


def create_app() -> FastAPI:
    """
    Create the FastAPI application.
    """

    app = FastAPI()
    init_extensions(app)
    init_middleware(app)
    init_routers(app)
    return app


app = create_app()
