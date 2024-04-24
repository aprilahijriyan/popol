from pydantic import __version__ as PYDANTIC_VERSION, Field
from fastapi import FastAPI
from saq.job import CronJob

from app.tasks import counter, scrape_quote

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
    APP_ENV: str = Field("local", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
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
            },
        }
    
    @property
    def SAQ_QUEUES(self):
        return {
            "default": {
                "url": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
                "functions": [scrape_quote],
                "concurrency": 10,
                "cron_jobs": [CronJob(counter, cron="* * * * *")],
                "context": {},
            }
        }
    
    DB_USERNAME: str = "popol_user"
    DB_PASSWORD: str = "popol_pass"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "popol_db"
    SQLALCHEMY_ASYNC_MODE: bool = False
    
    @property
    def SQLALCHEMY_DIALECT(self) -> str:
        dialect = "psycopg2"
        if self.SQLALCHEMY_ASYNC_MODE:
            dialect = "asyncpg"
        return dialect

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+{self.SQLALCHEMY_DIALECT}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
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
    DEFAULT_FROM_EMAIL: str = "Local <noreply@localhost>"

settings = AppSettings()


def init_settings(app: FastAPI) -> AppSettings:
    """
    Set the settings for the application.
    """

    app.state.settings = settings
    return settings
