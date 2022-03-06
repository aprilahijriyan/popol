from fastapi import FastAPI

from app.extensions import init_extensions
from app.middleware import init_middleware
from app.routers import init_routers
from app.settings import init_settings

app = FastAPI()
init_settings(app)
init_extensions(app)
init_middleware(app)
init_routers(app)
