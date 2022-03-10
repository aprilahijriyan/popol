from fastapi import FastAPI
from popol import cache
from popol.jobs import saq


def init_extensions(app: FastAPI):
    """
    Initialize extensions.
    """

    cache.setup(app)
    saq.setup(app)
