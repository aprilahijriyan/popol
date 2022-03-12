from fastapi import FastAPI
from popol import cache, email
from popol.db import sqlmodel
from popol.jobs import saq


def init_extensions(app: FastAPI):
    """
    Initialize extensions.
    """

    cache.setup(app)
    saq.setup(app)
    sqlmodel.setup(app)
    email.setup(app)
