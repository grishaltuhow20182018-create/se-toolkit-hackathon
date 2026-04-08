"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_DEBUG: bool = False
    BACKEND_RELOAD: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/djsetlist_db"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/djsetlist_db"

    # LLM / Qwen AI
    LLM_API_KEY: str = ""
    LLM_API_BASE_URL: str = "http://localhost:8080/v1"
    LLM_API_MODEL: str = "coder-model"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
