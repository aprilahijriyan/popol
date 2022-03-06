from fastapi import FastAPI
from popol import cache


def init_extensions(app: FastAPI):
    """
    Initialize extensions.
    """

    cache.setup(app)
