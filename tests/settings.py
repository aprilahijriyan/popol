from fastapi import FastAPI
from typing import Literal

from tests._saq_tasks import increment
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    APP_ENV: Literal["development", "production"] = "development"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def CACHES(self) -> dict:
        return {
            "default": {
                "backend": "popol.cache.backends.redis.RedisBackend",
                "options": {
                    "host": self.REDIS_HOST,
                    "port": self.REDIS_PORT,
                    "db": self.REDIS_DB,
                },
            },
            "aioredis": {
                "backend": "popol.cache.backends.redis.AsyncRedisBackend",
                "options": {
                    "host": self.REDIS_HOST,
                    "port": self.REDIS_PORT,
                    "db": 1,
                },
                "serializer": {
                    "class": "popol.cache.serializers.JSONSerializer",
                }
            },
        }
    
    @property
    def SAQ_QUEUES(self):
        return {
            "default": {
                "url": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
                "functions": [increment],
                "concurrency": 10,
                "context": {},
            }
        }

    DB_NAME: str = "popol_test_db.sqlite"
    SQLALCHEMY_ASYNC_MODE: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"sqlite:///{self.DB_NAME}"
    
    SQLALCHEMY_OPTIONS: dict = {}
    EMAIL_BACKEND: str = "popol.email.backend.EmailBackend"
    EMAIL_HOSTNAME: str = "localhost"
    EMAIL_PORT: int = 8025
    # EMAIL_USERNAME: Optional[str] = None
    # EMAIL_PASSWORD: Optional[str] = None
    # EMAIL_TIMEOUT: int = 60
    # EMAIL_USE_TLS: bool = False
    # EMAIL_START_TLS: bool = False
    # EMAIL_VALIDATE_CERTS: bool = True
    # EMAIL_CLIENT_CERT: Optional[str] = None
    # EMAIL_CLIENT_KEY: Optional[str] = None
    # EMAIL_CERT_BUNDLE: Optional[str] = None
    # EMAIL_ASYNC_MODE: bool = False
    DEFAULT_FROM_EMAIL: str = "Local <noreply@localhost.com>"

settings = AppSettings()


def init_settings(app: FastAPI) -> AppSettings:
    """
    Set the settings for the application.
    """

    app.state.settings = settings
    return settings
