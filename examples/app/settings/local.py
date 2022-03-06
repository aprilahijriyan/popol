from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_ENV: str = Field("local", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    CACHES = {
        "default": {
            "BACKEND": "popol.cache.backends.redis.RedisBackend",
            "OPTIONS": {
                "host": REDIS_HOST,
                "port": REDIS_PORT,
                "db": REDIS_DB,
            },
        }
    }
