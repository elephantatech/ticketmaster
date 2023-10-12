"""
config.py

This module provides the application settings using pydantic's BaseSettings.
Settings are loaded from environment variables or a .env file.

Attributes:
    settings (Settings): An instance of the Settings class with application settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for application configurations.

    Attributes:
        REDIS_URL (str): URL for the Redis server.
        TICKET_EXPIRATION (int): Time duration for ticket expiration, in seconds. Defaults to 2 weeks.
    """

    REDIS_URL: str = "redis://localhost:6379"
    TICKET_EXPIRATION: int = 2 * 7 * 24 * 60 * 60  # default: 2 weeks in seconds

    class Config:
        """Config class for pydantic BaseSettings."""

        env_file = ".env"  # if you want to read variables from a .env file


settings = Settings()
