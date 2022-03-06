from fastapi import FastAPI

from app.routers import goodreads


def init_routers(app: FastAPI):
    """
    Initialize routers.
    """

    app.include_router(goodreads.router)
