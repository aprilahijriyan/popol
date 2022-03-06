from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_ENV: str = Field("local", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
