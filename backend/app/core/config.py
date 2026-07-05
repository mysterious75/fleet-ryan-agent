"""
Fleet-[Client] Backend — Configuration
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "Fleet-[Client] API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Database (defaults to SQLite for local testing)
    DATABASE_URL: str = "sqlite+aiosqlite:///./fleet_ryan.db"
    DATABASE_ECHO: bool = False

    # Redis (optional — works without it)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False

    # Fleet APIs
    SAMSARA_API_TOKEN: Optional[str] = None
    SAMSARA_BASE_URL: str = "https://api.samsara.com"

    MOTIVE_API_KEY: Optional[str] = None
    MOTIVE_BASE_URL: str = "https://api.gomotive.com/v1"

    FLEETIO_API_TOKEN: Optional[str] = None
    FLEETIO_ACCOUNT_TOKEN: Optional[str] = None
    FLEETIO_BASE_URL: str = "https://secure.fleetio.com/api/v1"

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    FLEET_MANAGER_CHAT_ID: Optional[str] = None

    # Security
    SECRET_KEY: str = "change-me-in-production"
    API_KEY: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Monitoring
    HEARTBEAT_INTERVAL_SECONDS: int = 1800  # 30 minutes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
