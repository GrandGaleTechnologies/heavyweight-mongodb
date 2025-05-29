# type: ignore
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The settings for the application."""

    model_config = SettingsConfigDict(env_file=".env")

    # App
    DEBUG: bool = os.environ.get("DEBUG")

    # Logfire
    LOGFIRE_TOKEN: str | None = os.environ.get("LOGFIRE_TOKEN")

    # DB Settings
    MONGODB_URL: str = os.environ.get("MONGODB_URL")


@lru_cache
def get_settings():
    """This function returns the settings obj for the application."""
    return Settings()
