from fastapi import FastAPI

from app import models  # noqa
from app.extensions import init_extensions
from app.middleware import init_middleware
from app.routers import init_routers
from app.settings import init_settings

app = FastAPI(title="Popol", description="Demo API")
init_settings(app)
init_extensions(app)
init_middleware(app)
init_routers(app)
