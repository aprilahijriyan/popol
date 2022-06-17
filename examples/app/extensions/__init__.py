from fastapi import FastAPI
from popol import cache, context, email
from popol.db import sqlmodel
from popol.jobs import saq


def init_extensions(app: FastAPI):
    """
    Initialize extensions.
    """

    context.setup(app)
    cache.setup(app)
    saq.setup(app)
    sqlmodel.setup(app)
    email.setup(app)
