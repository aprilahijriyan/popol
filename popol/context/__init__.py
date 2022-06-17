from fastapi import FastAPI

from .vars import _app_ctx


def setup(app: FastAPI):
    """
    Register app to global context
    """
    _app_ctx.set(app)
