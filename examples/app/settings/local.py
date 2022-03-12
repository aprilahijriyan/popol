from pydantic import BaseSettings, Field
from saq.job import CronJob

from app.tasks import counter, scrape_quote


class Settings(BaseSettings):
    APP_ENV: str = Field("local", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    CACHES = {
        "default": {
            "backend": "popol.cache.backends.redis.RedisBackend",
            "options": {
                "host": REDIS_HOST,
                "port": REDIS_PORT,
                "db": REDIS_DB,
            },
        },
        "aioredis": {
            "backend": "popol.cache.backends.aioredis.AsyncRedisBackend",
            "options": {
                "host": REDIS_HOST,
                "port": REDIS_PORT,
                "db": 1,
            },
        },
    }
    SAQ_QUEUES = {
        "default": {
            "url": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            "functions": [scrape_quote],
            "concurrency": 10,
            "cron_jobs": [CronJob(counter, cron="* * * * *")],
            "context": {},
        }
    }
    DB_USERNAME = "popol_user"
    DB_PASSWORD = "popol_pass"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "popol_db"
    SQLALCHEMY_ASYNC_MODE = False
    SQLALCHEMY_DIALECT = "psycopg2"
    if SQLALCHEMY_ASYNC_MODE:
        SQLALCHEMY_DIALECT = "asyncpg"
    SQLALCHEMY_DATABASE_URI = f"postgresql+{SQLALCHEMY_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_OPTIONS = {}
