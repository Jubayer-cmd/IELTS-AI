"""
Application Configuration using Pydantic Settings.

This provides type-safe configuration with validation at startup.
All environment variables are loaded and validated here.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic Settings automatically reads from .env file and validates types.
    If a required field is missing or has wrong type, app fails fast at startup.
    """

    # ───────────────────────────────────────────
    # Database (PostgreSQL)
    # ───────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/ielts_db"

    # ───────────────────────────────────────────
    # Security & Auth
    # ───────────────────────────────────────────
    JWT_SECRET_KEY: str = Field(default="change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # ───────────────────────────────────────────
    # CORS
    # ───────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ───────────────────────────────────────────
    # LLM Provider Keys
    # ───────────────────────────────────────────
    OPENROUTER_API_KEY: str = ""
    GOOGLE_API_KEY: str | None = None

    # ───────────────────────────────────────────
    # LangSmith Tracing
    # ───────────────────────────────────────────
    LANGSMITH_TRACING: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "IELTS-AI"

    # ───────────────────────────────────────────
    # Payment - SSLCommerz
    # ───────────────────────────────────────────
    SSLCOMMERZ_STORE_ID: str | None = None
    SSLCOMMERZ_STORE_PASSWORD: str | None = None
    SSLCOMMERZ_IS_SANDBOX: bool = True

    # ───────────────────────────────────────────
    # Application Settings
    # ───────────────────────────────────────────
    EVALUATION_PRICE_BDT: int = 50
    FREE_TRIAL_CREDITS: int = 3
    MAX_WORD_COUNT: int = 400
    MIN_WORD_COUNT: int = 150

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),  # Check root first, then local
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Using @lru_cache ensures we only parse .env once,
    not on every request. This is a common FastAPI pattern.
    """
    return Settings()


# Convenience export
settings = get_settings()
