import os

from fastapi import FastAPI

app_env = os.getenv("APP_ENV", "local")

if app_env == "local":
    from .local import Settings  # noqa
elif app_env == "development":
    from .development import Settings  # noqa
elif app_env == "production":
    from .production import Settings  # noqa
else:
    raise ValueError(f"Unknown environment: {app_env}")

settings = Settings()


def init_settings(app: FastAPI) -> Settings:
    """
    Set the settings for the application.
    """

    app.state.settings = settings
    return settings
