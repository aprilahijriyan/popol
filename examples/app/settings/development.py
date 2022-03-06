from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_ENV: str = Field("development", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
