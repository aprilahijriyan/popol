from fastapi import FastAPI

from app.routers import account, goodreads


def init_routers(app: FastAPI):
    """
    Initialize routers.
    """

    app.include_router(goodreads.router)
    app.include_router(account.router)
