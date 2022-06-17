from fastapi import FastAPI
from starlette.datastructures import State

from .proxy import LocalProxy
from .vars import _app_ctx

current_app: FastAPI = LocalProxy(lambda: _app_ctx.get(None))
state: State = LocalProxy(lambda: current_app.state)
