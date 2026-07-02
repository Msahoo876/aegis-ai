"""
Application Configuration

This module contains all application settings loaded from environment variables.
It serves as the single source of truth for configuration across the application.
"""

from enum import Enum
from functools import lru_cache
from pathlib import Path

from typing import List
from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# ==========================================================
# Base Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

# ==========================================================
# Environment
# ==========================================================

class Environment(str, Enum):
    """Application environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


# ==========================================================
# AI Providers
# ==========================================================

class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"


# ==========================================================
# Settings
# ==========================================================

class Settings(BaseSettings):
    """
    Global application settings.

    Values are loaded from the .env file and validated using Pydantic.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ======================================================
    # Application
    # ======================================================

    APP_NAME: str = "Aegis AI"

    APP_VERSION: str = "0.1.0"

    APP_DESCRIPTION: str = (
        "Enterprise AI Software Engineering Platform"
    )

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    DEBUG: bool = True

    LOG_LEVEL: str = "INFO"

    # ======================================================
    # API
    # ======================================================

    API_V1_PREFIX: str = "/api/v1"

    # ======================================================
    # CORS
    # ======================================================

    CORS_ALLOWED_ORIGINS: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    )


    @property
    def cors_origins(self) -> list[str]:
        """
        Return the allowed CORS origins as a list.
        """

        return [
            origin.strip()
            for origin in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    # ======================================================
    # Server
    # ======================================================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: PostgresDsn

    # ======================================================
    # Redis
    # ======================================================

    REDIS_URL: RedisDsn

    # ======================================================
    # AI Configuration
    # ======================================================

    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI

    DEFAULT_MODEL: str = "gpt-5"

    EMBEDDING_MODEL: str = "text-embedding-3-large"

    TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="LLM temperature (0.0 - 2.0)",
    )

    MAX_TOKENS: int = 4096

    # ======================================================
    # API Keys
    # ======================================================

    OPENAI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    GROQ_API_KEY: str = ""

    OPENROUTER_API_KEY: str = ""

    OLLAMA_BASE_URL: str = "http://localhost:11434"


# ==========================================================
# Cached Settings Instance
# ==========================================================

@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The configuration is loaded only once during the application's
    lifetime, improving performance.
    """
    return Settings()


settings = get_settings()