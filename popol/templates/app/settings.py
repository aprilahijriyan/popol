from pydantic import __version__ as PYDANTIC_VERSION, Field
from fastapi import FastAPI

if PYDANTIC_VERSION.startswith("2"):
    try:
        from pydantic_settings import BaseSettings
    except ImportError:
        raise RuntimeError(
            "pydantic-settings is not installed. Please install it with `pip install pydantic-settings`"
        )
else:
    from pydantic import BaseSettings

class AppSettings(BaseSettings):
    DEBUG: bool = Field(True, env="DEBUG")

settings = AppSettings()


def init_settings(app: FastAPI) -> AppSettings:
    """
    Set the settings for the application.
    """

    app.state.settings = settings
    return settings
